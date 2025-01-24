from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Initialize Flask app
app = Flask(__name__)

# Set up the Chrome webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run Chrome in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Function to extract data from the website
def extract_data():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        URL = "https://ktu.edu.in/Menu/announcements"
        driver.get(URL)

        # Wait for the page to load
        time.sleep(5)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'p-b-15.p-t-15.border-.shadow-lg.card'))
        )
        main_container = driver.find_element(By.CLASS_NAME, 'p-b-15.p-t-15.border-.shadow-lg.card')
        nested_divs = main_container.find_elements(By.CLASS_NAME, 'p-t-15.p-b-15.shadow.row.m-b-25.row')

        data_list = []

        for div in nested_divs:
            inner_div = div.find_element(By.CLASS_NAME, 'col-sm-11')
            title = inner_div.find_element(By.TAG_NAME, 'h6').text.strip() if inner_div.find_elements(By.TAG_NAME, 'h6') else 'No Title'

            other_divs = inner_div.find_elements(By.TAG_NAME, 'div')
            first_data = ''
            second_data = ''

            for data_div in other_divs:
                if "font-14 text-theme h6 m-t-10 f-w-bold" in data_div.get_attribute('class'):
                    first_data = data_div.text.strip()
                elif "m-t-10 font-14" in data_div.get_attribute('class'):
                    second_data = data_div.text.strip()

            data_list.append({
                "TITLE": title,
                "DATE": first_data,
                "CONTENT": second_data,
            })

        return data_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        driver.quit()  # Ensure the driver is quit even if an error occurs

@app.route('/api/data', methods=['GET'])
def get_data():
    data = extract_data()  # Call the extract_data function
    return jsonify(data)  # Return the data as a JSON response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
