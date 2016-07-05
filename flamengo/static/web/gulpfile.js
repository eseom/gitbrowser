var gulp = require('gulp'),
  amdOptimize = require("amd-optimize"),
  htmlreplace = require('gulp-html-replace'),
  less = require('gulp-less'),
  htmlmin = require('gulp-htmlmin'),
  merge = require('merge-stream'),
  uglify = require('gulp-uglify'),
  minify = require('gulp-minify-css'),
  concat = require('gulp-concat'),
  gif = require('gulp-if'),
  resources = require('gulp-resources'),
  del = require('del'),
  runSequence = require('gulp-run-sequence');

gulp.task('scripts', function () {

  gulp.src('src/js/main.js')
    .pipe(amdOptimize("main",
      {
        name: "main",
        configFile: "./src/js/main.js",
        baseUrl: './src/js'
      }
    ))
    .pipe(concat('main.js'))
    .pipe(gulp.dest('./dist/'));
});

gulp.task('htmls', function () {
  return gulp.src('./src/html/**/*.html')
    .pipe(htmlmin({collapseWhitespace: true}))
    .pipe(gulp.dest('./dist/html/'))
});

gulp.task('replace', function () {
  gulp.src('./src/app.html')
    .pipe(resources())
    .pipe(gif('**/*.less', concat('less.file')))
    .pipe(gif('**/*.css', concat('css.file')))
    .pipe(gulp.dest('./dist/temp/'));

  var lessStream = gulp.src('./dist/temp/less.file').pipe(less()).pipe(concat('less-files.less'));
  var cssStream = gulp.src('./dist/temp/css.file').pipe(concat('css-files.css'));
  merge(lessStream, cssStream)
    .pipe(concat('style.css'))
    .pipe(minify())
    .pipe(gulp.dest('./dist/css/'));

  gulp.src('./src/app.html')
    .pipe(htmlreplace({
      css: 'css/style.css',
      js: {
        src: null,
        tpl: ''
      },
      requirejs: {
        src: [['require.js', 'main']],
        tpl: '<script src="%s" data-main="%s"></script>'
      }
    }))
    .pipe(gulp.dest('./dist'));
});

gulp.task('assets', function () {
  gulp.src('./src/bower_components/font-awesome/fonts/**/*.{ttf,woff,woff2,eof,svg}')
    .pipe(gulp.dest('./dist/fonts/'));
  gulp.src('./src/bower_components/requirejs/require.js')
    .pipe(gulp.dest('./dist/'));
});

gulp.task('cleanup', function () {
  // clean up
  del(['./dist/temp/']);
});

gulp.task('default', function () {
  runSequence(['scripts', 'htmls', 'assets', 'replace'], 'cleanup');
});
