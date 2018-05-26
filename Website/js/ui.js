var lMap, rMap;
var lYear, rYear;
// var lYearLayers = {}, rYearLayers = {};
//var layers = {};
var yearLayers = {};
var years = [2011, 2012, 2013, 2015, 2017];
var rooftop;

require([
  "esri/map",
  "esri/layers/ArcGISTiledMapServiceLayer",
  "esri/layers/CSVLayer",
  "esri/Color",
  "esri/symbols/SimpleMarkerSymbol",
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
  Color,
  SimpleMarkerSymbol,
  SimpleRenderer,
  InfoTemplate,
  esriRequest,
  array,
  Point,
  Graphic,
  GeoJsonLayer
) {
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

  var leftConnection = dojo.connect(lMap, "onExtentChange", leftChangeHandler);

  years.forEach(function(year) {
    mapServer =
      "https://www.historygis.udd.gov.taipei/arcgis/rest/services/Aerial/Ortho_" +
      year +
      "/MapServer";
    yearLayers[year] = new ArcGISTiledMapServiceLayer(mapServer);
    // layers["L"][year]["base"] = new ArcGISTiledMapServiceLayer(mapServer);
    // layers["R"][year]["base"] = new ArcGISTiledMapServiceLayer(mapServer);
  });

  lMap.addLayers([yearLayers[2011]]);
  rMap.addLayers([yearLayers[2017]]);

  function leftChangeHandler(ext) {
    rMap.setExtent(ext);
  }

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

  // $(document).ready(function() {
  //   $('input').iCheck({
  //     checkboxClass: 'icheckbox_flat-grey',
  //     radioClass: 'iradio_flat-grey'
  //   });

  //   $('input').on('ifChecked', function(event){
  //     alert("id = " + $(this).val());
  //   });
  // });

  rooftop = new CSVLayer("./Output.csv");
  var orangeRed = new Color([238, 69, 0, 0.5]); // hex is #ff4500
  var marker = new SimpleMarkerSymbol("solid", 15, null, orangeRed);
  var renderer = new SimpleRenderer(marker);
  rooftop.setRenderer(renderer);
  lMap.addLayer(rooftop);
  //rMap.addLayer(rooftop);
  rooftop.show();
  // rooftop.hide();

  $("#l-renew").iCheck({
    checkboxClass: "icheckbox_flat-grey",
    radioClass: "iradio_flat-grey"
  });

  $("#l-renew").on("ifChecked", function(event) {
    rooftop.show();
  });

  $("#l-renew").on("ifUnchecked", function(event) {
    rooftop.hide();
  });

  function dataLayerHandler(isLeft, isRenew, isChecked) {
    lMap.removeAllLayers();
    lMap.addLayers([yearLayers[from]]);
    rMap.removeAllLayers();
    rMap.addLayers([yearLayers[to]]);
  }
});
