import asyncio
import random
from database import add_audit_log

class OnboardingOrchestrator:
    def __init__(self):
        # Steps define karein
        self.workflow_steps = [
            "create_employee", 
            "create_email", 
            "assign_laptop", 
            "enroll_training", 
            "send_notification"
        ]

    async def run_full_workflow(self, workflow_id, employee_data):
        """Pure workflow ko autonomously chalane wala function"""
        await add_audit_log(workflow_id, f"Workflow started for {employee_data['name']}")

        for step in self.workflow_steps:
            await add_audit_log(workflow_id, f"Starting step: {step}")
            
            # Har step ko execute karo
            success = await self.execute_task(step)

            if not success:
                # Agar fail hua toh Recovery Agent ko bulao (Self-Correction)
                await add_audit_log(workflow_id, f"FAILURE detected in {step}", "MONITOR")
                recovered = await self.recovery_agent(workflow_id, step)
                
                if not recovered:
                    await add_audit_log(workflow_id, f"Workflow stalled at {step}", "ORCHESTRATOR")
                    return False
            else:
                await add_audit_log(workflow_id, f"Successfully completed: {step}")
            
            # Simulation ke liye thoda gap
            await asyncio.sleep(1)

        await add_audit_log(workflow_id, "Workflow completed successfully!", "ORCHESTRATOR")
        return True

    async def execute_task(self, step):
        """Simulate execution logic"""
        # Demo ke liye 'assign_laptop' ko intentionally fail karwayenge
        if step == "assign_laptop":
            return False # Simulate failure
        return True

    async def recovery_agent(self, workflow_id, failed_step):
        """Self-correction logic (Hackathon High-Score Point)"""
        await add_audit_log(workflow_id, f"Recovery Agent analyzing {failed_step} failure...", "RECOVERY")
        
        # Decision logic (Yahan aap OpenAI call bhi kar sakte hain reasoning ke liye)
        await asyncio.sleep(2) 
        
        recovery_action = "Assigned temporary loaner laptop from buffer stock"
        await add_audit_log(workflow_id, f"SELF-CORRECTED: {recovery_action}", "RECOVERY")
        
        return True