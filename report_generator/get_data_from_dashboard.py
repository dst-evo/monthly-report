import time
import os
import sys
import shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


# define submenues in sidebar to uncollapse
sub_counting = ['Produced boxes',
                'Incoming Items',
                'Reject Induct',
                'Total carton feed (ch. 1)',
                'Total carton waste (ch. 1)',
                'Total carton feed (ch. 2)',
                'Total carton waste (ch. 2)',
                ]
sub_timing = ['Idle time',
              'Run time',
              'Error time',
              'Corrective maintenance time',
              'Preventive maintenance time',
              ]
sub_bad_boxes = ['Bad boxes: All reasons',
                 'Bad boxes: Reject reason 1',
                 'Bad boxes: Reject reason 2',
                 'Bad boxes: Reject reason 3',
                 'Bad boxes: Reject reason 4',
                 'Bad boxes: Reject all other reasons',
                 'Bad boxes: Removed boxes',
                 ]


def create_configured_driver(ip_address):
    """
    Create and configure a Firefox WebDriver instance with download preferences and headless mode.

    Parameters:
    ip_address (str): The IP address to navigate to.

    Returns:
    webdriver (selenium.webdriver.firefox.webdriver.WebDriver): A configured Firefox WebDriver instance.
    """
    # Get the location of the script
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # Set up download preferences
    download_dir = os.path.join(script_dir, 'raw_data')

    # Create the download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference(
        "browser.download.manager.showWhenStarting", False)
    firefox_options.set_preference("browser.download.dir", download_dir)
    firefox_options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "text/csv")
    firefox_options.add_argument("--headless")  # Enable headless mode

    # Initialize the driver with the download preferences
    driver = webdriver.Firefox(options=firefox_options)

    # Connect to the specified IP address
    url = f"http://{ip_address}/dashboard/WebReport/index.php"
    driver.get(url)

    return driver


def login(driver, username, password):
    """
    Log in to the dashboard using the given username and password.

    Parameters:
    driver (webdriver): The Selenium WebDriver instance to interact with the page.
    username (str): The username for logging in.
    password (str): The password for logging in.

    Returns:
    None
    """
    # Locate the username input field and enter the given value
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)

    # Locate the password input field and enter the given value
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Locate the login button and click it
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()


def configure_and_download_data(driver, granularity, totalized, start_date, end_date, sidebar_button_text, file_name):
    """
    Configure and download data from the dashboard using the given parameters.

    Parameters:
    driver (webdriver): The Selenium WebDriver instance to interact with the page.
    granularity (str): The granularity value for the data, e.g., "month".
    totalized (str): The totalized value for the data, e.g., "yes".
    start_date (str): The start date for the data range in the format "dd/mm/yyyy hh:mm".
    end_date (str): The end date for the data range in the format "dd/mm/yyyy hh:mm".
    sidebar_button_text (str): The text of the sidebar button to click, e.g., "Produced boxes".
    file_name (str): The desired name for the downloaded file.

    Returns:
    None
    """
    # Locate the granularity dropdown and set it to the specified granularity
    granularity_dropdown = Select(
        driver.find_element(By.ID, "modal_granularity"))
    granularity_dropdown.select_by_value(granularity)

    # Locate the Totalized dropdown and set it to the specified totalized value
    granularity_dropdown = Select(
        driver.find_element(By.ID, "modal_totalized"))
    granularity_dropdown.select_by_value(totalized)

    # Click the start date input field, select all text, and send the desired date
    start_date_field = driver.find_element(
        By.XPATH, "//input[@id='modal_startdate'][@name='modal_startdate']")
    start_date_field.click()
    start_date_field.send_keys(Keys.CONTROL + "a")
    start_date_field.send_keys(start_date)

    # Click the end date input field, select all text, and send the desired date
    end_date_field = driver.find_element(
        By.XPATH, "//input[@id='modal_enddate'][@name='modal_enddate']")
    end_date_field.click()
    end_date_field.send_keys(Keys.CONTROL + "a")
    end_date_field.send_keys(end_date)

    # Locate the submit button and click it
    submit_button = driver.find_element(
        By.XPATH, "//button[@type='submit'][@name='action'][@value='set']")
    submit_button.click()

    # Add some delay to load the next page
    time.sleep(0.5)

    # Locate and click on the appropriate dropdown based on sidebar_button_text
    if sidebar_button_text in sub_counting:
        dropdown_text = 'Counting'
    elif sidebar_button_text in sub_timing:
        dropdown_text = 'Timing'
    elif sidebar_button_text in sub_bad_boxes:
        dropdown_text = 'Bad boxes'
    else:
        dropdown_text = None

    if dropdown_text is not None:
        dropdown_xpath = f"//a[contains(text(), '{dropdown_text}')]"
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, dropdown_xpath))
        )
        dropdown.click()

    # Locate and click on the specified sidebar button
    sidebar_button_xpath = f"//a[contains(text(), '{sidebar_button_text}')]"
    sidebar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, sidebar_button_xpath))
    )
    sidebar_button.click()

    time.sleep(0.5)

    # Locate and click on the "File CSV" link
    csv_link_xpath = "//a[contains(@href, 'filetype=csv')]"
    csv_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, csv_link_xpath))
    )
    csv_link.click()

    # Give the file some time to download
    time.sleep(1)

    # Get the latest downloaded file from the download directory
    download_directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "raw_data")
    latest_file = max([os.path.join(download_directory, f)
                      for f in os.listdir(download_directory)], key=os.path.getctime)

    # Rename the downloaded file to the specified file_name
    new_file_path = os.path.join(download_directory, file_name)
    shutil.move(latest_file, new_file_path)

    # Locate and click on the filter button to return to the start
    sidebar_button_xpath = "//a[contains(@href, 'filtersetup.php') and contains(., 'Filter')]"
    sidebar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, sidebar_button_xpath))
    )
    sidebar_button.click()
