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
PRACTITEST_INSRANCE_ID = '102520545'

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
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.practitest.com/talk-to-us/")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hs-form-iframe-0"))
    )
    driver.switch_to.frame(driver.find_element(By.ID, "hs-form-iframe-0"))

    # Example steps with reporting to PractiTest
    try:
        driver.find_element(By.NAME, "firstname").send_keys("John")
        add_test_step("Fill First Name", "Enter 'John' in First Name field", "First Name field should be filled",
                      "First Name field is filled", "PASSED")
    except Exception as e:
        add_test_step("Fill First Name", "Enter 'John' in First Name field", "First Name field should be filled",
                      f"Failed with error: {e}", "FAILED")

    try:
        driver.find_element(By.NAME, "lastname").send_keys("Doe")
        add_test_step("Fill Last Name", "Enter 'Doe' in Last Name field", "Last Name field should be filled",
                      "Last Name field is filled", "PASSED")
    except Exception as e:
        add_test_step("Fill Last Name", "Enter 'Doe' in Last Name field", "Last Name field should be filled",
                      f"Failed with error: {e}", "FAILED")

    try:
        driver.find_element(By.NAME, "company").send_keys("Test Company")
        add_test_step("Fill Company", "Enter 'Test Company' in Company field", "Company field should be filled",
                      "Company field is filled", "PASSED")
    except Exception as e:
        add_test_step("Fill Company", "Enter 'Test Company' in Company field", "Company field should be filled",
                      f"Failed with error: {e}", "FAILED")

    try:
        driver.find_element(By.NAME, "email").send_keys("john.doe@example.com")
        add_test_step("Fill Email", "Enter 'john.doe@example.com' in Email field", "Email field should be filled",
                      "Email field is filled", "PASSED")
    except Exception as e:
        add_test_step("Fill Email", "Enter 'john.doe@example.com' in Email field", "Email field should be filled",
                      f"Failed with error: {e}", "FAILED")

    try:
        driver.find_element(By.NAME, "phone").send_keys("+1234567890")
        add_test_step("Fill Phone", "Enter '+1234567890' in Phone field", "Phone field should be filled",
                      "Phone field is filled", "PASSED")
    except Exception as e:
        add_test_step("Fill Phone", "Enter '+1234567890' in Phone field", "Phone field should be filled",
                      f"Failed with error: {e}", "FAILED")

    try:
        job_title_dropdown = Select(driver.find_element(By.NAME, "job_title"))
        job_title_dropdown.select_by_visible_text("Consultant")
        add_test_step("Select Job Title", "Select 'Consultant' from Job Title dropdown",
                      "Job Title should be 'Consultant'", "Job Title is 'Consultant'", "PASSED")
    except Exception as e:
        add_test_step("Select Job Title", "Select 'Consultant' from Job Title dropdown",
                      "Job Title should be 'Consultant'", f"Failed with error: {e}", "FAILED")

    try:
        industry_dropdown = Select(driver.find_element(By.NAME, "industry_dd"))
        industry_dropdown.select_by_visible_text("Gaming")
        add_test_step("Select Industry", "Select 'Gaming' from Industry dropdown", "Industry should be 'Gaming'",
                      "Industry is 'Gaming'", "PASSED")
    except Exception as e:
        add_test_step("Select Industry", "Select 'Gaming' from Industry dropdown", "Industry should be 'Gaming'",
                      f"Failed with error: {e}", "FAILED")

    driver.quit()

    # After test execution, update PractiTest with the results
    update_practitest()


if __name__ == "__main__":
    test_practitest_contact_form()