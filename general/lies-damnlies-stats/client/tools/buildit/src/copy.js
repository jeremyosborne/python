/*
 * A simple copy utility used to move dirt... I mean files from spot a to
 * spot b.
 */

var fs = require('fs'),
    mkdir = require('./mkdir.js').mkdir,
    error = require('./logger.js').error,
    log = require('./logger.js').log,
    verbose = require('./logger.js').verbose,
    pathobject = require('./pathobject.js');

/**
 * Perform a full file copy from one path to another.
 * @param from {String} Path to the input file.
 * @param to {String} Path to the output file.
 */
function performFileCopy(from, to) {
        // Buffer, should be good for text and binary files.
    var fromBuffer = fs.readFileSync(from);

    log("copy file: from "+from+", to "+to);

    fs.writeFileSync(to, fromBuffer);
}

/**
 * Copy one file or directory (recursively) to another file (if a file) or
 * directory.
 * Copied files will always overwrite their target files, assuming the copier
 * has correct permissions.
 *
 * @param args {Object} Associative array of arguments.
 * @param args.from {String} The from location. If the from path is
 * a file, just the file will be copied. If the from path is a directory,
 * all of the contents, but not the directory itself, will be copied.
 * @param args.to {String} The path to the copy target. If to exists and is
 * a directory, the from path will be mirrored to this directory. If to
 * is an existing file and from is an existing file, from will overwrite to.
 * If from is a directory and to is an existing file, it will generate an
 * error.
 * If to does not exist, it will be treated as follows:
 * If to does not have a trailing slash, it will be treated as a file and
 * follow the same rules as if the from path were a file.
 * If to does have a trailing slash, it will be treated as a directory and
 * the directory will be created, and from will be copied to the directory.
 * @throw {Error} If from doesn't exist.
 */
function copy(args) {
    var from = pathobject(args.from),
        to = pathobject(args.to),
        // target directories we might need to make.
        dirlist,
        // files to copy from into to
        filelist,
        i;

    // to is either a file, a directory, or doesn't exist.
    if (to.inferFile() && from.isFile()) {
        // Copy from the from location directly to the to location.

        // Make the required directory structure, just in case the inferFile
        // leads to a directory that doesn't exist.
        mkdir(to.dirname());

        // Copy the file.
        performFileCopy(from.path, to.path);
    }
    else if (to.inferDirectory() && from.exists()) {
        if (from.isFile()) {
            // one to one copy from file to file located in this directory

            // Make the required directory structure just in case the inferred
            // directory doesn't exist.
            mkdir(to.path);

            // Copy the file.
            performFileCopy(from.path, to.join(from.baseName(path)));
        }
        else {
            // We assume from is a directory and treat it as such...
            // ... this might be bad, but I'll look the other way for now.

            // Make the required directory structure
            // Need to make sure the to directory exists first...
            mkdir(to.path);
            // ...followed by the subdirectory structure.
            dirlist = from.descendentDirectoryPaths();
            for (i = 0; i < dirlist.length; i++) {
                mkdir(to.join(dirlist[i]));
            }

            // Copy files.
            filelist = from.descendentFilePaths();
            for (i = 0; i < filelist.length; i++) {
                performFileCopy(from.join(filelist[i]), to.join(filelist[i]));
            }
        }
    }
    else {
        throw new Error("the combination of from: "+from.path+
            "and to: "+to.path+" is not valid.");
    }

}

exports.copy = copy;
