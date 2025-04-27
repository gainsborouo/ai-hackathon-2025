# Observatory

Human-centered design: exclusivity does not rely on “24/7 availability on demand.”  
Positioning: “This version of me is only known to those who have known me for a long time.”  
Not about idols belonging to fans, but fans belonging to the community and ecosystem of the idol’s brand and culture.

---

## Concept

Fans are grouped into familiarity levels based on engagement and time spent following the idol. As fans level up, they unlock new personality facets and creative content—presenting a multidimensional, human perspective.

---

## Pain Points Addressed

- **Idols**: Reduce pressure to always perform; share curated glimpses of self.
- **Fans**: Deeper, tiered access to content and interaction.
- **Management**: Fewer scheduling conflicts; controlled content rollout.
- **Partners**: Stable ecosystem for collaboration, less ad-hoc testing.

---

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

## Scripts

| Command            | Location | Description                      |
| ------------------ | -------- | -------------------------------- |
| `npm run dev`      | frontend | Start Vite dev server            |
| `npm run build`    | frontend | Build production assets          |
| `flask run`        | backend  | Start Flask development server   |
| `flask db upgrade` | backend  | Apply DB migrations              |
| `flask shell`      | backend  | Open Flask REPL with app context |

---

## Project Structure

### Frontend

```
frontend/
├── src/
│   ├── assets/          # Static assets (CSS, images)
│   ├── components/      # Reusable Vue components
│   ├── views/           # Vue pages (Home, Login, Register, etc.)
│   ├── store/           # Vuex store for state management
│   ├── router/          # Vue Router configuration
│   ├── main.js          # Entry point for the Vue app
│   └── App.vue          # Root Vue component
├── public/              # Public assets
├── vite.config.js       # Vite configuration
└── package.json         # Frontend dependencies and scripts
```

### Backend

```
backend/
├── controller/          # API controllers for various features
├── models.py            # SQLAlchemy models
├── routes.py            # API route definitions
├── seeder.py            # Database seeder script
├── app.py               # Flask application entry point
├── .env.example         # Example environment variables
└── pyproject.toml       # Backend dependencies and configuration
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
