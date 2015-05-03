/*
 * Tests for the copy utility. 
 */

var fs = require('fs'),
	path = require('path'),
	assert = require('assert'),
	// Module to test
	copy = require('../src/copy.js').copy,
	// We naively assume that our test files will not collide with anything.
	getTempFileName = require('./util/randomdata.js').getTempFileName,
	writeTempFile = require('./util/randomdata.js').writeTempFile,
	outFileName = "copytempfile.out";

//------------------------------------------------------------- Tests

// Setup
(function() {
	console.log("Setting up the copy test.");
	console.log("");	
	console.log("NOTE: You will be notified, via traceback, of test errors.");
	console.log("No errors, no test failures.");
	console.log("");
	
})();


// Test
(function() {
	// one-to-one local file copy test
	
	// Build temporary test file
	writeTempFile(1);	
		
	copy({
	    from: getTempFileName(1),
	    to: outFileName
	});
	
	assert.equal(path.existsSync(outFileName), true,
		"One-to-one local file copy creates a file.");
	
	// Remove all files
	fs.unlinkSync(getTempFileName(1));
	fs.unlinkSync(outFileName);
})();

// Teardown
(function() {
	console.log("Tearing down the test.");
	
	console.log("Tests completed.");
	console.log("");
})();
