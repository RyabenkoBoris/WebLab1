pm.test("Надсилання повідомлення успішне", function () {
    pm.response.to.have.status(201);
    pm.response.to.have.jsonBody("id");
    pm.response.to.have.jsonBody("user");
    pm.response.to.have.jsonBody("text");
});
pm.test("Облікові дані для автентифікації не надано.", function () {
    pm.response.to.have.status(401);
});
pm.test("Чату не існує.", function () {
    pm.response.to.have.status(404);
});