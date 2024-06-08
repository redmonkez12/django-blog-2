describe("test post list", () => {
    it("should display 2 posts with pagination", () => {
        cy.visit('http://localhost:8000/blog/');
        let cards = cy.get('[data-cy="cards"] > div');

        cards.should("have.length", 2);

        cards.first().find(".card-title")
            .should("have.text", "Learning .NET");
        cy.get('[data-cy="cards"] > div').eq(1).find(".card-title")
            .should("have.text", "Learning Javascript");
    });

    it("should login user", () => {
        cy.visit('http://localhost:8000/blog/');

        cy.get('[data-cy="login-button"]').click();
        cy.get('[data-cy="username"]').type("john");
        cy.get('[data-cy="password"]').type("john123");
        cy.get('[data-cy="form-log-in-button"]').click();

        cy.url().should("eq", "http://localhost:8000/");
    });
});