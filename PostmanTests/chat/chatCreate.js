pm.test("Створення нового чату успішне", function () {
    pm.response.to.have.status(201);
    pm.response.to.have.jsonBody("id");
    pm.response.to.have.jsonBody("name");
    pm.response.to.have.jsonBody("creator");
});
pm.test("Облікові дані для автентифікації не надано.", function () {
    pm.response.to.have.status(401);
});