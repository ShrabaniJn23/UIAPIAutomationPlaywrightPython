"""Test for creating a booking via Restful Booker API and returning bookingId"""
import pytest
from framework.api.api_client import APIClient

@pytest.mark.api
class TestRestfulBooker:
    @pytest.fixture(scope="class")
    def booking_data(self):
        return {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 123,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-04-01",
                "checkout": "2026-04-05"
            },
            "additionalneeds": "Breakfast"
        }

    def test_create_booking(self, booking_data):
        client = APIClient(base_url="https://restful-booker.herokuapp.com")
        response = client.post("/booking", json=booking_data)
        assert response.status_code == 200
        data = response.json()
        assert "bookingid" in data
        assert "booking" in data
        result = {
            "bookingid": data["bookingid"],
            "firstname": data["booking"]["firstname"],
            "lastname": data["booking"]["lastname"]
        }
        print(f"Created booking: {result}")
        return result
