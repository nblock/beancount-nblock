import ast

from beancount.core import data

from beancount_nblock.common import Error

__plugins__ = ("repel",)


def parse_configuration(config_str):
    if config_str is None or not config_str.strip():
        raise ValueError(Error(None, "This plugin requires configuration", None))

    try:
        return ast.literal_eval(config_str.strip())
    except SyntaxError:
        raise ValueError(Error(None, f"Syntax error in config: {config_str}", None))


def repel(entries, options_map, config_str=None):
    errors = []

    try:
        pairs = parse_configuration(config_str)
    except ValueError as err:
        errors.append(err.args[0])
        return (entries, errors)

    for entry in entries:
        if not isinstance(entry, data.Transaction):
            continue

        for tag, account in pairs:
            if tag in entry.tags and account in [p.account for p in entry.postings]:
                errors.append(
                    Error(
                        entry.meta,
                        f"The tag {tag!r} and the account {account!r} should not "
                        + "occur in the same transaction.",
                        entry,
                    )
                )

    return (entries, errors)
