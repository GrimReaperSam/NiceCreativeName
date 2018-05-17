var map, layer2011, layer2012, layer2013, layer2015, layer2017, layerSwipe;

require([
  "esri/map",
  "esri/layers/ArcGISTiledMapServiceLayer",
  "esri/layers/CSVLayer",
  "esri/Color",
  "esri/symbols/SimpleMarkerSymbol",
  "esri/renderers/SimpleRenderer",
  "esri/InfoTemplate",
  "esri/dijit/LayerSwipe",
  "esri/request",
  "dojo/_base/array",
  "esri/geometry/Point",
  "esri/graphic",
  "dojo/domReady!"
], function(
  Map,
  ArcGISTiledMapServiceLayer,
  CSVLayer,
  Color,
  SimpleMarkerSymbol,
  SimpleRenderer,
  InfoTemplate,
  LayerSwipe,
  esriRequest,
  array,
  Point,
  Graphic,
  GeoJsonLayer
) {
  var ext = new esri.geometry.Extent({
    xmin: 13520000,
    ymin: 2871000,
    xmax: 13545000,
    ymax: 2900000,
    spatialReference: { wkid: 3857 }
  });

  map = new Map("map", {
    nav: true,
    extent: ext,
    logo: false,
    zoom: 18
  });

  layer2017 = new ArcGISTiledMapServiceLayer(
    "https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2017/MapServer"
  );
  layer2015 = new ArcGISTiledMapServiceLayer(
    "https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2015/MapServer"
  );
  layer2013 = new ArcGISTiledMapServiceLayer(
    "https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2013/MapServer"
  );
  layer2012 = new ArcGISTiledMapServiceLayer(
    "https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2012/MapServer"
  );
  layer2011 = new ArcGISTiledMapServiceLayer(
    "https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_2011/MapServer"
  );

  map.addLayers([layer2017, layer2011]);
  //layerCurrent = layer2017;

  map.on("load", function(theMap) {
    layerSwipe = new LayerSwipe(
      {
        type: "vertical",
        map: map,
        layers: [layer2011]
      },
      "swipeDiv"
    );
    layerSwipe.startup();
  });

});

function changeLayer(tableidselections) {
  console.log("YEAR=" + tableidselections);
  map.removeAllLayers();

  if (tableidselections == 2011) {
    map.addLayers([layer2011]);
  }
  if (tableidselections == 2012) {
    map.addLayers([layer2012]);
  }
  if (tableidselections == 2013) {
    map.addLayers([layer2013]);
  }
  if (tableidselections == 2015) {
    map.addLayers([layer2015]);
  }
  if (tableidselections == 2017) {
    map.addLayers([layer2017]);
  }
}
