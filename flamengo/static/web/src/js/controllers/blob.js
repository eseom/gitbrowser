define([], function () {
  'use strict';
  return {
    url: '/blob/:rgroup/:rname/{path:any}',
    resolve: {
      blob: function ($http, $stateParams) {
        var rgroup = $stateParams.rgroup,
          rname = $stateParams.rname,
          path = $stateParams.path || '';
        return $http({
          url: '/repositories/blob/' + rgroup + '/' + rname + '/' + path,
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
