"""Etap 1 — to samo co w cwiczeniach, ale jako testy pytest

Uruchomienie:
    pytest test_lore_cli.py -v

Zasady etapu 1 sa tu zachowane w 100%:
- tylko stdlib + pytest (zero importow z E:\\github\\lore\\scripts\\test\\),
- izolacja srodowiska przez fixture,
- --offline przez caly czas.

Pierwszy test jest rozwiazany — reszta to TODO.
"""

import os
import subprocess

import pytest

LORE_EXE = r"E:\github\lore\target\release\lore.exe"


@pytest.fixture
def lore_env(tmp_path):
    """Izolowane srodowisko + katalogi na kazdy test (tmp_path sprzata sam)."""
    global_dir = tmp_path / "global"
    global_dir.mkdir()
    repo = tmp_path / "repo"
    repo.mkdir()
    env = os.environ.copy()
    env["LORE_GLOBAL_PATH"] = str(global_dir)
    env["LORE_AUTH_PATH"] = str(global_dir)
    return repo, env


def run_lore(repo, env, *args, cwd=None, check=True):
    """Mini-harness: lore.exe z --repository i --offline.

    check=True: rzuca subprocess.CalledProcessError przy rc != 0
    (wtedy test FAILUJE — tak ma byc dla nieoczekiwanych bledow).
    """
    argv = [LORE_EXE, "--repository", str(repo), "--offline", *args]
    result = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=cwd)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, argv, output=result.stdout, stderr=result.stderr
        )
    return result


def test_version():
    """(rozwiązany) Najprostszy mozliwy test CLI."""
    result = subprocess.run(
        [LORE_EXE, "--version"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "lore" in result.stdout


def test_repository_create(lore_env):
    repo, env = lore_env
    # TODO: repository create (offline), assert rc==0,
    #       "Created repository" w stdout, (repo / ".lore").is_dir()
    pytest.fail("TODO")


def test_commit_lifecycle(lore_env):
    repo, env = lore_env
    # TODO: create repo, plik hello.txt, stage, commit "first commit",
    #       "revision history --oneline" — asserty na "Commit succeeded"
    #       i na wystapienie "first commit" w historii.
    pytest.fail("TODO")


def test_stage_missing_file_fails(lore_env):
    repo, env = lore_env
    # TODO: create repo; stage brakujacego pliku z cwd=repo i check=False;
    #       assert rc == 255 i "Invalid path" w stderr.
    #       (pytest.raises(CalledProcessError) tez zadziala — wybierz styl.)
    pytest.fail("TODO")


def test_status_json(lore_env):
    repo, env = lore_env
    # TODO: create repo; status --json; parsowanie NDJSON (json.loads
    #       po liniach); ostatnie zdarzenie complete z data["status"] == 0;
    #       branchName == "main" w repositoryStatusRevision.
    pytest.fail("TODO")
