pm.test("Отримання профілю успішне", function () {
    pm.response.to.have.status(201);
    pm.response.to.have.jsonBody("email");
    pm.response.to.have.jsonBody("username");
    pm.response.to.have.jsonBody("gender");
    pm.response.to.have.jsonBody("birth_date");
});
pm.test("Реєстрація з невалідними даними", function () {
    pm.response.to.have.status(400);
    pm.response.to.have.jsonBody("email");
});
pm.test("Реєстрація з датою народження у майбутньому", function () {
    pm.response.to.have.status(400);
    pm.response.to.have.jsonBody("birth_date");
});