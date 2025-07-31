/* 
This is a SAMPLE FILE to get you started.
Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);

        });
    }
});

async function loginUser(email, password) {
    const response = await fetch('https://your-api-url/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
} else {
    alert('Login failed: ' + response.statusText);
}
}

/* 
verifie le token jwt dans les cookie controle la sibiliter de connexion
*/

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
}
function getCookie(name) {
    // Function to get a cookie value by its name
    // Your code here
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';')[0];
    return null;
}


async function fetchPlaces(token) {
    // Make a GET request to fetch places data
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaces function
        try {
        const response = await fetch('https://your-api-url/places', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const data = await response.json();
            displayPlaces(data.places); // ou data directement selon ton API
        } else {
            alert('Échec du chargement des lieux : ' + response.statusText);
        }
    } catch (error) {
        console.error('Erreur :', error);
    }
}

function displayPlaces(places) {
    // Clear the current content of the places list
    // Iterate over the places data
    // For each place, create a div element and set its content
    // Append the created element to the places list
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p>Prix par nuit : ${place.price}€</p>
            <button class="details-button">Voir les détails</button>`;
        placesList.appendChild(placeCard);
    });
}


document.getElementById('price-filter').addEventListener('change', (event) => {
    // Get the selected price value
    // Iterate over the places and show/hide them based on the selected price
    const selectedPrice = parseInt(event.target.value);
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const priceText = card.querySelector('p').textContent;
        const price = parseInt(priceText.replace(/\D/g, ''));
        card.style.display = price <= selectedPrice ? 'block' : 'none';
    });
});

/**
 * getPlaceIdFromURL() → extrait l'ID du lieu depuis l'URL
 */
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id') || urlParams.get('placeId');
}

/**
 * setupBackLink() → génère dynamiquement le lien de retour vers les détails du lieu
 */
function setupBackLink() {
    const backLink = document.getElementById('back-link');
    backLink.href = `place.html?id=${currentPlaceId}`; // corriger ici s'il avait mis place-details.html
}

/**
 * setupCharacterCounter() → met à jour le compteur de caractères dans le textarea
 */
function setupCharacterCounter() {
    const reviewTextarea = document.getElementById('review');
    const characterCount = document.getElementById('character-count');

    reviewTextarea.addEventListener('input', function () {
        const currentLength = this.value.length;
        const maxLength = this.getAttribute('maxlength');
        characterCount.textContent = `${currentLength}/${maxLength} characters`;

        if (currentLength > maxLength * 0.9) {
            characterCount.classList.add('warning');
        } else {
            characterCount.classList.remove('warning');
        }
    });
}

/**
 * setupFormSubmission() → gère la validation et l'envoi du formulaire d’avis
 */
function setupFormSubmission() {
    const reviewForm = document.getElementById('review-form');
    reviewForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const reviewText = document.getElementById('review').value.trim();
        const rating = document.getElementById('rating').value;

        if (!reviewText) {
            showError('Please enter a review before submitting.');
            return;
        }
        if (!rating) {
            showError('Please select a rating before submitting.');
            return;
        }

        await submitReview(authToken, currentPlaceId, reviewText, rating);
    });
}

/**
 * loadPlaceInfo() → récupère les infos du lieu via API pour les afficher
 */
async function loadPlaceInfo() {
    const placeInfoDiv = document.getElementById('place-info');

    try {
        const response = await fetch(`/api/places/${currentPlaceId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            const placeData = await response.json();
            placeInfoDiv.innerHTML = `
                <h3>Reviewing: ${escapeHtml(placeData.name || 'Unknown Place')}</h3>
                <p>${escapeHtml(placeData.description?.substring(0, 150) || 'No description available')}${placeData.description?.length > 150 ? '...' : ''}</p>
            `;
        } else {
            placeInfoDiv.innerHTML = `
                <h3>Reviewing Place ID: ${currentPlaceId}</h3>
                <p>Unable to load place details</p>
            `;
        }
    } catch (error) {
        console.error('Error loading place info:', error);
        placeInfoDiv.innerHTML = `
            <h3>Reviewing Place ID: ${currentPlaceId}</h3>
            <p>Unable to load place details</p>
        `;
    }
}

/**
 * submitReview() → envoie les données du formulaire à l’API via POST
 */
async function submitReview(token, placeId, reviewText, rating) {
    const submitButton = document.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;

    try {
        submitButton.textContent = 'Submitting...';
        submitButton.disabled = true;
        hideMessages();

        const response = await fetch(`/api/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                placeId: placeId
            })
        });

        await handleResponse(response);
    } catch (error) {
        console.error('Error submitting review:', error);
        showError('Network error occurred. Please check your connection and try again.');
    } finally {
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
}

/**
 * handleResponse() → gère le retour de l’API après soumission du formulaire
 */
async function handleResponse(response) {
    if (response.ok) {
        showSuccess('Review submitted successfully! Redirecting to place details...');
        document.getElementById('review-form').reset();
        document.getElementById('character-count').textContent = '0/1000 characters';
        document.getElementById('character-count').classList.remove('warning');

        setTimeout(() => {
            window.location.href = `place.html?id=${currentPlaceId}`;
        }, 2000);
    } else {
        let errorMessage = 'Failed to submit review. Please try again.';
        try {
            const errorData = await response.json();
            if (errorData.message) {
                errorMessage = errorData.message;
            }
        } catch (e) {}

        if (response.status === 401) {
            errorMessage = 'Authentication failed. Please log in again.';
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        } else if (response.status === 403) {
            errorMessage = 'You do not have permission to review this place.';
        } else if (response.status === 404) {
            errorMessage = 'Place not found. Please try again.';
        } else if (response.status >= 500) {
            errorMessage = 'Server error occurred. Please try again later.';
        }

        showError(errorMessage);
    }
}

/**
 * showSuccess() → affiche un message de succès
 */
function showSuccess(message) {
    const successDiv = document.getElementById('success-message');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * showError() → affiche un message d’erreur
 */
function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * hideMessages() → cache les messages de feedback
 */
function hideMessages() {
    document.getElementById('success-message').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

/**
 * escapeHtml() → protège contre les injections HTML
 */
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
