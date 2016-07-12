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
    controller: function profileCtrl($scope, $rootScope, $http, profile, Flash) {
      $rootScope.title = 'Profile';
      $scope.user = profile.data.user;
      $scope.nicknameEditable = profile.data.user.nickname.length === 0;
      $scope.setNicknameEditable = function () {
        $scope.nicknameEditable = true;
      };
      $scope.save = function () {
        var name = $scope.user.name.trim();
        var nickname = $scope.user.nickname.trim();
        if (nickname === '') {
          Flash.create('danger', 'required nickname.', 0, {class: 'flash-message'}, true);
          return;
        }
        if (name === '') {
          Flash.create('danger', 'required name.', 0, {class: 'flash-message'}, true);
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

          Flash.create('success', 'Your information was saved.', 0, {class: 'flash-message'}, true);
        });
      }
    }
  };
});
