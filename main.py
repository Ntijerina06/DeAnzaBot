import datetime
import time
from selenium import webdriver
from selenium.webdriver.safari.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Bot():
    def __init__(self, classes, password, username):
        s = Service('/usr/bin/safaridriver')
        self.driver = webdriver.Safari(service=s)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()
        self.driver.get("https://www.google.com/")
        self.classes = classes
        self.password = password
        self.username = username
    def switch_Window(self):
        original_window = self.driver.current_window_handle

        self.wait.until(EC.number_of_windows_to_be(2))

        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break

    def login(self):
        searchBar = self.driver.find_element(By.NAME, "q")
        searchBar.send_keys("https://ssoshib.fhda.edu/idp/profile/cas/login?execution=e1s1")
        searchBar.send_keys(Keys.RETURN)

        # Wait for and click the link to My Portal
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='rso']/div[1]/div/div/div/div[1]/div/div/span/a/h3"))).click()

        # Log in with username and password
        username = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='username']")))
        username.send_keys(self.username)  # input username

        password = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))

        password.send_keys(self.password)  # input password

        self.driver.find_element(By.XPATH, '//*[@id="btn-eventId-proceed"]').click()  #

    def go_Add_or_Drop_classes(self):
        registration_icon = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[@role='button' and @aria-label='Student Registration']")))
        self.driver.execute_script("arguments[0].click();", registration_icon)

        # Use JavaScript to scroll to the "Add or Drop Classes" link and click it
        add_drop_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Add or Drop Classes")))
        self.driver.execute_script("arguments[0].click();", add_drop_link)

        self.switch_Window()

        submit_bn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Submit']")))
        submit_bn.click()

    def addClasses(self):
        for i, Class in enumerate(self.classes):
            id = "crn_id" + str(i + 1)
            class_input = self.wait.until(EC.element_to_be_clickable((By.ID, id)))
            class_input.send_keys(Class)

        final_submit = self.driver.find_element(By.XPATH, "/html/body/div[3]/form/input[19]")

        final_submit.click()


def Exicute(password, username, classes, execute_time):
    # Get the current time
    now = datetime.datetime.now()

    # Convert execute_time (a string) to a datetime object
    target_time = datetime.datetime.strptime(execute_time, "%H:%M:%S")

    # Combine the target_time with today's date
    target_time = now.replace(hour=target_time.hour, minute=target_time.minute, second=target_time.second,
                              microsecond=0)

    wait_time = (target_time - now).total_seconds() - 5

    if wait_time < 0:
        print("The specified time has already passed.")
        return

    time.sleep(wait_time)

    print("Start")
    da = Bot(classes, password, username)
    da.login()
    da.go_Add_or_Drop_classes()
    da.addClasses()
    print("finished")








