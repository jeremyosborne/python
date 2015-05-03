buildit
node.js based build tools for projects



TODO
====
* Regular expression include or exclude option for the copy command.



SETUP
=====
Assuming buildit is located in your node_modules directory, your build script
will contain something like the following:

    // Build appcache files (HTML5 manifests).
var appcache = require('buildit').appcache,
    // Used to precompile templates.
    compileTemplates = require('buildit').compileTemplates,
    // uglify.js your files, and place a trailing semicolon on the results.
    compress = require('buildit').compress,
    // Concatenate multiple files together.
    concat = require('buildit').concat,
    // Copy file(s) from spot A to spot B.
    copy = require('buildit').copy,
    // Make a directory, as well as any intermediate directories.
    mkdir = require('buildit').mkdir,
    // Remove an entire path, subpaths, and files.
    rmrf = require('buildit').rmrf,
    // Build documentation.
    docit = require('buildit').docit,
    // Get access to logging functions.
    logger = require('buildit).logger;



LIBRARY NOTES
=============
* Steps to building ember_template_builder.js
    * Grab the file at: 
        https://github.com/emberjs/ember.js/blob/master/packages/handlebars/lib/main.js
    * Remove the window.Handlebars = Handlebars; reference.
    * Add the contents of the following file:
        https://github.com/emberjs/ember.js/blob/master/packages/ember-handlebars/lib/ext.js
    * Change the "Ember.create" function calls to "Object.create".
