/*
 * Utility to compress a JavaScript file.
 */

var fs = require('fs'),
    jsp = require("../lib/uglify-js").parser,
	pro = require("../lib/uglify-js").uglify,
    // Default file encoding
    // TODO: Move to a configuration file.
    defaultEncoding = "utf8",
	// Simple semi-colon check.
	checkForFinalSemicolon = /;$/;

/**
 * Compresses a JavaScript file.
 * @param args {Object} Associative array of arguments. 
 * @param args.from {String} Path to the file that we will compress.
 * @param [args.to] {String} Path to the output file. If ommitted, the
 * compressed code will overwrite the from file. 
 */
function compress(args) {
    var orig_code = fs.readFileSync(args.from, defaultEncoding),
        // BEGIN uglify process.
        // parse code and get the initial AST
        ast = jsp.parse(orig_code),
        // get a new AST with mangled names
        mangled_ast = pro.ast_mangle(ast),
        // get an AST with compression optimizations
        squeezed_ast = pro.ast_squeeze(mangled_ast), 
        // compressed code here
        final_code = pro.gen_code(squeezed_ast),
        // END uglify process
        outfile;

    // Uglify doesn't add a final semicolon by default.
    if (!checkForFinalSemicolon.test(final_code)) {
        final_code += ";";
    }
    
    // Our outfile is either the same file or the to file.
    outfile = fs.openSync(args.to || args.from, "w");
    fs.writeSync(outfile, final_code, null, defaultEncoding);
    fs.closeSync(outfile);
}

// Export
exports.compress = compress;

// TEST
//compress({
//    from: "templates.js"
//});
