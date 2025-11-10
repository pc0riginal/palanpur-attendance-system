from django.conf import settings
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

_mongo_client = None
_mongodb = None

def get_mongodb():
    """Get MongoDB database instance"""
    global _mongo_client, _mongodb
    
    if _mongodb is None:
        try:
            # Add connection timeout and retry settings
            _mongo_client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                socketTimeoutMS=20000,
                connectTimeoutMS=20000,
                maxPoolSize=10,
                retryWrites=True
            )
            _mongodb = _mongo_client[settings.MONGODB_NAME]
            # Test connection
            _mongo_client.server_info()
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            _mongodb = None
    
    return _mongodb

class MongoDBManager:
    """Manager class for MongoDB operations"""
    
    def __init__(self, collection_name):
        self.db = get_mongodb()
        self.collection = self.db[collection_name] if self.db is not None else None
    
    def _ensure_connection(self):
        """Ensure MongoDB connection is healthy"""
        if self.db is None:
            self.db = get_mongodb()
            self.collection = self.db[self.collection.name] if self.db is not None else None
        return self.collection is not None
    
    def insert_one(self, document):
        """Insert a single document"""
        if self._ensure_connection():
            return self.collection.insert_one(document)
        return None
    
    def insert_many(self, documents):
        """Insert multiple documents"""
        if self.collection is not None:
            return self.collection.insert_many(documents)
        return None
    
    def find_one(self, query):
        """Find a single document"""
        if self._ensure_connection():
            return self.collection.find_one(query)
        return None
    
    def find(self, query=None, sort=None, limit=None, skip=None):
        """Find multiple documents"""
        if self.collection is not None:
            cursor = self.collection.find(query or {})
            if sort:
                cursor = cursor.sort(sort)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            return list(cursor)
        return []
    
    def update_one(self, query, update):
        """Update a single document with retry logic"""
        if self._ensure_connection():
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    return self.collection.update_one(query, {'$set': update})
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"Update attempt {attempt + 1} failed: {e}")
                    import time
                    time.sleep(1)  # Wait 1 second before retry
        return None
    
    def update_many(self, query, update):
        """Update multiple documents"""
        if self.collection is not None:
            return self.collection.update_many(query, {'$set': update})
        return None
    
    def delete_one(self, query):
        """Delete a single document"""
        if self.collection is not None:
            return self.collection.delete_one(query)
        return None
    
    def delete_many(self, query):
        """Delete multiple documents"""
        if self.collection is not None:
            return self.collection.delete_many(query)
        return None
    
    def count(self, query=None):
        """Count documents"""
        if self.collection is not None:
            return self.collection.count_documents(query or {})
        return 0
