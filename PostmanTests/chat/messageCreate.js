pm.test("Статус-код 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Відповідь є масивом", function () {
    let jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an("array");
});

pm.test("Кожен об'єкт містить всі необхідні поля", function () {
    let jsonData = pm.response.json();
    
    jsonData.forEach((message) => {
        pm.expect(message).to.have.property("id");
        pm.expect(message).to.have.property("user");
        pm.expect(message).to.have.property("text");
        pm.expect(message).to.have.property("timestamp");
    });
});

pm.test("Перевірка типів даних у відповіді", function () {
    let jsonData = pm.response.json();
    
    jsonData.forEach((message) => {
        pm.expect(message.id).to.be.a("number");
        pm.expect(message.text).to.be.a("string");
        pm.expect(message.timestamp).to.be.a("string"); 

        pm.expect(message.user).to.satisfy(value => value === null || typeof value === "number");
    });
});