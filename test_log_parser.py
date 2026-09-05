import pytest
from log_parser import count_errors
@pytest.mark.parametrize("log_file, expected", [
    ("log.log", 2),
    ("clean.log", 0),
])

def test_count_errors(log_file, expected):
    assert count_errors(log_file) == expected

from log_parser import has_fatal
@pytest.mark.parametrize("log_file, expected", [
    ("log.log", True),
    ("clean.log", False),
])

def test_has_fatal(log_file, expected):
    assert has_fatal(log_file) == expected

from log_parser import find_errors
@pytest.mark.parametrize ("log_file, expected", [
    ("log.log", 1),
    ("clean.log", None),
])

def test_find_errors(log_file, expected):
    assert find_errors(log_file) == expected

from log_parser import has_warning
@pytest.mark.parametrize("log_file", "expected", [
    ("log.log", True),
    ("clean.log", False),
])
                        
def test_has_warning(log_file, expected):
    assert has_warning(log_file) == expected
