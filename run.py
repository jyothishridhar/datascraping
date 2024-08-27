# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import os

# # Function to log in to LinkedIn
# def linkedin_login(driver, email, password):
#     driver.get('https://www.linkedin.com/login')
#     time.sleep(2)  
#     driver.find_element(By.ID, 'username').send_keys(email)
#     time.sleep(2)
#     driver.find_element(By.ID, 'password').send_keys(password)
#     time.sleep(5)
#     driver.find_element(By.XPATH, "//button[contains(@class, 'btn__primary--large') and @type='submit']").click()
#     time.sleep(5)  

# # Function to check if the URL is valid
# def check_url(url, driver):
#     try:
#         driver.get(url)
#         time.sleep(4)  
#         if "This page doesn’t exist" in driver.page_source or "linkedin.com/404/" in driver.current_url:
#             return "Invalid"
#         else:
#             return "Valid"
#     except:
#         return "Invalid"

# # LinkedIn login credentials
# email = "poojashri0625@gmail.com"
# password = "neona@0625"

# file_path = 'C:\\LinkedIn\\LinkedIn_Profiles.txt'  
# output_dir = 'C:\\LinkedIn\\reports'
# os.makedirs(output_dir, exist_ok=True)  
# output_file_path = os.path.join(output_dir, 'LinkedIn_Profiles_with_status.xlsx')

# urls = []

# if file_path.endswith('.txt'):
#     with open(file_path, 'r') as file:
#         urls = file.readlines()
#     urls = [url.strip() for url in urls]
# elif file_path.endswith('.xlsx'):
#     df = pd.read_excel(file_path)
#     urls = df['URL'].tolist()

# options = Options()
# options.headless = False  
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# # Log in to LinkedIn
# linkedin_login(driver, email, password)

# results = []
# for url in urls:
#     status = check_url(url, driver)
#     results.append(status)

# driver.quit()

# # Save the results to an Excel file in the reports directory
# df = pd.DataFrame({'URL': urls, 'Status': results})
# df.to_excel(output_file_path, index=False)

# print(f"URL validation completed! Report saved at {output_file_path}")

import streamlit as st
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
    time.sleep(2)  
    driver.find_element(By.ID, 'username').send_keys(email)
    time.sleep(2)
    driver.find_element(By.ID, 'password').send_keys(password)
    time.sleep(5)
    driver.find_element(By.XPATH, "//button[contains(@class, 'btn__primary--large') and @type='submit']").click()
    time.sleep(15)  

# Function to check if the URL is valid
def check_url(url, driver):
    try:
        driver.get(url)
        time.sleep(8)  
        if "This page doesn’t exist" in driver.page_source or "linkedin.com/404/" in driver.current_url:
            return "Invalid"
        else:
            return "Valid"
    except:
        return "Invalid"

# Streamlit UI for input
st.title('LinkedIn URL Validator')

email = st.text_input("Enter your LinkedIn email")
password = st.text_input("Enter your LinkedIn password", type="password")

uploaded_file = st.file_uploader("Upload a file containing LinkedIn URLs", type=["txt", "xlsx"])

if st.button('Validate URLs'):
    if not uploaded_file:
        st.error("Please upload a file first!")
    elif not email or not password:
        st.error("Please enter your LinkedIn credentials!")
    else:
        # Load URLs from the uploaded file
        if uploaded_file.name.endswith('.txt'):
            urls = uploaded_file.read().decode("utf-8").splitlines()
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            urls = df['URL'].tolist()

        # Set up the Chrome WebDriver
        options = Options()
        options.headless = True  # Run in headless mode
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Log in to LinkedIn
        linkedin_login(driver, email, password)

        # Validate the URLs
        results = []
        for url in urls:
            status = check_url(url, driver)
            results.append({"URL": url, "Status": status})

        driver.quit()

        # Display and save the results
        results_df = pd.DataFrame(results)
        st.write(results_df)

        output_file_path = os.path.join('LinkedIn_Profiles_with_status.xlsx')
        results_df.to_excel(output_file_path, index=False)
        st.success(f"URL validation completed! Report saved as {output_file_path}")
        st.download_button(
            label="Download Excel file",
            data=open(output_file_path, "rb").read(),
            file_name="LinkedIn_Profiles_with_status.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


