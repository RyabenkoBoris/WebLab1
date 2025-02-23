pm.test("Видалення чату успішне", function () {
    pm.response.to.have.status(204);
});
pm.test("Облікові дані для автентифікації не надано.", function () {
    pm.response.to.have.status(401);
});
pm.test("Чату не існує.", function () {
    pm.response.to.have.status(404);
});