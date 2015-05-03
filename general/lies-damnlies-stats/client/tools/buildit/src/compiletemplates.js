/*
 * Module used to compile templates and output JavaScript template functions.
 */

var fs = require('fs'),
    path = require('path'),
    pathobject = require('./pathobject.js'),
    _ = require('../lib/underscore.js')._,
    Ember = require('../lib/ember_template_builder.js').Ember,
    // Default file encoding.
    defaultEncoding = "utf8";

/**
 * Generates the template var assignment prefix, something like:
 * "window.TEMPLATE.myTemplate = "
 *
 * @param templateName {String} The function that will
 * @param args {Object} Associative array of arguments.
 * @param args.templateVarName {String} The name of the variable that all templates
 * will be attached to.
 * @param args.globalVarName {String} The name of the global variable
 * for our JavaScript context.
 * @return {String} The template function prefix.
 */
function generateTemplateAssignmentPrefix(templateName, args) {
    // Square brackets in case we get funky names.
    return args.globalVarName+"."+args.templateVarName+"['"+templateName+"'] = ";
}

/**
 * Template to place at the top of the file.
 * @param args {Object} Associative array of arguments.
 * @param args.templateVarName {String} The name of the variable that all templates
 * will be attached to.
 * @param args.globalVarName {String} The name of the global variable
 * for our JavaScript context.
 * @return {String} Header for the template output file.
 */
function generateOutputFileHeader(args) {
    var header = ""
        + "/*\n"
        + " * Templates compiled on: " + new Date().toString() + "\n"
        + " */\n"
        + "\n"
        + "if (!{{globalVarName}}.{{templateVarName}}) {\n"
        + "    {{globalVarName}}.{{templateVarName}} = {};\n"
        + "}\n"
        + "\n";

    // Modify the underscore template settings to work with moustache-like
    // templates.
    _.templateSettings = {
        interpolate: /\{\{([^=].+?[^=])\}\}/g,
        evaluate: /\{\{=(.+?)=\}\}/g
    };

    return _.template(header, args);
}

/**
 * Functions used to clean (preprocess) a template string prior to sending
 * it to a processor.
 */
var cleaners = {
    /**
     * Remove extraneous html content.
     * Currently removes:
     * HTML comments.
     *
     * @param str {String} A template string.
     * @return {String} The cleaned template string.
     */
    html: function(str) {
        var reHtmlComments = /\<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)\>/g;

        // All we're doing is removing HTML comments for now.
        return str.replace(reHtmlComments, "");
    },
    /**
     * Remove unnecessary white space on the html content.
     * @param str {String} A template string.
     * @return {String} The cleaned template string.
     */
    htmlWhitespace: function(str) {
        return str.replace(/^\s+/, "").replace(/\s+$/, "").replace(/\>\s+\</g, "><");
    },
    /**
     * Remove "function anonymous" references from toString'd functions.
     * @param str {String} A template string.
     * @return {String} The cleaned template string.
     */
    anonFunc: function(str) {
          return str.replace(/^function anonymous\(/, "function(");
    },
};

/**
 * Collection of template processors.
 */
var processors = {
    /**
     * Compile a template using the underscore template engine, modified to
     * use moustache-like tokens.
     *
     * Interpolation (data-dereferencing) happens via the {{...}} markup,
     * where "..." denotes data references.
     *
     * Evaluation of javascript code happens via the {{=...=}} markup,
     * where "..." denotes the code to evaluate.
     *
     * See http://documentcloud.github.com/underscore/#template for
     * more information.
     *
     * @param str {String} Raw template string.
     * @param trim {Boolean} If true, preceeding, trailing, and any whitespace
     * between elements that does not represent content will be removed from
     * the template before processing.
     * @return {String} The compiled, functional template as a string.
     */
    underscorestache: function(str, trim) {
        // Modify the underscore template settings to work with moustache-like
        // templates.
        _.templateSettings = {
            interpolate: /\{\{([^=].+?[^=])\}\}/g,
            evaluate: /\{\{=(.+?)=\}\}/g
        };

        // Clean
        str = cleaners.html(str);

        if (trim) {
            str = cleaners.htmlWhitespace(str);
        }

        // Compile the template and return as a serialized string.
        return cleaners.anonFunc(_.template(str).toString());
    },
    /**
     * Compile a template using the emberjs version of Handlebars.
     *
     * See http://emberjs.com for more information.
     *
     * @param str {String} Raw template string.
     * @param trim {Boolean} If true, preceeding, trailing, and any whitespace
     * between elements that does not represent content will be removed from
     * the template before processing.
     * @return {String} The compiled, functional template as a string.
     */
    emberhandlebars: function(str, trim) {
        // Clean
        str = cleaners.html(str);

        if (trim) {
            str = cleaners.htmlWhitespace(str);
        }

        // Compile the template and return as a serialized string.
        // Ember templates are weird as of version 0.9.4. We need to take
        // the results of precompile, which is itself the parser function, 
        // and register it with the Handlebars.template instance once the
        // ember code has loaded.
        return "Handlebars.template("+
                cleaners.anonFunc(Ember.Handlebars.precompile(str).toString())+
                ");";
    },
};


