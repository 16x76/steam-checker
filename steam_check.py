from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.common.exceptions import TimeoutException
import time

def login_f(browser, login):
    global login_state
    try:
        login_elem = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input'))
        )
        login_elem.send_keys(login, Keys.RETURN)
        login_state = 1
    except NoSuchElementException:
        print("Поле логин не найдено")
def password_f(browser, password):
    global password_state
    try:
        login_elem = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input'))
        )
        login_elem.send_keys(password, Keys.RETURN)
        password_state = 1
    except NoSuchElementException:
        print("Поле пароль не найдено")

def link_f(browser):
    link = browser.current_url
    base_link = link.split("/profiles/")[0] + "/profiles/"
    return base_link

def edit_prof(browser):

    if edit == 1:       
        prof_edit = browser.find_element(btn)
        prof_edit.click()
        time.sleep(5)
        if EC.presence_of_element_located(button_dialog):
            prof_save = browser.find_element(button_dialog)
            prof_save.click()
            time.sleep(5)
            if browser.current_url.startswith("https://steamcommunity.com/profiles/") and "/edit/info" in browser.current_url:
                new_url = browser.current_url.replace("/edit/info", "")
                browser.get(new_url)  # Переходим на новый URL
                time.sleep(5)
        
def vac_check_f():
    try:
        vac_class = (By.CLASS_NAME, 'profile_ban')
        WebDriverWait(browser, 2).until(EC.presence_of_element_located(vac_class))
        vac_var = 1
    except TimeoutException:
        vac_var = 0
    return vac_var
logoutselector = (By.XPATH, '/html/body/div[1]/div[7]/div[1]/div/div[3]/div/div[2]/div/a[4]')

def main(browser):
    global btn
    global button_dialog

    with open('credentials.txt', 'r') as f:
        for line in f:
            login, password = line.strip().split(':')
            print(f"Login: {login}, Password: {password}")
            login_state = 0
            password_state = 0
            global edit
            btn = (By.CSS_SELECTOR, "#btn")
            button_dialog = (By.CSS_SELECTOR, "button.DialogButton:nth-child(1)")

            if login_state == 0 and password_state == 0:
                login_f(browser, login)
                password_f(browser, password)
                login_state = 1
                password_state = 1
                time.sleep(5)
                if link_f(browser) == 'https://steamcommunity.com/profiles/':
                    print("Вход выполнен успешно.")
                if EC.presence_of_element_located(btn):
                    edit = 1
                    edit_prof(browser)
                else:
                    edit = 0
                if vac_check_f() == 1:
                    print("На аккаунте бан")
                    with open('has_vac.txt', 'a') as output_file:
                        output_file.write(f"{login}:{password}\n")
                    logout = browser.find_element(By.XPATH, '//*[@id="account_pulldown"]')
                    logout.click()
                    logout_fr = WebDriverWait(browser, 2).until(
    EC.element_to_be_clickable(logoutselector)  # Используем условие ожидания
)
                    logout_fr.click()
                    time.sleep(5)
                    browser.get('https://steamcommunity.com/login/home/?goto=')
                        
                else:
                    print("На аккаунте нет бана")
                # Записываем успешные логин и пароль в файл output.txt
                    with open('output.txt', 'a') as output_file:
                        output_file.write(f"{login}:{password}\n")
                          # Выход из функции main после успешного входа
                    logout = browser.find_element(By.XPATH, '//*[@id="account_pulldown"]')
                    logout.click()
                    logout_fr = WebDriverWait(browser, 2).until(
    EC.element_to_be_clickable(logoutselector)  # Используем условие ожидания
)
                    logout_fr.click()
                    time.sleep(5)
                    browser.get('https://steamcommunity.com/login/home/?goto=')
                

        

if __name__ == "__main__":
    browser = webdriver.Firefox()
    browser.get('https://steamcommunity.com/login/home/?goto=')
    main(browser)