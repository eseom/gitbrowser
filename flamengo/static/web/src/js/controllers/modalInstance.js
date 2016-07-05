define([], function () {
  'use strict';
  return {
    controller: function ModalInstanceCtrl($scope,
                                           $uibModalInstance,
                                           $http,
                                           repos,
                                           callback) {
      $scope.availableRepos = repos.repos;
      $scope.availableGroups = repos.groups;
      $scope.current = repos.current || {};
      console.log($scope.current);

      $scope.ok = function () {
        console.log($scope.current)
        if (!$scope.current.name) {
          /* make repository */
          $http({
            method: 'POST',
            url: '/manage/repo/create',
            data: {
              name: this.name,
              group: this.group,
              description: this.description
            }
          }).then(function (response) {
            console.log(callback)
            callback && callback();
            $uibModalInstance.close(response.data);
          });
        } else {
          $http({
            method: 'POST',
            url: '/manage/repo/edit',
            data: {
              name: this.name,
              description: this.description
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
