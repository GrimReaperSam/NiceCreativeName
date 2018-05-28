var lMap, rMap;
var lYear, rYear;
var lYearLayers = {},
  rYearLayers = {};
var lRooftops, rRooftops;
var lRenewLayers = {},
  rRenewLayers = {};
var years = [2011, 2012, 2013, 2015, 2017];
var data = {};
// var rooftop;

require([
  "esri/dijit/Popup",
  "dojo/dom-construct",
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
  Popup,
  domConstruct,
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

  var lPopup = new Popup(
    {
      fillSymbol: new SimpleFillSymbol("solid", null, new Color([241, 195, 5, 0.7])),
      // popupWindow: false,
      titleInBody: false
      
    },
    domConstruct.create("div")
  );

  var rPopup = new Popup(
    {
      fillSymbol: new SimpleFillSymbol("solid", null, new Color([241, 195, 5, 0.7])),
      // popupWindow: false,
      titleInBody: false
    },
    domConstruct.create("div")
  );

  lMap = new Map("l-map", {
    // nav: true,
    extent: initExt,
    logo: false,
    zoom: 18,
    infoWindow: lPopup
  });

  rMap = new Map("r-map", {
    // nav: false,
    extent: initExt,
    logo: false,
    zoom: 18,
    infoWindow: rPopup
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

  lYear = 2011;
  rYear = 2017;
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
    hide_min_max: true,
    onFinish: function(data) {
      changeYear(data.from_value, data.to_value);
      lYear = data.from_value;
      rYear = data.to_value;
    }
  });

  function changeYear(from, to) {
    lMap.removeAllLayers();
    lMap.addLayer(lYearLayers[from]);
    rMap.removeAllLayers();
    rMap.addLayer(rYearLayers[to]);
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
  rMap.addLayer(rRooftops);
  rRooftops.hide();

  /*
    Load Final.csv using papaparse.js
    Save as {rid:{attr:val}} dictionary
  */

  Papa.parse("data/Final.csv", {
    delimiter: ",",
    header: true,
    trimHeader: true,
    dynamicTyping: true,
    skipEmptyLines: true,
    download: true,
    complete: function(results, file) {
      results.data.forEach(function(r) {
        data[r["district"]] = r;
      });
    }
  });

  /*
    Load GeoJson file
  */

  var polyMarker = new SimpleFillSymbol(
    "solid",
    null,
    new Color([241, 136, 5, 0.6])
  );
  var polyRenderer = new SimpleRenderer(polyMarker);

  lMap.on("load", function() {
    for (var rid in data) {
      lRenewLayers[rid] = addGeoJsonLayer(rid, true);
      rRenewLayers[rid] = addGeoJsonLayer(rid, false);
    }
  });

  function addGeoJsonLayer(rid, isLeft) {
    var infoTemplate = new InfoTemplate(
      rid,
      "Land Number: ${land_id}<br>" +
        data[rid]["featuresCount"] +
        " units with total area " +
        Math.round(data[rid]["area"])
    );

    var geoJsonLayer = new GeoJsonLayer({
      url: "data/GeoJson/" + rid + ".json",
      infoTemplate: infoTemplate
    });

    geoJsonLayer.on("load", function() {
      geoJsonLayer.maxScale = 0; // show the states layer at all scales
      // geoJsonLayer.setSelectionSymbol(
      //   new SimpleFillSymbol().setOutline(null).setColor("#fb9021")
      // );
    });

    geoJsonLayer.on("click", function(c) {});

    // change cursor to indicate features are click-able
    geoJsonLayer.on("mouse-over", function() {
      if (isLeft) lMap.setMapCursor("pointer");
      else rMap.setMapCursor("pointer");
    });
    geoJsonLayer.on("mouse-out", function() {
      if (isLeft) lMap.setMapCursor("default");
      else rMap.setMapCursor("default");
    });

    // Zoom-in to one guy
    // geoJsonLayer.on("update-end", function(e) {
    //   lMap.setExtent(e.target.extent.expand(3));
    // });

    geoJsonLayer.setRenderer(polyRenderer);
    if (isLeft) lMap.addLayer(geoJsonLayer);
    else rMap.addLayer(geoJsonLayer);

    return geoJsonLayer;
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
