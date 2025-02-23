pm.test("Користувач доданий до чату", function () {
    pm.response.to.have.status(200);
    pm.response.to.have.jsonBody("detail");
});
pm.test("Користувач вже є в чаті.", function () {
    pm.response.to.have.status(400);
    pm.response.to.have.jsonBody("detail");
});
pm.test("Облікові дані для автентифікації не надано.", function () {
    pm.response.to.have.status(401);
});
pm.test("Чату не існує.", function () {
    pm.response.to.have.status(404);
});