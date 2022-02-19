Deduplication
-------------

Mark duplicates in the imported entries against each other and against
entries in existing ledger.

Goals:

1. Reproducible:

2. Predictable: given a list of transactions from a set of imported
   files, it should be possible to predict which ones will be marked
   as duplicates. This requires that the

3. Fast: it should be reasonably fast.

How does it work:

- deduplication within one account
- deduplication across accounts
- entries within imports are not necessarily sorted by date

Example dataset::

  Account A: (-----)
  Account A: (=====--------)
  Account B:  (------------)
  Account B:           (===----)
  Account A:                (--------------)
  Account B:               (===------------)

1. load existing entries

2. Run the import on all input files producing an imported set::

     (filename, importer, account, entries)

   Make this a ``NamedTuple`` for easier access.

3. Sort imported set by::

     (max date, account, min date)

   We want entries form documents produced earlier in time to take
   precedence over transactions coming later in time.

   Most imports have a balance statement at the end with a date that
   is one day later than the reporting period (balance statement are
   effective at the beginning of the day). Thus using the end date
   should be more predictable than sorting on the earliest entry.

   Add :method:Ingest:sort() to perform the sorting?

   The sorting can be done like this::

     def key(x):
         dates = [entry.date for entry in x.entries]
         return max(dates), x.account, min(dates), x.filename

     imported.sort(key=key)

4. Sort the existing entries by date.

   The default deduplicationn mechanism uses a time window to restrict
   the match candidates. Sorting the existing entries allows to use
   bisection to search for the candidates without iterating the
   existing entries list. Sorting the existing entries does not affect
   the import process output.

   ::

      existing.sort(key=attrgetter('date'))

5. Run the deduplication algorithm on the first element of the
   imported set. Use the importer provided deduplication method::

     importer.deduplicate(entries, existing)

   The default implementation should look something like::

     for entry in entries:
         head = entry.date - datetime.timedelta(days=days)
         tail = entry.date + datetime.timedelta(days=days + 1)
         for target in iter_entries_dates(existing, head, tail):
             if self.cmp(entry, target):
                # Updating the metadata dictionary in place requires
                # to make sure that it is not shared among entries.
                assert sys.getrefcount(entry.meta) == 2
                entry.meta[DUPLICATE] = True
                break

   The default implementation of the comparison method should be based
   on the existing SimilarityComparator::

     class Importer:
        cmp = staticmethod(SimilarityComparator())

   Note: how to we add typing to that? Should we have a `ImporterBase`
   class with typing and an `Importer` class that derives from it with
   the implementation above?

6. Append the deduplicated entries to the existing entries list

7. Iterate from 4.

IDEA: Mark duplicated entries with filename:lineno of the matching entry
