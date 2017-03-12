
function initMap() {
  var columbia = {lat: 40.8075, lng: -73.9626};
// Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
    center : columbia,
    scrollwheel : false,
    zoom : 4
  });

  // var imsage = '../img/pin.png';

  var marker = new google.maps.Marker({
          map: map,
          position: columbia,
          // icon: image
        });

}