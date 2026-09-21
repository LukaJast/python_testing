"""Cwiczenie 3 — cykl zycia zmian: stage -> status -> commit -> history

Gotowe (rozwiązania cwiczenia 2): make_workspace + create_repo.
Twoje zadania: pisanie plików, stage, status (PUŁAPKA cwd!), commit, history.

Uruchomienie:
    python exercise_03_lifecycle.py
"""

import os
import subprocess
import tempfile
from pathlib import Path

LORE_EXE = r"E:\github\lore\target\release\lore.exe"


def make_workspace() -> tuple[Path, Path, dict]:
    work = Path(tempfile.mkdtemp(prefix="lore_ex3_"))
    global_dir = work / "global"
    global_dir.mkdir()
    repo = work / "repo"
    repo.mkdir()
    env = os.environ.copy()
    env["LORE_GLOBAL_PATH"] = str(global_dir)
    env["LORE_AUTH_PATH"] = str(global_dir)
    return work, repo, env


def create_repo(repo: Path, env: dict) -> str:
    """(rozwiązanie cw. 2) Tworzy repozytorium offline, zwraca stdout."""
    result = subprocess.run(
        [LORE_EXE, "--repository", str(repo), "repository", "create",
         "--offline", "LearningRepo"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, f"create: {result.stdout}{result.stderr}"
    return result.stdout


def run_lore(repo: Path, env: dict, *args: str, cwd=None) -> "subprocess.CompletedProcess":
    """Twoj mini-harness: uruchamia lore.exe z --repository i zwraca CompletedProcess.

    TODO 1: zbuduj argv jako liste:
            [LORE_EXE, "--repository", str(repo), "--offline"] + list(args)
            i uruchom subprocess.run z capture_output=True, text=True,
            env=env, cwd=cwd. (Nie sprawdzaj tu returncode — zostaw to testowi.)
    """
    raise NotImplementedError("TODO 1")


def main() -> None:
    work, repo, env = make_workspace()
    print(create_repo(repo, env).strip())

    # TODO 2: stwórz pliki w repo (Path.write_text):
    #   repo / "hello.txt"  <- "hello lore"
    #   repo / "sub" / "note.txt"  <- "note"   (zapomnij o mkdir!)

    # TODO 3: stage WIELE scieżek jednym wywołaniem:
    #   run_lore(repo, env, "stage", "hello.txt", "sub", cwd=repo)
    #   assert "Staging" w stdout

    # TODO 4 (PUŁAPKA cwd): uruchom status DWA razy i porównaj sciezki:
    #   a) run_lore(repo, env, "status", cwd=work)   <- katalog nadrzędny repo
    #   b) run_lore(repo, env, "status", cwd=repo)   <- root repo
    #   Wypisz oba. Sciezki w output sa wzgledne... czegom?
    #   (To wlasnie dlatego harness zawsze uruchamia komendy z cwd=root repo.)

    # TODO 5: commit:
    #   run_lore(repo, env, "commit", "first commit", cwd=repo)
    #   assert "Commit succeeded" w stdout

    # TODO 6: historia:
    #   run_lore(repo, env, "revision", "history", "--oneline", cwd=repo)
    #   assert "first commit" w stdout

    # ZADANIE (opcjonalne): status po commit — co sie zmienilo?


if __name__ == "__main__":
    main()
