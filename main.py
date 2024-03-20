from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path
from datetime import datetime
from time import sleep


def selenium_options():
    svc = Service(executable_path=binary_path)
    driver = webdriver.Chrome(service=svc)
    return driver


def get_friend_number(spy_mode, friend_number, driver):
    if not spy_mode:
        friend_number_url = "https://web.whatsapp.com/send?phone=" + friend_number + "&text=Online olduğun vaxtı xəbər verəcəyəm :)))"
    else:
        friend_number_url = "https://web.whatsapp.com/send?phone=" + friend_number
    check = False
    attemp = 0
    while True:
        attemp += 1
        if not check:
            driver.get(friend_number_url)
            try:
                last_seen = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/header/div[2]/div[2]')))
                sleep(4)
            except Exception as err:
                print(err)
            else:
                sleep(2)
                if last_seen:
                    while True:
                        if last_seen.text.capitalize() == 'Online':
                            check = True
                            print("Attemp >>> ", attemp)
                            last_online_time = datetime.now().strftime('%H:%M:%S')
                            if last_online_time and not spy_mode:
                                print("False spy Mode")
                                
                                number_text_box = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')))
                                sleep(2)
                                number_text_box.click()
                                sleep(2)
                            return last_online_time
                        else:
                            sleep(2)


def get_my_number(last_online_time, my_number, driver):
    my_number_url = f'https://web.whatsapp.com/send?phone={my_number}&text={last_online_time} vaxtında online oldu...'
    sent = False
    for i in range(3):
        if not sent:
            driver.get(my_number_url)
            try:
                number_text_box = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')))
            except Exception as err:
                print(err)
            else:
                sleep(2)
                number_text_box.click()
                sleep(2)
                sent = True
                print(f"{i}/3 OK")
                return True
                        

app = FastAPI()

@app.post("/run-the-spy-bot")
def run_the_spy_bot(friend_number: str, my_number: str, spy_mode: bool):
    driver = selenium_options()
    driver.get("https://web.whatsapp.com")
    try:
        while True:
            last_online_time = get_friend_number(spy_mode, friend_number, driver)
            if last_online_time:
                get_my_number(last_online_time, my_number, driver)
    except Exception as err:
        driver.quit()
        return {"error": err}