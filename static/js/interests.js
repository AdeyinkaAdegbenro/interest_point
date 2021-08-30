var app = angular.module('myApp');

app.controller('InterestsController', ['$scope', '$http', "$timeout", function($scope, $http, $timeout) {
  $http.defaults.xsrfCookieName = 'csrftoken';
  $http.defaults.xsrfHeaderName = 'X-CSRFToken';
  var poi = $scope;
  
  poi.current_coords = {
    lat: null, lng: null
  };

  poi.all_interests = [];

  poi.default_map_center = {lat: -33.8688, lng: 151.2195};

  poi.loadInterests = function () {
    $http.get('/index').then(function success (response) {
      console.log(response)
      poi.all_interests = response.data
    }).then(function error (err) {
      console.log(err)
    })
  };

  poi.loadInterests();
  loadUsers();
  sharedWithUser();

  poi.addPoint = function(){
    $("#points-modal").modal({detachable: false, closable: false}).modal('show');
    poi.initMap("map", "point-search", false);
  };

  poi.editInterest = function (interest) {
    $("#edit-points-modal").modal({detachable: false, closable: false}).modal('show');
    $("#edit-point-nickname").val(interest.name);
    poi.default_map_center = {
      lat: parseFloat(interest.latitude), lng: parseFloat(interest.longitude)
    };

    poi.current_coords.id = interest.id;
    poi.current_coords.lat = interest.latitude;
    poi.current_coords.lng = interest.longitude;

    poi.initMap("edit-map", "edit-point-search", true)

  };

  poi.submitPoint = function  () {
    $('#submit-point-button').addClass("loading");
    const url = '/index'; 
    // set #submit-point-button to loading class
    $http.post(url, {'latitude': poi.current_coords.lat.toString(),
                     'longitude': poi.current_coords.lng.toString(),
                     'name': $("#point-nickname").val()
    }).then(function successCallback (response) {
      poi.current_coords = {
        lat: null, lng: null
      }
      poi.message = "Point of Interest added successfully"
      $timeout(function() { poi.message = ''}, 3000);
      clearData("#point-nickname", "#points-modal", '#submit-point-button', "#point-search");
      poi.loadInterests()
    }).catch(function errorCallback (error) {
      console.log(error);
      poi.current_coords = {
        lat: null, lng: null
      }
      poi.message = "An error occurred while creating the Point of Interest"
      $timeout(function() { poi.message = ''}, 3000);
      clearData("#point-nickname", "#points-modal", '#submit-point-button', "#point-search");
      poi.loadInterests();
    });
  };

  poi.cancelButton = function (create) {
    poi.current_coords = {
      lat: null, lng: null
    }
    if (create) {
      clearData("#point-nickname", "#points-modal", '#submit-point-button', "#point-search");
    } else {
      clearData("#edit-point-nickname", "#edit-points-modal", '#edit-point-button', "#edit-point-search");
    }
  }

  function clearData (input, modal, button, map_search) {
    $(input).val("")
    $(modal).modal('hide');
    $(button).removeClass("loading");
    $(map_search).val("")
  }
  

  poi.initMap = function initMap(map_id, search_box_id, editing) {
    const mapDiv = document.getElementById(map_id);
    const mapOptions = {
      center: poi.default_map_center,
      zoom: 13,
      mapTypeId: "roadmap",
    };
    const map = new google.maps.Map(
      mapDiv,
      mapOptions
    );

    if (editing) {
      marker = new google.maps.Marker({
        position: poi.default_map_center,
        map: map,
        draggable: true
      });

      marker.addListener('dragend', function(event){
        console.log('event coords', event, event.latLng.lat(), event.latLng.lng())
        poi.current_coords.lat = event.latLng.lat()
        poi.current_coords.lng = event.latLng.lng()
      });
    }

    // Create the search box and link it to the UI element.
    const search_input = document.getElementById(search_box_id);
    const searchBox = new google.maps.places.SearchBox(search_input);
    
    // Bias the SearchBox results towards current map's viewport.
    map.addListener("bounds_changed", () => {
      searchBox.setBounds(map.getBounds());
    });
    let markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener("places_changed", () => {
      const places = searchBox.getPlaces();
  
      if (places.length == 0) {
        return;
      }
      // Clear out the old markers.
      markers.forEach((marker) => {
        marker.setMap(null);
      });
      markers = [];
      // For each place, get the icon, name and location.
      const bounds = new google.maps.LatLngBounds();
      places.forEach((place) => {
        var place_loc = place.geometry.location;
        var place_geo = place.geometry;
        if (!place_geo || !place_loc) {
          console.log("Returned place contains no geometry");
          return;
        }
        
        console.log('place coords', place, place_loc.lat(), place_loc.lng())
        poi.current_coords.lat = place_loc.lat()
        poi.current_coords.lng = place_loc.lng()
        const icon = {
          url: place.icon,
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(25, 25),
        };
        // Create a marker for each place.
        const place_marker = new google.maps.Marker({
          map,
          draggable: true,
          title: place.name,
          position: place_loc,
        });
        place_marker.addListener('dragend', function(event){
          poi.current_coords.lat = event.latLng.lat()
          poi.current_coords.lng = event.latLng.lng()
        });
        markers.push(place_marker);
  
        if (place_geo.viewport) {
          // Only geocodes have viewport.
          bounds.union(place_geo.viewport);
        } else {
          bounds.extend(place_loc);
        }
      });
      map.fitBounds(bounds);
    });

  }


  poi.updatePoint = function () {
    // call /index using angular.http and a new point
    $('#edit-point-button').addClass("loading")
    const url = 'index'; 
    // set #submit-point-button to loading class
    $http.put(url, {'latitude': poi.current_coords.lat.toString(),
                    'longitude': poi.current_coords.lng.toString(),
                    'name': $("#edit-point-nickname").val(),
                    'id': poi.current_coords.id
    }).then(function successCallback (response) {
      console.log(response)
      poi.current_coords = {
        lat: null, lng: null, id: null
      }
      poi.message = "Point of Interest updated successfully"
      $timeout(function() { poi.message = ''}, 3000);
      poi.loadInterests();
      clearData("#edit-point-nickname", "#edit-points-modal", '#edit-point-button', "#edit-point-search");
    }).catch(function errorCallback (error) {
      console.log(error);
      poi.current_coords = {
        lat: null, lng: null, id: null
      }
      poi.message = "An error occurred while creating the Point of Interest"
      $timeout(function() { poi.message = ''}, 3000);
      
      clearData("#edit-point-nickname", "#edit-points-modal", '#edit-point-button', "#edit-point-search");
    });
  }

  poi.openSharePoint = function (interest) {
    poi.current_shared_interest = interest.id;
    poi.current_shared_interest_name = interest.name;
    poi.shared_user = "";
    $('#share-modal').modal({detachable: false, closable: false}).modal('show');
    
    
  };

  poi.sharePoint = function () {
    $http.post('/share', 
              {'interest_id': poi.current_shared_interest, 
               "shared_user": poi.shared_user}).then(function (response) {
                console.log(response);
    }).catch(function (err) {
      console.log(err);
    });
  };

  function loadUsers () {
    $http.get('/users').then(function success (response) {
      poi.all_users = response.data
    }).catch(function error (err) {
      console.log(err)
    })
  };

  poi.cancelShareButton = function () {
    $('#share-modal').modal('hide');
    poi.current_shared_interest = null;
    poi.shared_user = null;
  };

  poi.updateSelected = function (shared_user) {
    poi.shared_user = shared_user;
  }

  poi.addToList = function (interest) {
    $('#add-list-button').addClass("loading");
    $http.post('/index', {'latitude': interest.latitude.toString(),
                    'longitude': interest.longitude.toString(),
                    'name': interest.name
    }).then(function successCallback (response) {
      console.log(response)
      poi.shared_message = "Point of Interest added successfully"
      $timeout(function() { poi.shared_message = ''}, 3000);
      $('#add-list-button').removeClass("loading");
      poi.loadInterests()
    }).catch(function errorCallback (error) {
      console.log(error);
      poi.shared_message = "An error occurred while creating the Point of Interest"
      $timeout(function() { poi.shared_message = ''}, 3000);
      poi.loadInterests();
      $('#add-list-button').removeClass("loading");
    });
  }

  function sharedWithUser () {
    $http.get('/share').then(function success (response) {
      console.log(response)
      poi.shared_with_me = response.data
      console.log('all_interests', poi.shared_with_me)
    }).catch(function error (err) {
      console.log(err)
    })
  }
  

  }]);