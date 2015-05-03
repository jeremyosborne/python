/*
 * Concat buildit module.
 */

var fs = require('fs'),
    path = require('path'),
    // Logging functions
    error = require('./logger.js').error,
    log = require('./logger.js').log,
    verbose = require('./logger.js').verbose,
    mkdir = require('./mkdir.js').mkdir,
    // Default file encoding
    defaultEncoding = "utf8",
    // The default choice for whether we keep a file or not.
    defaultKeepExistingFile = false;


/**
 * From a list of file paths, concatenate, in order, into a single
 * output file.
 *
 * @param args {Object} Associative array of arguments.
 * @param args.infiles {String[]} Array of file paths we wish to concatenate
 * together, in order from first (top) to last (bottom) of the resulting file.
 * @param args.outfile {String} The results file path.
 * @param [args.keepExistingFile=false] {Boolean} If the outfile already exists
 * should we keep it and concatenate to it, or overwrite it (the default).
 * @param [args.encoding="utf8"] {String} The encoding of the input and output
 * files.
 * @param [args.insertBetweenFiles="\n"] {String} Make an empty string
 * (or falsey) to put nothing between files. (Probably put an empty string by
 * default.)
 */
function concat(args) {
    var data,
        // local var is the file descriptor
        outfile,
        i,
        writemode;

    args = args || {};
    // Normalize
    args.keepExistingFile = args.keepExistingFile || defaultKeepExistingFile;
    args.infiles = args.infiles || [];
    args.encoding = args.encoding || defaultEncoding;

    if (args.outfile && args.infiles.length) {
        log("concat: attempting to concatenate files into: " + args.outfile);

        if (!path.existsSync(path.dirname(args.outfile))) {
            mkdir(path.dirname(args.outfile));
        }

        if (args.keepExistingFile) {
            log("concat: appending files to existing file (if outfile exists).");
        }
        else {
            log("concat: overwriting file (if outfile exists).");
        }

        outfile = fs.openSync(args.outfile, (args.keepExistingFile) ? "a" : "w");

        for (i = 0; i < args.infiles.length; i++) {
            verbose("concat: concatenating file: " + args.infiles[i]);
            data = fs.readFileSync(args.infiles[i], args.encoding);
            fs.writeSync(outfile, data, null, args.encoding);
            if (args.insertBetweenFiles) {
                fs.writeSync(outfile, data, null, args.insertBetweenFiles);
            }
        }

        fs.closeSync(outfile);
    }
    else {
        log("concat: could not concatenate file ("+args.outfile+")");
    }
}

exports.concat = concat;
