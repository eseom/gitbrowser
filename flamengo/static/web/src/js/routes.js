define(['./app', 'controllers'], function (app, controllers) {
  'use strict';
  return app.config(function ($stateProvider, $urlRouterProvider) {
    for (var k in controllers) {
      var c = controllers[k];
      var templatePath = k.replace(/([a-z](?=[A-Z]))/g, '$1 ').split(' ').join('/');
      $stateProvider.state(k, {
        url: c.url,
        templateUrl: 'html/' + templatePath + '.html',
        controller: k + 'Ctrl',
        resolve: c.resolve
      })
    }
    $urlRouterProvider.otherwise('/repository/');
  });
});
