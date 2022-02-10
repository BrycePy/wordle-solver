import wordle
import words
import math
from multiprocessing import Pool
import tqdm
import matplotlib.pyplot as plt
from colored import fg, bg, attr

def calculate_entropy(pipe):
    valid_words, vw = pipe
    pattern_table = dict()
    for pg in valid_words:
        pattern = wordle.Guess(pg, vw).get_hint_tuple()
        pattern = tuple(pattern)
        pattern_table[pattern] = pattern_table.get(pattern, 0) + 1
    prob = [pattern_table[x]/len(valid_words) for x in pattern_table]
    entropy = sum(p*math.log2(1/p) for p in prob)
    return entropy

def calculate_entropy_table(valid_words):
    #TODO fix this shit i think its wrong.
    with Pool(16) as p:
        #r = list(tqdm.tqdm(p.imap(calculate_entropy, valid_words), total=len(valid_words)))
        data = ((valid_words,word) for word in words.words)
        r = list(p.imap(calculate_entropy, data))

    sorted_entropy = sorted(zip(words.words, r), key=lambda x: x[1])

    for w, p in sorted_entropy[-5:]:
        print(w, p)
    
    return sorted_entropy

# this class implement solving method based on 3blue1brown method.
# next guess is picked based on word's entropy.
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
        print(game_state)
        self.print_game(game_state)
        if len(game_state) == 0:
            return "tares"

        possible_words = self.get_possible(game_state)
        print(possible_words)
        if len(possible_words)==1:
            return possible_words[0]

        cache = calculate_entropy_table(possible_words)
        return cache[-1][0]

if __name__ == "__main__":

    def variance(data):
        n = len(data)
        mean = sum(data) / n
        deviations = [(x - mean) ** 2 for x in data]
        variance = sum(deviations) / n
        return variance

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
        player = Robot()
        game = wordle.Wordle(player, "words")
        game.play_manual()


    #simulate("tests")
    main()
    #play()