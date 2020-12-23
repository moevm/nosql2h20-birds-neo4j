from frontend.widgets.QGoogleMapsWidget.QGoogleMapsWidget import QGoogleMap


class QGoogleMapsMarkerViewWidget(QGoogleMap):
    labels = []

    def __init__(self, api_key, parent=None):
        super(QGoogleMapsMarkerViewWidget, self).__init__(api_key, parent)

    def showMarkers(self, markersData):
        for label in self.labels:
            self.deleteMarker(label)
        self.labels = [item[0] for item in markersData]
        for item in markersData:
            markerLabel = item[0]
            self.addMarker(markerLabel, item[1], item[2], **dict(
                icon=item[3],
                draggable=True,
                title=markerLabel
            ))
