# Ćwiczenia: testy Lore w Pythonie — etap 1 (raw subprocess)

## Cel

Nauka pisania testów dla Lore **bez żadnych helperów** — same `subprocess.run()`
i surowe argumenty CLI (`lore.exe repository create --offline ...`).

Plan nauki ma dwa etapy:

| Etap | Co robimy | Gdzie |
| --- | --- | --- |
| **1 (tutaj)** | Raw `subprocess` + surowy CLI, offline, bez serwera | `lore_tests/` |
| 2 (później) | Publiczny harness (`E:\github\lore\scripts\test/`), porównanie obu podejść | osobna sesja |

## Zasady etapu 1

- **Zakaz importów z harnessu**: niczego z `E:\github\lore\scripts\test/`
  (klasa `Lore`, fixture'y z `conftest.py`, `error_types.py`, `lore_parsers.py`).
  Dozwolone: standard library Python + `pytest`.
- **Zawsze `--offline`** — żaden serwer, żadne logowanie, tylko lokalny store.
- **Izolacja środowiska**: każda sesja dostaje własne `LORE_GLOBAL_PATH` i
  `LORE_AUTH_PATH` (katalog tymczasowy). Dzięki temu Twoja prawdziwa
  konfiguracja/credentialle nie wpływają na testy, a testy nie zaśmiecają
  Twojej konfiguracji.
- **Katalogi tymczasowe** (`tempfile.mkdtemp` / `tmp_path` w pytest) —
  test nie zostawia śladu i można go uruchamiać dowolną liczbę razy.

## Środowisko

- Binarki: `E:\github\lore\target\release\lore.exe` (i `loreserver.exe` —
  w etapie 1 niepotrzebne).
- Python: Windows Python 3.14 z zainstalowanym `pytest` (sprawdzone),
  ewentualnie WSL-owy `.venv` z tego projektu (Python 3.12 + pytest).
  Pliki ćwiczeń są przenośne — jedyne, co może się zmienić, to ścieżka
  `LORE_EXE` na górze pliku. (W WSL binarka Linuxowa nie jest zbudowana;
  `.exe` da się uruchomić przez interop, ale trzymajmy się na razie
  natywnego Windowsa, żeby nie mieszać systemów ścieżek.)

Uruchamianie:

```powershell
cd E:\python_testing\lore_tests
python exercise_01_version.py
python exercise_02_repo_create.py
# ...
pytest test_lore_cli.py -v
```

W WSL (fish):

```fish
cd /mnt/e/python_testing/lore_tests
source /mnt/e/python_testing/.venv/bin/activate.fish
python exercise_01_version.py
```

(...i wtedy zmień `LORE_EXE` na `/mnt/e/github/lore/target/release/lore.exe`.)

## Sekwencja ćwiczeń

| Plik | Temat | Czego się uczysz |
| --- | --- | --- |
| `exercise_01_version.py` | `lore.exe --version` | argv jako lista, `capture_output`, `text`, `returncode`, stdout vs stderr |
| `exercise_02_repo_create.py` | `repository create --offline` | izolacja env (`LORE_GLOBAL_PATH`, `LORE_AUTH_PATH`), `--repository`, weryfikacja na dysku (`.lore/`) |
| `exercise_03_lifecycle.py` | `stage` → `status` → `commit` → `history` | własny helper `run_lore`, wiele ścieżek w jednym wywołaniu, **pułapka cwd** |
| `exercise_04_branches.py` | `branch create` / `switch --local` / `list` | flagi zależne od kontekstu (`--local`), marker bieżącej gałęzi |
| `exercise_05_errors.py` | błędy i kody wyjścia | rc != 0, `stderr`, własny wyjątek `LoreCommandError` (miniatura `error_types.py`) |
| `exercise_06_json.py` | `--json` (NDJSON) | parsowanie JSON line-by-line, zdarzenie `complete`, `branchListEntry` |
| `test_lore_cli.py` | całość jako testy pytest | fixture `tmp_path`, zamiana skryptów na testy |

Kolejność jest ważna — każde ćwiczenie buduje na poprzednim (rozwiązania
poprzednich ćwiczeń są wklejone jako gotowe helpery).

## Karta ściągawcza (sprawdzone na binarce 0.9.1-nightly)

### Kody wyjścia

| rc | znaczenie | przykład |
| --- | --- | --- |
| 0 | sukces | `repository create`, `commit` |
| 2 | błąd użycia CLI (clap) — zawsze w `stderr` | nieznana podkomenda |
| 40 | `Commit failed` (stdout) + `[Error] Nothing staged for commit` (stderr) | commit bez staged |
| 89 | `[Error] Repository not found: ...` (stderr) | komenda w katalogu nie-repo |
| 255 | `[Error] Invalid path ...` (stderr) | `stage` pliku, który nie istnieje, **gdy cwd jest wewnątrz repo** |

Uwaga: rc=0 nie zawsze znaczy, że wszystko poszło po Twojej myśli —
np. `stage` brakującego pliku z cwd **poza** repo zwraca 0 z napisem
"Ignoring invalid path ... No changes staged". Dlatego testy sprawdzają
**obracaj**: returncode I zawartość outputu.

### Formaty outputu

- Tekstowe komendy: ludzie czytelne; ścieżki w `status` są **względne
  względem cwd**, nie względem `--repository` (stąd pułapka z ćwiczenia 3).
- `branch list`: bieżąca gałąź ma marker `*` przed nazwą.
- `--json`: NDJSON — po jednym obiekcie JSON na linię, na końcu zawsze
  zdarzenie `{"tagName": "complete", "data": {"status": N, "error": {...}}}`.
  Całość trafia do `stdout`.
- `revision history --oneline`: `<numer> <wiadomość>` na linię.

### Pułapki, które już tu wpadliśmy (i Ty też możesz)

1. **cwd vs `--repository`**: `stage`/`status` interpretują względne
   ścieżki względem katalogu, z którego wywołano proces. Harness
   (`Lore.run`) dlatego zawsze uruchamia komendy z `cwd` = root repozytorium.
   W ćwiczeniu 3 porównasz oba warianty na własne oczy.
2. **`revision info --json`**: proces kończy się rc=0, ale ostatnie
   zdarzenie `complete` ma `status: 111` ("No remote configured") —
   zdarzenie poziomu RPC ≠ exit code procesu. W testach wiarygodny
   jest returncode, a JSON traktujemy jako dane, nie jako status.
3. **`branch switch` offline**: tryb offline implikuje `--local`;
   flaga jest więc opcjonalna, ale jawnie ją piszemy (czytelność testu).

## Etap 2 (gdy opanujesz etap 1)

Porównamy nasze ręczne rozwiązania z publicznym harnessem
(`E:\github\lore\scripts/test/`). Wstępna mapa (do uzupełnienia wspólnie):

| Czymu my (etap 1) | Co robi harness |
| --- | --- |
| `run_lore(...)` z ćwiczenia 3 | `Lore.run(...)` — ten sam pomysł + retry przy `ServerConnectionError` |
| `LoreCommandError` z ćwiczenia 5 | `error_types.py` — mapa output → nazwane wyjątki |
| ręczne `json.loads` w ćwiczeniu 6 | `lore_parsers.py` — typowane parse'y |
| `tmp_path` + `LORE_GLOBAL_PATH` | fixture'y `global_dir_name` / `new_lore_repo` |
| `--offline`, bez serwera | autouse `loreserver` na sesję, porty bez kolizji, xdist |
