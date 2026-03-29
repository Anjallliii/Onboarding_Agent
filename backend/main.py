from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from agents import OnboardingOrchestrator
from database import audit_collection

app = FastAPI()
orchestrator = OnboardingOrchestrator()

# Data validation model
class EmployeeData(BaseModel):
    name: str
    role: str
    department: str

@app.post("/start-onboarding")
async def start_onboarding(employee: EmployeeData, background_tasks: BackgroundTasks):
    # Unique ID generate karo har onboarding ke liye
    workflow_id = str(uuid.uuid4())
    
    # Convert Pydantic model to dictionary
    data = employee.dict()
    
    # BackgroundTasks use kar rahe hain taaki API turant response de 
    # aur agents peeche kaam karte rahein (Autonomy)
    background_tasks.add_task(orchestrator.run_full_workflow, workflow_id, data)
    
    return {
        "status": "Started", 
        "workflow_id": workflow_id, 
        "message": f"Onboarding agents triggered for {employee.name}"
    }

@app.get("/audit-logs/{workflow_id}")
async def get_audit_logs(workflow_id: str):
    # MongoDB se logs fetch karo
    logs = await audit_collection.find({"workflow_id": workflow_id}).to_list(length=100)
    
    # Frontend ke liye clean format
    return [{
        "message": log["message"], 
        "agent": log["agent"], 
        "timestamp": log["timestamp"]
    } for log in logs]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)