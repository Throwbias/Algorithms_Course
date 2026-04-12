from advds.applications.version_control import VersionControl


def test_version_control_initial_state():
    vc = VersionControl({"a.txt": "hello", "b.txt": "world"})

    assert vc.get_file(0, "a.txt") == "hello"
    assert vc.get_file(0, "b.txt") == "world"
    assert vc.list_files(0) == ["a.txt", "b.txt"]


def test_version_control_commit_new_file():
    vc = VersionControl({"a.txt": "hello"})

    v1 = vc.commit({"b.txt": "world"}, message="Add b.txt")

    assert v1 == 1
    assert vc.get_file(0, "b.txt") is None
    assert vc.get_file(v1, "b.txt") == "world"


def test_version_control_modify_file():
    vc = VersionControl({"a.txt": "hello"})

    v1 = vc.commit({"a.txt": "HELLO"}, message="Modify a.txt")

    assert vc.get_file(0, "a.txt") == "hello"
    assert vc.get_file(v1, "a.txt") == "HELLO"


def test_version_control_delete_file():
    vc = VersionControl({"a.txt": "hello", "b.txt": "world"})

    v1 = vc.commit({"b.txt": None}, message="Delete b.txt")

    assert vc.get_file(0, "b.txt") == "world"
    assert vc.get_file(v1, "b.txt") is None
    assert vc.list_files(v1) == ["a.txt"]


def test_version_control_diff():
    vc = VersionControl({"a.txt": "hello", "b.txt": "world"})

    v1 = vc.commit(
        {
            "a.txt": "HELLO",
            "c.txt": "new file",
            "b.txt": None,
        },
        message="Mixed changes"
    )

    diff = vc.diff(0, v1)

    assert diff["added"] == ["c.txt"]
    assert diff["removed"] == ["b.txt"]
    assert diff["modified"] == ["a.txt"]


def test_version_control_history():
    vc = VersionControl({"a.txt": "hello"})
    vc.commit({"b.txt": "world"}, message="Add b")
    vc.commit({"a.txt": "updated"}, message="Update a")

    history = vc.history()

    assert history[0] == (0, "Initial commit")
    assert history[1] == (1, "Add b")
    assert history[2] == (2, "Update a")