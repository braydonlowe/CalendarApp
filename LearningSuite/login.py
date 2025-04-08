from LearningSuite import selenium_imports as selenium
from Shared import getConfig


def login(driver: selenium.WebDriver, username: str, password: str) -> None:
    print("CALLED LOGIN\n")


    #Stil uses the config file this can probably be removed and we can put the URL into the DB.
    config = getConfig.load_config()

    login_url = config.get("website")

    driver.get(login_url)


    #Login Credentials
    driver.find_element(selenium.By.NAME, "username").send_keys(username)
    driver.find_element(selenium.By.NAME, "password").send_keys(password)


    login_button = driver.find_element(selenium.By.ID, "byuSignInButton")
    login_button.click()

    timerSeconds = 0
    foundElement = None

    #The user should have 60 seconds to finish logging in before it's done. 
    #As soon as the user logs in the driver should close.
    while (timerSeconds < 60 and foundElement == None):
        try:
            foundElement = selenium.WebDriverWait(driver, 60).until(
                selenium.EC.element_to_be_clickable((selenium.By.ID, "trust-browser-button"))
            )
            foundElement.click()
            
        except selenium.TimeoutException:
            print("Timeout waiting for the trust-browser-button.")

    print("Current URL:", driver.current_url)

