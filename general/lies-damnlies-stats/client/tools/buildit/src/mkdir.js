var fs = require('fs'),
    path = require('path'),
    error = require('./logger.js').error,
    log = require('./logger.js').log,
    verbose = require('./logger.js').verbose;


/**
 * Makes a directory, as one would make a directory using "mkdir -p dir/name".
 *
 * Synchronous command.
 *
 * Respects absolute paths (beginning with '/'). If the directory already exists
 * we do nothing.
 *
 * @param dir {String} The directory we wish to make. Assumes that the path
 * does or will lead to a directory. Does not attempt to intelligently handle
 * file paths by stripping off the file.
 */
function mkdir(dir) {
    var dirs,
        dirWalk = "";

    if (!path.existsSync(dir)) {
        log("mkdir: creating directory: " + dir);
        // Make the directory.
        dirs = dir.split('/');
        for (var i = 0; i < dirs.length; i++) {
            dirWalk += dirs[i] + "/";
            if (!path.existsSync(dirWalk)) {
                // It seems that "777" gets umask'd, which is what I want.
                fs.mkdirSync(dirWalk, "777");
                verbose("mkdir: created directory: " + dirWalk);
            }
            else {
                verbose("mkdir: directory already exists: " + dirWalk);
            }
        }
    }
    else {
        verbose("mkdir: directory already exists: " + dir);
    }
}

exports.mkdir = mkdir;
