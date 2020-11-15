HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no"/>
    <style type="text/css">
        html {
            height: 100%;
        }
        body {
            height: 100%;
            margin: 0;
            padding: 0
        }
        #map_canvas {
            height: 100%
        }
    </style>
    <script type="text/javascript"> CRAZY_CODE </script>
    <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script async defer
            src="https://maps.googleapis.com/maps/api/js?key=API_KEY"
            type="text/javascript"></script>
    <script type="text/javascript" src="qgmap.js"></script>
</head>
<body onload="initialize()">
<div id="map_canvas" style="width:100%; height:100%"></div>
</body>
</html>
'''