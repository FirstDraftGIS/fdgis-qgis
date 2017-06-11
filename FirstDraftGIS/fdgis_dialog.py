# -*- coding: utf-8 -*-
#import pip
import os

import fdgis, json
from os import listdir, rmdir
from os.path import dirname, join
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QDialog, QDialogButtonBox, QPushButton
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer
from tempfile import mkdtemp, NamedTemporaryFile
#from waitingspinnerwidget import QtWaitingSpinner

#class FirstDraftGISDialog(QDialog, FORM_CLASS):
class FirstDraftGISDialog(QDialog):
    sources = []
    def __init__(self, parent=None):
        try:
            super(FirstDraftGISDialog, self).__init__(parent)
            self.ui = uic.loadUi(os.path.join(dirname(__file__), 'ui_files/' + self.name_of_ui + '.ui'))

            # execute if click OK button
            self.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.execute)

        except Exception as e:
            print "[FirstDraftGISDialog.__init__ exception]: ", e

    def execute(self):
        try:
            print "starting start"
            self.collect_sources()
            zipped_shapefile = fdgis.make_map(self.sources, debug=True, map_format="shapefile")
            path_to_temp_dir = mkdtemp()
            print "path_to_temp_dir:", path_to_temp_dir
            zipped_shapefile.extractall(path_to_temp_dir)
            layers = []
            for filename in listdir(path_to_temp_dir):
                if filename.endswith(".shp"):
                    layer = QgsVectorLayer(join(path_to_temp_dir, filename), filename, "ogr")
                    layers.append(layer)
            QgsMapLayerRegistry.instance().addMapLayers(layers)
        except Exception as e:
            print e

    def open(self):
        self.ui.show()
        # don't use self.ui.exec_() method because testing is clearer with clicking
        # it's more clear to use clicked.connect(self.execute)

class FileDialog(FirstDraftGISDialog):
    name_of_ui = "file"
    def collect_sources(self):
        print "[FileDialog] starting collect_sources"
        #self.sources.append(self.text.text())

class LinkDialog(FirstDraftGISDialog):
    name_of_ui = "link"
    def collect_sources(self):
        try:
            print "[LinkDialog] starting collect_sources"
            self.sources.append(self.ui.link.text)
            print "[LinkDialog] finished collect_sources"
        except Exception as e:
            print "[LinkDialog.error] " + str(e)
            print "self.ui.link.text: ", self.ui.link.text
            raise e

class TextDialog(FirstDraftGISDialog):
    name_of_ui = "text"
    def collect_sources(self):
        print "[TextDialog] starting collect_sources"
        self.sources.append(self.ui.text.toPlainText())
