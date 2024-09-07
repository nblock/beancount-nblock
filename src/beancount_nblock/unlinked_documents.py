import collections
import fnmatch

from beancount.core import data

from beancount_nblock.common import Error

__plugins__ = ("unlinked_documents",)


# Default list of patterns a link should start with to be considered.
DEFAULT_PATTERNS = ["AR-*", "ER-*"]


def parse_patterns(config_str):
    return [x.strip() for x in config_str.split(",")]


def generate_error(link, values, description):
    try:
        single = values[0]
        return Error(single.meta, f"Missing {description} for link {link!r}", single)
    except IndexError:
        pass


def check_for_errors(cached):
    errors = []

    for key, values in cached.items():
        has_transaction = any(filter(lambda v: isinstance(v, data.Transaction), values))
        if not has_transaction:
            errors.append(generate_error(key, values, "transaction"))

        has_document = any(filter(lambda v: isinstance(v, data.Document), values))
        if not has_document:
            errors.append(generate_error(key, values, "document"))

    return errors


def unlinked_documents(entries, options_map, config_str=None):
    cache = collections.defaultdict(list)

    patterns = DEFAULT_PATTERNS
    if config_str is not None:
        patterns = parse_patterns(config_str)

    for entry in entries:
        if not isinstance(entry, data.Document | data.Transaction):
            continue

        for link in entry.links:
            for pattern in patterns:
                if fnmatch.fnmatch(link, pattern):
                    cache[link].append(entry)

    return (entries, check_for_errors(cache))
