/*
 * Tests for the logger module. 
 */

var logger = require('../src/logger.js');



//------------------------------------------------------------- Tests

// Setup
(function() {
	console.log("Setting up the logger test.");
	console.log("");
	console.log("NOTE: This is a visual test only. There are no asserts.");
	console.log("");
})();

//Test
(function() {
    console.log("BEGIN TEST: normal logging. Error messages are obvious.");
    logger.verbose("TEST FAIL: Should not see this.");
    logger.log("TEST PASS: Should see this.");
    logger.error("TEST PASS: Should see this.");
    console.log("END TEST: Should have seen 2 'TEST PASS' statements.");
    console.log("---");
})();

//Test
(function() {
    console.log("BEGIN TEST: maxvolume logging. Error messages are obvious.");
    // Turn on verbose logging
    logger.maxvolume();
    logger.verbose("TEST PASS: Should see this.");
    logger.log("TEST PASS: Should see this.");
    logger.error("TEST PASS: Should see this.");    
    console.log("END TEST: Should have seen 3 'TEST PASS' statements.");
    console.log("---");
})();


//Test
(function() {
    console.log("BEGIN TEST: mute logging. Error messages are obvious.");
    // Turn on verbose logging
    logger.mute();
    logger.verbose("TEST FAIL: Should not see this.");
    logger.log("TEST FAIL: Should not see this.");
    logger.error("TEST FAIL: Should not see this.");    
    console.log("END TEST: Should have seen 0 'TEST PASS' statements.");
    console.log("---");
})();


// End
(function() {
    console.log("TESTS COMPLETE!")
})();
