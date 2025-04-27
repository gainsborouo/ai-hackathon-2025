# Observatory
![Home Page](https://github.com/user-attachments/assets/380b6fd3-68f6-4d7d-adca-6c4e0af29d8a)

This project is a web-based platform that builds a human-centric, tiered fan community for idols. By tracking how long and how deeply each fan engages, it automatically assigns them to familiarity levels—unlocking different content and interaction opportunities that reveal the idol’s full personality and creative work. The result is more meaningful fan experiences, reduced scheduling pressure on idols, and clearer, conflict-free collaboration for managers and partners.

## Features

### Frontend

- User authentication (login, register)
- Live streaming for idols & fans
- Real-time chat & comments during streams
- Personal profile with fan-level indicator
- Responsive design with Tailwind CSS

### Backend

- Role‐based user management (fan, idol)
- Live‐stream session creation & management
    - not yet done
- Credit system: earn credits by watch time & interaction
- JWT‐based auth, secured endpoints

---

## Tech Stack

| Layer    | Technology                            |
| -------- | ------------------------------------- |
| Frontend | Vue 3, Vite, Tailwind CSS, Axios      |
| Backend  | Flask, SQLAlchemy                     |
| Storage  | MySQL (or MariaDB)                    |

---

## Prerequisites

- Node.js v16+
- Python 3.10+
- MySQL server (v5.7+ or v8)

---

## Setup

### 1. Clone repo

```bash
git clone https://github.com/gainsborouo/ai-hackathon-2025.git
cd ai-hackathon-2025
```

---

### 2. Backend

```
cd backend
```

#### 2.1 Environment setup
- [install poetry](https://python-poetry.org/docs/)
- `poetry install`
- `poetry env use python3`
- `poetry shell`: activate the environmnent
- `cp .env.example .env` and edit the .env

#### 2.3 Run server

```
python3 app.py
```

Backend API is now at http://localhost:8000/api/

---

### 3. Frontend

```bash
cd ../frontend
```

#### 3.1 Install dependencies

```bash
npm install
```

#### 3.2 Configure

```bash
cp .env.example .env
```

Then edit .env:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

#### 3.3 Run dev server

```
npm run dev
```

Access the app at http://localhost:5173

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
