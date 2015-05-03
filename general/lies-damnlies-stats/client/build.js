/*
 * nodejs buildit based script.
 *
 * Usage:
 * node build.js [target]
 *
 * Where:
 * target {String} The name of the build type to run. Valid targets are:
 *     "dev" (unmimified code)
 *     "docs" (build developer_docs)
 *     "dist" (build minified code and copy to the dist folder)
 * 
 * A release (minified) build is assumed when no target is passed.
 */

// Use the local version of the buildit module.
module.paths.unshift("./tools/buildit");

    // Build tools
var appcache = require('buildit').appcache,
    compileTemplates = require('buildit').compileTemplates,
    compress = require('buildit').compress,
    concat = require('buildit').concat,
    copy = require('buildit').copy,
    mkdir = require('buildit').mkdir,
    rmrf = require('buildit').rmrf,
    docit = require('buildit').docit,
    path = require('path');


    // Location for temporary build output.
var tmpdir = "build_tmp/",
    // Main output path.
    outdir = "build/",
    // Header information, to be prefixed to the source file post-minification.
    headerSrc = [
        "js/credits.js",
    ],
    // Templates
    templateFromPath = "templates/",
    templateLibPath = tmpdir+"ldls_templates.js",
    // Application code source files.
    appSrc = [
        // External libraries
        "lib/jquery/jquery.js",
        "lib/emberjs/ember.js",
        "lib/mymoms/extendeddate.js",
        // Zero intra-app dependencies.
        "js/string.js",
        "js/handlebar_helpers.js",
        "js/conf.js",
        "js/loc.js",
        "js/loggermixin.js",
        "js/notifications.js",
        "js/datavalidator.js",
        "js/dataconverter.js",
        "js/userinput_number.js",
        "js/userinput_calendardate.js",
        // Code with intra-app dependencies.
        "js/statdescription.js",
        "js/notificationsmixin.js",
        "js/datacache.js",
        "js/appcache.js",
        "js/pageheader.js",
        "js/pagebody.js",
        "js/pagefooter.js",
        "js/footermenu.js",
        "js/login.js",
        "js/stat.js",
        "js/statscache.js",
        "js/statschooserview.js",
        "js/statentry.js",
        "js/summary.js",
        "js/weeklysummary.js",
        "js/dailysummary.js",
        "js/statemanager.js",
        "js/app.js",
        // Templates are generated during the build, defined above.
        templateLibPath,
    ],
    // Temporary output library (pre-addition of credits).
    appTmpLibPath = tmpdir + "ldls.js",
    // Final application code output library.
    appLibPath = outdir + "ldls.js",
    // Images
    imgFromPath = "img/",
    imgToPath = outdir + "img/",
    // Html path
    htmlFromPath = "html/",
    // Stylesheets to concatenate together.
    appStyleSheets = [
        "css/blackonwhite.css",
    ],
    // Output for concatenated CSS.
    appCSSPath = outdir + "ldls.css",
    // Directory for distribution
    distdir = "dist/",
    // Files required for the appcache/manifest.
    appcacheArgs = {
        // Path to the manifest file.
        outfile: outdir + "ldls.manifest",
        // Fill in the various sections of the file.
        CACHE: [
            "ldls.css",
            "ldls.js",
            "img/touch-icon-57x57.png",
            "img/touch-icon-72x72.png",
            "img/touch-icon-114x114.png",
        ],
        NETWORK: [
            "/api/"
        ],
        // No fallback section (yet).
        //FALLBACK: [],
    };

if (process.argv[2] != "docs") {
    // Build necessary directories.
    mkdir(tmpdir);
    mkdir(outdir);
    
    // Build the appcache/manifest file.
    appcache(appcacheArgs);
    
    // Copy over html.
    copy({
        from: htmlFromPath,
        to: outdir,
    });

    // Copy over images.
    copy({
        from: imgFromPath,
        to: imgToPath,
    });
        
    // Build the templates.
    compileTemplates({
        from: templateFromPath,
        to: templateLibPath,
        compileType: "emberhandlebars",
        // This namespace is dependent on ember.
        templateVarName: "Ember.TEMPLATES",
        trim: true,
    });
    
    // Build the libraries
    concat({
        infiles: appSrc,
        outfile: appTmpLibPath,
    });
    // Minify the libraries.
    if (process.argv[2] != "dev") {
        compress({
            from: appTmpLibPath
        });
    }
    
    // Prefix the credits to the library.
    concat({
        infiles: headerSrc.concat([appTmpLibPath]),
        outfile: appLibPath,
    });
    
    // Package up the CSS
    concat({
        infiles: appStyleSheets,
        outfile: appCSSPath,
    });
    
    // Push the code to the dist folder.
    if (process.argv[2] == "dist") {
        copy({
            from: outdir,
            to: distdir,
        });
    }
    // Cleanup
    rmrf(tmpdir);
}
else if (process.argv[2] == "docs") {
    docit({
        from: path.resolve("./js/"),
        to: path.resolve("./developer_docs/"),
    });
}
