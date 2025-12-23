def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a la API de Citas Célebres"}
