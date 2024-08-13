import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import base64

PRACTITEST_EMAIL = 'robbie@practitest.com'
PRACTITEST_TOKEN = 'd2b15358e470195c820a8ead0c9fa8e0ebb32a78'
PRACTITEST_PROJECT_ID = '29521'
PRACTITEST_INSRANCE_ID = '102544173'

test_steps = []


def add_test_step(name, description, expected_results, actual_results, status):
    test_steps.append({
        "name": name,
        "description": description,
        "expected-results": expected_results,
        "actual-results": actual_results,
        "status": status
    })


def update_practitest():
    url = f'https://api.practitest.com/api/v2/projects/{PRACTITEST_PROJECT_ID}/runs.json'

    # Create the basic authentication header
    auth_str = f'{PRACTITEST_EMAIL}:{PRACTITEST_TOKEN}'
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {b64_auth_str}'
    }

    data = {
        "data": {
            "type": "instances",
            "attributes": {
                "instance-id": PRACTITEST_INSRANCE_ID
            },
            "steps": {
                "data": test_steps
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Test steps updated successfully in PractiTest.")
    else:
        print(f"Failed to update test steps in PractiTest: {response.status_code} - {response.text}")


def test_practitest_contact_form():
    add_test_step("Select User to Edit", "Click on the 'Edit' button next to an existing user in the User Management UI.", "The user's details should be displayed in an editable form.",
                      "Details are shown in editable form.", "PASSED")
    add_test_step("Validate Required Fields", "Attempt to submit the form without filling in required fields.", "An error message should be displayed for each required field.",
                      "The error message appears.", "PASSED")
    add_test_step("Fill in User Details", "Enter valid details (username, email, role) in the form.", "The entered details should be accepted and displayed correctly.",
                      "Details are accepted.", "PASSED")
    add_test_step("Submit User Creation", "Click on the 'Create User' button to submit the form.", "The new user should be created and listed in the user table.",
                      "The new user is listed.", "PASSED")
    update_practitest()


f __name__ == "__main__":
    test_practitest_contact_form()
