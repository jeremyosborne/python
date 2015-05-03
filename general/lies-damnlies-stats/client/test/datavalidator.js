describe("DataValidator uint", function() {
    // Static, not a class.
    var dv = DataValidator;

    it("should correctly validate an unsigned integer", function() {
        expect(DataValidator.uint(1)).toBe(true);
        expect(DataValidator.uint(0)).toBe(true);
        expect(DataValidator.uint(10000)).toBe(true);
        expect(DataValidator.uint( new Number(1) )).toBe(true);
        // Since JavaScript doesn't have floats, this gets converted
        // to an int within toValue; this should be true.
        expect(DataValidator.uint(1.0)).toBe(true);
    });
    
    it("should correctly invalidate non-unsigned integers, or unacceptable types.", function() {
        // Failure tests go here.
        expect(DataValidator.uint(-1.0)).toBe(false);
        expect(DataValidator.uint(-1)).toBe(false);
        expect(DataValidator.uint("1")).toBe(false);
        expect(DataValidator.uint(false)).toBe(false);
        // Too large, beyond the representation boundaries of a simple
        // int.
        expect(DataValidator.uint(1e100)).toBe(false);
    });

}); 

describe("DataValidator isocalendardate", function() {
    // Static, not a class.
    var dv = DataValidator;

    it("should correctly validate expected date formats", function() {
        expect(DataValidator.isocalendardate("2000-12-31")).toBe(true);
        expect(DataValidator.isocalendardate("2012-12-21")).toBe(true);
        expect(DataValidator.isocalendardate("2012-01-31")).toBe(true);
        // We only check format, not date validity. This should be true.
        expect(DataValidator.isocalendardate("2012-02-31")).toBe(true);
    });
    
    it("should correctly invalidate non-iso date input", function() {
        // Failure tests go here.
        expect(DataValidator.isocalendardate("2012-1-31")).toBe(false);
        // ISO months, not JavaScript months.
        expect(DataValidator.isocalendardate("2012-00-31")).toBe(false);
        // We're stuck on four-digit years, the Y10K problem.
        expect(DataValidator.isocalendardate("202-00-31")).toBe(false);
        expect(DataValidator.isocalendardate("10000-01-31")).toBe(false);
    });

}); 