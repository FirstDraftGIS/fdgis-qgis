# coding=utf-8
import unittest

from PyQt4.QtGui import QDialogButtonBox, QDialog

from fdgis_dialog import LinkDialog, TextDialog

from time import sleep

from utilities import get_qgis_app
QGIS_APP = get_qgis_app()


class FirstDraftGISDialogTest():

    dialog = None

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_dialog_cancel(self):
        print "dialog", self.dialog
        buttonBox = self.dialog.ui.buttonBox
        cancelButton = buttonBox.button(QDialogButtonBox.Cancel)
        button = cancelButton.click()
        result = self.dialog.ui.result()
        self.assertEqual(result, QDialog.Rejected)


class TestAddViaLink(unittest.TestCase, FirstDraftGISDialogTest):

    def setUp(self):
        self.dialog = LinkDialog(None)

    def test_dialog_ok(self):
        """Test we can click OK."""
        folder = "https://raw.githubusercontent.com/FirstDraftGIS/fdgis-qgis"
        url = folder + "/master/FirstDraftGIS/test/sources/australia.txt"
        self.dialog.ui.link.text = url
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Ok).click()
        result = self.dialog.ui.result()
        self.assertEqual(result, QDialog.Accepted)


class TestAddText(unittest.TestCase, FirstDraftGISDialogTest):

    def setUp(self):
        self.dialog = TextDialog(None)

    def test_dialog_ok(self):
        """Test we can click OK."""
        self.dialog.ui.text.setPlainText("Where is Paris, Texas?")
        self.dialog.ui.buttonBox.button(QDialogButtonBox.Ok).click()
        result = self.dialog.ui.result()
        self.assertEqual(result, QDialog.Accepted)

if __name__ == "__main__":
    for _class in [TestAddViaLink, TestAddText]:
        suite = unittest.makeSuite(_class)
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
