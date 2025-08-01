// === Global Variables ===
let authToken = null;
let currentPlaceId = null;

// === DOM Ready ===
document.addEventListener('DOMContentLoaded', () => {
    // Code pour la page de login (non modifié)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    // Pour pages de lieu ou d’avis
    currentPlaceId = getPlaceIdFromURL();

    if (currentPlaceId) {
        authToken = checkAuthentication();
        setupBackLink(); // Cette fonction est pour une page 'review' mais je la garde au cas où
        setupCharacterCounter();
        setupFormSubmission();
        loadPlaceInfo(); // Appel principal pour charger les infos et les avis
    }
});

// === Authentification ===
function loginUser(email, password) {
    return fetch('https://your-api-url/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    }).then(async response => {
        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html';
        } else {
            alert('Login failed: ' + response.statusText);
        }
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';')[0];
    return null;
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (loginLink) loginLink.textContent = token ? 'Logout' : 'Login';
    // Gérer la déconnexion si l'utilisateur clique sur "Logout"
    if (loginLink && token) {
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            document.cookie = `token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;
            window.location.reload();
        });
    }
    return token;
}

// === Task 1 & 2 - Lieux (non modifié) ===
async function fetchPlaces(token) {
    try {
        const response = await fetch('https://your-api-url/places', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const data = await response.json();
            displayPlaces(data.places);
        } else {
            alert('Échec du chargement des lieux : ' + response.statusText);
        }
    } catch (error) {
        console.error('Erreur :', error);
    }
}

function displayPlaces(places) {
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

document.getElementById('price-filter')?.addEventListener('change', (event) => {
    const selectedPrice = parseInt(event.target.value);
    const cards = document.querySelectorAll('.place-card');
    cards.forEach(card => {
        const priceText = card.querySelector('p').textContent;
        const price = parseInt(priceText.replace(/\D/g, ''));
        card.style.display = price <= selectedPrice ? 'block' : 'none';
    });
});

// === Task 3 & 4 - Détails & Avis (modifié) ===
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id') || urlParams.get('placeId');
}

function setupBackLink() {
    const backLink = document.getElementById('back-link');
    if (backLink) backLink.href = `place.html?id=${currentPlaceId}`;
}

function setupCharacterCounter() {
    const reviewTextarea = document.getElementById('review');
    const characterCount = document.getElementById('character-count');

    if (reviewTextarea && characterCount) {
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
}

function setupFormSubmission() {
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const reviewText = document.getElementById('review').value.trim();
            const rating = document.getElementById('rating').value;

            if (!reviewText) return showError('Please enter a review before submitting.');
            if (!rating) return showError('Please select a rating before submitting.');
            if (!authToken) return showError('You must be logged in to submit a review.');

            await submitReview(authToken, currentPlaceId, reviewText, rating);
        });
    }
}

// Fonction MODIFIÉE pour charger les infos du lieu
async function loadPlaceInfo() {
    const placeDetailsDiv = document.getElementById('place-details');
    if (!currentPlaceId) {
        placeDetailsDiv.innerHTML = '<h2>Place not found.</h2>';
        return;
    }

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
            // Génère le HTML pour les détails du lieu
            placeDetailsDiv.innerHTML = `
                <h2>${escapeHtml(placeData.name || 'Beautiful Beach House')}</h2>
                <p><strong>Host:</strong> ${escapeHtml(placeData.host || 'John Doe')}</p>
                <p><strong>Price per night:</strong> $${escapeHtml(placeData.price || '150')}</p>
                <p><strong>Description:</strong> ${escapeHtml(placeData.description || 'A beautiful beach house...')}</p>
                <p><strong>Amenities:</strong> ${escapeHtml(placeData.amenities?.join(', ') || 'WiFi, Pool, Air Conditioning')}</p>
            `;
            // Charge les avis
            loadReviews(placeData.reviews);
        } else {
            placeDetailsDiv.innerHTML = `
                <h2>Place ID: ${currentPlaceId}</h2>
                <p>Unable to load place details</p>
            `;
        }
    } catch (error) {
        console.error('Error loading place info:', error);
        placeDetailsDiv.innerHTML = `
            <h2>Place ID: ${currentPlaceId}</h2>
            <p>Unable to load place details</p>
        `;
    }
}

// Fonction NOUVELLE pour afficher les étoiles
function renderStars(rating) {
    let stars = '';
    for (let i = 0; i < 5; i++) {
        if (i < rating) {
            stars += '<span class="filled-star">★</span>';
        } else {
            stars += '<span>★</span>';
        }
    }
    return `<div class="star-rating">${stars}</div>`;
}

// Fonction NOUVELLE pour afficher les avis
function loadReviews(reviews) {
    const reviewsListDiv = document.getElementById('reviews-list');
    reviewsListDiv.innerHTML = ''; // Vide les avis précédents

    if (!reviews || reviews.length === 0) {
        reviewsListDiv.innerHTML = '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <h4>${escapeHtml(review.userName || 'Anonymous')}:</h4>
            <p>${escapeHtml(review.text)}</p>
            <p>Rating: ${renderStars(review.rating)}</p>
        `;
        reviewsListDiv.appendChild(reviewCard);
    });
}

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

// === Feedback / UI Utilities ===
function hideMessages() {
    document.getElementById('success-message').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

async function handleResponse(response) {
    // ... (votre code existant pour gérer les réponses)
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
            if (errorData.message) errorMessage = errorData.message;
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

function showSuccess(message) {
    const successDiv = document.getElementById('success-message');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showError(message) {
    const errorDiv = document.getElementById('error-message');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}