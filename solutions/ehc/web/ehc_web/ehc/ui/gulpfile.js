var gulp = require('gulp'),
    usemin = require('gulp-usemin'),
    wrap = require('gulp-wrap'),
    connect = require('gulp-connect'),
    watch = require('gulp-watch'),
    minifyCss = require('gulp-minify-css'),
    minifyJs = require('gulp-uglify'),
    concat = require('gulp-concat'),
    less = require('gulp-less'),
    rename = require('gulp-rename'),
    minifyHTML = require('gulp-minify-html'),
    gulpNgConfig = require('gulp-ng-config'),
    gutil = require('gulp-util');


var paths = {
    scripts: 'src/js/**/*.*',
    styles: 'src/less/**/*.*',
    images: 'src/img/**/*.*',
    templates: 'src/templates/**/*.html',
    index: 'src/index.html',
    bower_fonts: 'src/components/**/*.{ttf,woff,eof,svg}',
    ui_grid_fonts: 'src/components/angular-ui-grid/*.{ttf,woff,eof,svg}',
    bower_d3js: 'src/components/d3/d3.min.js',
    gulp_ng_config: './gulp_ng_config.json'
};

var ENV = process.env.LICENSE_UI_ENV ||'development';
console.info("LICENSE_UI_ENV: " + ENV);

/**
 * Handle bower components from index
 */
gulp.task('usemin', function() {
    return gulp.src(paths.index)
        .pipe(usemin({
            js: ['concat'],
            css: [minifyCss({keepSpecialComments: 0}), 'concat'],
        }))
        .on('error', gutil.log)
        .pipe(gulp.dest('dist/'));
});

/**
 * Copy assets
 */
//gulp.task('build-assets', ['copy-bower_fonts', 'copy-bower_d3js', 'config-environment']);
gulp.task('build-assets', ['copy-bower_fonts', 'config-environment']);

gulp.task('copy-bower_fonts', function() {
    return gulp.src(paths.bower_fonts)
        .pipe(rename({
            dirname: '/fonts'
        }))
        .pipe(gulp.dest('dist/lib'));
});

gulp.task('copy-ui-grid_fonts', function() {
    return gulp.src(paths.ui_grid_fonts)
        .pipe(gulp.dest('dist/lib/css'));
});

// gulp.task('copy-bower_d3js', function() {
//     return gulp.src(paths.bower_d3js)
//         .pipe(gulp.dest('dist/lib/js'));
// });

gulp.task('config-environment', function() {
    return gulp.src(paths.gulp_ng_config)
        .pipe(gulpNgConfig('RDash.config', {
            environment: ENV
        }))
        .on('error', gutil.log)
        .pipe(gulp.dest('src/js'))
});

/**
 * Handle custom files
 */
gulp.task('build-custom', ['custom-images', 'custom-js', 'custom-less', 'custom-templates']);

gulp.task('custom-images', function() {
    return gulp.src(paths.images)
        .pipe(gulp.dest('dist/img'));
});

gulp.task('custom-js', function() {
    return gulp.src(paths.scripts)
        // TODO: Production minifyJs()
        //.pipe(minifyJs())
        .pipe(concat('dashboard.min.js'))
        .on('error', gutil.log)
        .pipe(gulp.dest('dist/js'));
});

gulp.task('custom-less', function() {
    return gulp.src(paths.styles)
        .pipe(less())
        .pipe(concat('dashboard.css'))
        .pipe(gulp.dest('dist/css'));
});

gulp.task('custom-templates', function() {
    return gulp.src(paths.templates)
        .pipe(minifyHTML())
        .pipe(gulp.dest('dist/templates'));
});

/**
 * Watch custom files
 */
gulp.task('watch', function() {
    gulp.watch([paths.images], ['custom-images']);
    gulp.watch([paths.styles], ['custom-less']);
    gulp.watch([paths.scripts], ['custom-js'])
        .on('error', gutil.log);
    gulp.watch([paths.templates], ['custom-templates']);
    gulp.watch([paths.index], ['usemin']);
    gulp.watch([paths.gulp_ng_config], ['config-environment', 'custom-js']);
});

/**
 * Live reload server
 */
gulp.task('webserver', function() {
    connect.server({
        root: 'dist',
        livereload: true,
        port: 8888
    });
});

gulp.task('livereload', function() {
    gulp.src(['dist/**/*.*'])
        .pipe(watch())
        .on('error', gutil.log)
        .pipe(connect.reload());
});

/**
 * Gulp tasks
 */
gulp.task('build', ['usemin', 'build-assets', 'build-custom']);
gulp.task('default', ['build', 'webserver', 'livereload', 'watch']);
