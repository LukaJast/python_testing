import subprocess
import os
from pathlib import Path
import shutil

def create_repo(repo_name, repo_path):
    # print(repo_name, repo_path)
    cwd = Path(repo_path)
    cwd.mkdir()
    # os.mkdir(repo_path)
    # cwd = repo_path
    env = os.environ.copy()
    env["LORE_GLOBAL_PATH"] = "temp"
    env["LORE_AUTH_PATH"] = "temp"
    subprocess.run(["lore.exe", "repository", "create", "--offline", repo_name], cwd=repo_path, env=env, capture_output=False, text=True)
    return repo_path, repo_name, env

def create_loreignore(cwd):
    loreignore = Path(cwd) / ".loreignore"
    loreignore.write_text("temp\n")
    first_file = Path(cwd) / "first.txt"
    first_file.write_text("First file\n")
    subpath = Path(cwd) / "sub"
    subpath.mkdir()
    nested_file = subpath / "nested_file.txt"
    nested_file.write_text("Nested file")

def run_lore(env, cwd, *args):
    return subprocess.run(["lore.exe", *args], env=env, cwd=cwd, capture_output=True, text=True)
    
def checking_status(env, cwd):
    print("\n--- lore status --scan ---")
    result = run_lore(env, cwd, "status", "--scan")
    print(result.stdout)
    print(result.stderr)
    print("Return code: ", result.returncode)

def staging(env, cwd):
    print("\n--- lore stage . --scan ---")
    result = run_lore(env, cwd, "stage", ".", "--scan")
    print(result.stdout)
    print(result.stderr)
    print("Return code: ", result.returncode)
    return result

def staging_file(env, cwd, *file_names):
    print(f"\n--- lore stage {' '.join(file_names)} ---")
    result = run_lore(env, cwd, "stage", *file_names)
    print(result.stdout)
    print(result.stderr)
    print("Return code: ", result.returncode)
    return result

def commiting(env, cwd, message):
    print(f"\n--- lore commit {message!r} ---")
    result = run_lore(env,cwd, "commit", message)
    print(result.stdout)
    print(result.stderr)
    print("Return code: ", result.returncode)
    return result, message

def revision_history(env, cwd, depth):
    print(f"\n--- lore revision history {depth} ---")
    result = run_lore(env, cwd, "revision", "history", depth)
    print(result.stdout)
    print(result.stderr)
    print("Return code: ", result.returncode)
    lines = result.stdout.splitlines()
    # print(type(lines))
    # print(lines)
    # print(lines[0])
    # print(lines[4])
    parts = lines[0].split(":")
    revision = int(parts[1].strip())
    # print(revision)
    # print(type(revision))

    return result, revision

# # Phase 1, creating repo, commiting first files
# repo_path, repo_name, env = create_repo("testing", r"E:\python_testing\testing") 
# create_loreignore(repo_path)
# staging(env, repo_path)
# commiting(env, repo_path, "Operation on files")
# checking_status(env, repo_path)

# # Phase 2, work on modified files
# first_file = Path(repo_path) / "first.txt"
# first_file.write_text("First file\nModified line\n")
# checking_status(env, repo_path)
# staging_file(env, repo_path, "first.txt")
# checking_status(env, repo_path)
# result, message = commiting(env, repo_path, "First file modified") # we don't use this result veriable, here but i needed to inlcude it in order to take the second one - message
# checking_status(env, repo_path)

# result, revision = revision_history(env, repo_path, "1")
# print("Revision: ", revision)
# # print("Result STDOUT is: ", result.stdout)
# assert result.returncode == 0
# assert revision == 2
# assert message in result.stdout


# # shutil.rmtree(repo_path)