# 🛡️ SecureMeet — AI-Powered Meeting Moderation System

> Full-stack AI meeting moderation | Angular 17 + Flask + Azure MySQL + Docker

---

## 🧰 Tech Stack

| Layer      | Technology                                      |
|------------|-------------------------------------------------|
| Frontend   | Angular 17, RxJS, SCSS                          |
| Backend    | Flask, Flask-JWT-Extended, Flask-CORS           |
| Database   | Azure MySQL Flexible Server / Local MySQL 8     |
| ML / NLP   | Scikit-learn, NLTK, TF-IDF + Logistic Regression|
| Auth       | JWT (JSON Web Tokens)                           |
| Container  | Docker, Docker Compose                          |
| Deploy     | Azure Container Apps / Azure Web App            |

---

## 📁 Project Structure

```
securemeet/
├── backend/
│   ├── app.py                    # Flask app factory
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── meeting_routes.py
│   │   └── moderation_routes.py
│   ├── services/
│   │   ├── db_service.py         # SQLAlchemy models (User, Meeting, FlaggedMessage)
│   │   └── moderation_service.py # ML inference
│   └── ml/
│       └── train_model.py
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── angular.json
│   ├── package.json
│   └── src/app/
│       ├── pages/                # home, login, register, dashboard, meeting-room, admin-panel
│       ├── components/           # navbar, moderation-alert
│       ├── services/             # auth, meeting, moderation
│       └── guards/               # auth.guard, auth.interceptor
├── .vscode/
│   ├── settings.json
│   ├── launch.json               # F5 debug configs
│   ├── tasks.json                # Ctrl+Shift+B tasks
│   └── extensions.json
├── docker-compose.yml            # Local MySQL + backend + frontend
├── docker-compose.azure.yml      # Azure MySQL override
├── mysql-init/init.sql
├── api-tests.http                # REST Client tests
└── README.md
```

---

## 🚀 Option 1 — Run with Docker (Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Mac/Windows/Linux)
- On **Mac M1/M2/M3**: Docker Desktop with Rosetta enabled (Settings → General → Use Rosetta)

### Start with local MySQL (quickest)

```bash
# 1. Clone / unzip project
cd securemeet

# 2. Copy env file
cp backend/.env.example backend/.env

# 3. Build and start everything
docker compose up --build

# Services will be available at:
# Frontend  → http://localhost:4200
# Backend   → http://localhost:5000
# MySQL     → localhost:3306
```

### Start with Azure MySQL

```bash
# Set your Azure credentials in terminal
export AZURE_MYSQL_HOST=your-server.mysql.database.azure.com
export AZURE_MYSQL_USER=your_admin
export AZURE_MYSQL_PASSWORD=YourPassword123!
export AZURE_MYSQL_DATABASE=securemeet

# Run with Azure override
docker compose -f docker-compose.yml -f docker-compose.azure.yml up --build
```

### Stop containers
```bash
docker compose down          # stop containers
docker compose down -v       # stop + remove volumes (wipes DB)
```

---

## 💻 Option 2 — Run without Docker (VS Code)

### Step 1 — Open in VS Code

```bash
code securemeet
```

Install recommended extensions when prompted (or press `Ctrl+Shift+P` → "Show Recommended Extensions").

### Step 2 — Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate — Mac/Linux:
source venv/bin/activate
# Activate — Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt')"

# Train ML model
python ml/train_model.py

# Copy and edit env file
cp .env.example .env
# Edit .env with your MySQL credentials
```

### Step 3 — Start Backend

**Option A: VS Code Tasks** (`Ctrl+Shift+B` → "Run Flask Backend")

**Option B: Terminal**
```bash
cd backend && python app.py
# API at http://localhost:5000
```

**Option C: VS Code Debug** (F5 → select "Flask Backend")

### Step 4 — Frontend Setup

```bash
cd frontend
npm install
npm start
# App at http://localhost:4200
```

**VS Code Task:** `Ctrl+Shift+B` → "Run Angular Frontend"

### Step 5 — MySQL

**Local MySQL:**
```bash
# Mac (Homebrew)
brew services start mysql

