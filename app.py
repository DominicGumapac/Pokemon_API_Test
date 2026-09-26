from flask import Flask, jsonify, request, g
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pokemon.db")


REQUIRED_FIELDS = ["name", "type", "hp", "attack", "defense", "speed"]
NUMERIC_FIELDS = ["hp", "attack", "defense", "speed"]


SEED_DATA = [
    ("Bulbasaur",  "Grass/Poison", 45, 49, 49, 45),
    ("Charmander", "Fire",         39, 52, 43, 65),
    ("Squirtle",   "Water",        44, 48, 65, 43),
    ("Pikachu",    "Electric",     35, 55, 40, 90),
    ("Jigglypuff", "Normal/Fairy", 115, 45, 20, 20),
    ("Meowth",     "Normal",       40, 45, 35, 90),
    ("Psyduck",    "Water",        50, 52, 48, 55),
    ("Machop",     "Fighting",     70, 80, 50, 35),
    ("Geodude",    "Rock/Ground",  40, 80, 100, 20),
    ("Gastly",     "Ghost/Poison", 30, 35, 30, 80),
    ("Onix",       "Rock/Ground",  35, 45, 160, 70),
    ("Eevee",      "Normal",       55, 55, 50, 55),
    ("Snorlax",    "Normal",       160, 110, 65, 30),
    ("Dratini",    "Dragon",       41, 64, 45, 50),
    ("Mewtwo",     "Psychic",      106, 110, 90, 130),
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            hp INTEGER NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            speed INTEGER NOT NULL
        )
        """
    )
    count = conn.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]
    if count == 0:
        conn.executemany(
            "INSERT INTO pokemon (name, type, hp, attack, defense, speed) VALUES (?, ?, ?, ?, ?, ?)",
            SEED_DATA,
        )
        conn.commit()
    conn.close()


def row_to_dict(row):
    return {
        "id": row["id"],
        "name": row["name"],
        "type": row["type"],
        "hp": row["hp"],
        "attack": row["attack"],
        "defense": row["defense"],
        "speed": row["speed"],
    }


def validate_payload(data, partial=False):
    if data is None:
        return "Request body must be valid JSON."

    if not partial:
        missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] in (None, "")]
        if missing:
            return f"Missing required field(s): {', '.join(missing)}"

    for field in NUMERIC_FIELDS:
        if field in data and data[field] is not None:
            if not isinstance(data[field], (int, float)) or isinstance(data[field], bool):
                return f"Field '{field}' must be a number."

    for field in ["name", "type"]:
        if field in data and data[field] is not None:
            if not isinstance(data[field], str) or not data[field].strip():
                return f"Field '{field}' must be a non-empty string."

    return None


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Pokemon REST API",
        "endpoints": {
            "GET /pokemon": "List all pokemon",
            "GET /pokemon/<id>": "Get a single pokemon",
            "POST /pokemon": "Create a new pokemon",
            "PUT /pokemon/<id>": "Update an existing pokemon",
            "DELETE /pokemon/<id>": "Delete a pokemon",
        }
    }), 200


@app.route("/pokemon", methods=["GET"])
def get_all_pokemon():
    db = get_db()
    rows = db.execute("SELECT * FROM pokemon ORDER BY id").fetchall()
    return jsonify([row_to_dict(r) for r in rows]), 200


@app.route("/pokemon/<int:pokemon_id>", methods=["GET"])
def get_pokemon(pokemon_id):
    db = get_db()
    row = db.execute("SELECT * FROM pokemon WHERE id = ?", (pokemon_id,)).fetchone()
    if row is None:
        return jsonify({"error": f"Pokemon with id {pokemon_id} not found."}), 404
    return jsonify(row_to_dict(row)), 200


@app.route("/pokemon", methods=["POST"])
def create_pokemon():
    data = request.get_json(silent=True)
    error = validate_payload(data, partial=False)
    if error:
        return jsonify({"error": error}), 400

    db = get_db()
    cursor = db.execute(
        "INSERT INTO pokemon (name, type, hp, attack, defense, speed) VALUES (?, ?, ?, ?, ?, ?)",
        (data["name"], data["type"], data["hp"], data["attack"], data["defense"], data["speed"]),
    )
    db.commit()
    new_row = db.execute("SELECT * FROM pokemon WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(row_to_dict(new_row)), 201


@app.route("/pokemon/<int:pokemon_id>", methods=["PUT"])
def update_pokemon(pokemon_id):
    db = get_db()
    existing = db.execute("SELECT * FROM pokemon WHERE id = ?", (pokemon_id,)).fetchone()
    if existing is None:
        return jsonify({"error": f"Pokemon with id {pokemon_id} not found."}), 404

    data = request.get_json(silent=True)
    error = validate_payload(data, partial=True)
    if error:
        return jsonify({"error": error}), 400
    if not data:
        return jsonify({"error": "Request body must include at least one field to update."}), 400

    merged = row_to_dict(existing)
    merged.update({k: v for k, v in data.items() if k in REQUIRED_FIELDS})

    db.execute(
        "UPDATE pokemon SET name = ?, type = ?, hp = ?, attack = ?, defense = ?, speed = ? WHERE id = ?",
        (merged["name"], merged["type"], merged["hp"], merged["attack"], merged["defense"], merged["speed"], pokemon_id),
    )
    db.commit()
    updated_row = db.execute("SELECT * FROM pokemon WHERE id = ?", (pokemon_id,)).fetchone()
    return jsonify(row_to_dict(updated_row)), 200


@app.route("/pokemon/<int:pokemon_id>", methods=["DELETE"])
def delete_pokemon(pokemon_id):
    db = get_db()
    existing = db.execute("SELECT * FROM pokemon WHERE id = ?", (pokemon_id,)).fetchone()
    if existing is None:
        return jsonify({"error": f"Pokemon with id {pokemon_id} not found."}), 404

    db.execute("DELETE FROM pokemon WHERE id = ?", (pokemon_id,))
    db.commit()
    return jsonify({"message": f"Pokemon with id {pokemon_id} ('{existing['name']}') deleted successfully."}), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found."}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed on this endpoint."}), 405


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
