import requests_mock
import pytest


def test_weather(mocker, client):
    with requests_mock.Mocker() as mock:
        mock.get(
            "https://api.openweathermap.org/data/2.5/weather?q=London&appid=TEST&units=metric",
            json={
                "name": "London",
                "main": {"temp": 10},
                "weather": [{"description": "clear sky"}],
            },
        )

        response = client.get("/weather/London")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "city": "London",
            "temperature": 10,
            "description": "clear sky",
        }


@pytest.mark.parametrize(
    ("city", "expected"),
    [
        ("London", {"name": "London", "temperature": 10, "description": "clear sky"}),
        ("Paris", {"name": "Paris", "temperature": 15, "description": "few clouds"}),
        (
            "New York",
            {"name": "New York", "temperature": 5, "description": "light snow"},
        ),
    ],
)
def test_weather(city, expected, mocker, client):
    with requests_mock.Mocker() as mock:
        mock.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=TEST&units=metric",
            json={
                "name": city,
                "main": {"temp": expected["temperature"]},
                "weather": [{"description": expected["description"]}],
            },
        )
        response = client.get(f"/weather/{city}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == city
        assert data["weather"] == expected["description"]
