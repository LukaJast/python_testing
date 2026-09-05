# Przygotowanie środowiska Python + pytest + GitHub Actions w WSL/Linux

## Cel

Lokalnie pracujemy w WSL/Linux, a GitHub Actions uruchamia testy na runnerze Linux. Dzięki temu lokalne środowisko jest zbliżone do CI.

## 1. Python w WSL

Do tego projektu używamy Pythona z WSL, nie Windowsowego `python.exe`:

```fish
which python3
python3 --version
```

Windowsowego Pythona nie trzeba usuwać.

## 2. Virtual environment

W katalogu projektu:

```fish
python3 -m venv .venv
```

Jeśli Ubuntu zgłosi brak `ensurepip`, doinstaluj pakiet dla używanej wersji Pythona, np.:

```fish
sudo apt install python3.12-venv
```

Po udanym `venv` zwykle nie ma żadnego komunikatu; `exit code 0` oznacza sukces.

## 3. Aktywacja

Dla fish:

```fish
source .venv/bin/activate.fish
```

Sprawdź:

```fish
python --version
which python
```

`which python` powinno wskazywać na `.../.venv/bin/python`.

## 4. pytest

Po aktywacji:

```fish
python -m pip install pytest
```

Sprawdzenie:

```fish
python -m pytest --version
```

Preferujemy `python -m pytest`, bo jednoznacznie używa aktualnego interpretera Pythona.

## 5. `.venv` w `.gitignore`

Środowisko jest lokalne i nie powinno być wersjonowane:

```text
.venv/
```

## 6. Testy lokalne

```fish
python -m pytest
```

Najpierw sprawdzamy testy lokalnie, potem commit i push.

## 7. Zależności

Zależności projektu warto zapisać np. w `requirements.txt`:

```text
pytest
```

Wtedy można instalować je jednym poleceniem:

```fish
python -m pip install -r requirements.txt
```

Ten sam plik może być używany przez GitHub Actions.

## 8. GitHub Actions

Workflow znajduje się w:

```text
.github/workflows/tests.yml
```

Przykładowy schemat:

```yaml
name: Tests

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: python -m pip install -r requirements.txt

      - name: Run tests
        run: python -m pytest
```

`ubuntu-latest` oznacza runner Linux przygotowany przez GitHub. Nie jest to nasz lokalny WSL.

## 9. Typowy cykl pracy

```text
zmiana kodu
    ↓
python -m pytest
    ↓
lokalne testy OK
    ↓
git diff
    ↓
git add
    ↓
git commit
    ↓
git push
    ↓
GitHub Actions
    ↓
checkout repo
    ↓
Python + zależności
    ↓
pytest
    ↓
GREEN / RED
```

## 10. `.venv` a GitHub Actions

GitHub Actions nie korzysta z naszego lokalnego `.venv`.

Runner ma własne, świeże środowisko. Workflow musi sam przygotować Pythona i zainstalować zależności.

Dlatego deklarowanie zależności w `requirements.txt` (lub innym standardowym mechanizmie) jest istotne.

## 11. Co jest wspólne

WSL/Linux i CI mają wspólne:

- Python
- pytest
- Linux
- Git
- sposób uruchamiania testów
- instalowanie zależności

Różne są środowiska wykonawcze: lokalny WSL oraz tymczasowy runner GitHub Actions.

## 12. Stan naszego projektu

Aktualnie:

```text
WSL/Linux
Python 3.12.3
.venv
pytest
Git
GitHub Actions
```

Następny krok: sprawdzić `.gitignore`, zainstalować pytest w `.venv`, uruchomić testy lokalnie i przeprowadzić cykl RED → GREEN.
