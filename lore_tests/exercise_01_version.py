"""Cwiczenie 1 — pierwsze uruchomienie lore.exe przez subprocess.run()

Co tu sie uczysz:
- argv jako LISTA (nie jeden string — unikamy shella i cudzyslow),
- capture_output=True / text=True,
- roznic miedzy result.returncode, result.stdout i result.stderr.

Uruchomienie:
    python exercise_01_version.py
"""

import subprocess

LORE_EXE = r"E:\github\lore\target\release\lore.exe"


def main() -> None:
    result = subprocess.run(
        [LORE_EXE, "--version"],
        capture_output=True,  # przechwycenie stdout i stderr do pól result
        text=True,            # stringi zamiast bajtów
    )

    print("returncode:", result.returncode)
    print("stdout:    ", result.stdout.strip())
    print("stderr:    ", result.stderr.strip())

    # assert = mini-test w skrypcie: zatrzymuje program z wyjatkiem,
    # gdy zalozenie sie nie spelnia
    assert result.returncode == 0, "lore.exe --version konczy sie 0"
    assert "lore" in result.stdout.lower(), "stdout powinien zawierac wersje"

    # ZADANIA (opcjonalne, do eksploracji):
    # 1. Usun capture_output=True — gdzie wtedy trafia wynik?
    # 2. Zmień "--version" na "--version2" — jaki returncode? Gdzie błąd?
    # 3. Dodaj "--repository" do argumentów — co sie dzieje?


if __name__ == "__main__":
    main()
