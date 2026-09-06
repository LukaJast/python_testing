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

## Mały tutorial: debugowanie w PDB

`pdb` to debugger wbudowany w Pythona. Pozwala zatrzymać wykonywanie programu i sprawdzić jego stan krok po kroku.

### 1. `breakpoint()`

Najprostszy sposób zatrzymania programu to wstawienie `breakpoint()` w interesującym miejscu:

```python
for number, line in enumerate(file, start=1):
    breakpoint()
    if "WARNING" in line:
        return number
```

Następnie uruchamiamy test:

```fish
python -m pytest -k find_warning
```

Wykonanie zatrzyma się i pojawi się prompt:

```text
(Pdb)
```

### 2. Najważniejsze polecenia PDB

| Polecenie | Skrót | Znaczenie |
|---|---|---|
| `next` | `n` | wykonaj bieżącą linię i przejdź dalej |
| `step` | `s` | wejdź do wywoływanej funkcji |
| `return` | `r` | wykonuj do powrotu z bieżącej funkcji |
| `continue` | `c` | kontynuuj do następnego breakpointa |
| `print expr` | `p expr` | pokaż wartość wyrażenia |
| `where` | `w` | pokaż stos wywołań (call stack) |
| `up` | `u` | przejdź poziom wyżej na stosie |
| `down` | `d` | przejdź poziom niżej |
| `quit` | `q` | zakończ debugowanie |

Przykład:

```text
(Pdb) n
(Pdb) p number
2
(Pdb) p repr(line)
'WARNING\\n'
```

`p` nie oznacza „pokaż wynik ostatniej operacji”. To skrót od `print` i służy do ewaluowania wyrażenia w aktualnym kontekście.

### 3. `repr()` przy debugowaniu tekstu

Przy logach zwykły `print(line)` może ukryć znaki specjalne. `repr(line)` pokazuje reprezentację napisu, dzięki czemu widać np. końcowe `\\n`:

```text
'WARNING\\n'
```

To pozwala odróżnić:

```text
'WARNING\\n'
```

a:

```text
'WARNING'
```

Ma to znaczenie dla warunku:

```python
if line == "WARNING":
```

Pierwszy napis nie jest równy `"WARNING"`, drugi jest.

### 4. `n` kontra `s`

- `n` (`next`) przechodzi do następnej linii bez wchodzenia do wywoływanej funkcji.
- `s` (`step`) wchodzi do funkcji wywoływanej przez bieżącą linię.

Dlatego `s` użyte np. przy:

```python
with open(log_file, "r") as file:
```

może wejść do wewnętrznego kodu biblioteki Pythona. Jeśli przypadkowo wejdziesz zbyt głęboko, `r` pozwala wykonać bieżącą funkcję do jej powrotu.

### 5. `--pdb` w pytest

Można też uruchomić:

```fish
python -m pytest --pdb
```

Wtedy pytest uruchomi PDB po wystąpieniu błędu.

Przydatne połączenie:

```fish
python -m pytest -k warning -x --pdb
```

- `-k warning` — uruchom testy pasujące do wyrażenia `warning`
- `-x` — zatrzymaj pytest po pierwszym nieudanym teście
- `--pdb` — po błędzie uruchom PDB

### 6. `breakpoint()` a `--pdb`

`breakpoint()` zatrzymuje program **podczas wykonywania**, więc można prześledzić kod od wybranego miejsca za pomocą `n`, `s` itd.

`--pdb` zatrzymuje się **po błędzie testu**. Jest więc szczególnie przydatne do sprawdzenia stanu programu w momencie awarii.

`--pdb` nie pozwala cofnąć wykonania do wcześniejszej iteracji.

### 7. Brak reverse-step

Standardowy PDB nie ma mechanizmu cofania wykonania. Jeżeli kod wykonał już `return`, nie można poleceniem PDB wrócić do wcześniejszej instrukcji.

Jeżeli chcemy prześledzić wykonanie od początku, wstawiamy `breakpoint()` przed interesującym fragmentem i uruchamiamy test ponownie.

### 8. Praktyczny schemat debugowania

```text
1. Uruchom konkretny test:
   python -m pytest -k nazwa_testu

2. Wstaw breakpoint() w podejrzanym miejscu.

3. Uruchom test ponownie.

4. Używaj:
   n              → następna linia
   p zmienna      → wartość zmiennej
   p repr(line)   → dokładna reprezentacja tekstu
   w              → call stack
   c              → dalej

5. Usuń breakpoint().

6. Uruchom cały zestaw:
   python -m pytest
```

W naszym przypadku `p repr(line)` pokazało przyczynę wyniku `7`: pierwsze linie `WARNING` miały końcowe `\\n`, natomiast ostatnia linia pliku była `'WARNING'` bez końcowego znaku nowej linii. Dlatego `if line == "WARNING"` dopasował tylko linię 7.

### 9. Nasz konkretny przykład: `find_warning()`

Poniższy przykład pokazuje dokładnie sytuację, którą debugowaliśmy.

#### Dane wejściowe: `log.log`

```text
1 ERROR
2 WARNING
3 ERROR
4 Nastepna linia bez bledu/n i kolejna linia bez bledu
5 FATAL
6 WARNING
7 WARNING
```

