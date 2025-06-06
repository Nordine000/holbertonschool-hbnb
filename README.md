HBnB Evolution : Technique de Documentation (Partie 1)
Ce dépôt contient la documentation technique initiale pour HBnB Evolution , une application simplifiée de type AirBnB. Cette première partie est dédiée à la définition de l'architecture, de la logique métier et des flux d'interaction du système.

1. Aperçu du projet
HBnB Evolution est conçu pour permettre la gestion des utilisateurs, des propriétés (lieux), des avis et des équipements. Les fonctionnalités principales incluent :

Gestion des utilisateurs : Inscription, mise à jour de profil, identification des rôles (utilisateur/administrateur).
Gestion des lieux : Création, modification et liste de propriétés avec détails (prix, localisation, équipements).
Gestion des avis : Soumission, modification et liste d'avis pour les lieux visités.
Gestion des équipements : Création, modification et liste d'équipements associés aux lieux.
Toutes les entités possèdent un identifiant unique ainsi que des horodatages de création et de mise à jour pour l'audit.

2. Architecture de l'application
L'application convient à une architecture en trois couches pour une meilleure modularité et maintenabilité :

Couche de Présentation : Gère les interactions utilisateur via l'API.
Couche de Logique Métier : Contient les règles et modèles fondamentaux de l'application.
Couche de Persistance : S'occupe du stockage et de la récupération des données en base de données.
La communication entre ces canapés est facilitée par un patron Facade , simplifiant l'interface entre la présentation et la logique métier.

Vous trouverez le schéma de paquetage détaillé illustrant cette architecture et le patron Façade dans le fichier high_level_package_diagram.mmd.

3. Conception de la logique métier
La couche de logique métier est le cœur du système, définissant les entités clés et leurs relations : Utilisateur, Lieu, Aviset Équipement.

Utilisateur : Gère les informations des utilisateurs et leurs rôles.
Lieu : Représente une propriété à louer, liée à un propriétaire et pouvant recevoir des avis et des équipements.
Avis : Contient la note et le commentaire d'un utilisateur pour un lieu spécifique.
Équipement : Décrivez les fonctionnalités ou services disponibles dans un lieu.
Chaque entité partage des attributs communs comme un ID unique et des dates de création/mise à jour.

Le diagramme de classes détaillé pour ces entités, leurs attributs, méthodes et relations, est disponible dans le fichier business_logic_class_diagram.mmd.

4. Flux d'interaction des API
Des diagrammes de séquence ont été créés pour illustrer comment les différents couches de l'application interagissent lors des appels API majeurs. Ces diagrammes montrent le déroulement des opérations, de la réception de la requête à la réponse finale.

Les flux d'API documentés incluent :

Inscription d'un utilisateur
Création d'un lieu
Soumission d'un avis
Récupération d'une liste de lieux
Chaque flux d'interaction est détaillé dans son propre fichier de diagramme de séquence (.mmd), par exemple user_registration_sequence.mmd.

5. Visualisation des diagrammes
Les diagrammes de ce projet sont écrits en syntaxe Mermaid.js . Pour le visualiser correctement, vous aurez besoin d'un éditeur de texte ou d'une plateforme (comme GitHub) qui prend en charge le rendu Mermaid.js.