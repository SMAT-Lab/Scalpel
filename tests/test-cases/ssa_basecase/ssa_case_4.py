"""
The script is retrieved from https://github.com/ishepard/pydriller
"""
count = 0
start_counting = commit_hash is None

for commit in RepositoryMining(path_to_repo, reversed_order=True).traverse_commits():

    if not start_counting and commit_hash == commit.hash:
        start_counting = True

    # Skip commit if not counting
    if not start_counting:
        continue

    for modified_file in commit.modifications:
        if modified_file.filename == filepath:
            count += 1

            # Stop counting if the file has been created at the current commit
            if not modified_file.old_path:
                return count

            # Else rename filepath with the older one (which can be the same)
            filepath = modified_file.old_path

            break

