from src.frontend.widgets.QGoogleMapsWidget.QGoogleMapsWidget import QGoogleMap


class QGMapsLocatorWidget(QGoogleMap):
    markerLabel = None
    # Web mercator coords (WGS 84 proj or something):
    lat = None
    lang = None
    mass = None

    def __init__(self, api_key, parent=None):
        super(QGMapsLocatorWidget, self).__init__(api_key, parent)
        self.mapClicked.connect(self.setUpMarker)


    def setUpMarker(self, lat, lang):
        if not self.markerLabel:
            self.markerLabel = '<marker label here>'
            self.addMarker(self.markerLabel, lat, lang, **dict(
                icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
                draggable=True,
                title=self.markerLabel
            ))
        else:
            self.deleteMarker(self.markerLabel)
            self.addMarker(self.markerLabel, lat, lang, **dict(
                icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
                draggable=True,
                title=self.markerLabel
            ))

    def showMarkers(self, mass):
        for i, _ in enumerate(mass):
            markerLabel=mass[i][0]
            self.addMarker(markerLabel, mass[i][1], mass[i][2], **dict(
                icon=mass[i][3],
                draggable=True,
                title=markerLabel
            ))

    def getLocation(self):
        return self.lat, self.lang
