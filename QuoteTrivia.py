import requests
from bs4 import BeautifulSoup
import random
from pyfiglet import figlet_format
from termcolor import colored
import tkinter as tk
from PIL import ImageTk, Image



class Ascii():
	""" generate colorful ascii art text """

	def opening(self):
		""" introductory screen """
		welcome_text = figlet_format("Welcome To ", font="slant")
		q_text = figlet_format("Quotes ", font="slant")
		trivia_text = figlet_format("Trivia", font="slant")
		
		colored_welcome = colored(welcome_text, "red", attrs=["bold"])
		q_colored = colored(q_text, "yellow", attrs=["bold"])
		trivia_colored = colored(trivia_text, "cyan", attrs=["bold"])

		opening_screen = colored_welcome + q_colored + trivia_colored
		return opening_screen

	def loading(self):
		""" screen displayed while a game is beginning or being reset """
		generating_text = figlet_format("Generating ", font="slant")
		generating_quote = figlet_format("Quote ", font="slant")
		generating_dots = figlet_format("... ... ...", font="slant")

		generating_text_colored = colored(generating_text, "red", attrs=["bold"])
		generating_quote_colored = colored(generating_quote, "yellow", attrs=["bold"])
		generating_dots_colored = colored(generating_dots, "cyan", attrs=["bold", "blink"])

		loading_screen = generating_text_colored + generating_quote_colored + generating_dots_colored
		return loading_screen

	def ending(self):
		""" closing screen """
		thank_you = figlet_format("Thank You ", font="slant")
		for_playing = figlet_format("For Playing!", font="slant")

		thank_you_colored = colored(thank_you, "magenta", attrs=["bold"])
		for_playing_colored = colored(for_playing, "cyan", attrs=["bold"])

		ending_screen = thank_you_colored + for_playing_colored
		return ending_screen



class NewGame():
	""" generate and gather the data of a new randomly selected quote """

	def __init__(self):
		#randomly selects a dictionary from the list of data
		#variables store the values of the "text" and "name" keys
		self.random_selection = random.choice(data)
		self.random_quote = self.random_selection["text"]
		self.correct_answer = self.random_selection["name"]

		self.guesses_remaining = 4
		self.i = 0
	
	def get_correct_answer(self):
		""" returns the quote's attributed author """
		return self.correct_answer

	def get_new_quote(self):
		""" returns the quote """
		return self.random_quote

	def get_data(self):
		""" scrapes and gathers data from the selected author's biography """

		#uses the value of the dictionary's href tag to access the author's biography
		bio = requests.get("http://quotes.toscrape.com/" + self.random_selection["href"])
		bio_soup = BeautifulSoup(bio.text, "html.parser")

		self.born_date = bio_soup.find(class_ = "author-born-date").get_text()
		self.born_location = bio_soup.find(class_ = "author-born-location").get_text()[3:]

		#scrapes the description of the author. compiles all words into a list and searches
		#for keywords to determine the gender of the author
		description = bio_soup.find(class_ = "author-description").get_text().lower()
		list_of_words = description.split()

		female_count = list_of_words.count('her') + list_of_words.count('hers') + list_of_words.count("she")
		male_count = list_of_words.count('him') + list_of_words.count('his') + list_of_words.count("he")

		if male_count > female_count:
			self.gender = "male"
		else:
			self.gender = "female"

	def get_hints_list(self):
		""" compiles all hints together.
		returns a shuffled list of all hints """

		self.get_data()

		hint_birth_location = f"Hint: This person was born in " + self.born_location
		hint_birth_date = f"Hint: This person was born on " + self.born_date
		hint_gender = f"Hint: This person is a {self.gender}"
		hint_first_letter = f"Hint: The first letter of the author's name is " + self.random_selection["name"][0]

		chars = len(self.correct_answer.split()[-1])
		hint_number_of_chars_last_name = f"Hint: The author's last name contains {chars} characters"

		list_hints = [hint_birth_location, hint_birth_date, hint_gender, hint_first_letter]
		return list_hints

	def get_hint(self):
		""" retrieves a hint. increments index to avoid repeating hints. 
		decrements chances remaining """

		self.hints_list = self.get_hints_list()
		self.hint = self.hints_list[self.i]
		self.i += 1
		self.guesses_remaining -= 1
		return self.hint



