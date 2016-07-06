define([], function () {
  'use strict';
  return {
    controller: function repositoryEditCtrl($scope,
                                            $uibModalInstance,
                                            $http,
                                            repos,
                                            callback) {
      $scope.availableRepos = repos.repos;
      $scope.availableGroups = repos.groups;
      $scope.current = repos.current || {
          name: '',
          group: '',
          description: ''
        };
      $scope.new = angular.copy(repos.current);

      $scope.ok = function () {
        if (!$scope.current.name) {
          /* make repository */
          $http({
            method: 'POST',
            url: '/repositories',
            data: {
              name: $scope.new.name,
              group: $scope.new.group,
              description: $scope.new.description
            }
          }).then(function (response) {
            callback && callback();
            $uibModalInstance.close(response.data);
          });
        } else {
          $http({
            method: 'PUT',
            url: '/repositories/' + $scope.current.id,
            data: {
              // group: $scope.new.group // prevent to edit group here
              name: $scope.new.name,
              description: $scope.new.description
            }
          }).then(function (response) {
            callback && callback();
            $uibModalInstance.close(response.data);
          });
        }
      };

      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }
  };
});
