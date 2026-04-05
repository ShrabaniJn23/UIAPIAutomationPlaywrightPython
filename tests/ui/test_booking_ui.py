"""UI test to validate booking details using Playwright"""
import pytest
from playwright.sync_api import expect

BOOKER_UI_URL = "https://restful-booker.herokuapp.com/"

@pytest.mark.ui
class TestBookingUI:
    def test_validate_booking_details(self, page, booking_details):
        bookingid = booking_details["bookingid"]
        firstname = booking_details["firstname"]
        lastname = booking_details["lastname"]

        # Navigate to the Restful Booker UI
        page.goto(BOOKER_UI_URL)

        # Wait for the booking id to appear in the list and click it
        expect(page.locator(f"text='{bookingid}'")).to_be_visible(timeout=10000)
        page.click(f"text='{bookingid}'")

        # Validate first name and last name in the booking details
        fname = page.input_value("input[name='firstname']")
        lname = page.input_value("input[name='lastname']")
        assert fname == firstname, f"Expected firstname {firstname}, got {fname}"
        assert lname == lastname, f"Expected lastname {lastname}, got {lname}"
        print(f"Validated booking {bookingid}: {fname} {lname}")
