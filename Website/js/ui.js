var lMap, rMap;
var lYear, rYear;
var lYearLayers = {},
  rYearLayers = {};
var lRooftops, rRooftops;
//var layers = {};
//var yearLayers = {};
var years = [2011, 2012, 2013, 2015, 2017];
// var rooftop;

require([
  "esri/map",
  "esri/layers/ArcGISTiledMapServiceLayer",
  "esri/layers/CSVLayer",
  "esri/layers/FeatureLayer",
  "esri/Color",
  "esri/symbols/SimpleMarkerSymbol",
  "esri/symbols/SimpleFillSymbol",
  "esri/renderers/SimpleRenderer",
  "esri/InfoTemplate",
  "esri/request",
  "dojo/_base/array",
  "esri/geometry/Point",
  "esri/graphic",
  "js/geojsonlayer.js",
  "dojo/domReady!"
], function(
  Map,
  ArcGISTiledMapServiceLayer,
  CSVLayer,
  FeatureLayer,
  Color,
  SimpleMarkerSymbol,
  SimpleFillSymbol,
  SimpleRenderer,
  InfoTemplate,
  esriRequest,
  array,
  Point,
  Graphic,
  GeoJsonLayer
) {
  /*
    Initialize ArcGIS Maps Views
*/

  var initExt = new esri.geometry.Extent({
    xmin: 13520000,
    ymin: 2871000,
    xmax: 13545000,
    ymax: 2900000,
    spatialReference: { wkid: 3857 }
  });

  lMap = new Map("l-map", {
    // nav: true,
    extent: initExt,
    logo: false,
    zoom: 18
  });

  rMap = new Map("r-map", {
    // nav: false,
    extent: initExt,
    logo: false,
    zoom: 18
  });

  /*
    Bind right map with the left extent
*/

  var leftConnection = dojo.connect(lMap, "onExtentChange", leftChangeHandler);

  function leftChangeHandler(ext) {
    rMap.setExtent(ext);
  }

  /*
    Load historic maps
*/

  years.forEach(function(year) {
    mapServer =
      "https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_" +
      year +
      "/MapServer";
    //yearLayers[year] = new ArcGISTiledMapServiceLayer(mapServer);
    lYearLayers[year] = new ArcGISTiledMapServiceLayer(mapServer);
    rYearLayers[year] = new ArcGISTiledMapServiceLayer(mapServer);
  });

  lMap.addLayer(lYearLayers[2011]);
  rMap.addLayer(rYearLayers[2017]);

  /*
    Year selection slider
*/

  $("#year_slider").ionRangeSlider({
    type: "double",
    grid: true,
    from: 0,
    to: 4,
    step: 1,
    values: [2011, 2012, 2013, 2015, 2017],
    prettify_enabled: false,
    min_interval: 1,
    onFinish: function(data) {
      lYear = data.from_value;
      rYear = data.to_value;
      changeYear(lYear, rYear);
    }
  });

  function changeYear(from, to) {
    lMap.removeAllLayers();
    lMap.addLayer(yearLayers[from]);
    rMap.removeAllLayers();
    rMap.addLayer(yearLayers[to]);
  }

  /*
    Load rooftop csv
  */

  var dotMarker = new SimpleMarkerSymbol(
    "solid",
    10,
    null,
    new Color([0, 159, 183, 0.7])
  );
  var dotRenderer = new SimpleRenderer(dotMarker);

  lRooftops = new CSVLayer("data/Output.csv");
  lRooftops.setRenderer(dotRenderer);
  lMap.addLayer(lRooftops);
  lRooftops.hide();

  rRooftops = new CSVLayer("data/Output.csv");
  rRooftops.setRenderer(dotRenderer);
  lMap.addLayer(rRooftops);
  rRooftops.hide();

  /*
    TODO: 
    Load Final.csv using papaparse.js
    Save as {rid:{attr:val}} dictionary
  */

  /*
    Load GeoJson file
    TODO: Load all and save as {(rid:{year: layer}} dictionary
  */
// Assuming you have a list X of renewal land names:
Papa.parse("../Data/Final.csv", {
	delimiter: ",",
	header: true,
	trimHeader: true,
	download: true,
	complete: function(results, file) { 
		debugger
		// the results variable will contain the data you want! Have fun
	}
});

  var polyMarker = new SimpleFillSymbol(
    "solid",
    null,
    new Color([241, 136, 5, 0.7])
  );
  var polyRenderer = new SimpleRenderer(polyMarker);

  lMap.on("load", function() {
    X = ['中山區B0260b', '中山區B0508']
	geoJsonLayers = {}
	X.forEach(function(ri) {
	  geoJsonLayers[ri] = addGeoJsonLayer(ri)
	})
  });

  function addGeoJsonLayer(layer_name) {
    var rid = layer_name;

    var infoTemplate = new InfoTemplate(
      "Renewal Case " + rid,
      "Land ID: ${land_id}<br>"
    );

    var geoJsonLayer = new GeoJsonLayer({
      url: "../OCR/GeoJson/" + rid + ".json",
      infoTemplate: infoTemplate
    });

    // Zoom in to one guy
    geoJsonLayer.on("update-end", function(e) {
      lMap.setExtent(e.target.extent.expand(3));
    });

    geoJsonLayer.setRenderer(polyRenderer);
    lMap.addLayer(geoJsonLayer);
	
	return geoJsonLayer
  }

  /*
    Checkboxes for hiding/showing renew areas & rooftops
*/

  $("#l-renew").iCheck({
    checkboxClass: "icheckbox_flat-grey",
    radioClass: "iradio_flat-grey"
  });

  $("#l-renew").on("ifChecked", function(event) {});

  $("#l-renew").on("ifUnchecked", function(event) {});

  $("#r-renew").iCheck({
    checkboxClass: "icheckbox_flat-grey",
    radioClass: "iradio_flat-grey"
  });

  $("#r-renew").on("ifChecked", function(event) {});

  $("#r-renew").on("ifUnchecked", function(event) {});

  $("#l-roof").iCheck({
    checkboxClass: "icheckbox_flat-grey",
    radioClass: "iradio_flat-grey"
  });

  $("#l-roof").on("ifChecked", function(event) {
    lRooftops.show();
  });

  $("#l-roof").on("ifUnchecked", function(event) {
    lRooftops.hide();
  });

  $("#r-roof").iCheck({
    checkboxClass: "icheckbox_flat-grey",
    radioClass: "iradio_flat-grey"
  });

  $("#r-roof").on("ifChecked", function(event) {
    rRooftops.show();
  });

  $("#r-roof").on("ifUnchecked", function(event) {
    rRooftops.hide();
  });

  // function dataLayerHandler(isLeft, isRenew, isChecked) {
  //   lMap.removeAllLayers();
  //   lMap.addLayers([yearLayers[from]]);
  //   rMap.removeAllLayers();
  //   rMap.addLayers([yearLayers[to]]);
  // }
});
