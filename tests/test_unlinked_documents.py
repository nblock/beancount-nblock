from pathlib import Path

import pytest
from beancount.loader import load_file

import beancount_nblock.unlinked_documents as plugin

FIXTURES = Path("tests/fixtures/unlinked_documents")


class TestUnlinkedDocuments:
    def test_default_config(self):
        assert plugin.DEFAULT_PATTERNS == ["AR-*", "ER-*"]

    @pytest.mark.parametrize(
        "patterns, expected",
        [
            ("FOO-*", ["FOO-*"]),
            (" FOO-*", ["FOO-*"]),
            ("FOO-* ", ["FOO-*"]),
            ("FOO-*, BAR-*", ["FOO-*", "BAR-*"]),
        ],
    )
    def test_parse_patterns(self, patterns, expected):
        assert plugin.parse_patterns(patterns) == expected

    def test_ok(self):
        orig_entries, orig_errors, _ = load_file(FIXTURES / "ok.beancount")
        assert orig_errors == []

        entries, errors = plugin.unlinked_documents(orig_entries, {}, None)
        assert entries == orig_entries
        assert errors == []

    @pytest.mark.parametrize("name", ["transaction", "document"])
    def test_raises(self, name):
        orig_entries, orig_errors, _ = load_file(FIXTURES / f"{name}.beancount")
        assert orig_errors == []

        entries, errors = plugin.unlinked_documents(orig_entries, {}, "ER-*")
        assert entries == orig_entries
        assert len(errors) == 1
        assert errors[0].message == f"Missing {name} for link 'ER-some-id'"
