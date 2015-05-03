describe("StatDescription", function() {
    // Static, not a class.
    var dv = DataValidator;
    var sd;
    
    beforeEach(function() {
        sd = StatDescription.create({
            // Made up description.
            "content": {
                "age": "uint",
                "bday": "isocalendardate",
            },
        });
    });

    it("should correctly validate valid fields", function() {
        expect(sd.validateField("age", 100)).toBe(true);
        expect(sd.validateField("bday", "2012-12-21")).toBe(true);
    });

    it("should not validate incorrect fields", function() {
        expect(sd.validateField("age", "100")).toBe(false);
        expect(sd.validateField("bday", "2012-13-21")).toBe(false);
        // Fields that don't exist should return false.
        expect(sd.validateField("wine", "red")).toBe(false);
    });

    it("should validate objects correctly", function() {
        expect(sd.validateAll({
            "age": 100,
            "bday": "0050-01-01",})).toBe(true);
    });

}); 
