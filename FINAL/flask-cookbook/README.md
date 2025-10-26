# Flask Cookbook API (Angular-compatible)

A lightweight Flask backend that mirrors the endpoints expected by your Angular recipe app.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export FLASK_APP=app.py
flask db-init  # Create the SQLite database and seed some sample data
flask run --port 8080  # Angular expects 8080 by default
```

## Endpoints

- `GET    /api/recipes` — list all recipes
- `GET    /api/recipes/<id>` — get one
- `POST   /api/recipes` — create
- `PUT    /api/recipes/<id>` — update
- `DELETE /api/recipes/<id>` — delete
- `GET    /api/recipes/search?name=<q>` — search by name (contains, case-insensitive)
- `GET    /api/recipes/searchByIngredient?ingredient=<q>` — search by ingredient (contains, case-insensitive)
- `GET    /api/recipes/favorites` — list favorites
```

## Environment

- SQLite database at `instance/cookbook.db` (auto-created)
- CORS enabled for `http://localhost:4200` by default
