from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, validates, validates_schema
import os





app = Flask(__name__)

# --- Config ---
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///cookbook.db"  # stored in ./instance by default with relative sqlite:/// path
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False

# CORS (adjust origins as needed)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:4200", "http://127.0.0.1:4200", "*"]}})

db = SQLAlchemy(app)

# --- Model ---
class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Store ingredients as a JSON array
    ingredients = db.Column(db.JSON, nullable=False, default=list)
    instructions = db.Column(db.Text, nullable=False)
    favorite = db.Column(db.Boolean, nullable=False, default=False)
    imageUrl = db.Column(db.String(500), nullable=True)

# --- Schema / Validation ---
class RecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    ingredients = fields.List(fields.Str(), required=True)
    instructions = fields.Str(required=True)
    favorite = fields.Bool(load_default=False)
    imageUrl = fields.Str(allow_none=True, load_default=None)

    @validates("name")
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError("Name cannot be empty.")

    @validates("ingredients")
    def validate_ingredients(self, value):
        if not isinstance(value, list) or len(value) == 0:
            raise ValidationError("At least one ingredient is required.")

recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)

# --- Helpers ---
def not_found(msg="Resource not found"):
    return jsonify({"error": msg}), 404

def bad_request(msg="Bad request"):
    return jsonify({"error": msg}), 400

def created(data):
    return jsonify(data), 201

# --- Routes ---
@app.route("/api/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.order_by(Recipe.id.desc()).all()
    return jsonify(recipes_schema.dump(recipes))

@app.route("/api/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return not_found("Recipe not found")
    return jsonify(recipe_schema.dump(recipe))

@app.route("/api/recipes", methods=["POST"])
def create_recipe():
    try:
        payload = recipe_schema.load(request.get_json() or {})
    except ValidationError as err:
        return bad_request(err.messages)

    recipe = Recipe(**payload)
    db.session.add(recipe)
    db.session.commit()
    return created(recipe_schema.dump(recipe))





@app.route("/api/recipes/search")
def search_by_name():
    name = request.args.get("name", "").strip()
    q = Recipe.query
    if name:
        q = q.filter(Recipe.name.ilike(f"%{name}%"))
    results = q.order_by(Recipe.id.desc()).all()
    return jsonify(recipes_schema.dump(results))

@app.route("/api/recipes/searchByIngredient")
def search_by_ingredient():
    ingredient = request.args.get("ingredient", "").strip()
    if not ingredient:
        return bad_request({"ingredient": ["Ingredient query param is required"]})
    results = Recipe.query.filter(
        db.func.json_each(Recipe.ingredients).column("value").ilike(f"%{ingredient}%")
        if db.session.bind.dialect.name == "sqlite" and hasattr(db.func, "json_each")
        else Recipe.ingredients.cast(db.String).ilike(f"%{ingredient}%")
    ).all()
    return jsonify(recipes_schema.dump(results))

@app.route("/api/recipes/favorites")
def favorites():
    results = Recipe.query.filter_by(favorite=True).order_by(Recipe.id.desc()).all()
    return jsonify(recipes_schema.dump(results))

@app.route("/api/recipes/<int:id>/favorite", methods=["POST"])
def toggle_favorite(id):
    data = request.get_json()
    favorite = data.get("favorite")

    if favorite is None:
        return jsonify({"error": "Missing 'favorite' field"}), 400

    recipe = Recipe.query.get_or_404(id)
    recipe.favorite = favorite

    db.session.commit()

    # ✅ Return the updated recipe as JSON
    return jsonify(recipe_schema.dump(recipe)), 200


# @app.route("/api/recipes/<int:id>/favorite", methods=["PATCH"])
# def toggle_favorite(id):
#     data = request.get_json()
#     favorite = data.get("favorite")
#     # update only the favorite field in DB
#     return jsonify(update_recipe)

# # --- GET all favorite recipes ---
# @app.route("/api/recipes/favorites", methods=["GET"])
# def favorites():
#     results = Recipe.query.filter_by(favorite=True).order_by(Recipe.id.desc()).all()
#     return jsonify(recipes_schema.dump(results))

# # --- PATCH toggle/set favorite for a specific recipe ---
# @app.route("/api/recipes/<int:id>/favorite", methods=["PATCH"])
# def update_favorite(id):
#     recipe = Recipe.query.get_or_404(id)
#     data = request.get_json()

    # Validate input
    if "favorite" not in data:
        return jsonify({"error": "'favorite' field is required"}), 400

    # Update only the favorite field
    recipe.favorite = bool(data["favorite"])
    db.session.commit()

    return jsonify(recipe_schema.dump(recipe)), 200



# --- CLI for easy setup/seed ---
@app.cli.command("db-init")
def db_init():
    """Initialize the database and seed sample data."""
    db.create_all()
    if Recipe.query.count() == 0:
        samples = [
            {
                "name": "Classic Pancakes",
                "description": "Fluffy pancakes perfect for breakfast.",
                "ingredients": ["Flour", "Milk", "Eggs", "Sugar", "Baking Powder", "Salt"],
                "instructions": "Whisk dry ingredients, add wet, cook on griddle.",
                "favorite": True,
                "imageUrl": ""
            },
            {
                "name": "Spaghetti Aglio e Olio",
                "description": "Simple pasta with garlic and olive oil.",
                "ingredients": ["Spaghetti", "Garlic", "Olive Oil", "Chili Flakes", "Parsley", "Salt"],
                "instructions": "Cook pasta, sauté garlic in oil, toss with chili flakes and parsley.",
                "favorite": False,
                "imageUrl": ""
            }
        ]
        for r in samples:
            db.session.add(Recipe(**r))
        db.session.commit()
        print("Seeded sample recipes.")
    print("Database ready.")

# --- Error handlers ---
@app.errorhandler(404)
def handle_404(e):
    return not_found("Endpoint not found")

@app.errorhandler(405)
def handle_405(e):
    return bad_request("Method not allowed")

@app.errorhandler(400)
def handle_400(e):
    return bad_request("Invalid request")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8080, debug=True)
