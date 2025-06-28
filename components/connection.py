import pymongo

def get_database():
    try:
        # Connect to MongoDB server
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # Access the "PLP" database
        db = client["PLP"]

        # Check if the database exists by listing names
        if "PLP" in client.list_database_names():
            print("✅ MongoDB connection successful.")
        else:
            print("⚠️ MongoDB connected, but database 'PLP' not yet created (will be created on first insert).")

        return db

    except pymongo.errors.ConnectionFailure as e:
        print("❌ Failed to connect to MongoDB:", e)
        return None
