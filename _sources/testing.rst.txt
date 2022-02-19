Testing Importers
=================

Regression testing is key to maintaining importers code working.
Importers are often written against file formats with no official
specification and which may change without notice.  Given a typical importers setup, it is often the
case that at least some fixes need to to some of my importers every couple of
months

and thus often need to be adjusted to deal with input not observed
before or to input format changes.  Without a testing strategy it is
likely for these changes to introduce regressions which in the
best case results in errors in the importer but may result in
incomplete or incorrect imports.  Usually problems are discovered only
when you are trying to update your ledger making the timing
particularly annoying: you have other things to do.

Because the input files are poorly defined and unpredictable it is not
possible to write synthetic tests with exhaustive coverage.


The easiest and most relevant way to test the importers is to use some
real data files and compare what your importer extracts from them to
expected outputs.

For the importers to be at least somewhat reliable,
you really need to be able to reproduce the extractions on a number of
real inputs. And since the inputs are , it's not  In practice,

Beangulp has an integrated facility to implement importers tests that compare the importers output with expected output.

The testing entry point is :func:`beangulp.testing.main` a function
that wraps an importer instance in a command line interface like the
one implemented by the regular ingestion framework but with tho
additional commands dedicated to generate files recording the expected
output of the importer and to compare importer output with these.

The recommended way to integrate this facility with the importers is
to make them callable as scripts following the Python's convention:

.. code-block: python

   import beangulp

   class Importer(beangulp.Importer):
       # importer definition goes here
       pass

   if __name__ == '__main__':
       importer = Importer()
       beangulp.testing.main(Importer)

This makes 
       

, and with this process, it only sinks about a half-hour of my time: I
add the new downloaded file which causes breakage to the importer
directory, I fix the code by running it there locally as a test. And I
also run the tests over all the previously downloaded test inputs in
that directory (old and new) to ensure my importer is still working as
intended on the older files.  There is some support for automating
this process in beancount.ingest.regression. What we want is some
routine that will list the importer’s package directory, identify the
input files which are to be used for testing, and generate a suite of
unit tests which compares the output produced by importer methods to
the contents of “expected files” placed next to the test file.  For
example, given a package with an implementation of an importer and two
sample input files: /home/joe/importers/acmebank/__init__.py <- code
goes here /home/joe/importers/acmebank/sample1.csv
/home/joe/importers/acmebank/sample2.csv You can place this code in
the Python module (the __init__.py file): from beancount.ingest import
regression …  def test(): importer = Importer(...)  yield from
regression.compare_sample_files(importer) If your importer overrides
the extract() and file_date() methods, this will generate four unit
tests which get run automatically by pytest: A test which calls
extract() on sample1.csv, prints the extracted entries to a string,
and compares this string with the contents of sample1.csv.extract A
test which calls file_date() on sample1.csv and compares the date with
the one found in the sample1.csv.file_date file.  A test like (1) but
on sample2.csv A test like (2) but on sample2.csv Generating Test
Input At first, the files containing the expected outputs do not
exist. When an expected output file is absent like this, the
regression tests automatically generate those files from the extracted
output. This would result in the following list of files:
/home/joe/importers/acmebank/__init__.py <- code goes here
/home/joe/importers/acmebank/sample1.csv
/home/joe/importers/acmebank/sample1.csv.extract
/home/joe/importers/acmebank/sample1.csv.file_date
/home/joe/importers/acmebank/sample2.csv
/home/joe/importers/acmebank/sample2.csv.extract
/home/joe/importers/acmebank/sample2.csv.file_date You should inspect
the contents of the expected output files to visually assert that they
represent the contents of the downloaded files.  If you run the tests
again with those files present, the expected output files will be used
as inputs to the tests. If the contents differ in the future, the test
will fail and an error will be generated. (You can test this out now
if you want, by manually editing and inserting some unexpected data in
one of those files.)  When you edit your source code, you can always
re-run the tests to make sure it still works on those older
files. When a newly downloaded file fails, you repeat the process
above: You make a copy of it in that directory, fix the importer, run
it, check the expected files. That’s it.  Making Incremental
Improvements Sometimes I make improvements to the importers that
result in more or better output being generated even in the older
files, so that all the old tests will now fail. A good way to deal
with this is to keep all of these files under source control, locally
delete all the expected files, run the tests to regenerate new ones,
and then diff against the most recent commit to check that the changes
are as expected.
