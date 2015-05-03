/*
 * A helper for paths.
 */

var fs = require('fs'),
	path = require('path'),
	escapere = require('./escapere.js');

/**
 * Builds helper methods around a path string.
 * Designed to provide synchronous interaction with the file system. 
 */
function PathObject(path) {
	/**
	 * The string path.
	 * @property String
	 */
	this.path = path;
}

/**
 * Return the basename of the path, equvalent to the node module
 * path.basename call.
 * @return {String} The basename of the path, which equates to the file name
 * or the lowest level directory.
 */
PathObject.prototype.basename = function() {
	return path.basename(this.path);
};

/**
 * Return the dirname of the path, equvalent to the node module
 * path.dirname call.
 * @return {String} The dirname of the path.
 */
PathObject.prototype.dirname = function() {
	return path.dirname(this.path);
};

/**
 * Does this path exist?
 * @return {Boolean} True if the path leads to something that can be detected
 * to exist, false if not.
 */
PathObject.prototype.exists = function() {
	return path.existsSync(this.path);
};

/**
 * Is this path a file?
 * @return {Boolean} True if a file, false if not.
 */
PathObject.prototype.isFile = function() {
	return this.exists() && fs.statSync(this.path).isFile();
};

/**
 * Infers, according to blatent presence of a trailing slash or previous
 * existence, whether this path is a file or not.
 * @return {Boolean} True if an inferred file, false if not.
 */
PathObject.prototype.inferFile = function() {
	if (this.exists()) {
		return this.isFile();
	}
	else {
		// We're the inverse of isDirectory.
		return !(/\/[\W]*$/.test(this.path));
	}
};

/**
 * Is this path a directory?
 * @return {Boolean} True if a directory, false if not.
 */
PathObject.prototype.isDirectory = function() {
	return this.exists() && fs.statSync(this.path).isDirectory();
};

/**
 * Infers, according to blatent presence of a trailing slash or previous
 * existence, whether this path is a directory or not.
 * @return {Boolean} True if an inferred directory, false if not.
 */
PathObject.prototype.inferDirectory = function() {
	if (this.exists()) {
		return this.isDirectory();
	}
	else {
		// Trailing slash at the end of a line is the only inferred directory
		return /\/[\W]*$/.test(this.path);
	}
};

/**
 * If this path is a directory, takes the given path and returns the
 * path.join results with this.path.
 * @param p {String} The path to attempt to join with this.path.
 * @return {String} The joined path.
 * @throw {Error} Throws an error if we are trying to resolve any path
 * if this.path is anything other than a directory.
 */
PathObject.prototype.join = function(p) {
	if (!this.isDirectory()) {
		throw new Error("ERROR: Attempting to join "+path+" with a path that"+
			" is not a directory.");	
	}
	return path.join(this.path, p);
};

/**
 * Recursively builds and returns a list of files contained in this path, 
 * if this path is a directory.
 * 
 * @return {String[]} List of file paths as relative path references from
 * within this directory. If there are no files, or this.path points to
 * something that is not a directory, an empty array is returned.
 */
PathObject.prototype.descendentFilePaths = function() {
	// On the first call through, we capture the base directory to help us
	// form build a list of paths that don't include anything but the most
	// necessary path information.
    var relativeDir = this.path,
    	// Recursively do the work and return all results when done.
    	files = [];
    
    // Can only have descendant files if we are a directory.
    if (this.isDirectory()) {
    	// Start with this path and recurse until we get a list of all the
    	// files within the path.
        files = (function(cwd) {
	    		// readdirSync only returns the immediate content names within
	    		// a directory path. We have to figure out whether those names
	    		// are directories, files, or whatnot, and handle the paths
	    		// appropriately.
		    var items = fs.readdirSync(cwd),
			    nextPath,
			    files = [],
			    i;
		    
			for (i = 0; i < items.length; i++) {
			    nextPath = path.join(cwd, items[i]);
			    
			    if (fs.statSync(nextPath).isDirectory()) {
			    	// Recurse into directories
			        files = files.concat(arguments.callee.call(null, nextPath));
			    }
			    else if (fs.statSync(nextPath).isFile()){
			        // only the relative files get added to the copy list
			        files.push(nextPath.replace(new RegExp("^"+escapere(relativeDir)), ""));
			    }
			}
			
			return files;
	    })(relativeDir);	
    }
    
    // Always return an array.
    return files || [];
};

/**
 * Recursively builds and returns a list of directories contained in this path, 
 * if this path is a directory.
 * 
 * @return {String[]} List of directory paths as relative path references from
 * within this directory. If there are no directories, or this.path points to
 * something that is not a directory, an empty array is returned.
 */
PathObject.prototype.descendentDirectoryPaths = function() {
	// On the first call through, we capture the base directory to help us
	// form build a list of paths that don't include anything but the most
	// necessary path information.
    var relativeDir = this.path,
    	// Recursively do the work and return all results when done.
    	dirs = [];
    
    // Can only have descendant dirs if we are a directory.
    if (this.isDirectory()) {
    	// Start with this path and recurse until we get a list of all the
    	// directories within the path.
    	dirs = (function(cwd) {
	    		// readdirSync only returns the immediate content names within
	    		// a directory path. We have to figure out whether those names
	    		// are directories, files, or whatnot, and handle the paths
	    		// appropriately.
		    var items = fs.readdirSync(cwd),
			    nextPath,
			    dirs = [],
			    i;
		    
			for (i = 0; i < items.length; i++) {
			    nextPath = path.join(cwd, items[i]);
			    			    
			    if (fs.statSync(nextPath).isDirectory()) {
			    	// Recurse into directories
			        dirs = dirs.concat(arguments.callee.call(null, nextPath));
			        // We only want directories, and then only the relative
			        // paths of the directories.
			        dirs.push(nextPath.replace(new RegExp("^"+escapere(relativeDir)), ""));
			    }
			}
			
			return dirs;
	    })(relativeDir);	
    }
    
    // Always return an array.
    return dirs || [];
};

// Export constructor/factory function as module.
module.exports = function(path) {
	return new PathObject(path);
};
