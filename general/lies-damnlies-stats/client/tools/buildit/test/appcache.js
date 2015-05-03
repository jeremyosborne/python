/*
 * Tests for the appcache module. 
 */

var appcache = require('../src/appcache.js').appcache;



//------------------------------------------------------------- Tests

// Setup
(function() {
	console.log("Setting up the appcache test.");
	console.log("");
	console.log("NOTE: This is a visual test only. There are no asserts.");
	console.log("");
})();

//Test
(function() {
    appcache({
        outfile: "./test.appcache",
        CACHE: [
            "test.html",
            "invis.gif",
        ],
        NETWORK: [
            "http://awesome.com",
            "/api/",
        ],
        FALLBACK: [
            "/api/fail test.html",
        ],
    });
})();

// End
(function() {
    console.log("TESTS COMPLETE!");
    console.log("Please check the local directory and see if the file");
    console.log("contains three sections and a build number.");
})();
