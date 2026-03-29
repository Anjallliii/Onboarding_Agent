import motor.motor_asyncio
import os
from dotenv import load_dotenv

# .env file load karo
load_dotenv()

# MongoDB connection (agar local hai toh default yahi rahega)
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.onboarding_db
audit_collection = database.get_collection("audit_logs")

# Function jo har step ko save karega (Audit Trail)
async def add_audit_log(workflow_id: str, message: str, agent: str = "ORCHESTRATOR"):
    log_entry = {
        "workflow_id": workflow_id,
        "message": message,
        "agent": agent,
        "timestamp": os.popen('date /t').read().strip() # Simple Windows date
    }
    await audit_collection.insert_one(log_entry)
    print(f"[{agent}] {message}")