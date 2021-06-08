Caching Data
============

Some of the data conversions for binary files can be costly and slow.
This is usually the case for converting PDF files to text.  This is
particularly painful, since in the process of ingesting our downloaded
data we're typically going to run the tools multiple times—at least
twice if everything works without flaw: once to extract, twice to
file—and usually many more times if there are problems.  For this
reason, we want to cache these conversions, so that a painful 40
second PDF-to-text conversion doesn't have to be run twice, for
example.

Beancount aims to provide two levels of caching for conversions on
downloaded files:

- an in-memory caching of conversions so that multiple importers
requesting the same conversion runs them only once, and

- an on-disk caching of conversions so that multiple invocations of
the tools get reused.

In-Memory Caching
-----------------

In-memory caching works like this: your methods receive a wrapper
object for a given file and invoke the wrapper's ``convert()`` method,
providing a converter callable.

.. code-block: python

   import beangulp

   def slow_pdf_to_text(filename):
       pass
   
   class MyImporter(ImporterProtocol):

       # ...

       def extract(self, file):
           text = file.convert(slow_convert_pdf_to_text)
           match = re.search(..., text)

This conversion is automatically memoized: if two importers or two
different methods use the same converter on the file, the conversion
is only run once.  This is a simple way of handling redundant
conversions in-memory.  Make sure to always call those through the
`.convert()` method and share the converter functions to take
advantage of this.

On-Disk Caching
---------------

At the moment. Beancount only implements in-memory caching. On-disk
caching will be implemented later.  Track this ticket for status
updates.
