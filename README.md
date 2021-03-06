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
