# BudgetFlow — EC2 Deployment Guide

## Project Structure
```
budget_app/
├── app.py
├── requirements.txt
├── data.json          ← auto-created on first run
└── templates/
    └── index.html
```

---

## Step 1: Connect to Your EC2 Instance
```bash
ssh -i your-key.pem ec2-user@your-ec2-public-ip
```

---

## Step 2: Update System & Install Python
```bash
sudo yum update -y         # Amazon Linux
sudo yum install python3 python3-pip -y
```
Or for Ubuntu:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

---

## Step 3: Upload Your Files
From your local machine:
```bash
scp -i your-key.pem -r budget_app/ ec2-user@your-ec2-public-ip:~/
```

---

## Step 4: Install Dependencies
```bash
cd ~/budget_app
pip3 install -r requirements.txt
```

---

## Step 5: Open Port 5000 in EC2 Security Group
1. Go to AWS Console → EC2 → Security Groups
2. Select your instance's security group
3. Click "Edit inbound rules"
4. Add rule: Type=Custom TCP, Port=5000, Source=0.0.0.0/0
5. Save rules

---

## Step 6: Run the App
```bash
python3 app.py
```

Access at: http://your-ec2-public-ip:5000

---

## Step 7: Run in Background (so it keeps running after you disconnect)
```bash
nohup python3 app.py &
```

Or use screen:
```bash
screen -S budgetflow
python3 app.py
# Press Ctrl+A then D to detach
```

---

## Step 8: (Optional) Run on Port 80 with Nginx

Install Nginx:
```bash
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

Create Nginx config:
```bash
sudo nano /etc/nginx/conf.d/budgetflow.conf
```

Add this content:
```nginx
server {
    listen 80;
    server_name your-ec2-public-ip;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Restart Nginx:
```bash
sudo systemctl restart nginx
```

Now access at: http://your-ec2-public-ip (no port needed!)

---

## Features
- Add income and expense transactions
- Set monthly budget limits per category
- Visual spending progress bars
- 6-month spending chart
- Net balance calculation
- Delete transactions
- Data persisted in data.json
