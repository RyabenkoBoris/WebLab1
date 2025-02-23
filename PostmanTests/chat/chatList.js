pm.test("Отримання списку чатів успішне", function () {
    pm.response.to.have.status(200);

    pm.response.to.have.jsonBody();
    pm.response.to.have.jsonBody([]);

    let chats = pm.response.json();
    chats.forEach(chat => {
        pm.expect(chat).to.have.all.keys('id', 'name', 'creator');
        pm.expect(chat.id).to.be.a('number');
        pm.expect(chat.name).to.be.a('string');
        pm.expect(chat.creator).to.be.a('number');
    });
});

pm.test("Облікові дані для автентифікації не надано.", function () {
    pm.response.to.have.status(401);
});