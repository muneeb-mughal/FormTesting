#region IMPORTS
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.select import By
import logging as log
from json import loads
from time import sleep
from random import choice
from string import ascii_letters, digits
#endregion

class FormTestBot(object):
    def __init__(self, form_page_url: str, hooks_path: str) -> None:
        self.get_random_text = lambda n: ''.join(choice(ascii_letters + digits) for _ in range(n))
        self.hooks = loads(open(hooks_path, encoding='utf-8').read())
        self.url = form_page_url
        log.info('Web Element Hooks loaded...')

        self.table_id_map = {
            'Full Member': '#fullmember',
            'Non Member (school meal provider)': '#nonmemberschoolprovider',
            'Associate Member': '#associatemember',
            'Non Member (supplier)': '#nonmember',
        }

        with Firefox() as self.driver:
            membership_types = self.fetch_membership_types()
            self.test_form(list(map(lambda m: m.get_attribute('textContent'), membership_types)))

    def fetch_membership_types(self) -> list:
        '''
            Parameters: 
                None
            Returns:
                List of `WebElements`
            
            Description:
                Navigates the webdriver to the parameter `url` and searches for membership types using
                the hook `membership`
        '''
        self.driver.get(self.url)
        return self.driver.execute_script('''return Array.from(document.querySelector('select[name="Analysis.4"]').children).splice(1)''')

    def test_form(self, membership_types: list[str]) -> int:
        '''
            Parameters: 
                `membership_types` -> List of strings defining the membership types to be tested
            Returns:
                An integer `n` representing the total number of forms successfuly tested
            
            Description:
                Navigates the webdriver to the parameter `url` and fills in all the required
                fields. For each `membership type`, selects one of the membership packages and
                proceed to submit the form, this process is repeated till all the membership
                packages and types have exhausted.
        '''
        form_test_count = 0

        for membership_type in membership_types:
            self.driver.get(self.url)
            self.driver.find_element(By.XPATH, f"""//option[text()='{membership_type.strip()}']""").click() #! Select the right membership type
            table_rows_count = len(self.driver.execute_script('''return Array.from(document.querySelectorAll('#fullmember table tbody tr')).splice(1)''')) #! Count the total no of membership packages

            for i in range(table_rows_count):
                self._submit_form(membership_type, i)
                sleep(5)

    def _submit_form(self, membership_type: str, row_selection_index: int) -> bool:
        self.driver.get(self.url)
        self._fill_required_fields()
        self.driver.find_element(By.XPATH, f"""//option[text()='{membership_type.strip()}']""").click() #! Open the Membership Type combo box
        table_rows = self.driver.execute_script('''return Array.from(document.querySelectorAll('#fullmember table tbody tr')).splice(1)''') #! Read all the table rows
        table_rows[row_selection_index].find_elements(By.CSS_SELECTOR, 'input')[-1].click()  #! Select the respective Full Member Package

        self.driver.find_element(By.CSS_SELECTOR, self.hooks['payment_method']).click()
        choice(self.driver.find_elements(By.CSS_SELECTOR, self.hooks['payment_method_options'])).click()
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['agree']).click()
        self.driver.execute_script('arguments[0].click()', self.driver.find_element(By.CSS_SELECTOR, self.hooks['next']))

    def _fill_required_fields(self) -> None:
        '''
            Parameters: 
                None
            Returns:
                None
            Description:
                Fills in all the required fields with randomly generated strings
        '''
        first_name, last_name, job_title, company_name, street, city, zipcode = [self.get_random_text(7) for _ in range(7)] 

        self.driver.find_element(By.CSS_SELECTOR, self.hooks['first_name']).send_keys(first_name)
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['last_name']).send_keys(last_name)
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['job_title']).send_keys(job_title)
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['company_name']).send_keys(company_name)
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['telephone']).send_keys('+447458164455')
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['email']).send_keys('melophile34@gmail.com')
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['cemail']).send_keys('melophile34@gmail.com')
        self.driver.find_element(By.XPATH, '//a[text()="Enter manually"]').click() #! Click the enter manually link
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['zip']).send_keys(zipcode)
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['city']).send_keys(city)
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['street']).send_keys(street)
        
        self.driver.find_element(By.CSS_SELECTOR, self.hooks['membership']).click()


def main():
    FormTestBot('https://eventdata.uk/Delegate/LACA2022.aspx', './hooks.json')

if __name__ == '__main__':
    main()