"""Cwiczenie 2 — utworzenie repozytorium offline (repository create --offline)

Co tu sie uczysz:
- izolacja srodowiska: LORE_GLOBAL_PATH / LORE_AUTH_PATH (dlaczego — patrz README),
- globalna flaga --repository <sciezka>,
- weryfikacja po stronie Pythona: returncode, output i struktura na dysku (.lore/).

Uruchomienie:
    python exercise_02_repo_create.py
"""

import os
import subprocess
import tempfile
from pathlib import Path

LORE_EXE = r"E:\github\lore\target\release\lore.exe"


def make_workspace() -> tuple[Path, Path, Path]:
    """Swiezy obszar roboczy w katalogu tymczasowym (czysta sluzka na kazde uruchomienie)."""
    work = Path(tempfile.mkdtemp(prefix="lore_ex2_"))
    global_dir = work / "global"
    global_dir.mkdir()
    repo = work / "repo"
    repo.mkdir()
    return work, repo, global_dir


def main() -> None:
    work, repo, global_dir = make_workspace()
    print("work  :", work)
    print("repo  :", repo)
    print("global:", global_dir)

    # TODO 1: przygotuj srodowisko dla lore.exe — kopie os.environ z dodanymi
    #         LORE_GLOBAL_PATH i LORE_AUTH_PATH wskazujacymi na global_dir.
    #         Pytanie do rozmyslania: dlaczego NIE mozna tutaj zostawic
    #         Twojej prawdziwej globalnej konfiguracji?
    env = None  # np. dict z os.environ.copy() + 2 zmienne

    # TODO 2: uruchom utworzenie repozytorium:
    #         argv = [LORE_EXE, "--repository", str(repo), "repository",
    #                 "create", "--offline", "LearningRepo"]
    #         z capture_output=True, text=True, env=env
    result = None

    # TODO 3: wypisz result.stdout (i result.stderr, jezeli niepusty).

    # TODO 4: weryfikacja (assert):
    #   - result.returncode == 0
    #   - stdout zawiera "Created repository"
    #   - (repo / ".lore").is_dir()  — lore twori ukryty katalog .lore
    #   - (repo / ".lore" / "id").is_file() — 32 bajty hex, ID repozytorium

    # ZADANIE (opcjonalne): wyciagnij ID z linii
    # "Created repository LearningRepo in ... with ID <32 hex>"
    # i porownaj z zawartoscia pliku .lore/id (hex vs surowe bajty!).


if __name__ == "__main__":
    main()
