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
    controller: function blobCtrl($rootScope, $scope, $state, $sce, $stateParams, $http, blob) {
      var rgroup = $stateParams.rgroup,
        rname = $stateParams.rname;

      $rootScope.title = rgroup + '/' + rname;
      $scope.blob_content = blob.data.blob_content;
      $scope.paths = blob.data.path.split('/');
    }
  }
});
