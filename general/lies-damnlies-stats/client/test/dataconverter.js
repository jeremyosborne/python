describe("DataConverter touint", function() {
    // Static, not a class.
    var dc = DataConverter;

    it("should correctly convert to an unsigned integer", function() {
        expect(dc.touint(0)).toBe(0);
        expect(dc.touint("1.0")).toBe(1);
        expect(dc.touint("1")).toBe(1);
        expect(dc.touint(10000)).toBe(10000);
        expect(dc.touint( new Number(1) )).toBe(1);
        // Since JavaScript doesn't have floats, this gets converted
        // to an int within toValue; this should be true.
        expect(dc.touint(1.0)).toBe(1);
    });
    
    it("should return undefined for bad input.", function() {
        // Failure tests go here.
        expect(dc.touint(-4.2)).toBe(undefined);
        expect(dc.touint(-1.0)).toBe(undefined);
        expect(dc.touint(-1)).toBe(undefined);
        expect(dc.touint("-1")).toBe(undefined);
        expect(dc.touint(NaN)).toBe(undefined);
        expect(dc.touint([])).toBe(undefined);
        expect(dc.touint({})).toBe(undefined);
    });

}); 



describe("DataConverter toisocalendardate", function() {
    // Static, not a class.
    var dc = DataConverter;

    it("should correctly convert to an ISO Calendar Date", function() {
        expect(dc.toisocalendardate(new Date(2012, 0, 1))).toBe("2012-01-01");
        expect(dc.toisocalendardate(ExtendedDate(new Date(2012, 0, 1)))).toBe("2012-01-01");
    });
    
    it("should return undefined for bad input.", function() {
        // Failure tests go here.
        expect(dc.toisocalendardate({})).toBe(undefined);
    });

}); 



describe("DataConverter fromisocalendardate", function() {
    // Static, not a class.
    var dc = DataConverter;

    it("should correctly convert from an ISO Calendar Date", function() {
        expect(dc.fromisocalendardate("2012-12-21").getDate()).toBe(21);
        expect(dc.fromisocalendardate("2012-12-21").getMonth()).toBe(11);
        expect(dc.fromisocalendardate("2012-12-21").getFullYear()).toBe(2012);
        // It's an ExtendedDate, but ExtendedDate is a mixin, not a true 
        // class.
        expect(dc.fromisocalendardate("2012-12-21") instanceof Date).toBe(true);
    });
    
    it("should return undefined for bad input.", function() {
        // Failure tests go here.
        expect(dc.fromisocalendardate({})).toBe(undefined);
    });

}); 
