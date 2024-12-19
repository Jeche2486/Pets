document.addEventListener("DOMContentLoaded", () => {
    const addPetForm = document.getElementById("addPetForm");
    const petsTableBody = document.getElementById("petsTableBody");

    // Fetch and display all pets
    function fetchPets() {
        petsTableBody.innerHTML = "<tr><td colspan='5'>Loading pets...</td></tr>"; // Loading indicator
        fetch("/api/pets")
            .then(response => response.json())
            .then(data => {
                petsTableBody.innerHTML = ""; // Clear the table
                if (data.length === 0) {
                    petsTableBody.innerHTML = "<tr><td colspan='5'>No pets available. Add some!</td></tr>";
                    return;
                }
                data.forEach(pet => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${pet.Name}</td>
                        <td>${pet.Species}</td>
                        <td>${pet.Age}</td>
                        <td>${pet.Description}</td>
                        <td>
                            <button class="update-btn" data-id="${pet.PetID}">Update</button>
                            <button class="delete-btn" data-id="${pet.PetID}">Delete</button>
                        </td>
                    `;
                    petsTableBody.appendChild(row);
                });
                addEventListeners(); // Attach event listeners to new buttons
            })
            .catch(() => {
                petsTableBody.innerHTML = "<tr><td colspan='5'>Error fetching pets. Try again later.</td></tr>";
            });
    }

    // Add new pet
    addPetForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const newPet = {
            Name: document.getElementById("name").value,
            Species: document.getElementById("species").value,
            Age: parseInt(document.getElementById("age").value, 10),
            Description: document.getElementById("description").value
        };

        fetch("/api/pets", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newPet)
        })
            .then(response => {
                if (!response.ok) throw new Error("Failed to add pet.");
                return response.json();
            })
            .then(() => {
                addPetForm.reset();
                fetchPets();
            })
            .catch(() => {
                alert("Error adding pet. Please try again.");
            });
    });

    // Delete pet
    function deletePet(petId) {
        fetch(`/api/pets?petID=${petId}`, { method: "DELETE" }) // Use petID as a query parameter
            .then(response => {
                if (!response.ok) throw new Error("Failed to delete pet.");
                fetchPets();
            })
            .catch(() => {
                alert("Error deleting pet. Please try again.");
            });
    }

    // Update pet
    function updatePet(petId) {
        const petName = prompt("Enter new name for the pet:");
        const petSpecies = prompt("Enter new species:");
        const petAge = prompt("Enter new age:");
        const petDescription = prompt("Enter new description:");

        if (!petName || !petSpecies || !petAge) {
            alert("All fields are required.");
            return;
        }

        const updatedPet = {
            Name: petName,
            Species: petSpecies,
            Age: parseInt(petAge, 10),
            Description: petDescription
        };

        fetch(`/api/pets?petID=${petId}`, {  // Use petID as a query parameter
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedPet)
        })
            .then(response => {
                if (!response.ok) throw new Error("Failed to update pet.");
                fetchPets();
            })
            .catch(() => {
                alert("Error updating pet. Please try again.");
            });
    }

    // Add event listeners for update and delete buttons
    function addEventListeners() {
        document.querySelectorAll(".delete-btn").forEach(button => {
            button.addEventListener("click", () => deletePet(button.getAttribute("data-id")));
        });

        document.querySelectorAll(".update-btn").forEach(button => {
            button.addEventListener("click", () => updatePet(button.getAttribute("data-id")));
        });
    }

    // Initial fetch
    fetchPets();
});
