var map;
var layersLeft = {};
var layersRight = {};
var years = [2011, 2012, 2013, 2015, 2017];
var layerL, layerR;
var swipe;

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

  years.forEach (function(year) {
    mapServer = "https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_" + year + "/MapServer";
    layersLeft[year] = new ArcGISTiledMapServiceLayer(mapServer);
    layersRight[year] = new ArcGISTiledMapServiceLayer(mapServer);
  });

  layerL = layersLeft[2011];
  layerR = layersRight[2017];
  map.addLayers([layerR, layerL]);
  map.on("load", function(theMap) {
    swipe = new LayerSwipe(
      {
        type: "vertical",
        map: map,
        layers: [layerL]
      },
      "swipeDiv"
    );
    swipe.startup();
  });

});