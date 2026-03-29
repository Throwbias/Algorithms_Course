from src.flow.applications.scheduling import schedule_jobs_to_machines


def test_schedule_all_jobs_when_capacity_allows():
    jobs = ["J1", "J2", "J3"]
    machines = ["M1", "M2"]

    allowed = {
        "J1": ["M1", "M2"],
        "J2": ["M1"],
        "J3": ["M2"],
    }

    capacities = {
        "M1": 2,
        "M2": 1,
    }

    result = schedule_jobs_to_machines(jobs, machines, allowed, capacities, solver="ek")

    assert result["assignment_count"] == 3
    assert len(result["unassigned_jobs"]) == 0

    assigned = []
    for machine_jobs in result["schedule"].values():
        assigned.extend(machine_jobs)

    assert set(assigned) == set(jobs)


def test_schedule_respects_machine_capacities():
    jobs = ["J1", "J2", "J3", "J4"]
    machines = ["M1", "M2"]

    allowed = {
        "J1": ["M1", "M2"],
        "J2": ["M1", "M2"],
        "J3": ["M1", "M2"],
        "J4": ["M1", "M2"],
    }

    capacities = {
        "M1": 1,
        "M2": 2,
    }

    result = schedule_jobs_to_machines(jobs, machines, allowed, capacities, solver="ek")

    assert result["assignment_count"] == 3
    assert len(result["schedule"]["M1"]) <= 1
    assert len(result["schedule"]["M2"]) <= 2
    assert len(result["unassigned_jobs"]) == 1


def test_schedule_matches_push_relabel():
    jobs = ["J1", "J2", "J3", "J4"]
    machines = ["M1", "M2", "M3"]

    allowed = {
        "J1": ["M1", "M2"],
        "J2": ["M2"],
        "J3": ["M2", "M3"],
        "J4": ["M1", "M3"],
    }

    capacities = {
        "M1": 1,
        "M2": 2,
        "M3": 1,
    }

    result_ek = schedule_jobs_to_machines(jobs, machines, allowed, capacities, solver="ek")
    result_pr = schedule_jobs_to_machines(jobs, machines, allowed, capacities, solver="pr")

    assert result_ek["assignment_count"] == result_pr["assignment_count"] == 4


def test_schedule_rejects_unknown_machine():
    jobs = ["J1"]
    machines = ["M1"]

    allowed = {
        "J1": ["BAD_MACHINE"],
    }

    capacities = {
        "M1": 1,
    }

    try:
        schedule_jobs_to_machines(jobs, machines, allowed, capacities, solver="ek")
        assert False, "Expected ValueError for unknown machine"
    except ValueError:
        assert True


def test_schedule_rejects_missing_job_definition():
    jobs = ["J1", "J2"]
    machines = ["M1"]

    allowed = {
        "J1": ["M1"],
    }

    capacities = {
        "M1": 1,
    }

    try:
        schedule_jobs_to_machines(jobs, machines, allowed, capacities, solver="ek")
        assert False, "Expected ValueError for missing job entry"
    except ValueError:
        assert True