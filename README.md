````markdown
# ✅ FastAPI To-Do Application with SQL Database

This is a lightweight and efficient **To-Do API** built using **FastAPI** and **SQLAlchemy**, designed to manage tasks with features like prioritization, completion tracking, and detailed descriptions.

---

## 📌 Features

- 📝 Create, Read, Update, and Delete (CRUD) tasks
- 🔢 Set task priority
- 📄 Include detailed descriptions
- ✅ Mark tasks as complete/incomplete
- 🔍 Retrieve all tasks or filtered views (e.g., completed only)
- 💾 Uses a relational SQL database (e.g., SQLite/PostgreSQL)

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** — modern, high-performance web framework
- **SQLAlchemy** — ORM for database interaction
- **Pydantic** — data validation and parsing
- **Uvicorn** — ASGI server for running FastAPI
- **SQLite** (or any SQL database of your choice)

---

## 🧱 Database Schema

```python
class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
````

### 🔹 Field Details:

| Field         | Type    | Description                      |
| ------------- | ------- | -------------------------------- |
| `id`          | Integer | Unique identifier for each task  |
| `title`       | String  | Short title of the task          |
| `description` | String  | Detailed explanation of the task |
| `priority`    | Integer | Priority level (e.g., 1 = High)  |
| `complete`    | Boolean | Status of the task (True/False)  |

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/FarhanRiaaz/fastAPI-todos-app.git
cd fastAPI-todos-app
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

Ensure SQLAlchemy is configured properly. You can create the tables using:

```python
Base.metadata.create_all(bind=engine)
```

Or through a migration tool like Alembic.

### 5. Run the app

```bash
uvicorn main:app --reload
```

---

## 🌐 API Endpoints (Examples)

| Method   | Endpoint      | Description             |
| -------- | ------------- | ----------------------- |
| `GET`    | `/todos`      | Get all tasks           |
| `GET`    | `/todos/{id}` | Get task by ID          |
| `POST`   | `/todos`      | Create a new task       |
| `PUT`    | `/todos/{id}` | Update an existing task |
| `DELETE` | `/todos/{id}` | Delete a task by ID     |

---

## 🧠 What You'll Learn

* How to build RESTful APIs using FastAPI
* Structuring a modern Python project
* Working with relational databases via SQLAlchemy
* Handling validation with Pydantic
* Running async-ready servers with Uvicorn

---

## 🚧 Roadmap / Next Steps

* [ ] Add JWT-based user authentication
* [ ] Support filtering: by priority, complete/incomplete
* [ ] Docker support for containerized deployment
* [ ] Add unit testing with `pytest`
* [ ] Basic frontend UI (React, Flutter, or HTMX)

---

## 🙌 Contributing

Pull requests and issues are welcome!
Feel free to fork this project and enhance it.

---

## 👨‍💻 Author

**Farhan Riaaz**
🔗 [GitHub](https://github.com/FarhanRiaaz)

---

## 📃 License

This project is licensed under the **MIT License**.

````