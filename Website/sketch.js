// function setup() {
//     createCanvas(windowWidth, windowHeight, WEBGL)
// }

// function draw() {
//     background(255);
//     rotate(radians(45), [1, 0, 0]);
//     box();
// }
var tagZoomExtent = false;
var map;
require([
    "esri/map", "esri/layers/ArcGISTiledMapServiceLayer", 
    "esri/layers/CSVLayer", "esri/Color", "esri/symbols/SimpleMarkerSymbol",
    "esri/renderers/SimpleRenderer", "esri/InfoTemplate",
    "dojo/domReady!"
  ], function(
    Map, ArcGISTiledMapServiceLayer, CSVLayer, Color, SimpleMarkerSymbol, SimpleRenderer, InfoTemplate,
  ) {

    var ext = new esri.geometry.Extent({ xmin: 13520000, ymin: 2871000, xmax: 13545000, ymax: 2900000, "spatialReference": { "wkid": 3857 } });
    mapL = new Map("map", {
      nav: false,
      extent: ext,
      logo: false
    });
    var wmtsLayer = new ArcGISTiledMapServiceLayer("https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2012/MapServer");
    mapL.addLayer(wmtsLayer);


    csv = new CSVLayer("../Data/output.csv");
    var orangeRed = new Color([238, 69, 0, 0.5]); // hex is #ff4500
    var marker = new SimpleMarkerSymbol("solid", 15, null, orangeRed);
    var renderer = new SimpleRenderer(marker);
    csv.setRenderer(renderer);
    // var template = new InfoTemplate("${type}", "${place}");
    // csv.setInfoTemplate(template);
    mapL.addLayer(csv);
    
    mapR = new Map("map2", {
      nav: false,
      extent: ext,
      logo: false
    });
    var wmtsLayer2 = new ArcGISTiledMapServiceLayer("https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2013/MapServer");
    mapR.addLayer(wmtsLayer2);

    
    csv2 = new CSVLayer("../Data/output.csv");
    var orangeRed = new Color([0, 69, 238, 0.25]); // hex is #ff4500
    var marker = new SimpleMarkerSymbol("solid", 15, null, orangeRed);
    var renderer = new SimpleRenderer(marker);
    csv2.setRenderer(renderer);
    mapR.addLayer(csv2);

    mapL.on("extent-change", function () {
      if (!tagZoomExtent) {
          var xmin = mapL.extent.xmin;
          var xmax = mapL.extent.xmax;
          var ymin = mapL.extent.ymin;
          var ymax = mapL.extent.ymax;
          var sr = mapL.extent.spatialReference;
          mapR.setExtent(new esri.geometry.Extent(xmin, ymin, xmax, ymax, sr));
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
          mapL.setExtent(new esri.geometry.Extent(xmin, ymin, xmax, ymax, sr));
      }
      tagZoomExtent = !tagZoomExtent;
  });

});