/**
 * Reads template files in, cleans them of any extraneous content, and
 * outputs the compiled template(s) to a file.
 *
 * @param args {Object} Associative array of arguments.
 * @param args.from {String} Path to the templates. If path is a directory,
 * all ".template" files within the directory will be processed. If path
 * is a file, only the file will be processed.
 * @param args.to {String} The name of the file in which all input
 * templates will be output.
 * @param [args.appendToFile=false] {Boolean} By default, the templates will
 * not be appended to the output file. If this is set to true, the compiler
 * will attempt to append the contents to the output file.
 * @param [args.compileType="underscorestache"] {String} The name of the
 * template processor. Valid values: "underscorestache", "emberhandlebars".
 * @param [args.templateVarName="TEMPLATE"] {String} The name of the global
 * object that each template function will be attached to.
 * @param [args.trim=false] {Boolean} Remove preceeding and trailing
 * newlines in the template. The way whitespace is removed depends on the
 * type of template processor.
 */
function compileTemplates(args) {
    var from = pathobject(args.from),
        to,
        processor = processors[args.compileType || "underscorestache"],
        fileOutFlag = (args.appendToFile) ? "a" : "w",
        // Temp variable
        fileContents,
        // List of directory contents for when we're dealing with a directory
        // of templates
        directoryContents,
        // List of template file paths
        templateFilePaths = [],
        // Giant strings of processed templates
        templates = "",
        // The name of the current template
        templateName,
        // Used to identify and remove the .template suffix
        templateSuffix = /\.template$/,
        i;

    // Normalize values.
    // We pass the args object around, clean it up.
    args.templateVarName = args.templateVarName || "TEMPLATE",
    args.globalVarName = args.globalVarName || "window";

    // Figure out how many files we need to deal with.
    if (from.isFile()) {
        //console.log('from is a file');
        templateFilePaths[0] = from.path;
    }
    else if (from.isDirectory()) {
        //console.log("from is a directory");
        directoryContents = from.descendentFilePaths();
        // Build our list of file paths, but only if they're templates
        for (i = 0; i < directoryContents.length; i++) {
            if (templateSuffix.test(directoryContents[i])) {
                templateFilePaths.push(from.join(directoryContents[i]));
            }
        }
    }
    else {
        console.log("from is not anything we can use.");
        throw new Error("ERROR: unusuable from path: " + from.path);
    }

    // Read the file(s) in and process each template.
    for (i = 0; i < templateFilePaths.length; i++) {
        fileContents = fs.readFileSync(templateFilePaths[i], defaultEncoding);
        templateName = path.basename(templateFilePaths[i]).replace(templateSuffix, "");
        // Process each template and attach to the global variable.
        templates += generateTemplateAssignmentPrefix(templateName, args)
            + processor(fileContents, args.trim)
            // Prevents processing errors since the template is formed via
            // an assignment, and we're (likely) concatenating lots of templates
            // together.
            + ";";
    }

    // Output the information.
    to = fs.openSync(args.to, fileOutFlag);
    // Add the header to the file.
    fs.writeSync(to, generateOutputFileHeader(args), null, defaultEncoding);
    // Write all of the templates to the output file
    fs.writeSync(to, templates, null, defaultEncoding);
    fs.closeSync(to);
}

// Exports
exports.compileTemplates = compileTemplates;

// TEST
//compileTemplates({
//    from: "test.template",
//    to: "templates.js",
//    appendToFile: true,
//    compileType: "underscorestache",
//    templateVarName: "Templates"
//});
