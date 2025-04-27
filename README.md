# Observatory
![Home Page](https://github.com/user-attachments/assets/380b6fd3-68f6-4d7d-adca-6c4e0af29d8a)

## Features

### Frontend

- User authentication (login, register)
- Live streaming for idols & fans
- Real-time chat & comments during streams
- Personal profile with fan-level indicator
- Responsive design with Tailwind CSS

### Backend

- Role‐based user management (fan, idol, admin)
- Live‐stream session creation & management
- Credit system: earn credits by watch time & interaction
- Comment prioritization (e.g. upvoted questions surface higher)
- JWT‐based auth, secured endpoints

---

## Tech Stack

| Layer    | Technology                            |
| -------- | ------------------------------------- |
| Frontend | Vue 3, Vite, Tailwind CSS, Axios      |
| Backend  | Flask, SQLAlchemy, Flask‐JWT‐Extended |
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

#### 2.1 Create & activate virtual env

```bash
python3 -m venv .venv
source .venv/bin/activate # macOS/Linux
.\.venv\Scripts\activate # Windows PowerShell
```

#### 2.2 Install dependencies

```
pip install poetry
poetry install
```

#### 2.3 Configure environment

```
cp .env.example .env
```

Then edit .env:

```
DATABASE_URL=mysql+pymysql://<user>:<pass>@<host>:<port>/<db>
JWT_SECRET=YOUR_SECRET_KEY
```

#### 2.4 Initialize database

```
flask db upgrade
```

#### 2.5 Run server

```
flask run --host=0.0.0.0 --port=8000
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
