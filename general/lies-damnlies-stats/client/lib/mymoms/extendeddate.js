/**
 * @fileoverview Methods and factory used to extend the native Date objects or
 * the native Date prototype.
 *
 * @author Jeremy Osborne, jeremywosborne at gmail dot com
 */
(function(){

        // As defined by the ECMAScript Standard
    var MS_PER_DAY = 86400000,
        MS_PER_WEEK = MS_PER_DAY * 7,
        MAX_WEEK_DAY = 6;

    //--------------------------------------------------------------------------
    
    /**
     * @class Extend a native Date object.
     * @example
     * // Generate a new extended date object (factory).
     * var d = ExtendedDate();
     * // Extend a pre-existing date object (extend instance).
     * var d2 = ExtendedDate(new Date());
     * // Extend the native Date prototype (extend prototype).
     * ExtendedDate(Date.prototype);
     * @name ExtendedDate
     * @static
     * @param [d] {Date} Extend a pre-existing date object. If not passed in,
     * a new Date() is created (time of now).
     * @return {ExtendedDate} Returns the extended date object.
     */
    var ExtendedDate = function(d) {
        d = d || new Date();

        // Extend the date object
        d.copy = copy;

        d.monthStartDay = monthStartDay;
        d.monthEndDay = monthEndDay;
        d.monthEndDate = monthEndDate;        
        d.monthDecrement = monthDecrement;
        d.monthIncrement = monthIncrement;

        d.weekStartDate = weekStartDate;
        d.weekEndDate = weekEndDate;
        d.weekDecrement = weekDecrement;
        d.weekIncrement = weekIncrement;
        d.isWithinWeek = isWithinWeek;
        
        d.dayDecrement = dayDecrement;
        d.dayIncrement = dayIncrement;

        d.isSameCalendarDate = isSameCalendarDate;
                
        d.toISOCalendarDate = toISOCalendarDate;

        return d;
    };

    /**
     * Tests to see if the passed in operand is the same calendar date as
     * self, ignoring any time component less significant than days.
     * Only year, month, and day are checked.
     * @param other {Date} Date to test.
     * @return {Boolean} True if the calendar dates are the same, false if not.
     */
    var isSameCalendarDate = function(other) {
        var self = this;
        
        return self.getFullYear() === other.getFullYear() &&
            self.getMonth() === other.getMonth() &&
            self.getDate() === other.getDate();
    };

    /**
     * Returns the date in the ISO 8601 calendar date extended format:
     * YYYY-MM-DD
     * @return {String} Calendar date extended format for this date.
     */
    var toISOCalendarDate = function() {
        var now = this,
            month = now.getMonth()+1,
            day = now.getDate();
        
        month = (month < 10) ? "0"+month : month;
        day = (day < 10) ? "0"+day : day;        
        
        return now.getFullYear() + "-" + month + "-" + day;
    };

    /**
     * Return a clone (different instance, same date) of this object.
     * @return {ExtendedDate} Clone of this date.
     */
    var copy = function() {
        return ExtendedDate(new Date(this.getTime()));
    };

    /**
     * Increment this date 1 day into the future.
     * @name dayIncrement
     * @methodOf ExtendedDate
     * @return {ExtendedDate} Reference to this date.
     */
    var dayIncrement = function() {        
        this.setTime(this.getTime() + MS_PER_DAY);
        
        return this;
    };

    /**
     * Decrement this date 1 day into the past.
     * @name dayDecrement
     * @methodOf ExtendedDate
     * @return {ExtendedDate} Reference to this date.
     */
    var dayDecrement = function() {
        this.setTime(this.getTime() - MS_PER_DAY);
        
        return this;
    };
    
    /**
     * Get the start of the week to which this date belongs.
     * @name weekStartDate
     * @methodOf ExtendedDate
     * @return {ExtendedDate} Whatever day is 0 according to JavaScript is
     * the day that gets returned.
     */
    var weekStartDate = function() {
        var pastBoundary = new Date(this.getTime());
        
        // The beginning of the week is:
        // day 0, hour 0, minute 0, seconds 0, ms 0
        // There is no setDay, so mimic one.
        pastBoundary.setTime(pastBoundary.getTime() - (pastBoundary.getDay() * MS_PER_DAY));
        pastBoundary.setHours(0);
        pastBoundary.setMinutes(0);
        pastBoundary.setSeconds(0);
        pastBoundary.setMilliseconds(0);
        
        return ExtendedDate(pastBoundary);
    };

    /**
     * Get the end of the week to which this date belongs.
     * @name weekEndDate
     * @methodOf ExtendedDate
     * @return {ExtendedDate} Whatever day is 6 according to JavaScript is
     * the day that gets returned.
     */
    var weekEndDate = function() {
        var futureBoundary = new Date(this.getTime());
        
        // The end of the week is:
        // day 6, hour 23, minute 59, seconds 59, ms 999
        // There is no setDay, so mimic one.
        futureBoundary.setTime(futureBoundary.getTime() + ((MAX_WEEK_DAY - futureBoundary.getDay()) * MS_PER_DAY));
        futureBoundary.setHours(23);
        futureBoundary.setMinutes(59);
        futureBoundary.setSeconds(59);
        futureBoundary.setMilliseconds(999);
        
        return ExtendedDate(futureBoundary);
    };

    /**
     * Decrements the week by one (moves date, in place, 7 days into the past).
     * @name weekDecrement
     * @methodOf ExtendedDate
     * @return {ExtendedDate} Reference to this date.
     */
    var weekDecrement = function() {
        this.setTime(this.getTime() - MS_PER_WEEK);
        
        return this;
    };
    
    /**
     * Increments the week by one (moves date, in place, 7 days into future).
     * @name weekIncrement
     * @methodOf ExtendedDate
     * @return {ExtendedDate} Reference to this date.
     */
    var weekIncrement = function() {
        this.setTime(this.getTime() + MS_PER_WEEK);
        
        return this;
    };

    /**
     * Tests to see if a date is within the week of this particular date object.
     * @param compare {Date} Compares the input date object with this particular
     * date object to find out if the Date object is within the date boundaries.
     * @return {Boolean} True if the the input date object is within the same
     * week as this date object, false if not.
     */
    var isWithinWeek = function(compare) {
        var pastBoundary = new Date(this.getTime()),
            futureBoundary = new Date(this.getTime());

        // The beginning of the week is:
        // day 0, hour 0, minute 0, seconds 0, ms 0
        // There is no setDay, so mimic one.
        pastBoundary.setTime(pastBoundary.getTime() - (pastBoundary.getDay() * MS_PER_DAY));
        pastBoundary.setHours(0);
        pastBoundary.setMinutes(0);
        pastBoundary.setSeconds(0);
        pastBoundary.setMilliseconds(0);
                
        // The end of the week is:
        // day 6, hour 23, minute 59, seconds 59, ms 999
        // There is no setDay, so mimic one.
        futureBoundary.setTime(futureBoundary.getTime() + ((MAX_WEEK_DAY - futureBoundary.getDay()) * MS_PER_DAY));
        futureBoundary.setHours(23);
        futureBoundary.setMinutes(59);
        futureBoundary.setSeconds(59);
        futureBoundary.setMilliseconds(999);
        
        return (compare.getTime() >= pastBoundary.getTime() &&
            compare.getTime() <= futureBoundary.getTime())
    };

    /**
     * Decrements the month by one, handling the beginning of year wrap-around.
     * @name monthDecrement
     * @methodOf ExtendedDate
     * @return {ExtendedDate} Reference to this date.
     */
    var monthDecrement = function() {
        var now = this,
            // Set up to handle January wrap around to previous year
            // JavaScript month indices are zero based (January is 0)
            prevMonth = now.getMonth() ? (now.getMonth() - 1) : 11,
            // Handle wrap around from, or the fact that the prevMonth is
            // set to December (11th index)
            prevYear = (prevMonth == 11) ? now.getFullYear() - 1 : now.getFullYear();

        // Setup the new date, ignoring anything lower than the day level
        now.setDate(1);
        now.setMonth(prevMonth);
        now.setYear(prevYear);
        
        return now;
    };

    /**
     * Decrements the month by one, handling the end of year wrap-around.
     * @name monthIncrement
     * @methodOf ExtendedDate
     * @return {ExtendedDate} Reference to this date.
     */
    var monthIncrement = function() {
        var now = this,
            // Set up to handle December wrap around to next year
            // JavaScript month indices are zero based (December is 11)
            nextMonth = (now.getMonth() == 11) ? 0 : (now.getMonth() + 1),
            // Handle wrap around from, or the fact that the prevMonth is
            // set to December (11th index)
            nextYear = (nextMonth == 0) ? now.getFullYear() + 1 : now.getFullYear();

        // Setup the new date, ignoring anything lower than the day level
        now.setDate(1);
        now.setMonth(nextMonth);
        now.setYear(nextYear);

        return now;
    };

    /**
     * Gets the first day of the week in the month in which the native Date
     * object resides.
     * @name monthStartDay
     * @methodOf ExtendedDate
     * @return {number} Integer number of the first day of the week of the
     * month (0 - 6).
     */
    var monthStartDay = function() {
            // Make copies of needed values
        var d = new Date(this);
        
        // Process:
        // Set to first day of month
        // return the day of the week
        d.setDate(1);
        return d.getDay();
    };

    /**
     * Gets the last numeric date of the month in which the native Date object
     * resides.
     * @name monthEndDate
     * @methodOf ExtendedDate
     * @return {number} Integer number of the last day of the month (0 - 31).
     */
    var monthEndDate = function() {
            // Make copies of needed values
        var d = new Date(this),
            m = d.getMonth() + 1;
            
        // Need to deal with potential leap years, hence we need to set the
        // month to the current year. Months are 0 - 11.
        m = (m > 11) ? 0 : m;
        // Process: Move us forward one month
        // Set to first date of month
        // Backup one day
        // return the date
        d.setMonth(m);
        d.setDate(1);
        d = new Date(d - MS_PER_DAY);
        return d.getDate();
    };

    /**
     * Gets the last day of the week in the month in which the native Date
     * object resides.
     * @name monthEndDay
     * @methodOf ExtendedDate
     * @return {number} Integer number of the last day of the week of the
     * month (0 - 6).
     */
    var monthEndDay = function() {
            // Make copies of needed values
        var d = new Date(this),
            m = d.getMonth() + 1;

        // Need to deal with potential leap years, hence we need to set the
        // month to the current year. Months are 0 - 11.
        m = (m > 11) ? 0 : m;
        // Process: Move us forward one month
        // Set to first date of month
        // Backup one day
        // return the day of the week
        d.setMonth(m);
        d.setDate(1);
        d = new Date(d - MS_PER_DAY);
        return d.getDay();
    };

    // Export
    window.ExtendedDate = ExtendedDate;
})();
