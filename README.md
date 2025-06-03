# beancount-nblock
A collection of beancount plugins.

## unlinked_documents: find missing links between documents and transactions
It might be desireable to enforce a link between certain kind of documents and
a corresponding transaction. Typical use cases are incoming and outgoing
invoices where a receipt (referenced via a document directive) should have a
matching transaction.

The following is valid, according to this plugin:

```
2019-01-01 * "Payee" "A description" ^ER-some-id
  Assets:Bank:Checking     300.00 EUR
  Expenses:Home

2019-01-01 document Assets:Bank:Checking "/path/to/receipt.pdf" ^ER-some-id
```

An error is generated in case either of the above directives is missing.

### Usage
Add the following to your beancount file:
```
plugin "beancount_nblock.unlinked_documents"
```

The default list of patterns is: `AR-*`, `ER-*`. A custom list of patterns may
be configured via:
```
plugin "beancount_nblock.unlinked_documents" "PATTERN-FOO-*,PATTERN-BAR-*
```

## repel: avoid specific combinations of tags and accounts in a single transaction
Check for combinations of tag and account names and raise an error in case they
occur together in a transaction.

Consider the tag/account pair `(FOO, Assets:Checking)` where `FOO` is a tag and
`Assets:Checking` is an account name. The following transaction is flagged by
the plugin:

```
2019-01-01 * "Payee" "A description" #FOO
  Assets:Checking     300.00 EUR
  Expenses:Home
```

### Usage
Add the following to your beancount file:
```
plugin "beancount_nblock.repel" "PLUGIN CONFIGURATION"
```

where `PLUGIN CONFIGURATION` is a list of tag/account tuples such as `"[('FOO',
'Assets:Checking')]"`. The tag `FOO` should not occur in the same transaction as
the account `Assets:Checking`.

## file_ordering: enforces strict date ordering within individual Beancount files
This Beancount plugin validates that each Beancount file that contains 2 or more
transactions is strictly chronologically ordered. I.e., no transaction that
occurs later in a given file (in file order) has a date that occurs earlier (in
calendar order) than a previous transaction in the same file.

While Beancount by default doesn't care about file ordering of directives,
ensuring in-file date ordering on transaction is a useful check to avoid certain
kinds of booking errors, e.g., copy-pasting an old transaction, forgetting to
bump its date.

This plugin was developed by Stefano Zacchiroli and released under GNU General
Public License (GPL), version 2 or above. It was incorporated into this
repository from <https://github.com/zacchiro/beancount-plugins-zack> at commit
a86a50bbd7fcc6e202db35dce3ca3af0a504493c to simplify distribution and
installation via pip.

### Usage
Add the following to your beancount file:
```
plugin "beancount_nblock.file_ordering"
```
