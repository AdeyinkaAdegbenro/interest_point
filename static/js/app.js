var app = angular.module('myApp', ['ngRoute']);

// configuring routing.
app.config(function($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', { // If URL is at /, uses template at
            templateUrl: '/static/pages/index.html', // this location
            controller: 'InterestsController' // and apply instructions from this controller
        })
    .otherwise({ // Any other URL, take me back to /
        redirectTo: '/'
    });
});

