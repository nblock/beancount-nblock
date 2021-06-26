from pathlib import Path

import pytest
from beancount.loader import load_file

from beancount_nblock.repel import repel

from tests.utils import build_error

FIXTURES = Path("tests/fixtures/repel")


class TestRepel:
    @pytest.mark.parametrize(
        "config_str, msg",
        [
            (None, "This plugin requires configuration"),
            ("", "This plugin requires configuration"),
            ("[", "Syntax error in config: ["),
        ],
    )
    def test_raises_on_config_error(self, config_str, msg):
        entries, errors = repel([], {}, config_str)
        assert [build_error(message=msg)] == errors

    @pytest.mark.parametrize(
        "config", [[("FOO", "Assets:Other")], [("BAR", "Assets:Checking")]]
    )
    def test_no_matches(self, config):
        orig_entries, orig_errors, _ = load_file(FIXTURES / "single.beancount")
        assert orig_errors == []

        entries, errors = repel(orig_entries, {}, str(config))
        assert entries == orig_entries
        assert errors == []

    def test_match(self):
        orig_entries, orig_errors, _ = load_file(FIXTURES / "single.beancount")
        assert orig_errors == []

        config = [("FOO", "Assets:Checking")]
        entries, errors = repel(orig_entries, {}, str(config))
        assert len(errors) == 1
        assert errors[0].message == (
            "The tag 'FOO' and the account 'Assets:Checking' "
            "should not occur in the same transaction."
        )
