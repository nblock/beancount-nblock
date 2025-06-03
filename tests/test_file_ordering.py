from pathlib import Path

from beancount.loader import load_file

import beancount_nblock.file_ordering as plugin

FIXTURES = Path("tests/fixtures/file_ordering")


class TestFileOrdering:
    def test_ok(self):
        orig_entries, orig_errors, _ = load_file(FIXTURES / "ok.beancount")
        assert orig_errors == []

        entries, errors = plugin.validate_file_ordering(orig_entries, {})
        assert entries == orig_entries
        assert errors == []

    def test_wrong_order(self):
        orig_entries, orig_errors, _ = load_file(FIXTURES / "order.beancount")
        assert orig_errors == []

        entries, errors = plugin.validate_file_ordering(orig_entries, {})
        assert len(errors) == 1
        assert errors[0].message == (
            "Date 2019-01-01 occurs after 2019-01-02, violating in-file date ordering"
        )
