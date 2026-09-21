"""Cwiczenie 5 — błędy: kody wyjścia, stderr, własny wyjatke

Cel: zrozumiec, jak lore zglosza bledy, i zbudowac wlasne
LoreCommandError + run_lore_checked — to miniatura tego, co harness
robi w error_types.py (ale tam mapa jest o wiele wieksza).

Uruchomienie:
    python exercise_05_errors.py
"""

import os
import subprocess
import tempfile
from pathlib import Path

LORE_EXE = r"E:\github\lore\target\release\lore.exe"


def make_workspace() -> tuple[Path, Path, dict]:
    work = Path(tempfile.mkdtemp(prefix="lore_ex5_"))
    global_dir = work / "global"
    global_dir.mkdir()
    repo = work / "repo"
    repo.mkdir()
    env = os.environ.copy()
    env["LORE_GLOBAL_PATH"] = str(global_dir)
    env["LORE_AUTH_PATH"] = str(global_dir)
    return work, repo, global_dir, env


def setup_repo(repo: Path, env: dict) -> None:
    result = subprocess.run(
        [LORE_EXE, "--repository", str(repo), "repository", "create",
         "--offline", "LearningRepo"],
        capture_output=True, text=True, env=env,
    )
    assert result.returncode == 0, f"{result.stdout}{result.stderr}"


def main() -> None:
    work, repo, global_dir, env = make_workspace()
    setup_repo(repo, env)

    def run(*args, cwd=None):
        return subprocess.run(
            [LORE_EXE, "--repository", str(repo), "--offline", *args],
            capture_output=True, text=True, env=env, cwd=cwd,
        )

    # TODO 1: nieznana podkomenda -> rc == 2, "unrecognized subcommand"
    #         — sprawdź, czy blad jest w STDOUT, czy w STDERR?
    result = run("nonsense-command")
    print("rc:", result.returncode)
    print("stdout:", repr(result.stdout))
    print("stderr:", repr(result.stderr))

    # TODO 2: komenda w katalogu, ktory nie jest repozytorium:
    #   subprocess.run([LORE_EXE, "--repository", str(work / "notrepo"), "status"], ...)
    #   (katalog notrepo trzeba najpierw utworzyc)
    #   oczekiwane: rc == 89, "Repository not found" (w stderr)

    # TODO 3: stage brakujacego pliku Z cwd=repo:
    #   oczekiwane: rc == 255, "[Error] Invalid path" (w stderr)
    #   Potem spróbuj z cwd=work — co sie zmienia? (patrz README, puzapka 1)

    # TODO 4: commit bez staged:
    #   oczekiwane: rc == 40, "Commit failed" (w stdout!)
    #   oraz "[Error] Nothing staged for commit" (w stderr)

    # TODO 5: zbuduj wlasny wyjatke i helper:
    #
    #     class LoreCommandError(Exception):
    #         def __init__(self, returncode, argv, stdout, stderr):
    #             ...
    #
    #     def run_checked(*args, cwd=None):
    #         """Jak run(), ale rzuca LoreCommandError gdy rc != 0."""
    #
    #   i napisz funkcje expect_error(args, expected_rc, needle),
    #   ktora w testach zastapi cztery TODO powyzej:
    #   - przechwytuje LoreCommandError,
    #   - sprawdza expected_rc i ze needle wystepuje w stdout+stderr.
    #
    #   Wskazówka: to wlasnie wzorzec z error_types.py harnessu —
    #   tam jest mapa "fragment outputu -> nazwany wyjatke".


if __name__ == "__main__":
    main()
