# -*- coding: utf-8 -*-
import fdgis
from os import listdir
from os import rmdir
from os.path import dirname
from os.path import join
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from PyQt4.QtGui import QPushButton
from qgis.core import QgsMapLayerRegistry
from qgis.core import QgsVectorLayer
from tempfile import mkdtemp
from tempfile import NamedTemporaryFile


class FirstDraftGISDialog(QDialog):

    sources = []

    def __init__(self, parent=None):
        try:
            super(FirstDraftGISDialog, self).__init__(parent)
            relative_path = 'ui_files/' + self.name_of_ui + '.ui'
            absolute_path = join(dirname(__file__), relative_path)
            self.ui = uic.loadUi(absolute_path)

            # execute if click OK button
            self.okButton = self.ui.buttonBox.button(QDialogButtonBox.Ok)
            self.okButton.clicked.connect(self.execute)

        except Exception as e:
            print "[FirstDraftGISDialog.__init__ exception]: ", e

    def execute(self):
        try:
            print "starting start"
            self.collect_sources()
            zipped_shapefile = fdgis.make_map(
                self.sources,
                debug=False,
                map_format="shapefile",
                timeout=15)
            path_to_temp_dir = mkdtemp()
            print "path_to_temp_dir:", path_to_temp_dir
            zipped_shapefile.extractall(path_to_temp_dir)
            layers = []
            for filename in listdir(path_to_temp_dir):
                if filename.endswith(".shp"):
                    filepath = join(path_to_temp_dir, filename)
                    layer = QgsVectorLayer(filepath, filename, "ogr")
                    layers.append(layer)
            QgsMapLayerRegistry.instance().addMapLayers(layers)


        except Exception as e:
            print e

        # clear so don't reuse sources for the next request
        self.sources = []

    def open(self):
        self.ui.show()
        # don't use self.ui.exec_() method because
        # testing is clearer with clicking
        # it's more clear to use clicked.connect(self.execute)


class FileDialog(FirstDraftGISDialog):

    name_of_ui = "file"

    def collect_sources(self):
        print "[FileDialog] starting collect_sources"
        # self.sources.append(self.text.text())


class LinkDialog(FirstDraftGISDialog):

    name_of_ui = "link"

    def collect_sources(self):
        try:
            print "[LinkDialog] starting collect_sources"
            text = self.ui.link.text
            # there's a really weird thing going on here
            # when I run 'make test', text is a string
            # when I use this extension in QGIS normally, text is a method
            if str(type(text)) in ["<type 'builtin_function_or_method'>"]:
                text = text()
            self.sources.append(text)
            print "[LinkDialog] finished collect_sources"
        except Exception as e:
            print "[LinkDialog.error] " + str(e)
            print "self.ui.link.text: ", self.ui.link.text()
            raise e


class TextDialog(FirstDraftGISDialog):

    name_of_ui = "text"

    def collect_sources(self):
        print "[TextDialog] starting collect_sources"
        self.sources.append(self.ui.text.toPlainText())
