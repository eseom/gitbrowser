define([], function () {
  return function cloneIndicator() {
    return ({
      replace: true,
      scope: {
        cloneUrl: '=cloneurl'
      },
      templateUrl: 'html/directives/clone-indicator.html'
    });
  };
});
