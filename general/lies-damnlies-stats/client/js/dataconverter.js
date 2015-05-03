(function(exports) {


/**
 * @class Aids in data conversion in from server web API friendly to
 * application friendly formats.
 * @singleton
 */
var DataConverter = {
    /**
     * Returns the default value of a uint is 0.
     * @return {Number} The default value of a uint is 0.
     */
    "defaultuint": function() {
        return 0;
    },
    /**
     * Convert to an unsigned integer that is appropriate for delivering
     * back to the server.
     * @param n {mixed} Object to convert to an unsigned integer.
     * @return {Number|Undefined} Returns a number if the input was valid,
     * or undefined if the conversion could not be made.
     */
    "touint": function(n) {
        n = parseInt(n, 10);
        return (n >= 0 && isFinite(n) && 
            (parseFloat(n) == parseInt(n, 10)) &&
            parseFloat(n) == parseInt(n, 10)) ? n : undefined;
    },
    /**
     * Convert from an unsigned integer.
     * @param n {Number} An unsigned integer.
     * @return {Number} Returns a number.
     */
    "fromuint": function(n) {
        // This is purely an interface function.
        // We assume it's a valid number already, but we'll at least do
        // a cursory parseInt.
        return parseInt(n, 10);
    },
    /**
     * Returns the default value of an ISO Calendar Date
     * @return {String|Undefined} Returns a string format ISO Calendar Date.
     */
    "defaultisocalendardate": function() {
        return ExtendedDate().toISOCalendarDate();
    },
    /**
     * Converts an ExtendedDate to an ISO Calendar Date suitable for being
     * delivered back to the server.
     * @param d {Date|ExtendedDate} A date object. NOTE: passing a plain date
     * object into this function will convert it to an ExtendedDate. You have
     * been warned (and it's assumed that all dates floating around this app
     * are ExtendedDates).
     * @return {String|Undefined} Returns a string format ISO Calendar Date
     * or undefined if the conversion could not be made.
     */
    "toisocalendardate": function(d) {
        try {
            if (d instanceof Date && !d.toISOCalendarDate) {
                // Convert.
                d = ExtendedDate(d)
            }
            // We expect ExtendedDate types by default.
            return d.toISOCalendarDate();
        } catch(e) {
            return undefined;
        }
    },
    
    /**
     * Converts from an ISO Calendar Date to an ExtendedDate type.
     * @param d {String} An ISO Calendar Date in string form.
     * @return {ExtendedDate|Undefined} An extended date produced from the 
     * ISO calendar date, or undefined if the conversion could not be made. 
     */
    "fromisocalendardate": function(d) {
        try {
            // We assume the ISO Calendar Date is already in good form.
            d = d.split("-");
            // Construct the date based on the parts
            // and set the time to noon to workaround potential and annoying 
            // daylight savings time boundary problems when doing date arithmetic.
            d = new Date(parseInt(d[0], 10),
                // JavaScript months are counted 0 - 11, don't ask me why.
                parseInt(d[1], 10) - 1,
                parseInt(d[2], 10),
                12,
                0,
                0,
                0
            );
            return ExtendedDate(d);
        } catch(e) {
            return undefined;
        }
    },
};
exports.DataConverter = DataConverter;


})(window);
