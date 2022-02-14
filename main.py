from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.select import By
import logging as log
from json import loads
from time import sleep
from random import choice
from string import ascii_letters, digits

log.basicConfig(format='| %(levelname)s : %(asctime)s | = %(messages)s =')

get_random_name = lambda n : ''.join(choice(ascii_letters + digits) for _ in range(n))

with Firefox() as driver:
    hooks = loads(open('./hooks.json', encoding='utf-8').read())
    log.info('Hooks loaded.')
    driver.get('https://eventdata.uk/Delegate/LACA2022.aspx')

    first_name, last_name, job_title, company_name = [get_random_name(5) for _ in range(4)] 

    driver.find_element(By.CSS_SELECTOR, hooks['first_name']).send_keys(first_name)
    driver.find_element(By.CSS_SELECTOR, hooks['last_name']).send_keys(last_name)
    driver.find_element(By.CSS_SELECTOR, hooks['job_title']).send_keys(job_title)
    driver.find_element(By.CSS_SELECTOR, hooks['company_name']).send_keys(company_name)
    driver.find_element(By.CSS_SELECTOR, hooks['telephone']).send_keys('+447458164455')
    driver.find_element(By.CSS_SELECTOR, hooks['email']).send_keys('melophile34@gmail.com')
    driver.find_element(By.CSS_SELECTOR, hooks['cemail']).send_keys('melophile34@gmail.com')
    driver.find_element(By.CSS_SELECTOR, hooks['membership']).click()
    
    # Fetch the 4 LAC membership types
    # driver.execute_script('''return Array.from(document.querySelector('select[name="Analysis.4"]').children).splice(1)''')
    # Fetch all the rows inside the membership table
    # driver.execute_script('''document.querySelector('#fullmember').querySelector('table').querySelector('tbody').querySelectorAll('tr')''')

    sleep(10)