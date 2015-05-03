/*
 * Simple manifest (appcache) file builder.
 * See for example of the manifest file we are talking about:
 * http://www.whatwg.org/specs/web-apps/current-work/multipage/offline.html
 */

var fs = require('fs'),
    error = require('./logger.js').error,
    log = require('./logger.js').log,
    verbose = require('./logger.js').verbose;


/**
 * Build a manifest file in the style of offline web applications.
 *
 * @param args {Object} Associative array of arguments.
 * @param args.outfile {String} The path to put the file name. Path is assumed to
 * include the name of the file.
 * @param args.CACHE {String[]} List of files/URLs to include in the CACHE 
 * section.
 * @param args.NETWORK {String[]} List of URLs to include in the NETWORK
 * section.
 * @param args.FALLBACK {String[]} List of fallback entries to include in the
 * FALLBACK section.
 */
function appcache(args) {
    var outfile,
        i;

    log("appcache: attempting to build a manifest file at: " + args.outfile);

    outfile = fs.openSync(args.outfile, "w");

    // Build the template.
    
    // Required header.
    fs.writeSync(outfile, "CACHE MANIFEST\n");

    // Write the build header. If we're rebuilding the appcache, we want to
    // make sure the new manifest file is used.
    // We use a JavaScript time assuming that we won't run builds faster
    // than a millisecond apart.
    fs.writeSync(outfile, "# build: "+Date.now()+"\n");
    
    // Always just assume an array.
    if (args.CACHE) {
        fs.writeSync(outfile, "\n");
        fs.writeSync(outfile, "CACHE:\n");
        for (i = 0; i < args.CACHE.length; i++) {
            fs.writeSync(outfile, args.CACHE[i]+"\n");
        }
    }
    
    if (args.NETWORK) {
        fs.writeSync(outfile, "\n");
        fs.writeSync(outfile, "NETWORK:\n");
        for (i = 0; i < args.NETWORK.length; i++) {
            fs.writeSync(outfile, args.NETWORK[i]+"\n");
        }
    }

    if (args.FALLBACK) {
        fs.writeSync(outfile, "\n");
        fs.writeSync(outfile, "FALLBACK:\n");
        for (i = 0; i < args.FALLBACK.length; i++) {
            fs.writeSync(outfile, args.FALLBACK[i]+"\n");
        }
    }
    
    // Append a final line.
    fs.writeSync(outfile, "\n");
    // Cleanup and done.
    fs.closeSync(outfile);
}

// Export
exports.appcache = appcache;
