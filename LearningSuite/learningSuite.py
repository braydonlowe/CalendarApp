from LearningSuite import selenium_imports as selenium
from LearningSuite import login
from LearningSuite import getSchedule



def createDriver(debugMode: bool) -> selenium.WebDriver:
    
    #Headless means that the browser will not appear when the script is run.
    
    if debugMode:
        return selenium.webdriver.Chrome()
    chrome_options = selenium.Options()
    chrome_options.add_argument("--headless")
    return selenium.webdriver.Chrome(options=chrome_options)


def learningSuite(debugMode: bool) -> None:
    driver = createDriver(debugMode)
    login.login(driver)
    class_events = getSchedule.getSchedule(driver)
    driver.quit()
    #Here is where I would put it into the DB