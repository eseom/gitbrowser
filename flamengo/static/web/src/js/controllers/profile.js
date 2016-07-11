define([], function () {
  'use strict';
  return {
    url: '/profile',
    resolve: {
      profile: function ($http) {
        return $http.get('/auth/me');
      }
    },
    controller: function profileCtrl($scope, $rootScope, $http, profile) {
      $rootScope.title = 'Profile';
      $scope.user = profile.data.user;

      $scope.save = function () {
        var data = {
          id: $scope.user.id,
          nickname: $scope.user.nickname,
          name: $scope.user.name
        };
        if ($scope.user.password !== '' && $scope.user.password === $scope.user.passwordConfirm)
          data.password = $scope.user.password;
        $http({
          method: 'POST',
          url: '/auth/save',
          data: data
        }).then(function (response) {
          $scope.user.password = '';
          $scope.user.passwordConfirm = '';
        });
      }
    }
  };
});
