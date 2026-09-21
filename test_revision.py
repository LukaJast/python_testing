import pytest
from pathlib import Path

from exercise3a_harness import create_repo, revision_history,create_loreignore, run_lore, checking_status, staging, staging_file,commiting, revision_history  
def test_revision_history():
    repo_path, repo_name, env = create_repo("testing", r"E:\python_testing\testing") 
    create_loreignore(repo_path)
    staging(env, repo_path)
    commiting(env, repo_path, "Operation on files")
    checking_status(env, repo_path)

    # Phase 2, work on modified files
    first_file = Path(repo_path) / "first.txt"
    first_file.write_text("First file\nModified line\n")
    # checking_status(env, repo_path)
    staging_file(env, repo_path, "first.txt")
    checking_status(env, repo_path)
    result, message = commiting(env, repo_path, "First file modified") # we don't use this result veriable, here but i needed to inlcude it in order to take the second one - message
    checking_status(env, repo_path)

    result, revision = revision_history(env, repo_path, "1")
    print("Revision: ", revision)
    # print("Result STDOUT is: ", result.stdout)
    assert result.returncode == 0
    assert revision == 2
    assert message in result.stdout
