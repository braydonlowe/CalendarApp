from LearningSuite import selenium_imports as selenium
import time

scheduledItems = {}


def getSchedule(driver: selenium.WebDriver) -> dict:
    #Wait a short time for the page to load.
    time.sleep(5)
    counter = 1
    while True:
        try:
            assignment_name = driver.find_element(selenium.By.XPATH, f"/html/body/div[2]/div[2]/div/main/div/table/tr[{counter}]/td[1]/div/span[1]").text
            class_name = driver.find_element(selenium.By.XPATH, f"/html/body/div[2]/div[2]/div/main/div/table/tr[{counter}]/td[2]").text
            date_due = driver.find_element(selenium.By.XPATH, f"/html/body/div[2]/div[2]/div/main/div/table/tr[{counter}]/td[3]/time").text
            checkbox = driver.find_element(selenium.By.XPATH, f"/html/body/div[2]/div[2]/div/main/div/table/tr[{counter}]/td[4]/input")
            if checkbox.is_selected():
                checked = True
            else:
                checked = False

            if class_name not in scheduledItems:
                scheduledItems[class_name] = []

            scheduledItems[class_name].append({
                "assignement": assignment_name,
                "due_date": date_due,
                "completed": checked
            })

        except:
            break
        counter += 2

    #Date time: w-22 outer div with an inner div of <time 

    #print(scheduledItems)
    return scheduledItems