class VersionControl:
    def __init__(self, initial_files=None):
        """
        initial_files: dict mapping filename -> contents/value
        """
        self.versions = [dict(initial_files or {})]
        self.messages = ["Initial commit"]

    def commit(self, changes, message="Commit"):
        """
        changes: dict mapping filename -> new value
                 if value is None, delete the file
        """
        new_state = dict(self.versions[-1])

        for filename, value in changes.items():
            if value is None:
                new_state.pop(filename, None)
            else:
                new_state[filename] = value

        self.versions.append(new_state)
        self.messages.append(message)
        return len(self.versions) - 1

    def get_file(self, version, filename):
        return self.versions[version].get(filename)

    def list_files(self, version):
        return sorted(self.versions[version].keys())

    def diff(self, version_a, version_b):
        files_a = self.versions[version_a]
        files_b = self.versions[version_b]

        all_files = sorted(set(files_a.keys()) | set(files_b.keys()))
        result = {"added": [], "removed": [], "modified": []}

        for filename in all_files:
            in_a = filename in files_a
            in_b = filename in files_b

            if not in_a and in_b:
                result["added"].append(filename)
            elif in_a and not in_b:
                result["removed"].append(filename)
            elif files_a[filename] != files_b[filename]:
                result["modified"].append(filename)

        return result

    def latest_version(self):
        return len(self.versions) - 1

    def history(self):
        return list(enumerate(self.messages))