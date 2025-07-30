# 🚧 This branch is still under development

# FastAPI To-Do Application (Under Development)

A boilerplate FastAPI application to manage a To‑Do list, using **SQLAlchemy** for SQL database integration. You can use this project as a starting point for building CRUD APIs backed by a relational database.

## Getting Started

This project includes a basic FastAPI setup with a To‑Do schema, endpoints to create/read/update/delete tasks, and SQL operations using SQLAlchemy models. It’s ideal for bootstrapping a REST API project with a clean and extensible structure.

By using this boilerplate as a standard initializer, you maintain consistent patterns across API projects, reduce setup time, and avoid repetitive boilerplate coding.

## How to Use

**Step 1: Clone the repository**

```bash
git clone https://github.com/FarhanRiaaz/fastAPI-todos-app.git
cd fastAPI-todos-app
````

**Step 2: Set up virtual environment**

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

**Step 3: Install required dependencies**

```bash
pip install -r requirements.txt
```

**Step 4: Initialize the database**

Make sure your `database.py` is configured with the appropriate engine (e.g., SQLite or PostgreSQL), then create tables using:

```python
from DataLayer.database import Base, engine
Base.metadata.create_all(bind=engine)
```

**Step 5: Run the application**

```bash
uvicorn main:app --reload
```

---

## API Overview

The To‑Do API supports the following operations on the `todos` table:

### Database Schema

```python
class Todos(Base):
    __tablename__ = 'todos'
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String)
    description = Column(String)
    priority    = Column(Integer)
    complete    = Column(Boolean, default=False)
```

### Endpoints

| Method   | Endpoint      | Description                  |
| -------- | ------------- | ---------------------------- |
| `GET`    | `/todos`      | Retrieve all tasks           |
| `GET`    | `/todos/{id}` | Retrieve a single task by ID |
| `POST`   | `/todos`      | Create a new task            |
| `PUT`    | `/todos/{id}` | Update an existing task      |
| `DELETE` | `/todos/{id}` | Delete a task by ID          |

---

## What’s Included (Features)

* ✅ CRUD operations on To‑Do tasks
* 🔢 Priority field to mark task importance
* ✅ Mark tasks as complete/incomplete
* 🧩 SQL database support (via SQLAlchemy)
* ✅ Ready to be extended with user auth, pagination, filtering, etc.

---

## Roadmap & Next‑Steps

Upcoming enhancements:

* [ ] JWT authentication
* [ ] Filtering and pagination (e.g., by priority or completion status)
* [ ] Docker container support (Dockerfile, `docker-compose`)
* [ ] Unit tests with `pytest`
* [ ] Frontend UI integration (React, Flutter, or HTMX)

---

## Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork the repo and submit a pull request to enhance or extend the app.

---

## Author

**Farhan Riaaz** —
🔗 GitHub: [https://github.com/FarhanRiaaz](https://github.com/FarhanRiaaz)

---

## License

This project is licensed under [MIT License](LICENSE).
