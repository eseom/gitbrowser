define([], function () {
  'use strict';
  return {
    name: 'profile',
    url: '/profile',
    resolve: {
      profile: function ($http) {
        return $http.get('/auth/me');
      }
    },
    controller: function profileCtrl($scope, $rootScope, $http, profile) {
      $rootScope.title = 'Profile';
      $scope.user = profile.data.user;
      $scope.nicknameEditable = false;
      $scope.setNicknameEditable = function () {
        $scope.nicknameEditable = true;
      };

      $scope.save = function () {
        var name = $scope.user.name.trim();
        var nickname = $scope.user.nickname.trim();
        if (nickname === '') {
          $rootScope.flashError('required nickname.');
          return;
        }
        if (name === '') {
          $rootScope.flashError('required name.');
          return;
        }
        var data = {
          id: $scope.user.id,
          nickname: $scope.user.nickname,
          name: $scope.user.name
        };
        if ($scope.user.password !== '' && $scope.user.password === $scope.user.passwordConfirm)
          data.password = $scope.user.password;
        $http({
          method: 'PUT',
          url: '/auth/save',
          data: data
        }).then(function (response) {
          $scope.user.password = '';
          $scope.user.passwordConfirm = '';

          $rootScope.flashMessage('saved.');
        });
      }
    }
  };
});