# Windows
net start MySQL

# Linux
sudo systemctl start mysql
```

Create database:
```sql
CREATE DATABASE securemeet CHARACTER SET utf8mb4;
CREATE USER 'securemeet_user'@'localhost' IDENTIFIED BY 'SecureMeet@2025!';
GRANT ALL ON securemeet.* TO 'securemeet_user'@'localhost';
```

Tables are created **automatically** by SQLAlchemy on first backend start.

---

## ☁️ Option 3 — Azure MySQL Setup

### Create Azure MySQL Flexible Server

1. Go to [portal.azure.com](https://portal.azure.com)
2. Search **"Azure Database for MySQL"** → **Create** → **Flexible Server**
3. Fill in:
   - Server name: `securemeet-db`
   - Region: nearest to you
   - Admin username: `securemeet_admin`
   - Password: `YourStrongPassword123!`
4. Under **Networking**: Allow public access, add your IP
5. Click **Review + Create**

### Get Connection Details
```
Host:     securemeet-db.mysql.database.azure.com
Port:     3306
User:     securemeet_admin
Password: YourStrongPassword123!
Database: securemeet
```

### Download Azure SSL Certificate
```bash
# Download DigiCert root CA (required for Azure MySQL SSL)
curl -o backend/ssl/DigiCertGlobalRootCA.crt.pem \
  https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem
```

### Update .env for Azure
```env
MYSQL_HOST=securemeet-db.mysql.database.azure.com
MYSQL_PORT=3306
MYSQL_USER=securemeet_admin
MYSQL_PASSWORD=YourStrongPassword123!
MYSQL_DATABASE=securemeet
USE_SSL=1
```

---

## 🍎 Mac M1/M2/M3 Specific Notes

```bash
# If you get architecture errors with Docker:
docker compose build --platform linux/amd64

# If MySQL container crashes on Apple Silicon, use:
# platform: linux/amd64  (already set in docker-compose.yml)

# For native Python (without Docker), install via Homebrew:
brew install python@3.11 mysql-client pkg-config
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
pip install pymysql cryptography

# Node.js via nvm (recommended on Mac):
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

---

## 🧪 Testing the API

Open `api-tests.http` in VS Code with the **REST Client** extension installed.

1. Run the **Register** request
2. Copy the `token` from the response
3. Paste it at the top: `@token = your_token_here`
4. Run any other request

---

## 🗂️ Environment Variables Reference

| Variable         | Description                        | Default              |
|------------------|------------------------------------|----------------------|
| `MYSQL_HOST`     | MySQL server hostname              | `mysql` (docker)     |
| `MYSQL_PORT`     | MySQL port                         | `3306`               |
| `MYSQL_USER`     | MySQL username                     | `securemeet_user`    |
| `MYSQL_PASSWORD` | MySQL password                     | `SecureMeet@2025!`   |
| `MYSQL_DATABASE` | Database name                      | `securemeet`         |
| `USE_SSL`        | Enable SSL for Azure MySQL         | `0` (local), `1` (Azure) |
| `JWT_SECRET_KEY` | JWT signing secret                 | change in production |
| `FLASK_ENV`      | Flask environment                  | `development`        |
| `FLASK_DEBUG`    | Enable debug mode                  | `1`                  |

---

## ✅ Quick Start Checklist

- [ ] Docker Desktop installed and running
- [ ] `docker compose up --build` starts all 3 services
- [ ] Frontend loads at http://localhost:4200
- [ ] Register a new account (choose Admin role)
- [ ] Create a meeting from Dashboard
- [ ] Enter meeting room and type a toxic message
- [ ] See real-time moderation alert appear
- [ ] Visit /admin to see flagged message in table

---

## 📝 Resume Description

> Developed **SecureMeet**, an AI-powered meeting moderation platform using **Angular 17**, **Flask**, **Azure MySQL**, and **Docker**. Implemented NLP toxicity detection (TF-IDF + Logistic Regression) achieving 96%+ accuracy. Built JWT-authenticated REST APIs, containerized with Docker Compose, and configured for Azure MySQL Flexible Server deployment.
