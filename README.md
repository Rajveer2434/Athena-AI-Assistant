# 🤖 Athena AI Assistant

Athena AI Assistant is a Streamlit-based virtual assistant that combines AI-powered conversations with productivity tools such as task management, note-taking, and weather information.

## 🚀 Features

### 💬 AI Chat
- Ask questions using Google's Gemini AI model.
- Generate intelligent responses in real time.

### ✅ Task Manager
- Add and manage daily tasks.
- Store tasks in a local SQLite database.
- View all tasks from the dashboard.

### 📝 Notes Manager
- Save important notes.
- Retrieve previously saved notes.
- Persistent storage using SQLite.

### 🌦 Weather Information
- Get real-time weather updates.
- View:
  - Temperature
  - Humidity
  - Weather Condition

### 📊 Dashboard
- Overview of:
  - Total Tasks
  - Total Notes

---

## 🛠 Tech Stack

- Python
- Streamlit
- SQLite
- Google Gemini API
- OpenWeatherMap API
- Pandas
- Requests
- python-dotenv

---

## 📂 Project Structure

```text
Athena-AI-Assistant/
│
├── app.py
│
├── modules/
│   ├── ai_chat.py
│   ├── task_manager.py
│   ├── notes_manager.py
│   ├── weather.py
│   └── __init__.py
│
├── utils/
│   ├── db.py
│   └── assistant.db
│
├── .env
├── requirement.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/athena-ai-assistant.git
cd athena-ai-assistant
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirement.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Get Gemini API Key from:

https://ai.google.dev/

---

## ▶️ Run Application

```bash
streamlit run app.py
```

---

## 🗄 Database

The project uses SQLite for storing:

### Tasks Table

| Column | Type |
|----------|--------|
| id | INTEGER |
| task | TEXT |
| status | TEXT |

### Notes Table

| Column | Type |
|----------|--------|
| id | INTEGER |
| note | TEXT |

---

## 📸 Application Modules

### Dashboard
Displays:
- Total Tasks
- Total Notes

### AI Chat
Uses Gemini AI for generating responses.

### Tasks
- Add Tasks
- View Tasks

### Notes
- Save Notes
- View Notes

### Weather
Fetches live weather information using OpenWeatherMap API.

---

## 🔮 Future Enhancements

- Voice Assistant Support
- Task Completion Tracking
- Reminder Notifications
- User Authentication
- Cloud Database Integration
- Chat History Storage
- Dark Mode UI

---

## 👨‍💻 Author

Adarsh Mundhe

GitHub:
https://github.com/Adarsh9154

LinkedIn:
https://www.linkedin.com/in/adarsh-mundhe-07247827b/

---

## ⭐ If you found this project useful

Give the repository a star and support the project.
