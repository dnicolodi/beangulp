__copyright__ = "Copyright (C) 2016  Martin Blais"
__license__ = "GNU GPLv2"

from os import path
from unittest import mock
import re
import textwrap
import unittest

from beancount.utils import test_utils
from beangulp.importer import ImporterProtocol
from beangulp import identify
from beangulp.test_utils import TestScriptsBase, TestExamplesBase


class _TestImporter(ImporterProtocol):

    def __init__(self, filename):
        self.filename = filename

    def identify(self, file):
        return file.name == self.filename


class TestScriptIdentifyFunctions(test_utils.TestTempdirMixin, unittest.TestCase):

    def test_find_imports(self):
        file1 = path.join(self.tempdir, 'file1.test')
        file2 = path.join(self.tempdir, 'file2.test')
        file3 = path.join(self.tempdir, 'file3.test')
        for filename in [file1, file2, file3]:
            open(filename, 'w')

        imp1a = _TestImporter(file1)
        imp1b = _TestImporter(file1)
        imp2 = _TestImporter(file2)

        config = [imp1a, imp1b, imp2]
        imports = list(identify.find_imports(config, self.tempdir))
        self.assertEqual([(file1, [imp1a, imp1b]),
                          (file2, [imp2]),
                          (file3, [])],
                         imports)

    @mock.patch.object(identify, 'FILE_TOO_LARGE_THRESHOLD', 128)
    def test_find_imports__file_too_large(self):
        file1 = path.join(self.tempdir, 'file1.test')
        file2 = path.join(self.tempdir, 'file2.test')
        with open(file1, 'w') as file:
            file.write('*' * 16)
        with open(file2, 'w') as file:
            file.write('*' * 256)

        imp = mock.MagicMock()
        imp.identify = mock.MagicMock(return_value=True)

        imports = list(identify.find_imports([imp], self.tempdir))
        self.assertEqual([(file1, [imp])], imports)

    def test_find_imports__raises_exception(self):
        file1 = path.join(self.tempdir, 'file1.test')
        with open(file1, 'w'):
            pass
        imp = mock.MagicMock()
        imp.identify = mock.MagicMock(side_effect=ValueError("Unexpected error!"))
        imports = list(identify.find_imports([imp], self.tempdir))
        self.assertEqual([(file1, [])], imports)


class TestScriptIdentify(TestScriptsBase):

    def test_identify(self):
        regexp = textwrap.dedent("""\
            \\*\\*\\*\\* .*/Downloads/ofxdownload.ofx
            Importer: +mybank-checking-ofx
            Account: +Assets:Checking

            \\*\\*\\*\\* .*/Downloads/Subdir/bank.csv
            Importer: +mybank-credit-csv
            Account: +Liabilities:CreditCard

            \\*\\*\\*\\* .*/Downloads/Subdir/readme.txt

            """).strip()

        with test_utils.capture('stdout', 'stderr') as (stdout, stderr):
            test_utils.run_with_args(
                self.ingest, ['-d', path.join(self.tempdir, 'Downloads'), 'identify'],
                identify.__file__)
        output = stdout.getvalue().strip()
        self.assertTrue(re.match(regexp, output))


class TestIdentifyExamples(TestExamplesBase, TestScriptsBase):

    def test_identify_examples(self):
        with test_utils.capture('stdout', 'stderr') as (stdout, stderr):
            result = test_utils.run_with_args(
                self.ingest, ['-d', path.join(self.example_dir, 'Downloads'), 'identify'],
                identify.__file__)

        self.assertEqual(0, result)
        output = stdout.getvalue()
        errors = stderr.getvalue()
        self.assertTrue(not errors or re.search('ERROR.*pdf2txt', errors))

        self.assertRegex(output, 'Downloads/UTrade20160215.csv')
        self.assertRegex(output, 'Importer:.*importers.utrade.utrade_csv.Importer')
        self.assertRegex(output, 'Account:.*Assets:US:UTrade')

        self.assertRegex(output, 'Downloads/ofxdownload.ofx')
        self.assertRegex(output,
                         'Importer:.*beangulp.importers.ofx_importer.Importer')
        self.assertRegex(output, 'Account:.*Liabilities:US:CreditCard')


if __name__ == '__main__':
    unittest.main()
