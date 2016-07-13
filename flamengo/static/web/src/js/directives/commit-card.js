define([], function () {
  return function commitCard($timeout,
                             $rootScope,
                             $animate) {
    return {
      replace: true,
      scope: {
        rgroup: '=rgroup',
        rname: '=rname',
        commit: '=commit'
      },
      templateUrl: 'html/directives/commit-card.html',
      link: function (scope, element, attributes) {
      }
    }
  };
});