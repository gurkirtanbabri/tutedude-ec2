# tutedude‑ec2

A small Todo app with a Flask backend and a Vite/React (or similar) frontend. The project is set up to run on an Ubuntu EC2 instance using **Supervisor** (or optionally **systemd**) to keep both services alive and automatically restart them.

---

## Prerequisites

- Ubuntu 20.04+ (default `ubuntu` user on AWS EC2)
- **Node.js** (>=18) and **npm**
- **Python 3.11** (or compatible) with `venv`
- `supervisor` package (`sudo apt install supervisor`)
- Git (to clone the repo)

---

## Quick start (Supervisor – no sudo moves)

```bash
# 1️⃣ Clone the repo (if you haven't already)
git clone https://github.com/gurkirtanbabri/tutedude-ec2.git
cd tutedude-ec2

# 2️⃣ Create logs directory (once)
sudo -u ubuntu mkdir -p /home/ubuntu/tutedude-ec2/logs

# 3️⃣ Backend – virtual environment & deps
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # Flask, pymongo, etc.
deactivate
cd ..

# 4️⃣ Frontend – install npm deps
cd frontend
npm install
cd ..

# 5️⃣ Start services with Supervisor
# Frontend
sudo -u ubuntu supervisord -c $(pwd)/supervisord_frontend.conf
# Backend (in another terminal or background)
sudo -u ubuntu supervisord -c $(pwd)/supervisord_backend.conf
```

### Verify

```bash
# Check status of each program
sudo -u ubuntu supervisorctl -c $(pwd)/supervisord_frontend.conf status
sudo -u ubuntu supervisorctl -c $(pwd)/supervisord_backend.conf status
```

You should see both `frontend` and `backend` listed as **RUNNING**.

---

## Logs

- Frontend stdout: `/home/ubuntu/tutedude-ec2/logs/frontend_stdout.log`
- Frontend stderr: `/home/ubuntu/tutedude-ec2/logs/frontend_stderr.log`
- Backend stdout:  `/home/ubuntu/tutedude-ec2/logs/backend_stdout.log`
- Backend stderr:  `/home/ubuntu/tutedude-ec2/logs/backend_stderr.log`

Use `tail -f <logfile>` to watch live output.

---

## Optional: systemd (global) version

If you prefer the classic system‑wide approach, copy the unit files to `/etc/systemd/system/` and enable them:

```bash
sudo cp todo-backend.service /etc/systemd/system/
sudo cp todo-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now todo-backend.service
time sudo systemctl enable --now todo-frontend.service
```

Both methods achieve the same goal – keeping the services up and auto‑restarting on failure.

---

## Environment variables

Backend reads optional variables from `backend/.env` (e.g., `MONGO_URI`). Add any needed keys there; the Supervisor config loads the file automatically.

---

## Stopping / Restarting

```bash
# Supervisor
sudo -u ubuntu supervisorctl -c supervisord_frontend.conf stop frontend
sudo -u ubuntu supervisorctl -c supervisord_backend.conf restart backend

# Systemd (if used)
sudo systemctl stop todo-frontend.service
sudo systemctl restart todo-backend.service
```

---

## License

MIT – feel free to fork, modify, and deploy.
