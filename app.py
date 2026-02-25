from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime, date
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'budgetflow-secret-key-change-in-production'

DATA_FILE = 'data.json'

CATEGORY_ICONS = {
    'Housing': '🏠',
    'Food': '🍔',
    'Transport': '🚗',
    'Utilities': '💡',
    'Healthcare': '🏥',
    'Entertainment': '🎮',
    'Shopping': '🛍️',
    'Education': '📚',
    'Salary': '💵',
    'Freelance': '💻',
    'Investment': '📈',
    'Other Income': '💰',
    'Other': '💳',
}


def load_data():
    if not os.path.exists(DATA_FILE):
        return {'transactions': [], 'budgets': {}}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_stats(transactions):
    today = date.today()
    current_month = today.strftime('%Y-%m')

    total_income = 0
    total_expenses = 0

    for t in transactions:
        t_month = t['date'][:7]
        if t_month == current_month:
            if t['type'] == 'income':
                total_income += t['amount']
            else:
                total_expenses += t['amount']

    balance = total_income - total_expenses
    return total_income, total_expenses, balance


def get_budget_progress(transactions, budgets):
    today = date.today()
    current_month = today.strftime('%Y-%m')

    spent_by_category = defaultdict(float)
    for t in transactions:
        if t['type'] == 'expense' and t['date'][:7] == current_month:
            spent_by_category[t['category']] += t['amount']

    result = []
    for category, limit in budgets.items():
        result.append({
            'category': category,
            'limit': limit,
            'spent': spent_by_category.get(category, 0)
        })
    return result


def get_chart_data(transactions):
    from calendar import month_abbr
    today = date.today()
    months = []
    for i in range(5, -1, -1):
        m = today.month - i
        y = today.year
        if m <= 0:
            m += 12
            y -= 1
        months.append((y, m, month_abbr[m]))

    chart = []
    max_val = 1
    raw = []
    for y, m, label in months:
        key = f'{y}-{m:02d}'
        inc = sum(t['amount'] for t in transactions if t['type'] == 'income' and t['date'][:7] == key)
        exp = sum(t['amount'] for t in transactions if t['type'] == 'expense' and t['date'][:7] == key)
        raw.append((label, inc, exp))
        max_val = max(max_val, inc, exp)

    for label, inc, exp in raw:
        chart.append({
            'label': label,
            'income_pct': round(inc / max_val * 100),
            'expense_pct': round(exp / max_val * 100),
        })

    return chart


@app.route('/')
def index():
    data = load_data()
    transactions = sorted(data['transactions'], key=lambda x: x['date'], reverse=True)
    total_income, total_expenses, balance = get_stats(transactions)
    budgets = get_budget_progress(transactions, data.get('budgets', {}))
    chart_data = get_chart_data(transactions)

    return render_template(
        'index.html',
        transactions=transactions[:20],
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        budgets=budgets,
        chart_data=chart_data,
        category_icons=CATEGORY_ICONS,
    )


@app.route('/add', methods=['POST'])
def add_transaction():
    data = load_data()

    try:
        amount = float(request.form['amount'])
        if amount <= 0:
            raise ValueError("Amount must be positive")

        transaction = {
            'id': int(datetime.now().timestamp() * 1000),
            'type': request.form['type'],
            'description': request.form['description'].strip(),
            'amount': amount,
            'category': request.form['category'],
            'date': request.form['date'],
        }

        data['transactions'].append(transaction)
        save_data(data)
        flash(f'Transaction added successfully!', 'success')

    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('index'))


@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    data = load_data()
    data['transactions'] = [t for t in data['transactions'] if t['id'] != transaction_id]
    save_data(data)
    flash('Transaction deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/set-budget', methods=['POST'])
def set_budget():
    data = load_data()

    try:
        category = request.form['category']
        limit = float(request.form['limit'])
        if limit <= 0:
            raise ValueError("Budget limit must be positive")

        if 'budgets' not in data:
            data['budgets'] = {}
        data['budgets'][category] = limit
        save_data(data)
        flash(f'Budget set for {category}: ${limit:.2f}/month', 'success')

    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