class Play():
	""" provides a randomly selected quote. accepts user guesses. incorrect guesses yield
	hints. the game ends when the user enters three incorrect guesses or provides the 
	correct answer. class contains Graphical User Interface elements, which update 
	depending on user input """

	def __init__(self):

		#game banner
		self.logo = ImageTk.PhotoImage(Image.open("/Users/rueda/Desktop/projects/scraper/graphics/logo.png"))
		self.panel = tk.Label(root, image = self.logo)
		self.panel.pack()

		#button that proceeds to the next screen 
		self.play_button = tk.Button(root, text = "PLAY", fg = "PaleGreen3", width = 12, command = self.loading_screen)
		self.play_button.config(font=("Retro Gaming", 25))
		self.play_button.pack()

		#play again button
		self.play_again = tk.Button(root, text = "PLAY AGAIN", fg = "PaleGreen3", width = 12, command=lambda: self.loading_screen())
		self.play_again.config(font=("Retro Gaming", 25))

		#attribution
		self.attribution = tk.Label(root, text = "Created by Kevin Rueda\ngithub.com/RuedaKV", pady = 10)
		self.attribution.pack()

	def loading_screen(self):
		""" buffer screen between opening screen and the beginning of gameplay. 
		clears all widgets from previous screen or previous game. 
		initializes game information through the creation of a NewGame() object """

		clear_widgets()
		self.game = NewGame()
		self.make_guess()

	def make_guess(self):
		""" screen that displays the selected quote. accepts user input through a text 
		box and submission button """

		#display quote
		self.quote_label = tk.Label(root, text = "Quote: " + self.game.get_new_quote(), wraplength=275)
		self.quote_label.pack()

		#user input box
		self.v = tk.StringVar()
		self.guess = tk.Entry(root)
		self.guess.pack()

		#user input submission 
		#checks if the user input is equal to the correct answer
		#lambda either executes correct_guess() or incorrect_guess()
		self.submit = tk.Button(root, text = "Submit Answer", command = lambda: self.correct_guess()
			if [char for char in self.input_guess()] == [char for char in self.game.get_correct_answer().strip().lower()] 
			else self.incorrect_guess())
		self.submit.pack()

	def input_guess(self):
		""" returns the user entry. removes whitespace and makes the entry lowercase """
		self.user_guess = self.guess.get().strip().lower()
		return self.user_guess

	def correct_guess(self):
		""" displays a victory screen. provides the user with a "Play Again" button which 
		restarts the game """

		clear_widgets()

		#victory banner
		self.win = ImageTk.PhotoImage(Image.open("/Users/rueda/Desktop/projects/scraper/graphics/won.png"))
		self.panel_win = tk.Label(root, image = self.win)

		self.panel_win.pack()
		self.play_again.pack()

	def incorrect_guess(self):
		""" provides users with a hint. executes closing_screen() if user fails to 
		make a correct guess after 3 hints """

		self.hint_label = tk.Label(root, text = self.game.get_hint(), wraplength=250)
		self.hint_label.pack()

		if self.game.guesses_remaining == 0:
			self.closing_screen()

	def closing_screen(self):
		""" screen displayed after losing the game. allows users to play a new game """

		clear_widgets()

		#loss banner
		self.lost = ImageTk.PhotoImage(Image.open("/Users/rueda/Desktop/projects/scraper/graphics/lost.png"))
		self.panel_lost = tk.Label(root, image = self.lost)
		self.panel_lost.pack()

		#shows correct answer
		lost = tk.Label(root, text = "Correct Answer:", wraplength=250)
		lost.config(font=("TkDefaultFont", 20))


		lost_answer = tk.Label(root, text = self.game.get_correct_answer(), fg = "deep sky blue", wraplength=250)
		lost_answer.config(font=("TkDefaultFont", 20))

		lost.pack()
		lost_answer.pack()

		self.play_again.pack()



""" initializes graphical user interface """
root = tk.Tk()
root.configure(highlightbackground = "black", highlightthickness = 1, bd = 1, relief = "solid")
root.title("Quote Trivia")
root.option_add("*fonts", "Helvetica")
root.geometry("300x500")

frame = tk.Frame(root)
frame.config(highlightbackground = "black", highlightthickness = 1, bd = 1, relief = "solid")
frame.pack()

def all_children(root):
	""" obtains a list of all widgets in gui """
	_list = root.winfo_children()

	for item in _list:
		if item.winfo_children():
			_list.extend(item.winfo_children())
	return _list

def clear_widgets():
	""" clears all widgets in gui """
	widget_list = all_children(root)
	for item in widget_list:
		item.pack_forget()


		
""" inital data collection """
data = []

#makes a request to each page. searches for and all "quote" tags
page = 0
while page < 11:
	response = requests.get("http://quotes.toscrape.com/page/" + str(page) + "/")
	soup = BeautifulSoup(response.text, "html.parser")
	quotes = soup.find_all(class_="quote")

	#iterates through each quote tag
	#for each quote tag, a dictionary is created containing the text quote, the attributed author,
	#and the href to the author's biography. each dictionary is appended to the list of data
	for quote in quotes:
		data.append({
			"text":quote.find(class_="text").get_text(),
			"name":quote.find(class_="author").get_text(),
			"href":quote.find("a")["href"]
		})
	#time.sleep(2)
	page += 1



""" begins the first game """
o = Play()
root.mainloop()
