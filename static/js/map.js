
let map;
let places;
let infoWindow;
let markers = [];
let autocomplete;
const MARKER_PATH =
  "https://developers.google.com/maps/documentation/javascript/images/marker_green";
const sfBayCoords = {
  lat: 37.601773,
  lng: -122.20287,
};

function initMap() {
  
  map = new google.maps.Map(document.querySelector('#map'), {
    center: sfBayCoords,
    zoom: 11,
  });

  infoWindow = new google.maps.InfoWindow({
    content: document.getElementById("info-content"),
  });

  // Create the autocomplete object and associate it with the UI input control.
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("autocomplete"),
    {
      types: ["(regions)"],
      fields: ["address_components", "geometry", "icon", "name"],
    }
  );
  places = new google.maps.places.PlacesService(map);
  autocomplete.addListener("place_changed", onPlaceChanged);
} 
// When the user selects a city, get the place details for the city and
// zoom the map in on the city.
function onPlaceChanged() {
  const place = autocomplete.getPlace();

  if (place.geometry && place.geometry.location) {
    //Changes the center of the map to the given LatLng
    map.panTo(place.geometry.location);
    map.setZoom(15);
    search();
  } else {
    document.getElementById("autocomplete").placeholder = "Please enter a city or zip code first!";
  }
}

// Search for stores in the selected city, within the viewport of the map.
function search() {
  const search = {
    bounds: map.getBounds(),
    keyword: ["supermarket", "grocery"],
  };

  places.nearbySearch(search, (results, status, pagination) => {
    if (status === google.maps.places.PlacesServiceStatus.OK && results) {
      clearMarkers();

      // Create a marker for each hotel found, and
      // assign a letter of the alphabetic to each marker icon.
      for (let i = 0; i < results.length; i++) {
        const markerLetter = String.fromCharCode("A".charCodeAt(0) + (i % 26));
        const markerIcon = MARKER_PATH + markerLetter + ".png";

        // Use marker animation to drop the icons incrementally on the map.
        markers[i] = new google.maps.Marker({
          position: results[i].geometry.location,
          animation: google.maps.Animation.DROP,
          icon: markerIcon,
        });
        // If the user clicks a hotel marker, show the details of that hotel
        // in an info window.
        markers[i].placeResult = results[i];
        google.maps.event.addListener(markers[i], "click", showInfoWindow);
        setTimeout(dropMarker(i), i * 100);
      }
    }
  });
}

function clearMarkers() {
  for (let i = 0; i < markers.length; i++) {
    if (markers[i]) {
      markers[i].setMap(null);
    }
  }

  markers = [];
}

function dropMarker(i) {
  return function () {
    markers[i].setMap(map);
  };
}


// Get the place details for a store. Show the information in an info window,
// anchored on the marker for the store that the user selected.
function showInfoWindow() {
  // @ts-ignore
  const marker = this;

  places.getDetails(
    { placeId: marker.placeResult.place_id },
    (place, status) => {
      if (status !== google.maps.places.PlacesServiceStatus.OK) {
        return;
      }
      infoWindow.open(map, marker);
      buildIWContent(place);
    }
  );
}

// Load the place information into the HTML elements used by the info window.
function buildIWContent(place) {
  document.getElementById("iw-icon").innerHTML =
    '<img class="storeIcon" ' + 'src="' + place.icon + '"/>';
  document.getElementById("iw-url").innerHTML =
  '<b><a href="' + place.url + '">' + place.name + "</a></b>";
  document.getElementById("iw-hours").textContent = place.opening_hours['weekday_text'];
  document.getElementById("iw-address").textContent = place.vicinity;
  if (place.formatted_phone_number) {
    document.getElementById("iw-phone-row").style.display = "";
    document.getElementById("iw-phone").textContent =
      place.formatted_phone_number;
  } else {
    document.getElementById("iw-phone-row").style.display = "none";
  }
}


