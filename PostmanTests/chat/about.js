pm.test("Отримано інформацію про додаток", function () {
    pm.response.to.have.status(200);
    pm.response.to.have.jsonBody("name");
    pm.response.to.have.jsonBody("description");
    pm.response.to.have.jsonBody("logo");
});
