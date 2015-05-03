/*
 * Simple logging functions for this package.
 */

    // Log levels
    // Display all log messages.
var LOG_LEVEL_VERBOSE = 3,
    // No verbose messages.
    LOG_LEVEL_NORMAL = 2,
    // Only error messages.
    LOG_LEVEL_ERROR = 1,
    // No log messages displayed.
    LOG_LEVEL_QUIET = 0,
    // The current logging level.
    logLevel = LOG_LEVEL_NORMAL;

/**
 * Shorthand to console.log, throttled by the logging level.
 * @param msg {String} Message to display to standard out.
 */
function verbose(msg) {
    if (logLevel >= LOG_LEVEL_VERBOSE) {
        console.log(msg);
    }
}
/**
 * Shorthand to console.log, throttled by the logging level.
 * @param msg {String} Message to display to standard out.
 */
function log(msg) {
    if (logLevel >= LOG_LEVEL_NORMAL) {
        console.log(msg);
    }
}
/**
 * Shorthand to console.error, throttled by the logging level.
 * @param msg {String} Message to display to standard error.
 */
function error(msg) {
    if (logLevel >= LOG_LEVEL_ERROR) {
        console.error(msg);
    }
}

/**
 * Silence log messages.
 */
function mute() {
    logLevel = LOG_LEVEL_QUIET;
}

/**
 * Maximum log message volume.
 */
function maxvolume() {
    logLevel = LOG_LEVEL_VERBOSE;
}

// Exports.
module.exports.verbose = verbose;
module.exports.log = log;
module.exports.error = error;
module.exports.mute = mute;
module.exports.maxvolume = maxvolume;
// Logging level export.
module.exports.LOG_LEVEL_VERBOSE = LOG_LEVEL_VERBOSE;
module.exports.LOG_LEVEL_NORMAL = LOG_LEVEL_NORMAL;
module.exports.LOG_LEVEL_ERROR = LOG_LEVEL_ERROR;
module.exports.LOG_LEVEL_QUIET = LOG_LEVEL_QUIET;
