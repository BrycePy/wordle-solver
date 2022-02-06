import words
from colored import fg, bg, attr

class Guess:
    def __init__(self, target_word, guess):
        self.target_word = target_word
        self.guess = guess

    def is_correct(self):
        return (self.target_word == self.guess)

    def get_hint(self):
        temp = list(self.target_word)
        hint = [0, 0, 0, 0, 0]
        for i, char in enumerate(self.guess):
            if char == temp[i]:
                hint[i] = 2
                temp[i] = None
        for i, char in enumerate(self.guess):
            if hint[i] == 2: continue
            if char in temp:
                at = temp.index(char)
                hint[i] = 1
                temp[at] = None
        return list(zip(self.guess, hint))

class Player:
    def next_guess(self, game_state):
        self.print_game(game_state)
        return input("guess>")

    def game_output(self, text):
        print(text)

    def game_end(self, won, game_state):
        self.print_game(game_state)
        print("ended", won)
        return

    def print_game(self, game_state):
        color_templete = [
                        fg("white")+bg("dark_gray"),
                        fg("white")+bg(94),
                        fg("white")+bg("green"),
                        ]
        print("")
        for guess in game_state:
            print("".join(f"{color_templete[c[1]]} {c[0]} " for c in guess) + attr('reset'))

class Wordle:
    def __init__(self, player, word):
        self.game_state = []
        self.player = player
        self.target_word = word
        self.ended = False

    def next(self):
        player_guess = self.player.next_guess(self.game_state).lower()
        guess_obj = Guess(self.target_word, player_guess)
        self.game_state.append(guess_obj.get_hint())
        if guess_obj.is_correct():
            self.end(True)
        # elif len(self.game_state)==6:
        #     self.end(False)

    def play(self, word=None):
        self.set_word(word)
        round = 0
        while not self.ended:
            round += 1
            self.next()
            if self.ended: break
        return round

    def end(self, won):
        self.player.game_end(won, self.game_state)
        self.ended = True

    def set_word(self, word=None):
        if word:
            self.target_word = word
            self.game_state.clear()
            self.ended = False

    def clone(self):
        cloned = Wordle(self.player, self.target_word)
        cloned.game_state = self.game_state.copy()
        cloned.ended = self.ended
        return cloned

if __name__ == "__main__":
    print(len(words.words), len(words.answers))
    player = Player()
    game = Wordle(player, "hyena")
    game.play()