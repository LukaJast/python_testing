"""Exercise 3 (refactoring) - every lore call goes through run_lore()

You finished this file with five repeated subprocess.run calls. It works,
but changing one detail (e.g. adding --offline everywhere) means editing
five places. A single harness function fixes that: one place to change,
one place to remember.

What you learn here:
- *args: one function taking a variable number of arguments
- capture_output=True + text=True, then echoing the output yourself
- rerun safety: os.mkdir() crashes if the directory already exists

Run:
    python exercise3.py
"""

import os
import subprocess
import sys
from pathlib import Path

LORE_EXE = "lore.exe"


def make_env(global_dir):
    """(Given) Isolated lore env: global and auth paths point at global_dir."""
    env = os.environ.copy()
    env["LORE_GLOBAL_PATH"] = str(global_dir)
    env["LORE_AUTH_PATH"] = str(global_dir)
    return env


def run_lore(env, *args, cwd=None):
    """Your mini-harness: every lore command goes through this one function.

    TODO 1: build the argv list: [LORE_EXE, *args]
            (the * unpacks the args tuple into the list)
            and call subprocess.run with capture_output=True, text=True,
            env=env, cwd=cwd.
    TODO 2: echo result.stdout to sys.stdout and result.stderr to sys.stderr
            (so running the script looks the same as before),
            then return result.
    """
    raise NotImplementedError("TODO 1")


def create_repo(repo_name, repo_path):
    """TODO 3: rewrite this to use make_env + run_lore.

    Old version, for reference:

        os.mkdir(repo_path)
        env = os.environ.copy()
        env["LORE_GLOBAL_PATH"] = "temp"
        env["LORE_AUTH_PATH"] = "temp"
        subprocess.run(["lore.exe", "repository", "create", "--offline", repo_name],
                       cwd=repo_path, env=env, capture_output=False)

    Note: os.mkdir() crashes on rerun because the directory already exists.
    Try Path(repo_path).mkdir(exist_ok=True) instead.
    """
    raise NotImplementedError("TODO 3")


def write_stage_commit(file, content, cwd, global_dir):
    """TODO 4: rewrite this to use make_env + run_lore (four lore calls).

    Old version, for reference:

        (Path(cwd) / file).write_text(content)
        env = os.environ.copy()
        env["LORE_GLOBAL_PATH"] = global_dir
        env["LORE_AUTH_PATH"] = global_dir
        subpath = Path(cwd) / "sub"
        os.mkdir(subpath)
        (subpath / "second.txt").write_text("Another file")
        file2 = str(subpath / "second.txt")
        subprocess.run(["lore.exe", "stage", file, file2], cwd=cwd, env=env,
                       capture_output=False, text=True)
        subprocess.run(["lore.exe", "commit", f"Committing {file}, {file2}"],
                       cwd=cwd, env=env, capture_output=False, text=True)
        subprocess.run(["lore.exe", "revision", "info"], cwd=cwd, env=env,
                       capture_output=False, text=True)
        subprocess.run(["lore.exe", "status"], cwd=cwd, env=env,
                       capture_output=False, text=True)

    Hints: the file writes stay the same; only the lore calls change into
    run_lore(env, "stage", file, file2, cwd=cwd) and friends.
    """
    raise NotImplementedError("TODO 4")


def main():
    create_repo("Exercise3", r"E:\python_testing\Exercise3")
    write_stage_commit(
        "hello.txt",
        "Hello world!",
        r"E:\python_testing\Exercise3",
        r"E:\python_testing\Exercise3\temp",
    )


if __name__ == "__main__":
    main()