define([], function () {
  'use strict';
  return {
    url: '/repository/:group',
    resolve: {
      repos: function ($http, $stateParams) {
        var group = $stateParams.group;
        return $http({
          url: '/repos' + (group ? '/' + group : ''),
          method: 'GET'
        });
      }
    },
    controller: function repositoryCtrl($scope, $rootScope, $stateParams, repos) {
      var group = $stateParams.group;
      $rootScope.title = 'repository';
      $scope.isGroups = group === '';
      $scope.repos = repos.data.repos;
    }
  };
});