Istotny szczegół: ostatnia linia pliku nie ma końcowego `\\n`.

#### Błędna definicja w `log_parser.py`

```python
def find_warning(log_file):
    """Find line number with first WARNING"""
    with open(log_file, "r") as file:
        for number, line in enumerate(file, start=1):
            if line == "WARNING":
                print(number)
                return number
```

Intencją funkcji było znalezienie **pierwszego** `WARNING`, czyli dla naszego pliku wynik powinien wynosić `2`.

Uruchomienie testu:

```fish
python -m pytest -k find_warning
```

dało:

```text
FAILED test_log_parser.py::test_find_warning[log.log-2]
AssertionError: assert 7 == 2
```

#### Debugowanie przez `breakpoint()`

Dodaliśmy breakpoint:

```python
def find_warning(log_file):
    """Find line number with first WARNING"""
    with open(log_file, "r") as file:
        for number, line in enumerate(file, start=1):
            breakpoint()
            if line == "WARNING":
                print(number)
                return number
```

Następnie:

```fish
python -m pytest -k find_warning
```

Debugger pozwolił nam obserwować kolejne iteracje:

```text
(Pdb) p number
1
(Pdb) p repr(line)
"'ERROR\\n'"
```

następnie:

```text
(Pdb) p number
2
(Pdb) p repr(line)
"'WARNING\\n'"
```

Dla linii 2 warunek:

```python
line == "WARNING"
```

jest więc fałszywy, ponieważ faktyczna wartość to:

```python
"WARNING\\n"
```

Debugger prowadził dalej przez kolejne linie. Na końcu otrzymaliśmy:

```text
(Pdb) p number
7
(Pdb) p repr(line)
"'WARNING'"
```

Tym razem:

```python
line == "WARNING"
```

jest prawdziwe, ponieważ ostatnia linia nie zawiera `\\n`.

Funkcja zwróciła więc `7` zamiast `2`.

#### Co dokładnie wykryliśmy

Problem nie znajdował się w `enumerate()` ani w numerowaniu linii. Problemem było założenie zapisane w warunku:

```python
if line == "WARNING":
```

Przy odczycie pliku większość linii miała postać:

```text
'WARNING\\n'
```

a ostatnia:

```text
'WARNING'
```

`repr(line)` pozwolił nam zobaczyć znak `\\n`, którego zwykły `print(line)` nie pokazywał w oczywisty sposób.

Dla funkcji, która ma wykrywać wystąpienie `WARNING` w linii, poprawiliśmy warunek na:

```python
if "WARNING" in line:
```

Po poprawce:

```fish
python -m pytest -k warning
```

dało:

```text
6 passed
```

a cały zestaw:

```fish
python -m pytest
```

dał:

```text
12 passed
```

Ten przykład dobrze pokazuje podstawowy schemat debugowania:

```text
test → nieoczekiwany wynik
          ↓
     breakpoint()
          ↓
      n / s / r
          ↓
     p number
     p repr(line)
          ↓
  obserwacja rzeczywistego stanu
          ↓
  znalezienie przyczyny
```

#### 10. Ręczne wywołanie funkcji poza pytest

Możemy też sprawdzić funkcję bez frameworka testowego, tworząc mały plik `debug_test.py`:

```python
from log_parser import find_warning

result = find_warning("log.log")
print("result:", result)
```

Uruchamiamy go:

```fish
python debug_test.py
```

Jeżeli w `find_warning()` nadal znajduje się `breakpoint()`, program zatrzyma się w PDB.

Możemy wtedy np. sprawdzić:

```text
(Pdb) p log_file
'log.log'
```

a następnie:

```text
(Pdb) r
```

`r` wykonuje funkcję do jej `return`. W naszym przypadku otrzymaliśmy:

```text
'ERROR\n'
'WARNING\n'
'ERROR\n'
'Nastepna linia bez bledu/n i kolejna linia bez bledu\n'
'FATAL\n'
'WARNING\n'
'WARNING'
7
--Return-- ... ->7
```

Po powrocie do `debug_test.py`:

```text
result : 7
```

To pokazuje dwie różne rzeczy:

- `7` wypisane wcześniej pochodziło z `print(number)` znajdującego się **wewnątrz `find_warning()`**,
- `result : 7` pokazuje wartość, którą funkcja **zwróciła** i którą zapisaliśmy do zmiennej `result`.

Możemy następnie zmienić tylko argument:

```python
result = find_warning("clean.log")
```

i ponownie uruchomić:

```fish
python debug_test.py
```

Wynik:

```text
result: None
```

Dzieje się tak dlatego, że `find_warning()` nie znajduje `WARNING` w `clean.log`, więc nie wykonuje żadnego jawnego `return`. Funkcja dochodzi do końca, a Python zwraca wtedy `None`.

Ręczne wywołanie jest więc prostym sposobem sprawdzenia **rzeczywistego zachowania funkcji bez pytesta**. Dopiero pytest nakłada na to oczekiwanie zapisane w `assert`.

Dla `clean.log`:

```python
assert find_warning("clean.log") == None
```

jest równoważne:

```python
assert None == None
```

Dla `log.log` mieliśmy natomiast:

```text
find_warning("log.log") → 7
oczekiwany wynik        → 2
```

czyli test wykrywał:

```python
assert 7 == 2
```
