// React Example for handling the workflow
const startOnboarding = async (employeeData) => {
  // 1. Backend ko request bhejo
  const response = await fetch('http://127.0.0.1:8000/start-onboarding', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(employeeData)
  });
  
  const result = await response.json();
  const workflowId = result.workflow_id;

  // 2. Interval set karo logs fetch karne ke liye (Audit Trail live dikhane ke liye)
  const interval = setInterval(async () => {
    const logResponse = await fetch(`http://127.0.0.1:8000/audit-logs/${workflowId}`);
    const logs = await logResponse.json();
    
    // UI state update karo logs ke saath
    setAuditLogs(logs);

    // Agar last log "Success" ya "Completed" hai, toh polling band kar do
    if (logs.some(log => log.message.includes("successfully"))) {
      clearInterval(interval);
      setWorkflowStatus("COMPLETED");
    }
  }, 2000); // Har 2 second mein update
};