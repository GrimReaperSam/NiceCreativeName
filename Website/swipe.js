
var tagZoomExtent = false;
var mapL, mapR, layerSwipe, lyrBottom, lyrUpper, lyrRight;
require([
    "esri/map", "esri/layers/ArcGISTiledMapServiceLayer", 
    "esri/layers/CSVLayer", "esri/Color", "esri/symbols/SimpleMarkerSymbol",
    "esri/renderers/SimpleRenderer", "esri/InfoTemplate", "esri/dijit/LayerSwipe", "esri/request", "dojo/_base/array", "esri/geometry/Point",
    "esri/graphic", "./geojsonlayer.js",
    "dojo/domReady!"
  ], function(
    Map, ArcGISTiledMapServiceLayer, 
    CSVLayer, Color, SimpleMarkerSymbol, SimpleRenderer, 
    InfoTemplate, LayerSwipe, esriRequest, array, Point, Graphic,
    GeoJsonLayer
  ) {

    var ext = new esri.geometry.Extent({ xmin: 13520000, ymin: 2871000, xmax: 13545000, ymax: 2900000, "spatialReference": { "wkid": 3857 } });
    mapL = new Map("map", {
      nav: false,
      extent: ext,
      logo: false
    });

    mapR = new Map("map2", {
      nav: false,
      extent: ext,
      logo: false
    });

    lyrBottom = new ArcGISTiledMapServiceLayer("https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2013/MapServer");
    lyrUpper = new ArcGISTiledMapServiceLayer("https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2012/MapServer");
    mapL.addLayers([lyrBottom, lyrUpper]);
    lyrRight = new ArcGISTiledMapServiceLayer("https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2013/MapServer");
    mapR.addLayer(lyrRight);

    csv = new CSVLayer("../Data/output.csv");
    var orangeRed = new Color([238, 69, 0, 0.5]); // hex is #ff4500
    var marker = new SimpleMarkerSymbol("solid", 15, null, orangeRed);
    var renderer = new SimpleRenderer(marker);
    csv.setRenderer(renderer);
    // var template = new InfoTemplate("${type}", "${place}");
    // csv.setInfoTemplate(template);
    // mapL.addLayer(csv);
    csv2 = new CSVLayer("../Data/output.csv");
    var orangeRed = new Color([0, 69, 238, 0.25]); // hex is #ff4500
    var marker = new SimpleMarkerSymbol("solid", 15, null, orangeRed);
    var renderer = new SimpleRenderer(marker);
    csv2.setRenderer(renderer);
    // mapR.addLayer(csv2);

    mapL.on("extent-change", function () {
      if (!tagZoomExtent) {
          var xmin = mapL.extent.xmin;
          var xmax = mapL.extent.xmax;
          var ymin = mapL.extent.ymin;
          var ymax = mapL.extent.ymax;
          var sr = mapL.extent.spatialReference;
          mapR.setExtent(new esri.geometry.Extent(xmin, ymin, xmin + (xmax - xmin) * 2, ymax, sr));
      }
      tagZoomExtent = !tagZoomExtent;
  });

  mapR.on("extent-change", function () {
      if (!tagZoomExtent) {
          var xmin = mapR.extent.xmin;
          var xmax = mapR.extent.xmax;
          var ymin = mapR.extent.ymin;
          var ymax = mapR.extent.ymax;
          var sr = mapR.extent.spatialReference;
          mapL.setExtent(new esri.geometry.Extent(xmin, ymin, xmin + (xmax - xmin) * 2, ymax, sr));
      }
      tagZoomExtent = !tagZoomExtent;
  });



var featureLayer = new GeoJsonLayer({
    url: "../B0694.json"
})
// mapL.addLayer(featureLayer);

mapL.on("load", function(theMap) {
    layerSwipe = new LayerSwipe({
        type: "vertical",
        left: $("#map").width() / 2,
        map: mapL,
        layers: [lyrUpper, csv]
    }, "LayerSwipe");
    layerSwipe.startup();
});

});



