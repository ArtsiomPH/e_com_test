import motor.motor_asyncio

db_url = "mongodb://mongodb:27017"


client = motor.motor_asyncio.AsyncIOMotorClient(db_url)

db = client["test-form"]
forms_collection = db["forms"]
