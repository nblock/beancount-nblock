from beancount_nblock.common import Error


def build_error(source=None, message=None, entry=None):
    return Error(source=source, message=message, entry=entry)
