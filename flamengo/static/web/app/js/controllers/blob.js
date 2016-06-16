define([], function () {
  'use strict';
  return {
    url: '/blob/:group/:repo/:branch/{path:any}',
    resolve: {
      blob: function ($http, $stateParams) {
        var group = $stateParams.group,
          repo = $stateParams.repo,
          branch = $stateParams.branch,
          path = $stateParams.path || '';
        return $http({
          url: '/blob/' + group + '/' + repo + '/' + branch + '/' + path,
          method: 'GET'
        });
      }
    },
    controller: function blobCtrl($scope, $state, $sce, $stateParams, $http, blob) {
      $scope.blob_content = blob.data.blob_content
    }
  }
});
