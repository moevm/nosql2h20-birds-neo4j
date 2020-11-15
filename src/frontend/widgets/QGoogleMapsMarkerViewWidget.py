from src.frontend.widgets.QGoogleMapsWidget.QGoogleMapsWidget import QGoogleMap


class QGoogleMapsMarkerViewWidget(QGoogleMap):
    def __init__(self, api_key, parent=None):
        super(QGoogleMapsMarkerViewWidget, self).__init__(api_key, parent)

    def showMarkers(self, markersData):
        for item in markersData:
            markerLabel = item[0]
            self.addMarker(markerLabel, item[1], item[2], **dict(
                icon=item[3],
                draggable=True,
                title=markerLabel
            ))
