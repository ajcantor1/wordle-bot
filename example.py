import pandas as pd
from argparse import ArgumentParser
from game_simulator import GameSimulator

class ImplGameSimulator(GameSimulator):

    def get_next_guess(self):
        

        df = pd.read_csv('score.csv')        
        for idx, letter in self.correct_letters:
            df = df[df['guess'].str[idx] == letter]

        for letter in self.absent_letters:
            df = df[~(df['guess'].str.contains(letter))]     

        for idx, letter in self.present_letters:
            df = df[df['guess'].str.contains(letter)]
            df = df[~(df['guess'].str[idx] == letter)]

        for guess in self.guesses:
            df = df[df['guess'] != guess]

        df = df[df['mean q(g)']==df['mean q(g)'].min()]
        df = df[df['var q(g)']==df['var q(g)'].min()]
        return  df['guess'].item()


def get_args():
    
    parser = ArgumentParser()

    parser.add_argument(
        '-d', 
        '--driver', 
        help="path to driver file", 
        type=str, 
        default='./chromedriver'
    )

    parser.add_argument(
        '-u', 
        '--url', 
        help="url", 
        type=str, 
        default='https://www.nytimes.com/games/wordle/index.html'
    )

    parser.add_argument(
        '-f', 
        '--first_guess', 
        help="first guess", 
        type=str, 
        default='slate'
    )

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = get_args()
    gameSimulator = ImplGameSimulator(args.driver, args.url, args.first_guess)
    gameSimulator.run()