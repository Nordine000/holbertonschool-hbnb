#!/usr/bin/python3
"""
Repository interface and implementations for data persistence
"""
from abc import ABC, abstractmethod
from app import db

class Repository(ABC):
    """Abstract base class for repository pattern"""
    
    @abstractmethod
    def add(self, obj):
        """Add an object to the repository"""
        pass
    
    @abstractmethod
    def get(self, obj_id):
        """Get an object by its ID"""
        pass
    
    @abstractmethod
    def get_all(self):
        """Get all objects from the repository"""
        pass
    
    @abstractmethod
    def update(self, obj_id, data):
        """Update an object in the repository"""
        pass
    
    @abstractmethod
    def delete(self, obj_id):
        """Delete an object from the repository"""
        pass
    
    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute"""
        pass

class InMemoryRepository(Repository):
    """In-memory repository implementation for development/testing"""
    
    def __init__(self):
        self._storage = {}
    
    def add(self, obj):
        """Add an object to the in-memory storage"""
        self._storage[obj.id] = obj
        return obj
    
    def get(self, obj_id):
        """Get an object by its ID"""
        return self._storage.get(obj_id)
    
    def get_all(self):
        """Get all objects from storage"""
        return list(self._storage.values())
    
    def update(self, obj_id, obj):
        """Update an object in storage"""
        if obj_id in self._storage:
            self._storage[obj_id] = obj
            return obj
        return None
    
    def delete(self, obj_id):
        """Delete an object from storage"""
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute"""
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None

class SQLAlchemyRepository(Repository):
    """SQLAlchemy repository implementation for database persistence"""
    
    def __init__(self, model):
        """
        Initialize repository with a specific model
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    def add(self, obj):
        """
        Add an object to the database
        
        Args:
            obj: Object instance to add
            
        Returns:
            obj: The added object
        """
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get(self, obj_id):
        """
        Get an object by its ID
        
        Args:
            obj_id: ID of the object to retrieve
            
        Returns:
            Object instance or None if not found
        """
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """
        Get all objects of this model type
        
        Returns:
            List of all objects
        """
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """
        Update an object in the database
        
        Args:
            obj_id: ID of the object to update
            data: Dictionary of data to update
            
        Returns:
            Updated object or None if not found
        """
        try:
            obj = self.get(obj_id)
            if obj:
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                db.session.commit()
                return obj
            return None
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, obj_id):
        """
        Delete an object from the database
        
        Args:
            obj_id: ID of the object to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            obj = self.get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_by_attribute(self, attr_name, attr_value):
        """
        Get an object by a specific attribute
        
        Args:
            attr_name: Name of the attribute
            attr_value: Value of the attribute
            
        Returns:
            Object instance or None if not found
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
    
    def get_by_attributes(self, **kwargs):
        """
        Get objects by multiple attributes
        
        Args:
            **kwargs: Attribute name-value pairs
            
        Returns:
            List of matching objects
        """
        return self.model.query.filter_by(**kwargs).all()
