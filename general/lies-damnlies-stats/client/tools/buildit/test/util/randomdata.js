/*
 * Helper code used to produce random test data.
 */

var fs = require('fs'),
    path = require('path'),
    //
    // module vars
    // We'll assume this won't collide with anything else in the directory.
    tempFileNameTemplate = "concattempfile."+new Date().getTime()+".{{NUM}}.txt",
    // TODO: Get this information from a config file.
    defaultEncoding = "utf8";


/**
 * Produce a random line of text, appended with a newline.
 */
function randomLine() {
        // Total line length _not_ including the newline.
    var lineLength = 79,
        charsToChooseFrom = "abcdefghijklmnopqrstuvwxyz 0123456789",
        numCharsToChooseFrom = charsToChooseFrom.length,
        line = "",
        i;

    for (i = 0; i < lineLength; i++) {
        line += charsToChooseFrom[Math.floor(Math.random() * numCharsToChooseFrom)];
    }

    return line;
}

/**
 * Gets the name of a tempfile by number.
 * @param num {Number} The number of the tempfile.
 * @param [path="."] {String} Directory path in which we should place the
 * temp file. The path will be joined to the temp file name via a call
 * to path.join().
 */
function getTempFileName(num, p) {
    p = p || ".";
    return path.join(p, tempFileNameTemplate.replace("{{NUM}}", num));
}

/**
 * Writes a temporary file to disk, using the module specified file name
 * template and a random line generator.
 * @param num {Number} The number of the tempfile to write.
 * @param [p="."] {String} Directory path in which we should place the
 * temp file. The path will be joined to the temp file name via a call
 * to path.join().
 */
function writeTempFile(num, p) {
    var outfilePath = getTempFileName(num, p),
    	outfile = fs.openSync(outfilePath, "w"),
    	// Numlines is arbitrary
    	numLines = 80,
    	i;

    console.log("Writing a temporary file to: " +outfilePath);

    for (i = 0; i < numLines; i++) {
        fs.writeSync(outfile, randomLine(), null, defaultEncoding);
    }

    fs.closeSync(outfile);
}

// Export
exports.getTempFileName = getTempFileName;
exports.writeTempFile = writeTempFile;
