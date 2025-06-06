# HBnB Project - Technical Documentation
*Comprehensive System Design and Architecture Blueprint*

---

## Table of Contents
1. [Introduction](#introduction)
2. [High-Level Architecture](#high-level-architecture)
3. [Business Logic Layer](#business-logic-layer)
4. [API Interaction Flow](#api-interaction-flow)
5. [Design Decisions and Rationale](#design-decisions-and-rationale)

---

## Introduction

### Project Overview
The HBnB (HolbertonBnB) project is a comprehensive web application that mimics the core functionality of Airbnb. It allows users to register, create place listings, write reviews, and manage amenities in a rental marketplace environment.

### Document Purpose
This technical documentation serves as the definitive blueprint for the HBnB project implementation. It provides detailed architectural diagrams, class structures, and interaction flows that will guide developers throughout the implementation phases. The document ensures consistency, maintainability, and scalability of the system architecture.

### Document Scope
This documentation covers:
- System architecture and design patterns
- Detailed class diagrams and relationships
- API interaction sequences
- Design rationale and implementation guidelines

---

## High-Level Architecture

### System Overview
The HBnB application follows a **three-layered architecture** pattern, implementing the **Facade design pattern** to ensure separation of concerns and maintainable code structure.

```mermaid
classDiagram
    class PresentationLayer {
        <<Interface>>
        +ServiceAPI
        +ServiceUser
        +ServiceReview
        +ServicePlace
        +ServiceAmenity
    }
    
    class BusinessLogicLayer {
        +FacadeBL <<Facade>>
        +User
        +Place
        +Review
        +Amenity
    }
    
    class PersistenceLayer {
        +UserRepository
        +PlaceRepository
        +ReviewRepository
        +AmenityRepository
    }
    
    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
```

### Architecture Layers

**Presentation Layer**
- **Purpose**: Handles all user interactions and API endpoints
- **Components**: RESTful API services for each entity (User, Place, Review, Amenity)
- **Responsibilities**: Request validation, response formatting, HTTP status management
- **Design Pattern**: Service-oriented architecture with dedicated services per entity

**Business Logic Layer**
- **Purpose**: Contains core business rules and application logic
- **Components**: Facade pattern implementation with domain models
- **Responsibilities**: Data validation, business rule enforcement, entity relationships management
- **Design Pattern**: Facade pattern to simplify complex subsystem interactions

**Persistence Layer**
- **Purpose**: Manages data storage and retrieval operations
- **Components**: Repository pattern for each entity
- **Responsibilities**: Database operations, data mapping, query optimization
- **Design Pattern**: Repository pattern for data access abstraction

### Key Architectural Benefits
- **Separation of Concerns**: Each layer has distinct responsibilities
- **Maintainability**: Changes in one layer don't affect others
- **Testability**: Each layer can be tested independently
- **Scalability**: Layers can be scaled independently based on needs

---

## Business Logic Layer

### Domain Model Overview
The Business Logic Layer contains four core entities that represent the main business concepts of the HBnB application.

```mermaid
classDiagram
    class User {
        +id : UUID
        +lastName : str
        +firstName: str
        +password: str
        +email : str
        +created_at : datetime
        +updated_at : datetime
    }
    
    class Place {
        +id : UUID
        +title : str
        +description : str
        +price : int
        +latitude : float
        +longitude : float
        +created_at: datetime
        +updated_at: datetime
    }
    
    class Review {
        +id : UUID
        +place : str
        +user : str
        +rating : int
        +comment : str
        +created_at: datetime
        +updated_at: datetime
    }
    
    class Amenity {
        +id : UUID
        +name: str
        +description: str
        +created_at: datetime
        +updated_at: datetime
        +create() : void
        +update() : void
        +delete() : void
    }

    Place --> User : owned_by
    Review --> User : written_by
    Review --> Place : reviews
    Place o-- Amenity : has_amenities
```

### Entity Descriptions

**User Entity**
- **Purpose**: Represents system users (both guests and hosts)
- **Key Attributes**: 
  - UUID-based identification for security
  - Email serves as unique identifier
  - Password stored with hashing
  - Audit trail with creation/update timestamps
- **Relationships**: One-to-many with Places (as owner) and Reviews (as author)

**Place Entity**
- **Purpose**: Represents rental properties/accommodations
- **Key Attributes**:
  - Descriptive information (title, description)
  - Pricing information
  - Geographic coordinates for location-based searches
  - Audit timestamps
- **Relationships**: 
  - Belongs to one User (owner)
  - Has many Reviews
  - Associated with multiple Amenities

**Review Entity**
- **Purpose**: Represents user feedback on places
- **Key Attributes**:
  - Numeric rating system
  - Text-based comments
  - References to both User and Place
- **Relationships**: 
  - Belongs to one User (reviewer)
  - Belongs to one Place (reviewed property)
- **Business Rules**: One review per user per place

**Amenity Entity**
- **Purpose**: Represents features/services available at places
- **Key Attributes**:
  - Name and description for user-friendly display
  - CRUD operations support
- **Relationships**: Many-to-many with Places
- **Design Note**: Aggregation relationship allows amenities to exist independently

### Relationship Analysis

**User-Place Association**
- Type: One-to-Many
- Rationale: Users can own multiple places, but each place has one owner
- Implementation: Foreign key in Place table

**User-Review Association**
- Type: One-to-Many
- Rationale: Users can write multiple reviews, but each review has one author
- Implementation: Foreign key in Review table

**Place-Review Association**
- Type: One-to-Many
- Rationale: Places can have multiple reviews, but each review is for one place
- Implementation: Foreign key in Review table

**Place-Amenity Aggregation**
- Type: Many-to-Many (Aggregation)
- Rationale: Places can have multiple amenities, amenities can be shared across places
- Implementation: Junction table with foreign keys
- Aggregation Choice: Amenities exist independently of places

---

## API Interaction Flow

### User Registration Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer<br/>(ServiceAPI)
    participant BL as Business Logic Layer<br/>(FacadeBL)
    participant Model as User Model
    participant DB as Persistence Layer<br/>(FacadeDB)

    Client->>API: POST /users<br/>{firstName, lastName, email, password}
    API->>BL: registerUser(userData)
    BL->>Model: validateUserData(userData)
    Model-->>BL: validation result
    
    alt validation successful
        BL->>Model: createUser(userData)
        Model->>Model: hashPassword()
        Model->>Model: generateUniqueId()
        Model->>Model: setCreationDateTime()
        BL->>DB: saveUser(userObject)
        DB->>DB: checkEmailUniqueness()
        DB->>DB: insertUserToDatabase()
        DB-->>BL: user saved successfully
        BL-->>API: user created with ID
        API-->>Client: 201 Created<br/>{userId, message: "User registered"}
    else validation failed
        BL-->>API: validation errors
        API-->>Client: 400 Bad Request<br/>{errors}
    end
```

**Flow Analysis**
- **Security**: Password hashing occurs at model level
- **Validation**: Multi-layered validation (API and Business Logic)
- **Uniqueness**: Email uniqueness enforced at database level
- **Error Handling**: Proper HTTP status codes and error messages
- **Audit Trail**: Automatic timestamp generation

### Place Search Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer<br/>(ServiceAPI)
    participant BL as Business Logic Layer<br/>(FacadeBL)
    participant PlaceModel as Place Model
    participant AmenityModel as Amenity Model
    participant UserModel as User Model
    participant DB as Persistence Layer<br/>(FacadeDB)

    Client->>API: GET /places?location=Paris&minPrice=50&maxPrice=200&amenities=wifi,parking
    API->>BL: getPlaces(filterCriteria)
    BL->>PlaceModel: validateFilters(filterCriteria)
    PlaceModel-->>BL: filters validated
    
    BL->>DB: fetchPlaces(filterCriteria)
    DB->>DB: queryPlacesByLocation()
    DB->>DB: filterByPriceRange()
    DB->>DB: filterByAmenities()
    DB-->>BL: places list
    
    loop for each place
        BL->>UserModel: getOwnerInfo(ownerId)
        UserModel->>DB: getUserById(ownerId)
        DB-->>UserModel: owner data
        UserModel-->>BL: owner info
        
        BL->>AmenityModel: getPlaceAmenities(placeId)
        AmenityModel->>DB: getAmenitiesByPlaceId(placeId)
        DB-->>AmenityModel: amenities list
        AmenityModel-->>BL: place amenities
    end
    
    BL->>PlaceModel: formatPlacesResponse(placesData)
    PlaceModel-->>BL: formatted places
    BL-->>API: places list with details
    API-->>Client: 200 OK<br/>{places: [...], count: X}
```

**Flow Analysis**
- **Query Optimization**: Efficient filtering at database level
- **Data Enrichment**: Additional data (owner, amenities) loaded separately
- **Performance**: Batch processing for related data
- **Response Format**: Structured JSON with metadata (count)

### Review Submission Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer<br/>(ServiceAPI)
    participant BL as Business Logic Layer<br/>(FacadeBL)
    participant ReviewModel as Review Model
    participant UserModel as User Model
    participant PlaceModel as Place Model
    participant DB as Persistence Layer<br/>(FacadeDB)

    Client->>API: POST /reviews<br/>{placeId, userId, rating, comment}
    API->>BL: submitReview(reviewData)
    
    BL->>UserModel: verifyUserExists(userId)
    UserModel->>DB: getUserById(userId)
    DB-->>UserModel: user data
    UserModel-->>BL: user verified
    
    BL->>PlaceModel: verifyPlaceExists(placeId)
    PlaceModel->>DB: getPlaceById(placeId)
    DB-->>PlaceModel: place data
    PlaceModel-->>BL: place verified
    
    BL->>ReviewModel: checkExistingReview(userId, placeId)
    ReviewModel->>DB: findExistingReview(userId, placeId)
    DB-->>ReviewModel: existing review check
    ReviewModel-->>BL: review check result
    
    alt no existing review and valid data
        BL->>ReviewModel: validateReviewData(reviewData)
        ReviewModel-->>BL: validation result
        BL->>ReviewModel: createReview(reviewData)
        ReviewModel->>ReviewModel: generateUniqueId()
        ReviewModel->>ReviewModel: setCreationDateTime()
        BL->>DB: saveReview(reviewObject)
        DB->>DB: insertReviewToDatabase()
        DB-->>BL: review saved successfully
        BL-->>API: review created with ID
        API-->>Client: 201 Created<br/>{reviewId, message: "Review submitted"}
    else review already exists or invalid data
        BL-->>API: error message
        API-->>Client: 400 Bad Request<br/>{error}
    end
```

**Flow Analysis**
- **Data Integrity**: Verification of user and place existence
- **Business Rules**: Enforcement of one-review-per-user-per-place rule
- **Validation**: Multi-step validation process
- **Error Handling**: Comprehensive error scenarios coverage
- **Atomic Operations**: Review creation as single transaction

---

## Design Decisions and Rationale

### Architectural Patterns

**Facade Pattern Implementation**
- **Decision**: Use Facade pattern in Business Logic Layer
- **Rationale**: Simplifies complex interactions between multiple models
- **Benefits**: Reduces coupling, centralizes business logic, improves maintainability
- **Trade-offs**: Additional abstraction layer, potential performance overhead

**Repository Pattern for Data Access**
- **Decision**: Implement Repository pattern in Persistence Layer
- **Rationale**: Abstracts database operations, enables easy testing
- **Benefits**: Database-agnostic code, improved testability, centralized query logic
- **Trade-offs**: Additional code complexity, learning curve

### Data Modeling Decisions

**UUID for Primary Keys**
- **Decision**: Use UUID instead of auto-incrementing integers
- **Rationale**: Enhanced security, distributed system compatibility, no sequential guessing
- **Benefits**: Better security, scalability for distributed systems
- **Trade-offs**: Larger storage requirement, potential performance impact

**Aggregation vs Composition for Place-Amenity**
- **Decision**: Use Aggregation instead of Composition
- **Rationale**: Amenities exist independently and can be shared across places
- **Benefits**: Reusability, consistency, easier maintenance
- **Trade-offs**: More complex queries for place-specific amenity data

### Security Considerations

**Password Handling**
- **Decision**: Hash passwords at model level
- **Rationale**: Ensure passwords are never stored in plain text
- **Implementation**: Bcrypt or similar hashing algorithm
- **Benefits**: Enhanced security, follows best practices

**Email as Unique Identifier**
- **Decision**: Use email as unique user identifier
- **Rationale**: Natural unique identifier, user-friendly
- **Benefits**: Prevents duplicate accounts, easy user identification
- **Trade-offs**: Privacy considerations, potential for email enumeration

### Performance Optimizations

**Lazy Loading for Related Data**
- **Decision**: Load related data (owner, amenities) separately
- **Rationale**: Avoid expensive JOIN operations, load only when needed
- **Benefits**: Better performance for large datasets, flexibility
- **Trade-offs**: Multiple database queries, complexity in data assembly

**Filter Validation**
- **Decision**: Validate search filters before database query
- **Rationale**: Prevent invalid or malicious query parameters
- **Benefits**: Better security, improved error messages, query optimization
- **Trade-offs**: Additional validation logic

### Scalability Considerations

**Stateless Design**
- **Decision**: Design all layers to be stateless
- **Rationale**: Enables horizontal scaling, improves reliability
- **Benefits**: Better scalability, easier deployment, fault tolerance
- **Trade-offs**: Session management complexity

**Database Query Optimization**
- **Decision**: Implement filtering at database level
- **Rationale**: Reduce data transfer, improve response times
- **Benefits**: Better performance, reduced network traffic
- **Trade-offs**: More complex database queries, database-specific optimizations

---

## Implementation Guidelines

### Development Phases
1. **Phase 1**: Implement Persistence Layer and basic CRUD operations
2. **Phase 2**: Develop Business Logic Layer with domain models
3. **Phase 3**: Create Presentation Layer with API endpoints
4. **Phase 4**: Implement complex business flows and validations
5. **Phase 5**: Add security features and optimization

### Testing Strategy
- **Unit Tests**: Each layer should have comprehensive unit tests
- **Integration Tests**: Test interactions between layers
- **API Tests**: End-to-end testing of API endpoints
- **Performance Tests**: Load testing for scalability validation

### Code Quality Standards
- **Naming Conventions**: Use clear, descriptive names for classes and methods
- **Documentation**: All public methods should have comprehensive documentation
- **Error Handling**: Implement consistent error handling across all layers
- **Logging**: Add appropriate logging for debugging and monitoring

---

*This document serves as the foundational reference for the HBnB project implementation. All developers should refer to this documentation to ensure consistency with the established architecture and design patterns.*