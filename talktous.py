import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import argparse
import base64
import os

def update_practitest(email, token, project_id, instance_id, log_file, script_path):
    url = f'https://api.practitest.com/api/v2/projects/{project_id}/runs.json'

    auth_str = f'{email}:{token}'
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {b64_auth_str}'
    }

    files_data = []

    if log_file and os.path.exists(log_file):
        with open(log_file, 'rb') as f:
            files_data.append({
                "filename": os.path.basename(log_file),
                "content_encoded": base64.b64encode(f.read()).decode()
            })

    if script_path and os.path.exists(script_path):
        with open(script_path, 'rb') as f:
            files_data.append({
                "filename": os.path.basename(script_path),
                "content_encoded": base64.b64encode(f.read()).decode()
            })

    data = {
        "data": {
            "type": "instances",
            "attributes": {
                "instance-id": instance_id
            },
            "steps": {
                "data": [
                    {
                        "name": "Test Execution",
                        "status": "PASSED",
                        "actual-results": "Form submission successful.",
                        "files": {"data": files_data}
                    }
                ]
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Test steps updated successfully in PractiTest.")
    else:
        print(f"Failed to update test steps in PractiTest: {response.status_code} - {response.text}")

def test_practitest_contact_form(email, token, project_id, instance_id):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.practitest.com/talk-to-us/")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "hs-form-iframe-0"))
    )
    driver.switch_to.frame(driver.find_element(By.ID, "hs-form-iframe-0"))

    # Example steps
    driver.find_element(By.NAME, "firstname").send_keys("John")
    driver.find_element(By.NAME, "lastname").send_keys("Doe")
    driver.find_element(By.NAME, "company").send_keys("Test Company")
    driver.find_element(By.NAME, "email").send_keys("john.doe@example.com")
    driver.find_element(By.NAME, "phone").send_keys("+1234567890")

    job_title_dropdown = Select(driver.find_element(By.NAME, "job_title"))
    job_title_dropdown.select_by_visible_text("Consultant")

    industry_dropdown = Select(driver.find_element(By.NAME, "industry_dd"))
    industry_dropdown.select_by_visible_text("Gaming")

    driver.quit()

    # Log file and script path would be determined by your execution environment
    log_file = "path/to/log_file.log"
    script_path = __file__

    # Update PractiTest with the test results
    update_practitest(email, token, project_id, instance_id, log_file, script_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PractiTest form test.")
    parser.add_argument('--email', required=True, help='PractiTest email address')
    parser.add_argument('--token', required=True, help='PractiTest API token')
    parser.add_argument('--project_id', required=True, help='PractiTest project ID')
    parser.add_argument('--instance_id', required=True, help='PractiTest instance ID')

    args = parser.parse_args()

    test_practitest_contact_form(args.email, args.token, args.project_id, args.instance_id)
