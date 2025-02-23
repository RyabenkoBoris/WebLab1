pm.test("Оновлення токена успішне", function () {
    pm.response.to.have.status(200);
    pm.response.to.have.jsonBody("access");
});
pm.test("Токен недійсний або прострочений.", function () {
    pm.response.to.have.status(401);
});