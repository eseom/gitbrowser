define([], function () {
  'use strict';
  return {
    url: '/blob/:group/:repo/{path:any}',
    resolve: {
      blob: function ($http, $stateParams) {
        var group = $stateParams.group,
          repo = $stateParams.repo,
          path = $stateParams.path || '';
        return $http({
          url: '/repositories/blob/' + group + '/' + repo + '/' + path,
          method: 'GET'
        });
      }
    },
    controller: function blobCtrl($scope, $state, $sce, $stateParams, $http, blob) {
      $scope.blob_content = blob.data.blob_content;
      $scope.path = blob.data.path;
    }
  }
});
