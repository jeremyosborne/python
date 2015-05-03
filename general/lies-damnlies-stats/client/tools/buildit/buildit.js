/*
 * Some simple tools I want for building my javascript projects.
 */

module.exports = {
    appcache: require('./src/appcache.js').appcache,
    compileTemplates: require('./src/compiletemplates.js').compileTemplates,
    compress: require('./src/compress.js').compress,
    concat: require('./src/concat.js').concat,
    copy: require('./src/copy.js').copy,
    docit: require('./src/docit.js').docit,
    logger: require('./src/logger.js'),
    mkdir: require('./src/mkdir.js').mkdir,
    rmrf: require('./lib/rmrf.js').sync,
};
