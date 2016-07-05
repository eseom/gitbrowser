define([], function () {
  return function branchIndicator() {
    return ({
      replace: true,
      scope: {
        branches: '=branches',
        currentBranch: '=currentbranch',
        urlcallback: '=urlcallback'
      },
      templateUrl: 'html/directives/branch-indicator.html'
    });
  };
});
