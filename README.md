# Pet Community Management System

Welcome to the **Pet Community Management System**! This project is a web application designed to manage pet profiles. Users can create, view, update, and delete (CRUD) pet profiles efficiently through a user-friendly interface.

---

## Features

### Backend
- **Database Management:** Stores pet data in a MySQL database.
- **API Endpoints:** Handles CRUD operations using parameters for secure and efficient interactions.
- **Error Handling:** Provides clear feedback for operations like update and delete.

### Frontend
- **Dynamic UI:** Displays pet profiles in a structured table format.
- **Live Updates:** Automatically refreshes the list after any changes.
- **Action Controls:** Allows editing and deleting profiles directly from the table.

---

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy, MySQL
- **Frontend:** HTML, CSS, JavaScript

---

## Installation Guide

### Prerequisites
- Python 3.8+
- MySQL Server
- Pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pet-community-management.git
   cd pet-community-management
   ```
2. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database:
   - Update the `db_config` dictionary in `app.py` with your MySQL credentials.
   - Create the database and table:
     ```sql
     CREATE DATABASE pet_community;
     USE pet_community;
     CREATE TABLE Pets (
         PetID INT AUTO_INCREMENT PRIMARY KEY,
         Name VARCHAR(100) NOT NULL,
         Species VARCHAR(50) NOT NULL,
         Age INT NOT NULL,
         Description TEXT,
         DateAdded DATETIME DEFAULT CURRENT_TIMESTAMP
     );
     ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Access the app in your browser:
   ```
   http://localhost:5000
   ```

---

## Usage

1. **Add a Pet:** Fill out the form with the pet's details and click "Add Pet."
2. **View Pets:** Pet profiles are displayed in a table with their name, species, age, and actions.
3. **Update a Pet:** Click the "Edit" button, update the fields in the modal, and save.
4. **Delete a Pet:** Click the "Delete" button to remove a pet from the list.

---

## API Endpoints

| Method   | Endpoint               | Description                   |
|----------|------------------------|-------------------------------|
| `GET`    | `/api/pets`            | Retrieve all pets             |
| `POST`   | `/api/pets`            | Add a new pet                 |
| `PUT`    | `/api/pets`            | Update a pet (via parameters) |
| `DELETE` | `/api/pets`            | Delete a pet (via parameters) |

---

## Project Structure
```
pet-community-management/
|-- static/
|   |-- css/
|   |   |-- styles.css
|   |-- js/
|       |-- script.js
|-- templates/
|   |-- index.html
|-- app.py
|-- requirements.txt
|-- README.md
```

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a branch for your feature or bug fix.
3. Commit and push your changes.
4. Open a pull request with details.

