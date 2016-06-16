define(['./app', 'controllers'], function (app, controllers) {
  'use strict';
  return app.config(function ($stateProvider, $urlRouterProvider) {
    for (var k in controllers) {
      var c = controllers[k];
      $stateProvider.state(k, {
        url: c.url,
        templateUrl: 'html/' + k + '.html',
        controller: k + 'Ctrl',
        resolve: c.resolve
      })
    }
    $urlRouterProvider.otherwise('/dashboard/');
  });
});
