# Pokemon REST API

A REST API built with **Flask** (Python) and **SQLite** that supports full CRUD
(Create, Read, Update, Delete) operations on a hand-crafted list of 15 Pokemon.

Built for the *Build Your Own API Server Challenge*.

## Tech Stack

- **Backend framework:** Flask (Python)
- **Database:** SQLite (ships with Python, no extra setup required)
- **Testing tool used:** curl

## Project Structure

```
pokemon-api/
├── app.py              # Flask app: routes, validation, DB logic
├── requirements.txt    # Python dependencies
├── pokemon.db           # SQLite database (auto-created on first run)
├── .gitignore
└── README.md
```

## Setup & Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/pokemon-api.git
   cd pokemon-api
   ```

2. (Recommended) create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   python app.py
   ```

The server starts at `http://127.0.0.1:5000`. On first run it automatically
creates `pokemon.db` and seeds it with 15 hand-crafted Pokemon.

## Data Model

Each Pokemon record has the following fields:

| Field     | Type    | Required | Description                     |
|-----------|---------|----------|----------------------------------|
| id        | integer | auto     | Unique identifier (auto-generated) |
| name      | string  | yes      | Pokemon name                    |
| type      | string  | yes      | Elemental type(s), e.g. "Fire/Flying" |
| hp        | integer | yes      | Hit points                      |
| attack    | integer | yes      | Attack stat                     |
| defense   | integer | yes      | Defense stat                    |
| speed     | integer | yes      | Speed stat                      |

## Endpoints

Base URL: `http://127.0.0.1:5000`

### 1. GET /pokemon
Returns the full list of Pokemon.

**Request**
```bash
curl -X GET http://127.0.0.1:5000/pokemon
```

**Response — 200 OK**
```json
[
  {
    "id": 1,
    "name": "Bulbasaur",
    "type": "Grass/Poison",
    "hp": 45,
    "attack": 49,
    "defense": 49,
    "speed": 45
  },
  {
    "id": 2,
    "name": "Charmander",
    "type": "Fire",
    "hp": 39,
    "attack": 52,
    "defense": 43,
    "speed": 65
  }
]
```

---

### 2. GET /pokemon/:id
Returns a single Pokemon by id.

**Request**
```bash
curl -X GET http://127.0.0.1:5000/pokemon/1
```

**Response — 200 OK**
```json
{
  "id": 1,
  "name": "Bulbasaur",
  "type": "Grass/Poison",
  "hp": 45,
  "attack": 49,
  "defense": 49,
  "speed": 45
}
```

**Response — 404 Not Found** (id doesn't exist)
```json
{
  "error": "Pokemon with id 999 not found."
}
```

---

### 3. POST /pokemon
Creates a new Pokemon. All fields in the data model (except `id`) are required.

**Request**
```bash
curl -X POST http://127.0.0.1:5000/pokemon \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Charizard",
        "type": "Fire/Flying",
        "hp": 78,
        "attack": 84,
        "defense": 78,
        "speed": 100
      }'
```

**Response — 201 Created**
```json
{
  "id": 16,
  "name": "Charizard",
  "type": "Fire/Flying",
  "hp": 78,
  "attack": 84,
  "defense": 78,
  "speed": 100
}
```

**Response — 400 Bad Request** (missing required field(s))
```bash
curl -X POST http://127.0.0.1:5000/pokemon \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete"}'
```
```json
{
  "error": "Missing required field(s): type, hp, attack, defense, speed"
}
```

---

### 4. PUT /pokemon/:id
Updates an existing Pokemon. Accepts a full or partial body — only the
fields you include are changed. Field types are still validated.

**Request**
```bash
curl -X PUT http://127.0.0.1:5000/pokemon/1 \
  -H "Content-Type: application/json" \
  -d '{"hp": 100}'
```

**Response — 200 OK**
```json
{
  "id": 1,
  "name": "Bulbasaur",
  "type": "Grass/Poison",
  "hp": 100,
  "attack": 49,
  "defense": 49,
  "speed": 45
}
```

**Response — 404 Not Found**
```json
{
  "error": "Pokemon with id 999 not found."
}
```

**Response — 400 Bad Request** (wrong field type)
```bash
curl -X PUT http://127.0.0.1:5000/pokemon/2 \
  -H "Content-Type: application/json" \
  -d '{"hp": "not-a-number"}'
```
```json
{
  "error": "Field 'hp' must be a number."
}
```

---

### 5. DELETE /pokemon/:id
Deletes a Pokemon by id.

**Request**
```bash
curl -X DELETE http://127.0.0.1:5000/pokemon/16
```

**Response — 200 OK**
```json
{
  "message": "Pokemon with id 16 ('Charizard') deleted successfully."
}
```

**Response — 404 Not Found**
```json
{
  "error": "Pokemon with id 999 not found."
}
```

## HTTP Status Codes Used

| Code | Meaning                                            |
|------|-----------------------------------------------------|
| 200  | Successful GET, PUT, or DELETE                      |
| 201  | Successful POST (resource created)                  |
| 400  | Bad request — missing required field or wrong type  |
| 404  | Resource not found                                   |

## Validation Rules

- `POST /pokemon` requires all of: `name`, `type`, `hp`, `attack`, `defense`, `speed`.
  Missing any of these returns `400` with a message listing exactly which
  fields are missing.
- `PUT /pokemon/:id` allows partial updates, but any field you do include
  must be the correct type (`name`/`type` must be non-empty strings,
  `hp`/`attack`/`defense`/`speed` must be numbers).
- Requesting a nonexistent id on `GET`, `PUT`, or `DELETE` returns `404`.

## Author's Notes

The 15 seed Pokemon were hand-typed into `SEED_DATA` in `app.py` — they were
not pulled from PokeAPI or any other external source.
