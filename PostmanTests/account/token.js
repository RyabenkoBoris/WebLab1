pm.test("Отримання токена успішне", function () {
    pm.response.to.have.status(200);
    pm.response.to.have.jsonBody("access");
    pm.response.to.have.jsonBody("refresh");
});
pm.test("Невалідні дані", function () {
    pm.response.to.have.status(401);
});