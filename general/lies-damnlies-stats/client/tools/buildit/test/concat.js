/*
 * Tests for the concat utility.
 */

var fs = require('fs'),
    path = require('path'),
    assert = require('assert'),
    // Module to test
    concat = require('../src/concat.js').concat,
    // We'll assume that our target file will not collide with anything else
    // in the directory.
    getTempFileName = require('./util/randomdata.js').getTempFileName,
    writeTempFile = require('./util/randomdata.js').writeTempFile,
    concatOutFileName = "concattempfile.out";

//------------------------------------------------------------- Tests

// Setup
(function() {
    console.log("Setting up the concat test.");
    console.log("");

    console.log("NOTE: You will be notified, via traceback, of test errors.");
    console.log("No errors, no test failures.");
    console.log("");

    // Build our temporary files
    writeTempFile(1);
    writeTempFile(2);

    // Concatenate the files together
    concat({
        infiles: [
            getTempFileName(1),
            getTempFileName(2)
        ],
        outfile: concatOutFileName
    });
})();

// Test 1
(function() {
    // File size check
    var originalFileSize = fs.statSync(getTempFileName(1)).size
            + fs.statSync(getTempFileName(2)).size,
        outFileSize = fs.statSync(concatOutFileName).size;

    assert.equal(outFileSize, originalFileSize,
        "Concat is the same size as all of the input files.");
})();

// Test 2
(function() {
    // Build our temporary files
    writeTempFile(3);
    writeTempFile(4);

    // Concatenate files together in a directory that doesn't yet exist
    concat({
        infiles: [
            getTempFileName(3),
            getTempFileName(4)
        ],
        outfile: path.join("TESTESTE", concatOutFileName)
    });

    assert.equal(path.existsSync(path.join("TESTESTE", concatOutFileName)),
        true,
        "Concat created a file in a directory that didn't yet exist.");

    // Remove all test files
    fs.unlinkSync(getTempFileName(3));
    fs.unlinkSync(getTempFileName(4));
    fs.unlinkSync(path.join("TESTESTE", concatOutFileName));
    fs.rmdirSync("TESTESTE");
})();


// Teardown
(function() {
    console.log("Tearing down the concat test.");

    // Remove all files
    fs.unlinkSync(getTempFileName(1));
    fs.unlinkSync(getTempFileName(2));
    fs.unlinkSync(concatOutFileName);

})();
