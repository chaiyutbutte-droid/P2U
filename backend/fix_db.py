
import pymongo
from config import Config

# Parse MongoDB URI
# Assuming Config.MONGODB_SETTINGS["host"] is the URI
uri = Config.MONGODB_SETTINGS["host"]
db_name = Config.MONGODB_SETTINGS["db"]

client = pymongo.MongoClient(uri)
db = client[db_name]
users_collection = db["users"]

print("Removing 'topup_transactions' field from all users...")
result = users_collection.update_many(
    {}, 
    {"$unset": {"topup_transactions": ""}}
)

print(f"Matched {result.matched_count} users, modified {result.modified_count} users.")
