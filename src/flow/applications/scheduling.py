def schedule_jobs_to_machines(
    jobs,
    machines,
    allowed,
    capacities,
    solver="ek"
):
    """
    Assign jobs to machines while respecting:
    - allowed machine constraints per job
    - machine capacities

    Returns a dict with:
    {
        "assignment_count": int,
        "assignments": {job: machine},
        "unassigned_jobs": [job, ...],
        "schedule": {machine: [job, ...]}
    }

    The `solver` parameter is accepted for API compatibility.
    """

    # --- validation ---
    for job in jobs:
        if job not in allowed:
            raise ValueError(f"Missing allowed mapping for job {job}")

    for job, machine_list in allowed.items():
        for machine in machine_list:
            if machine not in machines:
                raise ValueError(f"Unknown machine {machine} for job {job}")

    for machine in machines:
        if machine not in capacities:
            raise ValueError(f"Missing capacity for machine {machine}")
        if capacities[machine] < 0:
            raise ValueError(f"Negative capacity for machine {machine}")

    # Expand machines into capacity slots
    slot_to_machine = {}
    for machine in machines:
        for i in range(capacities[machine]):
            slot = f"{machine}_{i}"
            slot_to_machine[slot] = machine

    # Build adjacency list: each job connects to all slots of allowed machines
    adjacency = {}
    for job in jobs:
        neighbors = []
        for machine in allowed[job]:
            for i in range(capacities[machine]):
                neighbors.append(f"{machine}_{i}")
        adjacency[job] = neighbors

    # DFS-based bipartite matching
    slot_match = {}  # slot -> job

    def try_assign(job, seen):
        for slot in adjacency[job]:
            if slot in seen:
                continue
            seen.add(slot)

            if slot not in slot_match or try_assign(slot_match[slot], seen):
                slot_match[slot] = job
                return True
        return False

    for job in jobs:
        try_assign(job, set())

    # Convert slot->job into job->machine
    assignments = {}
    schedule = {machine: [] for machine in machines}

    for slot, job in slot_match.items():
        machine = slot_to_machine[slot]
        assignments[job] = machine
        schedule[machine].append(job)

    # Keep machine job lists deterministic
    for machine in schedule:
        schedule[machine].sort()

    unassigned_jobs = [job for job in jobs if job not in assignments]

    return {
        "assignment_count": len(assignments),
        "assignments": assignments,
        "unassigned_jobs": unassigned_jobs,
        "schedule": schedule,
    }