"""Cwiczenie 6 — tryb --json (NDJSON): maszynowy output Lore

Cel: parsowanie NDJSON (JSON line-by-line), zdarzenie "complete",
wyciaganie konkretnych wartosci (branchName, isCurrent) do assertow.

Uruchomienie:
    python exercise_06_json.py
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

LORE_EXE = r"E:\github\lore\target\release\lore.exe"


def make_workspace() -> tuple[Path, Path, dict]:
    work = Path(tempfile.mkdtemp(prefix="lore_ex6_"))
    global_dir = work / "global"
    global_dir.mkdir()
    repo = work / "repo"
    repo.mkdir()
    env = os.environ.copy()
    env["LORE_GLOBAL_PATH"] = str(global_dir)
    env["LORE_AUTH_PATH"] = str(global_dir)
    return work, repo, env


def run_lore(repo: Path, env: dict, *args: str, cwd: Path | None = None):
    argv = [LORE_EXE, "--repository", str(repo), "--offline", *args]
    return subprocess.run(argv, capture_output=True, text=True, env=env, cwd=cwd)


def setup_repo(repo: Path, env: dict) -> None:
    result = run_lore(repo, env, "repository", "create")
    assert result.returncode == 0, f"{result.stdout}{result.stderr}"
    (repo / "hello.txt").write_text("hello lore\n", encoding="utf-8")
    result = run_lore(repo, env, "stage", "hello.txt", cwd=repo)
    assert result.returncode == 0, f"{result.stdout}{result.stderr}"
    result = run_lore(repo, env, "commit", "initial commit", cwd=repo)
    assert result.returncode == 0, f"{result.stdout}{result.stderr}"


def parse_ndjson(stdout: str) -> list[dict]:
    """Zwraca liste zdarzen (słownikow) z outputu NDJSON."""
    # TODO 1: dla kazdej NIEPUSTEJ linii w stdout: json.loads(linia)
    #         (wskazówka: splitlines())
    raise NotImplementedError("TODO 1")


def main() -> None:
    work, repo, env = make_workspace()
    setup_repo(repo, env)

    # TODO 2: status --json:
    #   result = run_lore(repo, env, "status", "--json", cwd=repo)
    #   assert result.returncode == 0
    #   events = parse_ndjson(result.stdout)
    #   - ostatnie zdarzenie ma tagName == "complete" i data["status"] == 0
    #   - znajdź zdarzenie repositoryStatusRevision i wypisz branchName
    #     (powinno byc "main")

    # TODO 3: branch list --json:
    #   zbierz wszystkie zdarzenia branchListEntry,
    #   wypisz liste nazw (data["name"]),
    #   znajdź galeź z data["isCurrent"] == True i wypisz jej nazwe.

    # TODO 4 (obserwacja, bez assertow): revision info --json
    #   - process rc?
    #   - ostatnie zdarzenie complete ma status 0? Dlaczego nie?
    #   (patrz README, puzapka 2: zdarzenie RPC != exit code procesu)


if __name__ == "__main__":
    main()
