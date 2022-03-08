from abc import ABC, abstractmethod
from selenium import webdriver
from pyshadow.main import Shadow
from enum import Enum
from time import sleep

GAME_ROUNDS = 6
WORD_LENGTH = 5

class Evaluation(Enum):
    PRESENT = "present"
    ABSENT  = "absent"
    CORRECT = "correct"

class GameSimulator(ABC):

    def __init__(self, driver_file, url, first_guess):

        self.correct_letters = []
        self.present_letters = []
        self.absent_letters  = []

        driver = webdriver.Chrome(executable_path=driver_file)
        driver.get(url)

        self.shadow = Shadow(driver)
        self.__sleep(seconds=15)
        self.shadow.find_element(".close-icon").click()

        self.guesses = [first_guess]

    @abstractmethod
    def get_next_guess(self):
        pass

    def evaluate_guess(self, last_guess):
    
        row = f'game-row[letters="{last_guess}"]>game-tile'

        game_tiles = self.shadow.find_elements(row)
    
        for idx, game_tile in enumerate(game_tiles):
            
            letter = self.shadow.get_attribute(game_tile, 'letter')
            evaluation = Evaluation(self.shadow.get_attribute(game_tile, 'evaluation'))
        
            if evaluation == Evaluation.PRESENT:
                present_letter = (idx, letter) 
                if present_letter not in self.present_letters:
                    self.present_letters.append(present_letter)
            
            elif evaluation == Evaluation.CORRECT:
                correct_letter = (idx, letter) 
                if correct_letter not in self.correct_letters:
                    self.correct_letters.append(correct_letter)


            elif evaluation == Evaluation.ABSENT:
                self.absent_letters.append(letter)

    def enter_guess(self, guess):
        for letter in guess:
            self.shadow.find_element(f'button[data-key="{letter}"]').click()
        self.shadow.find_element('button[data-key="↵"]').click()

    def run(self):

        for game_round in range(GAME_ROUNDS):
            self.enter_guess(self.guesses[game_round])
            self.evaluate_guess(self.guesses[game_round])

            if len(self.correct_letters) == WORD_LENGTH:
                break

            self.__sleep()
            self.guesses.append(self.get_next_guess())

    def __sleep(self, seconds=2):
        self.shadow.set_explicit_wait(5, 2)
        sleep(seconds)