Upgrading to Newer Releases
===========================

Importers are deeply routed in the workflow of Beancount users and
care is taken to do not break existing setups. However, backward
incompatible changes are sometimes required to improve the user
experience in writing and running importers and to improve the
framework on the base of use in the field. An upgrade path from old
version to new ones is provided and documented here. Along with the
testing infrastructure provided by Beangulp, that helps in identifying
early any regression in importer implementations, upgrading to new
versions should be straighforward.


Upgrading from ``beancount.ingest`` to Beangulp
-----------------------------------------------

``beangulp`` is the continuation of the development of
``beancount.ingest``. Importers written for ``beancount.ingest``
should be trivial to port to ``beangulp``.

``beancount.ingest`` has been split off from the ``beancount``
codebase into the ``beangulp`` project.

Beangulp 0.1 
