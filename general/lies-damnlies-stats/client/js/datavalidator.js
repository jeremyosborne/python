(function(exports) {


/**
 * @class Collection of type validators.
 * @singleton
 */
var DataValidator = {
    /**
     * To pass the test, number must be: an integer, unsigned (0 or greater),
     * and not a string (must be a real (N)number type).
     * @param n {mixed} Object to test for integerness.
     * @return {Boolean} true if the input is an int according to our tests,
     * false if not.
     */
    "uint": function(n) {
        return (typeof n === 'number' || n instanceof Number) && 
            parseFloat(n) == parseInt(n, 10) && 
            isFinite(n) && 
            n >= 0;
    },
    /**
     * To pass the test, date must be: a string, and in the ISO Calendar Date
     * format of YYYY-MM-DD. 
     * (This code will break in about 8000 years ;) ).
     * @param d {mixed} Object to test for dateness.
     * @return {Boolean} true if the input passes our tests,
     * false if not.
     */
    "isocalendardate": function(d) {
        if (typeof d == "string" || d instanceof Date) {
            d = d.split("-")
            return d.length === 3 &&
                // Year validation
                d[0].length === 4 && 
                // Month validation (these are ISO months, not JavaScript months)
                d[1].length === 2 &&
                parseInt(d[1], 10) >= 1 &&
                parseInt(d[1], 10) <= 12 && 
                // Day validation... it's the server's job to validate the 
                // correctness of the date, we're just validating the format.
                d[2].length === 2 &&
                parseInt(d[2], 10) >= 1 &&
                parseInt(d[2], 10) <= 31;
        }
        // else, fail
        return false;
    },    
};
exports.DataValidator = DataValidator;


})(window);
