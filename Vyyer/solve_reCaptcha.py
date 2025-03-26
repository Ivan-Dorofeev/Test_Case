import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class NJMVCAddressUpdater:
    def __init__(self, captcha_service_api_key=None, driver_path=None, headless=False):
        """
        :param captcha_service_api_key: API ключ сервиса решения капчи
        :param driver_path: Путь к chromedriver
        :param headless: Режим без отображения браузера
        """
        self.captcha_api_key = captcha_service_api_key
        self.driver = self._init_driver(driver_path, headless)
        self.wait = WebDriverWait(self.driver, 20)

    def _init_driver(self, driver_path, headless):
        """Настройка и запуск браузера"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('detach', True) # чтобы не закрывалось окно браузера

        service = webdriver.ChromeService(executable_path=driver_path) if driver_path else None
        return webdriver.Chrome(service=service, options=options)

    def _get_recaptcha_solution(self, site_key, page_url):
        """
        Получение решения reCAPTCHA через сервис 2Captcha

        :param site_key: Ключ сайта для reCAPTCHA
        :param page_url: URL страницы с капчей
        :return: Токен решения или None
        """
        if not self.captcha_api_key:
            print("Ошибка: Не указан API ключ сервиса капчи")
            return None

        # Отправка капчи в сервис
        captcha_url = "http://2captcha.com/in.php"
        params = {
            'key': self.captcha_api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }

        try:
            response = requests.get(captcha_url, params=params)
            data = response.json()
            print('captcha_url data =', data)
            if data['status'] != 1:
                print(f"Ошибка сервиса капчи: {data.get('request', 'Unknown error')}")
                return None

            captcha_id = data['request']
            print(f"Капча отправлена на решение, ID: {captcha_id}")

            # Ожидание решения
            result_url = "http://2captcha.com/res.php"
            for _ in range(30):  # Максимум 30 попыток с интервалом 5 секунд
                time.sleep(5)
                result_params = {
                    'key': self.captcha_api_key,
                    'action': 'get',
                    'id': captcha_id,
                    'json': 1
                }
                result_response = requests.get(result_url, params=result_params)
                result_data = result_response.json()
                print('result solution captha = ', result_data)

                if result_data['status'] == 1:
                    print("Капча успешно решена!")
                    return result_data['request']
                elif result_data['request'] != 'CAPCHA_NOT_READY':
                    print(f"Ошибка решения капчи: {result_data['request']}")
                    return None

            print("Время ожидания решения капчи истекло")
            return None

        except Exception as e:
            print(f"Ошибка при работе с сервисом капчи: {str(e)}")
            return None

    def _solve_recaptcha(self):
        """Решение reCAPTCHA на странице"""
        try:
            # Получаем ключ сайта и URL
            site_key = self.driver.find_element(By.CSS_SELECTOR, 'div.g-recaptcha[data-sitekey]').get_attribute('data-sitekey')
            page_url = self.driver.current_url
            print(f"Найдена reCAPTCHA, ключ сайта: {site_key}")
            # Получаем решение от сервиса
            solution = self._get_recaptcha_solution(site_key, page_url)
            if not solution:
                return False


            # Вводим решение в страницу
            print('Вводим решение в страницу')
            self.driver.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML = '{solution}';")
            time.sleep(1)
            return True

        except Exception as e:
            print(f"Ошибка при решении reCAPTCHA: {str(e)}")
            return False

    def submit_address_change(self, zip_code, license_id, dob):
        """
        Отправка формы смены адреса

        :param zip_code: Почтовый индекс
        :param license_id: Номер водительского удостоверения
        :param dob: Дата рождения (MM/DD/YYYY)
        :return: Статус и сообщение
        """
        try:
            # Открываем страницу
            self.driver.get("https://mymvc.state.nj.us/address-change/doblogin.xhtml")

            # Заполняем поля
            self.driver.find_element(By.ID, "loginForm:zip").send_keys(zip_code)
            self.driver.find_element(By.ID, "loginForm:dln").send_keys(license_id)
            self.driver.find_element(By.ID, "loginForm:dob").send_keys(dob)

            # Проверяем наличие капчи
            try:
                recaptcha_div = self.driver.find_element(By.CSS_SELECTOR, 'div.g-recaptcha')
                print("Обнаружена reCAPTCHA, решаем...")
                if not self._solve_recaptcha():
                    return False, "Не удалось решить reCAPTCHA"
            except:
                print("reCAPTCHA не обнаружена")


            # делаем кнопку Login кликабельной
            submit_btn = self.driver.find_element(By.ID, "loginForm:login")
            self.driver.execute_script('arguments[0].removeAttribute("disabled");', submit_btn)
            time.sleep(1)

            # Отправляем форму
            print('Кликаем по форме')
            submit_btn = self.driver.find_element(By.ID, "loginForm:login")
            submit_btn.click()

            return True, 'Готово'
        except Exception as e:
            return False, f"Ошибка: {str(e)}"

    def close(self):
        """Закрытие браузера"""
        self.driver.quit()


# Пример использования
if __name__ == "__main__":
    # Конфигурация
    CAPTCHA_API_KEY = "ac7d0af7a0b3a10023e55b8c731bd371"  # API ключ сервиса reCaptcha
    ZIP_CODE = "87534"  # Пример почтового индекса
    LICENSE_ID = "S90090186154952"  # Пример номера водительского удостоверения
    DOB = "04/06/1995"  # Пример даты рождения

    # Инициализация
    print("Запуск автоматизатора смены адреса NJ MVC...")
    updater = NJMVCAddressUpdater(
        captcha_service_api_key=CAPTCHA_API_KEY,
        headless=False
    )

    try:
        # Отправка формы
        print("Отправка данных...")
        success, message = updater.submit_address_change(ZIP_CODE, LICENSE_ID, DOB)

        # Вывод результата
        print("\nРезультат:")
        print("Успех:", success)
        print("Сообщение:", message)
        time.sleep(10)
    except KeyboardInterrupt:
        print("\nПрервано пользователем")
