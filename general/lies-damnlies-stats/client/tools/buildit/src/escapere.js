/*
 * The only purpose of this module is to provide a function that can be used
 * to escape regular expressions.
 * 
 * This function was found on:
 * http://80.68.89.23/2006/Jan/20/escape/
 * 
 * and all credit appears to go to Colin Snover,  of which the aove web page
 * points to:
 * http://zetafleet.com/blog
 */

/**
 * Take a string and return a string that is escaped in a way as to allow
 * correct passing in to a call to new RegExp(text).
 * @param text {String} The text we wish to escape for use with a regular
 * expression.
 */
module.exports = function(text) {
    return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
};
