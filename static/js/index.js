var map;
var markerClusterer = null;
var coordinates_lat = [];
var coordinates_lng = [];
var tweets = [];
var markers = [];
var prev_infowindow = null;

function initMap() {
  var myLatLng = {lat: 40.8075, lng: -73.9626};
  
  // Create a map object and specify the DOM element for display.
  map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    scrollwheel: false,
    zoom: 4
  });

  markerClusterer = new MarkerClusterer(map, markers)

}

function Search() {
  var select = document.getElementById("dropdown");
  var searchKey = select.options[select.selectedIndex].value;
  console.log(searchKey);
  httpGetAsync("searchf/", searchKey);
}

function httpGetAsync(theUrl, keyword) {
  // resetVariables()
  console.log("in the http get part");
  $.getJSON(theUrl + keyword, function(result){
    processJsonResult(result, keyword);
  });
}

function processJsonResult(result, keyword) {
  var tweets_list = result[keyword];
  if (tweets_list == null) {
    alert("No results found");
    return;
  }
  console.log("in the result part");
  console.log(tweets_list);
  for (var i = 0; i < tweets_list.length; i++) {
    var tweet = tweets_list[i];
    coordinates_lng.push(tweet.coordinates[0]);
    coordinates_lat.push(tweet.coordinates[1]);
    tweets.push(tweet.text);
  }
  generateMarkers();
}

function generateMarkers() {
  for (var i = 0; i < tweets.length; i++) {
    
    var location = { 
      lat : parseFloat(coordinates_lat[i]),
      lng : parseFloat(coordinates_lng[i])
    }

    var contentString = '<div id="content">'+
            "<p>" + tweets[i] + "</p>" +
            "</div>";

    var marker = new google.maps.Marker({
      position: location,
      title: 'Hello World!'
    });

    var infowindow = new google.maps.InfoWindow();

    bindInfoWindow(marker, map, infowindow, contentString);

    markers.push(marker);

  }

  markerClusterer.addMarkers(markers);

}

function bindInfoWindow(marker, map, infowindow, html) {
  marker.addListener('click', function() {
    if( prev_infowindow != null ) {
        prev_infowindow.close();
    }
    prev_infowindow = infowindow;
    infowindow.setContent(html);
    infowindow.open(map, this);
  });
}