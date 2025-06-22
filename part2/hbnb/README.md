# HBnB - Partie 2 : API RESTful avec Flask

## 🎯 Objectif du Projet

Cette deuxième partie du projet **HBnB** consiste à transformer une conception logicielle (déjà élaborée dans la partie 1) en une application **fonctionnelle** et **évolutive**, basée sur l’architecture suivante :

- Une **API RESTful** propulsée par **Flask** et **Flask-RESTx**
- Une couche **logique métier** implémentant les entités cœur du domaine : `User`, `Place`, `Review`, `Amenity`
- Une **architecture modulaire** avec séparation claire des responsabilités
- Un référentiel **en mémoire** pour le stockage temporaire des objets
- Des points de terminaison API organisés proprement sous `/api/v1/`

---

## 🗂️ Structure du Projet

```mermaid
hbnb/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── persistence/
│   │   └── repository.py
│   ├── services/
│   │   └── facade.py
│   └── __init__.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
```

---

## 🧠 Architecture : modèle de façade

Un **modèle de conception Façade** centralise les interactions entre les couches de **Présentation**, **Logique métier** et **Persistance** :

```mermaid
[ Flask RESTx Routes ]
         ↓
[ API Handlers ]
         ↓
     HBnBFacade
         ↓
[ InMemoryRepository ]
         ↑
[ Entités Métier ]
```

Ce modèle permet :
- Une séparation nette des responsabilités
- Une testabilité accrue
- Une future migration simple vers SQLAlchemy

---

## 👤 Entités Métier

### User
- `id`, `first_name`, `last_name`, `email`, `is_admin`, `created_at`, `updated_at`

### Place
- `id`, `title`, `description`, `price`, `latitude`, `longitude`, `owner`, `amenities`, `reviews`, `created_at`, `updated_at`

### Amenity
- `id`, `name`, `created_at`, `updated_at`

### Review
- `id`, `text`, `rating`, `user`, `place`, `created_at`, `updated_at`

Chaque entité hérite de `BaseModel` : UUID, timestamps et méthode `update()` générique.