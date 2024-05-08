document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch all dentists
    async function fetchDentists() {
        try {
            const response = await fetch("/api/dentists");
            if (!response.ok) {
                throw new Error("Failed to fetch dentists");
            }
            const dentists = await response.json();
            // Call a function to display dentists
            displayDentists(dentists);
        } catch (error) {
            console.error("Error fetching dentists:", error);
        }
    }

    // Function to fetch all treatments
    async function fetchTreatments() {
        try {
            const response = await fetch("/api/treatments");
            if (!response.ok) {
                throw new Error("Failed to fetch treatments");
            }
            const treatments = await response.json();
            // Call a function to display treatments
            displayTreatments(treatments);
        } catch (error) {
            console.error("Error fetching treatments:", error);
        }
    }

    // Function to display dentists
    function displayDentists(dentists) {
        const dentistsContainer = document.getElementById("dentists");
        dentistsContainer.innerHTML = "";
        dentists.forEach(dentist => {
            const dentistElement = document.createElement("div");
            dentistElement.textContent = `${dentist.name} - ${dentist.specialization}`;
            dentistsContainer.appendChild(dentistElement);
        });
    }

    // Function to display treatments
    function displayTreatments(treatments) {
        const treatmentsContainer = document.getElementById("treatments");
        treatmentsContainer.innerHTML = "";
        treatments.forEach(treatment => {
            const treatmentElement = document.createElement("div");
            treatmentElement.textContent = `${treatment.name} - ${treatment.description}`;
            treatmentsContainer.appendChild(treatmentElement);
        });
    }

    // Fetch dentists and treatments when the page loads
    fetchDentists();
    fetchTreatments();
});
