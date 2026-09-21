"""Cwiczenie 4 — galezie: branch create / branch switch --local / branch list

Gotowe: setup + repo + jeden commit (rozwiązania cw. 2-3 skrócone).
Twoje zadania: create, switch, list.

Uruchomienie:
    python exercise_04_branches.py
"""

import os
import subprocess
import tempfile
from pathlib import Path

LORE_EXE = r"E:\github\lore\target\release\lore.exe"


def make_workspace() -> tuple[Path, Path, dict]:
    work = Path(tempfile.mkdtemp(prefix="lore_ex4_"))
    global_dir = work / "global"
    global_dir.mkdir()
    repo = work / "repo"
    repo.mkdir()
    env = os.environ.copy()
    env["LORE_GLOBAL_PATH"] = str(global_dir)
    env["LORE_AUTH_PATH"] = str(global_dir)
    return work, repo, env


def run_lore(repo: Path, env: dict, *args: str, cwd: Path | None = None):
    """(rozwiązanie cw. 3) Twoj mini-harness."""
    argv = [LORE_EXE, "--repository", str(repo), "--offline", *args]
    return subprocess.run(argv, capture_output=True, text=True, env=env, cwd=cwd)


def setup_repo(repo: Path, env: dict) -> None:
    """(rozwiązania cw. 2-3) repo + jeden commit."""
    result = run_lore(repo, env, "repository", "create")
    assert result.returncode == 0, f"{result.stdout}{result.stderr}"
    (repo / "hello.txt").write_text("hello lore\n", encoding="utf-8")
    result = run_lore(repo, env, "stage", "hello.txt", cwd=repo)
    assert result.returncode == 0, f"{result.stdout}{result.stderr}"
    result = run_lore(repo, env, "commit", "initial commit", cwd=repo)
    assert result.returncode == 0, f"{result.stdout}{result.stderr}"


def main() -> None:
    work, repo, env = make_workspace()
    setup_repo(repo, env)

    # TODO 1: utwórz galeź:
    #   run_lore(repo, env, "branch", "create", "feature-x", cwd=repo)
    #   assert "Created branch feature-x" w stdout

    # TODO 2: przejdź na nia (offline = lokalna najnowsza rewizja):
    #   run_lore(repo, env, "branch", "switch", "feature-x", "--local", cwd=repo)
    #   assert "Switched to branch feature-x" w stdout
    #   Pytanie: dlaczego --local? Co sie dzieje bez niego w trybie offline?

    # TODO 3: wypisz galezie i sprawdz marker biezacej:
    #   run_lore(repo, env, "branch", "list", cwd=repo)
    #   assert "* feature-x" w stdout  (gwiazdka = biezaca galez)
    #   assert "main" w stdout

    # ZADANIE (opcjonalne): commit na feature-x i porównaj
    # "revision history --oneline" przed i po.


if __name__ == "__main__":
    main()
