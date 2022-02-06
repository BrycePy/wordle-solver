import wordle
import words
import math
from multiprocessing import Pool
import tqdm
import matplotlib.pyplot as plt
import robot


def calculate_entropy(vw):
    pattern_table = dict()
    for pg in words.words:
        pattern = wordle.Guess(pg, vw).get_hint_tuple()
        pattern = tuple(pattern)
        pattern_table[pattern] = pattern_table.get(pattern, 0) + 1
    prob = [pattern_table[x]/len(words.words) for x in pattern_table]
    entropy = sum(p*math.log2(1/p) for p in prob)
    return entropy

def calculate_entropy_table(valid_words):
    #TODO fix this shit i think its wrong.
    with Pool(16) as p:
        #r = list(tqdm.tqdm(p.imap(calculate_entropy, valid_words), total=len(valid_words)))
        r = list(p.imap(calculate_entropy, valid_words))

    sorted_entropy = sorted(zip(valid_words, r), key=lambda x: x[1])

    for w, p in sorted_entropy[-5:]:
        print(w, p)
    
    return sorted_entropy


def variance(data):
    n = len(data)
    mean = sum(data) / n
    deviations = [(x - mean) ** 2 for x in data]
    variance = sum(deviations) / n
    return variance

class Robot(wordle.Player):
    def __init__(self):
        super().__init__()
        self.known_pos = [list() for _ in range(5)]
        self.contains = set()
        self.not_contains = set()

    def get_possible(self, game_state):
        for guess in game_state:
            for i, data in enumerate(guess):
                char, status = data
                if status == 0:
                    self.not_contains.add(char)
                    if isinstance(self.known_pos[i], list):
                        self.known_pos[i].append(char)
                elif status == 1:
                    self.contains.add(char)
                    if isinstance(self.known_pos[i], list):
                        self.known_pos[i].append(char)
                elif status == 2:
                    self.known_pos[i] = char

        for known in self.known_pos:
            if not isinstance(known, list):
                if known in self.not_contains:
                    self.not_contains.remove(known)

        self.not_contains.difference_update(self.contains)

        def valid(word):
            for i, c in enumerate(word):
                if c in self.not_contains:
                    return False
                if isinstance(self.known_pos[i], list):
                    if c in self.known_pos[i]:
                        return False
                else:
                    if c != self.known_pos[i]:
                        return False
            for c in self.contains:
                if c not in word:
                    return False
            return True

        possible_words = words.words.copy()
        possible_words = [word for word in possible_words if valid(word)]

        return possible_words

    def next_guess(self, game_state):
        self.print_game(game_state)
        if len(game_state) == 0:
            return "tares"

        possible_words = self.get_possible(game_state)
        print(possible_words)

        cache = calculate_entropy_table(possible_words)
        for i in range(min(len(cache), 5)):
            print(i, cache[-1-i][0])

        return cache[-1-int(input("index>"))][0]

    # def game_end(self, won, game_state):
    #     return


def simulate(word):
    player = Robot()
    game = wordle.Wordle(player, word)
    result = game.play()
    return result


def main():
    r = list(tqdm.tqdm(map(simulate, words.answers), total=len(words.answers)))

    fail = sum(1 for x in r if x > 6)

    print("average", sum(r)/len(r))
    print("min", min(r))
    print("max", max(r))
    print("fail_rate", fail, fail/len(r))
    print("standard d", variance(r)**0.5)

    n = 10
    values_count = [r.count(x) for x in range(n)]

    plt.bar(range(n), values_count)
    plt.show()

def play():
    player = robot.Robot()
    game = wordle.Wordle(player, "words")
    game.play_manual()

if __name__ == "__main__":
    #main()
    play()