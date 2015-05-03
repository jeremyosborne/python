(function(exports) {



/**
 * Various configuration settings for the client.
 * @name ldlsConf
 */
exports.ldlsConf = {
    /**
     * Selector to find the header of the page.
     */
    "pageHeaderSelector": "#app-header",
    /**
     * Selector to find the body of the page.
     */
    "pageBodySelector": "#app-body",
    /**
     * Selector to find the footer of the page.
     */
    "pageFooterSelector": "#app-footer",
    /**
     * URL to get a statistics data from.
     * @type {String}
     */
    "getURL": "/api/stats/get/",
    /**
     * URL to create new, or update existing stats.
     * @type {String}
     */
    "saveURL": "/api/stats/save/",
    /**
     * URL to delete existing stats. 
     * @type {String}
     */
    "deleteURL": "/api/stats/delete/",
    /**
     * URL to retrieve the list of, and data model descriptions, of stats
     * supported by the server.
     */
    "describeURL": "/api/stats/describe",
    /**
     * URL to login.
     * @type {String}
     */
    "authLoginURL": "/api/auth/login",
    /**
     * URL to logout.
     * @type {String}
     */
    "authLogoutURL": "/api/auth/logout",
    /**
     * URL to test current login status, and if logged in provide basic
     * information about the logged in user.
     * @type {String}
     */
    "authInfoURL": "/api/auth/info",
};



})(window);
