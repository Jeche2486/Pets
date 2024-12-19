from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure MySQL database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pet_community'
}

# Dynamically create the SQLAlchemy URI
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# Set the URI in the app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define the Pets table model
class Pet(db.Model):
    __tablename__ = 'Pets'
    PetID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Species = db.Column(db.String(50), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.Text)
    DateAdded = db.Column(db.DateTime, default=datetime.utcnow)

# Routes for CRUD operations
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/pets", methods=["POST"])
def add_pet():
    data = request.get_json()

    # Validate request body
    if not data:
        return jsonify({"message": "Request data is required"}), 400
    if 'Name' not in data or 'Species' not in data or 'Age' not in data:
        return jsonify({"message": "Name, Species, and Age are required fields"}), 400

    # Check if a pet with the same name already exists
    existing_pet = Pet.query.filter_by(Name=data['Name']).first()
    if existing_pet:
        return jsonify({"message": f"A pet with the name '{data['Name']}' already exists"}), 409

    # Create the new pet profile
    new_pet = Pet(
        Name=data['Name'],
        Species=data['Species'],
        Age=data['Age'],
        Description=data.get('Description', "")
    )
    try:
        db.session.add(new_pet)
        db.session.commit()
        return jsonify({"message": "Pet profile created successfully!"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of error
        return jsonify({"message": "Failed to create pet profile.", "error": str(e)}), 500


# # Create a new pet profile
# @app.route("/api/pets", methods=["POST"])
# def add_pet():
#     data = request.get_json()
#     new_pet = Pet(
#         Name=data['Name'],
#         Species=data['Species'],
#         Age=data['Age'],
#         Description=data.get('Description', "")
#     )
#     db.session.add(new_pet)
#     db.session.commit()
#     return jsonify({"message": "Pet profile created successfully!"}), 201



@app.route("/api/pets", methods=["GET"])
def get_pets():
    pet_id = request.args.get("petID")  # Case-insensitive for flexibility

    if pet_id:
        try:
            pet = Pet.query.get(int(pet_id))  # Ensure integer conversion for ID
            if pet:
                return jsonify({
                    "PetID": pet.PetID,
                    "Name": pet.Name,
                    "Species": pet.Species,
                    "Age": pet.Age,
                    "Description": pet.Description,
                    "DateAdded": pet.DateAdded
                })
            else:
                return jsonify({"message": "Pet not found"}), 404
        except ValueError:  # Handle invalid ID format (non-integer)
            return jsonify({"message": "Invalid PetID format (must be an integer)"}), 400

    else:
        pets = Pet.query.all()
        pets_list = [
            {
                "PetID": pet.PetID,
                "Name": pet.Name,
                "Species": pet.Species,
                "Age": pet.Age,
                "Description": pet.Description,
                "DateAdded": pet.DateAdded
            }
            for pet in pets
        ]
        return jsonify(pets_list)
    

    
# # Retrieve all pet profiles or a specific profile by ID
# @app.route("/api/pets", methods=["GET"])
# def get_pets():
#     pet_id = request.args.get("PetID")
#     if pet_id:
#         pet = Pet.query.get(pet_id)
#         if pet:
#             return jsonify({
#                 "PetID": pet.PetID,
#                 "Name": pet.Name,
#                 "Species": pet.Species,
#                 "Age": pet.Age,
#                 "Description": pet.Description,
#                 "DateAdded": pet.DateAdded
#             })
#         return jsonify({"message": "Pet not found"}), 404
#     else:
#         pets = Pet.query.all()
#         pets_list = [{
#             "PetID": pet.PetID,
#             "Name": pet.Name,
#             "Species": pet.Species,
#             "Age": pet.Age,
#             "Description": pet.Description,
#             "DateAdded": pet.DateAdded
#         } for pet in pets]
#         return jsonify(pets_list)

@app.route("/api/pets", methods=["PUT"])
def update_pet():
    # Extract 'petID' from the query parameters
    pet_id = request.args.get("petID", type=int)
    if not pet_id:
        return jsonify({"message": "Missing or invalid 'petID' query parameter."}), 400

    # Fetch the pet record by ID
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"message": "Pet not found"}), 404

    # Get and validate the JSON payload from the request
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Request must be in JSON format."}), 400
    except Exception as e:
        return jsonify({"message": "Invalid JSON format.", "error": str(e)}), 400

    # Update fields only if provided in the JSON
    pet.Name = data.get("Name", pet.Name)
    pet.Species = data.get("Species", pet.Species)
    pet.Age = data.get("Age", pet.Age)
    pet.Description = data.get("Description", pet.Description)

    try:
        # Commit changes to the database
        db.session.commit()
        return jsonify({"message": "Pet profile updated successfully!"})
    except Exception as e:
        db.session.rollback()  # Rollback in case of failure
        return jsonify({"message": "Failed to update the pet profile.", "error": str(e)}), 500


# Update a pet profile
# @app.route("/api/pets/<int:pet_id>", methods=["PUT"])
# def update_pet(pet_id):
#     pet = Pet.query.get(pet_id)
#     if not pet:
#         return jsonify({"message": "Pet not found"}), 404

#     data = request.get_json()
#     pet.Name = data.get("Name", pet.Name)
#     pet.Species = data.get("Species", pet.Species)
#     pet.Age = data.get("Age", pet.Age)
#     pet.Description = data.get("Description", pet.Description)

#     db.session.commit()
#     return jsonify({"message": "Pet profile updated successfully!"})

@app.route("/api/pets", methods=["DELETE"])
def delete_pet():
    pet_id = request.args.get("petID")  # Retrieve petID from query parameters
    if not pet_id:
        return jsonify({"message": "PetID query parameter is required"}), 400

    try:
        pet_id = int(pet_id)  # Ensure petID is an integer
    except ValueError:
        return jsonify({"message": "Invalid PetID format (must be an integer)"}), 400

    # Look up the pet by ID
    pet = Pet.query.get(pet_id)
    if not pet:
        return jsonify({"message": "Pet not found"}), 404

    # Delete the pet record
    try:
        db.session.delete(pet)
        db.session.commit()
        return jsonify({"message": "Pet profile deleted successfully!"})
    except Exception as e:
        db.session.rollback()  # Rollback if any error occurs
        return jsonify({"message": "Failed to delete pet profile.", "error": str(e)}), 500


# # Delete a pet profile
# @app.route("/api/pets/<int:pet_id>", methods=["DELETE"])
# def delete_pet(pet_id):
#     pet = Pet.query.get(pet_id)
#     if not pet:
#         return jsonify({"message": "Pet not found"}), 404

#     db.session.delete(pet)
#     db.session.commit()
#     return jsonify({"message": "Pet profile deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
