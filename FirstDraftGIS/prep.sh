sudo apt-get install pyqt4-dev-tools
sudo pip install pb_tool
make

echo "copying into plugin dir"
rm ~/.qgis2/python/plugins/FirstDraftGIS -fr
cp ~/FirstDraftGIS/fdgis-qgis/FirstDraftGIS ~/.qgis2/python/plugins/ -fr
