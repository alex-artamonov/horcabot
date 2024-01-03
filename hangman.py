from random import choice
import pseudographics as pg

# imgs = [s06, s05, s04, s03, s02, s01, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]
# imgs = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]
# imgs = [pg.s0, pg.s1, pg.s2, pg.s3, pg.s4,
#         pg.s5, pg.s6, pg.s7, pg.s8, pg.s9, pg.s10, pg.s11]

FILENAME = "words.txt"
LINK = "https://www.wordreference.com/es/en/translation.asp?spen="
ACENTOS = {"E": "eé",
           "A": "aá",
           "U": "uüú",
           "N": "nñ",
           "I": "ií",
           "O": "oó"}


class Hangman:
    def __init__(self, id: int = 0) -> None:
        self.id = id
        self.mistake_nbr = 0
        self.mask = "----"
        self.used = []
        # self.word = self._get_word()
        self.word = 'anón'.upper()
        self.word = 'añan'.upper()
        self.finished = False
        self.imgs = [
            pg.s0,
            pg.s1,
            pg.s2,
            pg.s3,
            pg.s4,
            pg.s5,
            pg.s6,
            pg.s7,
            pg.s8,
            pg.s9,
            pg.s10,
            pg.s11,
        ]
        print(self.word)

    def letter_in(self):
        if self.letter in "AEIOUN":
            print(ACENTOS[self.letter].upper())
            for letter in ACENTOS[self.letter].upper():
                if letter in self.word:
                    self.letter = letter
                    return True
            # return any([acento in self.word for acento in ACENTOS[self.letter].upper()])
        return self.letter in self.word

    def _get_word(self):
        lst = []
        with open(FILENAME) as read:
            for line in read:
                lst.append(line.strip())
        return choice(lst).upper()

    def get_letter(self, prompt: str = "Adivina una letra\n"):
        output = self.input(prompt)
        return output

    def get_response(self, letter: str):
        if self.finished:
            return "Juego terminado"
        letter = letter.upper()
        if len(letter) > 1:
            raise ValueError("Sólo una letra!")
        if letter in self.used:
            # output = 'Try again, this letter has been used already.'
            return "Inténtalo de nuevo, esta letra ya ha sido utilizada."
        self.used.append(letter)
        self.letter = letter
        if self.letter_in():
            mask_lst = list(self.mask)
            lst = [i for i in range(len(self.word)) if self.word[i] == self.letter]
            for c in lst:
                mask_lst[c] = self.letter
            self.mask = "".join(mask_lst)
            if not "-" in mask_lst:
                self.finished = True
                output = "Has ganado!\n" + "<b>" + self.word + "</b>"
                return output
            return self.mask
        else:
            if len(self.imgs) > self.mistake_nbr + 1:
                output = self.imgs[self.mistake_nbr] + "\n" + self.mask
            else:
                output = (
                    self.imgs[-1] + "\n" + "Has perdido!\n" + "<b>" + self.word + "</b>"
                )
                self.finished = True
            self.mistake_nbr += 1
        return output

    def play(self):
        while not self.finished:
            letter = self.get_letter()
            try:
                game.display(game.get_response(letter))
            except ValueError as e:
                game.display(e)

    def play_again(self):
        while True:
            reply = self.get_letter('Want to play again? ("Y/n")\n')
            if reply.upper() in ("Y", ""):
                return True
            elif reply.upper() == "N":
                return False


if __name__ == "__main__":
    game = Hangman()
    # game.finished = True
    game.input = input
    game.display = print
    # game.start()
    game.play()
