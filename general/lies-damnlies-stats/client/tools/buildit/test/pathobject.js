/*
 * Tests for the pathobject module. 
 */

var assert = require('assert'),
	// Module to test
	PathObject = require('../src/pathobject.js');



//------------------------------------------------------------- Tests

// Setup
(function() {
	console.log("Setting up the pathobject test.");
	console.log("");
	console.log("NOTE: You will be notified, via traceback, of test errors.");
	console.log("No errors, no test failures.");
	console.log("");
})();

//Test
(function() {
	// basename
	assert.equal(PathObject('dogs/cats/pigs.html').basename(), "pigs.html",
		"Filename should be returned.");
	assert.equal(PathObject('dogs/cats/pigs/').basename(), "pigs/",
		"Lowest level directory should be returned.");
})();

//Test
(function() {
	// dirname
	assert.equal(PathObject('dogs/cats/pigs.html').dirname(), "dogs/cats",
		"Correct dirname returned");
	assert.equal(PathObject('dogs/cats/pigs/').dirname(), "dogs/cats",
		"Correct dirname returned.");
})();


// Test
(function() {
	// inferFile
	assert.equal(PathObject('.').inferFile(), false,
		"Real directory should always return false.");

	assert.equal(PathObject('blahblah/').inferFile(), false,
		"Fake but implied directory should always return false.");
	assert.equal(PathObject('blahblah/   ').inferFile(), false,
		"Fake but implied directory should always return false.");
	assert.equal(PathObject('/   \n').inferFile(), false,
		"Fake but implied directory should always return false.");
	
	assert.equal(PathObject('blahblahb/blahblash').inferFile(), true,
		"No trailing slash on non-existent directory, inferred file.");
})();


(function() {
	// inferDirectory
	assert.equal(PathObject('.').inferDirectory(), true,
		"Real directory should always return true.");

	assert.equal(PathObject('blahblah/').inferDirectory(), true,
		"Fake but implied directory should always return true.");
	assert.equal(PathObject('blahblah/   ').inferDirectory(), true,
		"Fake but implied directory should always return true.");
	assert.equal(PathObject('/   \n').inferDirectory(), true,
		"Fake but implied directory should always return true.");
	
	assert.equal(PathObject('blahblahb/blahblash').inferDirectory(), false,
		"No trailing slash on non-existent directory, no inferred directory");
})();

// Teardown
(function() {
	console.log("Tests completed.");
	console.log("");
})();