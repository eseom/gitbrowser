define([], function () {
  'use strict';
  return {
    url: '/commit/:group/:repo/:hexsha',
    resolve: {
      commit: function ($http, $stateParams) {
        var group = $stateParams.group,
          repo = $stateParams.repo,
          hexsha = $stateParams.hexsha;
        return $http({
          url: '/commit/' + group + '/' + repo + '/' + hexsha,
          method: 'GET'
        });
      }
    },
    controller: function commitCtrl($scope, $state, $sce, $stateParams, $http, commit) {
      var hexsha = $stateParams.hexsha || '';
      commit.data.diff_contents.forEach(function (data) {
        angular.element(document.getElementById('diffContents')).append(
          diffview.buildView({
            baseTextLines: data.baseTextLines,
            newTextLines: data.newTextLines,
            opcodes: data.opcodes,
            baseTextName: data.baseTextName,
            newTextName: data.newTextName,
            contextSize: 3
          }));
      });
      $scope.parents = commit.data.parents;
      $scope.hexsha = hexsha;
      $scope.commit = commit.data.commit;
    }
  }
});
