import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.flow.applications.scheduling import schedule_jobs_to_machines


jobs = ["JobA", "JobB", "JobC", "JobD"]
machines = ["Machine1", "Machine2"]

allowed_assignments = {
    "JobA": ["Machine1", "Machine2"],
    "JobB": ["Machine1"],
    "JobC": ["Machine2"],
    "JobD": ["Machine1", "Machine2"],
}

machine_capacities = {
    "Machine1": 2,
    "Machine2": 1,
}

result = schedule_jobs_to_machines(
    jobs,
    machines,
    allowed_assignments,
    machine_capacities,
    solver="ek",
)

print("Assigned jobs:", result["assignment_count"])
print("Unassigned jobs:", result["unassigned_jobs"])
print("Schedule:")
for machine, assigned_jobs in result["schedule"].items():
    print(f"  {machine}: {assigned_jobs}")