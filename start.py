import wordle
import words

import robot_3blue1brown
import robot_top15

import tqdm
from multiprocessing import Pool
import matplotlib.pyplot as plt
import random

player_list = {
    "manual": wordle.Player,
    "3blue1brown": robot_3blue1brown.Robot,
    "top15char": robot_top15.Robot
}

def simulate(player_class, word):
    player = player_class()
    game = wordle.Wordle(player, word)
    result = game.play()

def solve(player_class):
    player = player_class()
    game = wordle.Wordle(player, "words")
    game.play_manual(False)

if __name__ == "__main__":
    print("Mode:")
    print("0. play an unknown word")
    print("1. play a specific word")
    print("2. play a random word")
    mode = int(input(">"))

    print("")
    print("Player:")
    for player_index, player_name in enumerate(player_list):
        print(f"{player_index}. {player_name}")
    player = int(input(">"))
    player_class = list(player_list.items())[player][1]

    if mode == 0:
        solve(player_class)

    elif mode == 1:
        simulate(player_class, input("word to simulate >"))

    elif mode == 2:
        simulate(player_class, random.choice(words.answers))
