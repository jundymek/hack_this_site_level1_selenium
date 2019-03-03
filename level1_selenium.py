import os
from selenium import webdriver
from bs4 import BeautifulSoup
from itertools import permutations
from credentials import LOGIN, PASSWORD


class Level1:

    def __init__(self):
        with open('wordlist.txt', 'r') as f:
            self.wordlist = [word.strip() for word in f.readlines()]
        if os.uname()[0] == 'Linux':
            self.driver = webdriver.Chrome(os.getcwd() + '/driver-linux/chromedriver')
        else:
            self.driver = webdriver.Chrome(os.getcwd() + '/driver-mac/chromedriver')

    def login(self):
        """
        Login to hackthissite.org using credentials from credentials.py file
        """
        self.driver.get('https://www.hackthissite.org')
        login = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        login.send_keys(LOGIN)
        password.send_keys(PASSWORD)
        self.driver.find_element_by_name('btn_submit').click()

    def get_words_to_unscramble(self):
        """
        Gets list of words to unscrable.
        :return: list
        """
        self.driver.get('https://www.hackthissite.org/missions/prog/1/')
        html = self.driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        x = soup.find_all('li')[-10:]
        words_to_unscramble = [word.get_text().strip() for word in x]
        return words_to_unscramble

    def get_answer(self, scrambled_words):
        """
        Unscrambles every word in list and returns answer.
        :param scrambled_words:
        :return: str
        """
        result_list = []
        for word in scrambled_words:
            for z in permutations(word):
                if ''.join(z) in self.wordlist:
                    if ''.join(z) not in result_list:
                        result_list.append(''.join(z))
        return ','.join(x for x in result_list)

    def submit_answer(self, result):
        """
        Submits answer to proper field.
        :param result:
        :return: None
        """
        final = self.driver.find_element_by_name('solution')
        final.send_keys(result)
        self.driver.find_element_by_name('submitbutton').click()


if __name__ == '__main__':
    main = Level1()
    main.login()
    words = main.get_words_to_unscramble()
    answer_words = main.get_answer(words)
    main.submit_answer(answer_words)
