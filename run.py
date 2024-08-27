import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Function to log in to LinkedIn
def linkedin_login(driver, email, password):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)  # Wait for the login page to load
    driver.find_element(By.ID, 'username').send_keys(email)
    time.sleep(2)
    driver.find_element(By.ID, 'password').send_keys(password)
    time.sleep(20)
    driver.find_element(By.XPATH, "//button[contains(@class, 'btn__primary--large') and @type='submit']").click()
    time.sleep(3)  # Wait for the login process to complete

# Function to check if the URL is valid
def check_url(url, driver):
    try:
        driver.get(url)
        time.sleep(4)  # Wait for the page to load
        if "This page doesn’t exist" in driver.page_source or "linkedin.com/404/" in driver.current_url:
            return "Invalid"
        else:
            return "Valid"
    except:
        return "Invalid"

# LinkedIn login credentials
email = "poojashri0625@gmail.com"
password = "neona@0625"

file_path = 'C:\\LinkedIn\\LinkedIn_Profiles.txt'  
output_dir = 'C:\\LinkedIn\\reports'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
output_file_path = os.path.join(output_dir, 'LinkedIn_Profiles_with_status.xlsx')

urls = []

if file_path.endswith('.txt'):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]
elif file_path.endswith('.xlsx'):
    df = pd.read_excel(file_path)
    urls = df['URL'].tolist()

options = Options()
options.headless = False  # Set to False so you can see the login process
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Log in to LinkedIn
linkedin_login(driver, email, password)

results = []
for url in urls:
    status = check_url(url, driver)
    results.append(status)

# driver.quit()

# Save the results to an Excel file in the reports directory
df = pd.DataFrame({'URL': urls, 'Status': results})
df.to_excel(output_file_path, index=False)

print(f"URL validation completed! Report saved at {output_file_path}")

# import requests

# def check_linkedin_url(url):
#     try:
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             return "Valid"
#         elif response.status_code == 404 or "404" in response.url:
#             return "Invalid"
#         else:
#             return "Unknown"
#     except requests.exceptions.RequestException:
#         return "Error"

# file_path = 'C:\\LinkedIn\\LinkedIn_Profiles.txt'
# output_dir = 'C:\\LinkedIn\\reports'
# output_file_path = os.path.join(output_dir, 'LinkedIn_Profiles_with_status.xlsx')

# urls = []

# # Load URLs from the text file
# with open(file_path, 'r') as file:
#     urls = file.readlines()
# urls = [url.strip() for url in urls]

# # Check each URL and store the results
# results = []
# for url in urls:
#     status = check_linkedin_url(url)
#     results.append(status)

# # Save the results to an Excel file
# df = pd.DataFrame({'URL': urls, 'Status': results})
# df.to_excel(output_file_path, index=False)

# print(f"URL validation completed! Report saved at {output_file_path}")

