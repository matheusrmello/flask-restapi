import pytest
from application import create_app


class TestApplication():
    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "Matheus",
            "last_name": "Roberto",
            "cpf": "602.927.330-20",
            "email": "contato@matheus.com",
            "birth_date": "1998-06-10"
            }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "Matheus",
            "last_name": "Roberto",
            "cpf": "123.456.789-11",
            "email": "contato@matheus.com",
            "birth_date": "1998-06-10"
            }

    def test_get_users(self, client):
        response = client.get("/users")
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post('/user', json=valid_user)
        assert response.status_code == 201
        assert b"successfully" in response.data

        response = client.post('/user', json=invalid_user)
        assert response.status_code == 400
        assert b"invalid" in response.data
