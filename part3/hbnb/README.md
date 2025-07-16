# 📊 Diagramme Entité-Relation – Projet HBnB

Ce diagramme représente la structure du schéma de base de données du projet HBnB, incluant les entités principales et leurs relations telles que définies dans le modèle relationnel.

## 🧬 Entités incluses :
- `User`
- `Place`
- `Review`
- `Amenity`
- `Place_Amenity` (table de jointure)

## 🔗 Relations :
- Un `User` peut posséder plusieurs `Places`
- Un `User` peut écrire plusieurs `Reviews`
- Un `Place` peut avoir plusieurs `Reviews`
- Un `Place` peut être lié à plusieurs `Amenities`
- Un `Amenity` peut être partagé par plusieurs `Places`

---

```mermaid
erDiagram
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : included_in

    USER {
        CHAR(36) id PK
        VARCHAR(255) first_name
        VARCHAR(255) last_name
        VARCHAR(255) email UNIQUE
        VARCHAR(255) password
        BOOLEAN is_admin
    }

    PLACE {
        CHAR(36) id PK
        VARCHAR(255) title
        TEXT description
        DECIMAL(10,2) price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id FK
    }

    REVIEW {
        CHAR(36)