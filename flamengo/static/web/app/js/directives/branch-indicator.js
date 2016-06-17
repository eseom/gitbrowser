define([], function () {
  return function branchIndicator() {
    return ({
      replace: true,
      scope: {
        branches: '=branches',
        currentBranch: '=currentbranch'
      },
      templateUrl: 'html/directives/branch-indicator.html'
    });
  };
});
