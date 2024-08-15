import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import base64
import argparse
import os  # Ensure os is imported for file path operations

test_steps = []

def add_test_step(name, description, expected_results, actual_results, status):
    test_steps.append({
        "name": name,
        "description": description,
        "expected-results": expected_results,
        "actual-results": actual_results,
        "status": status
    })

def update_practitest(email, token, project_id, instance_id):
    url = f'https://api.practitest.com/api/v2/projects/{project_id}/runs.json'

    # Create the basic authentication header
    auth_str = f'{email}:{token}'
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {b64_auth_str}'
    }

    data = {
        "data": {
            "type": "instances",
            "attributes": {
                "instance-id": instance_id
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
    add_test_step("Credit card details", "Enter valid credit card details (card number, expiration date, CVV).", "Details sheon in Green.",
                      "No CVV field.", "FAILED")
    add_test_step("Submit the payment.", "Click on the Submit button", "The button is clicked and the form closes.",
                      "The form is still open and there is an error message.", "FAILED")
    add_test_step("Confirmation message", "Verify that the payment is processed successfully and a confirmation message is displayed.", "TConfirmation message shown.",
                      "Confirmation message shown.", "NO RUN")
    
    # Log file and script path would be determined by your execution environment
    log_file = "path/to/log_file.log"
    script_path = __file__

    # Update PractiTest with the test results
    update_practitest(args.email, args.token, args.project_id, args.instance_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PractiTest form test.")
    parser.add_argument('--email', required=True, help='PractiTest email address')
    parser.add_argument('--token', required=True, help='PractiTest API token')
    parser.add_argument('--project_id', required=True, help='PractiTest project ID')
    parser.add_argument('--instance_id', required=True, help='PractiTest instance ID')

    args = parser.parse_args()

    test_practitest_contact_form()
