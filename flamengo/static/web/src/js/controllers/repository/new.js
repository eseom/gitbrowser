define([], function () {
  'use strict';
  return {
    controller: function repositoryNewCtrl($scope,
                                           $uibModalInstance,
                                           $http,
                                           repos,
                                           callback) {
      $scope.availableGroups = repos.groups;
      $scope.new = {
        type: 'public',
        group: '',
        name: '',
        description: ''
      };

      $scope.ok = function () {
        /* make repository */
        $http({
          method: 'POST',
          url: '/repositories',
          data: {
            type: $scope.new.type,
            group: $scope.new.group,
            name: $scope.new.name,
            description: $scope.new.description
          }
        }).then(function (response) {
          callback && callback();
          $uibModalInstance.close(response.data);
        });
      };

      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }
  };
});
