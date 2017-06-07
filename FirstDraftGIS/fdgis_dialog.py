# -*- coding: utf-8 -*-
#import pip
import os

import api, json
from os import listdir, rmdir
from os.path import dirname, join
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QDialog, QPushButton
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer
from tempfile import mkdtemp, NamedTemporaryFile
#from waitingspinnerwidget import QtWaitingSpinner

#class FirstDraftGISDialog(QDialog, FORM_CLASS):
class FirstDraftGISDialog(QDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(FirstDraftGISDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        #self.setupUi(self)
        self.ui = uic.loadUi(os.path.join(dirname(__file__), 'ui_files/' + name_of_ui + '.ui'))

        #self.spinner = QtWaitingSpinner(self)

        #self.add_data_button = QPushButton(self.tr('Add Data'))
        #print "ops:", dir(self.add_data_button)
        #self.ui.addDataButton.clicked.connect(self.execute)

        #self.sources = []

        #pip.main(["install", "fdgis"])

        debug = True
        if debug:
            print "starting dialog init"
            #print "addData:",
            #print "self.add_data_button", self.add_data_button

    def execute(self):
        try:
            print "starting start"
            #self.ui.btn_start.clicked.connect(self.spinner_start)

            zipped_shapefile = api.make_map(self.sources, debug=True, map_format="shapefile")
            #print "geojson_map", geojson_map
            path_to_temp_dir = mkdtemp()
            print "path_to_temp_dir:", path_to_temp_dir
            zipped_shapefile.extractall(path_to_temp_dir)
            layers = []
            for filename in listdir(path_to_temp_dir):
                if filename.endswith(".shp"):
                    layer = QgsVectorLayer(join(path_to_temp_dir, filename), filename, "ogr")
                    layers.append(layer)
            QgsMapLayerRegistry.instance().addMapLayers(layers)
            #self.spinner_stop()
            #rmdir(path_to_temp_dir)
            #with open("/tmp/fdgistest.geojson", "wb") as f:
            #    f.write(json.dumps(geojson_map))
            #layer = QgsVectorLayer("/tmp/fdgistest.geojson", "fdgis_map", "ogr")
            #temp = NamedTemporaryFile()
            #temp.write(json.dumps(geojson_map))
            #layer = QgsVectorLayer(temp.name, "fdgis_map", "ogr")
            #layer = QgsVectorLayer(json.dumps(geojson_map), "fdgismap", "ogr")
            #temp.close()
        except Exception as e:
            print e

class FileDialog(FirstDraftGISDialog):
    name_of_ui = "file"
    def collect_sources(self):
        print "[FileDialog] starting collect_sources"
        #self.sources.append(self.text.text())

class LinkDialog(FirstDraftGISDialog):
    name_of_ui = "link"
    def collect_sources(self):
        print "[LinkDialog] starting collect_sources"
        self.sources.append(self.link.text())

class TextDialog(FirstDraftGISDialog):
    name_of_ui = "text"
    def collect_sources(self):
        print "[TextDialog] starting collect_sources"
        self.sources.append(self.text.text())
