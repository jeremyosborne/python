/*
 * Generate source code documentation (a. la. node-jsdoc-toolit).
 */

var error = require('./logger.js').error,
    log = require('./logger.js').log,
    exec = require('child_process').exec;



/**
 * Take JavaScript source code located in one directory and output generated
 * documentation to another directory of choice.
 *
 * @param args {Object} Associative array of arguments.
 * @param args.from {String} The directory from which to generate documentation.
 * Use an absolute path.
 * @param args.to {String} The directory in which to place the generated
 * documentation. If it does not exist, it will be created.
 * Use an absolute path.
 */
function docit(args) {

    log("docit: Attempting to document js files located in: " + args.from);
    log("docit: Attempting to output documentation to: " + args.to);

    exec(
        // Notes about the command located at the jsdoc-toolkit website at:
        // http://code.google.com/p/jsdoc-toolkit/wiki/CommandlineOptions
        [
            "node " + __dirname + "/../lib/node-jsdoc-toolkit/app/run.js",
            // All functions, including private, will be output.
            "--private",
            // Ignore all code, only document comments with @name tags.
            "--nocode",
            // Provide verbose feedback about what is happening.
            "--verbose",
            // Required. Use this template to format the output.
            "--template=" + __dirname + "/../lib/node-jsdoc-toolkit/templates/codeview",
            // Where to place output files
            "--directory="+args.to,
            // Finally the input files and directories
            // NOTE: If the source directory is more than one level deep, we may need to
            // turn on the -r flag to force recursion into the directories.
            args.from
        ].join(" "),
        // Callback
        function(err, stdout, stderr) {
            log("docit: jsdoc-toolkit stdout--------------------------");
            log(stdout);
            error("docit: jsdoc-toolkit stderr--------------------------");
            error(stderr);
            if (err !== null) {
                error('docit: jsdoc-toolkit error: ' + err);
            }
        }
    );
}

exports.docit = docit;
