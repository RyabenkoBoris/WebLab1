pm.test("Отримання профілю успішне", function () {
    pm.response.to.have.status(200);
    pm.response.to.have.jsonBody("email");
    pm.response.to.have.jsonBody("username");
    pm.response.to.have.jsonBody("gender");
    pm.response.to.have.jsonBody("birth_date");
});

pm.test("Облікові дані для автентифікації не надано.", function () {
    pm.response.to.have.status(401);
});