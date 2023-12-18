from random import choice
import pseu as pg

# imgs = [s06, s05, s04, s03, s02, s01, s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]
# imgs = [s0, s1, s2, s3, s4, s5, s6, s7, s8, s9]
# imgs = [pg.s0, pg.s1, pg.s2, pg.s3, pg.s4,
#         pg.s5, pg.s6, pg.s7, pg.s8, pg.s9, pg.s10, pg.s11]

FILENAME = "words.txt"
LINK = "https://www.wordreference.com/es/en/translation.asp?spen="

class Hangman:
    def __init__(self, id: int) -> None:
        self.id = id
        self.mistake_nbr = 0
        self.mask = "----"
        self.used = []
        self.word = self._get_word()
        self.finished = False
        self.imgs = [pg.s0, pg.s1, pg.s2, pg.s3, pg.s4,
        pg.s5, pg.s6, pg.s7, pg.s8, pg.s9, pg.s10, pg.s11]

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
        letter = letter.upper()
        if self.finished:
            return "Juego terminado"
        if len(letter) > 1:
            raise ValueError("Sólo una letra!")
        if letter in self.used:
            # output = 'Try again, this letter has been used already.'
            return "Inténtalo de nuevo, esta letra ya ha sido utilizada."
        self.used.append(letter)
        if letter in self.word:
            mask_lst = list(self.mask)
            lst = [i for i in range(len(self.word)) if self.word[i] == letter]
            for c in lst:
                mask_lst[c] = letter
            self.mask = "".join(mask_lst)
            if not "-" in mask_lst:
                self.finished = True
                output = "Has ganado!\n" + "<b>" + self.word + "</b>"
                return output
            return self.mask
            if not "-" in mask_lst:
                if self.play_again():
                    self.start()
                else:
                    return
        else:
            if len(self.imgs) > self.mistake_nbr + 1:
                output = self.imgs[self.mistake_nbr] + "\n" + self.mask
            else:
                output = self.imgs[-1] + "\n" + "Has perdido!\n" + "<b>" + self.word + "</b>"
                self.finished = True
            self.mistake_nbr += 1
        return output

    def start(self):
        lst = []

        with open(FILENAME) as read:
            for line in read:
                lst.append(line.strip())
        word = choice(lst)
        mask_lst = list(self.mask)
        image_counter = 0
        while True:
            letter = self.get_letter()
            if letter in self.used:
                self.display("Inténtalo de nuevo, esta letra ya ha sido utilizada.")
            else:
                if letter in word:
                    self.used.append(letter)
                    lst = [i for i in range(len(word)) if word[i] == letter]
                    for c in lst:
                        mask_lst[c] = letter
                    self.display("".join(mask_lst))
                    if not "-" in mask_lst:
                        if self.play_again():
                            self.start()
                        else:
                            return
                else:
                    self.used.append(letter)
                    self.display(self.imgs[image_counter])
                    self.display("".join(mask_lst))
                    image_counter += 1
                    if image_counter == len(self.imgs):
                        self.display(word)
                        if self.play_again():
                            self.start()
                        else:
                            return

    def play_again(self):
        while True:
            reply = self.get_letter('Want to play again? ("Y/n")\n')
            if reply.upper() in ("Y", ""):
                return True
            elif reply.upper() == "N":
                return False


if __name__ == "__main__":
    game = Hangman(1)
    game.input = input
    game.display = print
    game.start()
