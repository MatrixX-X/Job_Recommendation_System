from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json


def main():

    # Start Chrome WebDriver
    driver = webdriver.Chrome()

    driver.get("https://www.naukri.com/")

    # Wait for the login button and click it
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
    login_button.click()

    # Fill in login details
    time.sleep(2)  # Wait for the login form to appear
# Locate and enter username
    username_field = driver.find_element(By.XPATH, "//div[@class='form-row']/input[@type='text']")
    username_field.send_keys("") # enter your email here

# Locate and enter password
    password_field = driver.find_element(By.XPATH, "//div[@class='form-row']/input[@type='password']")
    password_field.send_keys("") # enter your password here

    # Locate and click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'loginButton')]")
    login_button.click()

    

    # Wait for the search input field to appear
    wait = WebDriverWait(driver, 10)
    search_field = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "suggestor-input")))

    # Enter "Java jobs" in the search field
    search_field.send_keys("Data Engineer jobs")

    # Press ENTER to trigger search
    search_field.send_keys(Keys.RETURN)

    driver.get("https://www.naukri.com/data-engineer-jobs?k=data%20engineer%20jobs&nignbevent_src=jobsearchDeskGNB")
    # Wait for login to complete
    time.sleep(15)


    final = []
    time.sleep(5) 
    rows = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")

    # print(len(rows))
    # for row in rows:
    #     print(f"{row.text}")
    #     print("---------------------")
    #     final.append(row.text)

    for k in range(1,3):
        url = "https://www.naukri.com/data-engineer-jobs-" + str(k) + "?k=data+engineer+jobs&nignbevent_src=jobsearchDeskGNB"
        driver.get(url)
        time.sleep(10) 
        rows = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")

        for row in rows:
            print(f"{row.text}")
            print("---------------------")
            final.append(row.text)

    
    
    with open("Data_Engineer_data.json", "a") as file:
        json.dump(final, file)  # Saves as a JSON array

    driver.close()

if __name__ == '__main__':
    main()
