from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from collections import Counter
import matplotlib.pyplot as plt
import re

completeList = []
def getData(url):
	try:
		html = urlopen(url)
	except HTTPError as e:
		return None
	try:
		soup = BeautifulSoup(html.read(), "html.parser")
		#Pick out title of top games
		titleList = [x.text for x in soup.find("div", {"class":"body"}).findAll("a", text=re.compile(""))]
		#Pick out the number 1 top game
		firstRating = soup.find("div", {"class":"body"}).find("b", text=re.compile("\d"))
		#Pick out ratings with regular expression; EXAMPLE: 100.00%, 83.42%, 68.69% etc
		ratingsList = [x.text for x in soup.find("div", {"class":"body"}).findAll("td", text=re.compile("\d"))]
		#TODO: pick out console type with regular expression; EXAMPLE: (PS4) (PlayStation4) (3DS) (WIIU)
		global consoleList
		consoleList = []
		for item in titleList:
			console = re.findall(r"\((\w+\s\d*)\)", str(item))
			if len(console) == 0:
				console = re.findall(r"\((\w+)\)", str(item))
				consoleList.append(console)
			elif len(console) > 0:
				consoleList.append(console)
	except HTTPError as e:
		return None
	print(consoleList)
	print(titleList)

	print("Console List: "+str(consoleList))

	firstRating = firstRating.text
	ratingsList.insert(0, firstRating)
	print(ratingsList)

	global completeList
	completeList = (zip(titleList, ratingsList))
	completeList = dict(completeList)
	print(completeList)
	print("\n")

#Write a functon that evaluates whether a game is worth playing and if you own
def worthPlaying(score_floor):
	for key, value in completeList.items():
		value = value.strip('%')
		if float(value) > score_floor and key in games_I_can_play:
			print(key+" averages a "+value+"% so it is worth playing and you can play it!")
		elif float(value) > score_floor and key not in games_I_can_play:
			print(key+" averages a "+value+"% so it is worth playing but you can't play it :( ")
		else:
			print(key+" averages a "+value+"% so it is not worth playing..")

#Write function that takes a list of the consoles you own as parameters
def systemsOwned(can_I_play_it=False):
	systems_I_own_list = ['PlayStation 4', 'PS4','3DS', 'PC']
	global games_I_can_play 
	games_I_can_play = []
	for system in systems_I_own_list:
		for key, value in completeList.items():
			if system in key:
				games_I_can_play.append(key)
				can_I_play_it = True

#TODO: Write function that computes what console the popular games are on by percentage 
#EXAMPLE: 80% of the games are on PS4, 20% are on 3DS
global cnt 
def computeConsolePopularity():
	PS4_count = 0
	WIIU_count = 0
	DS3_count = 0
	XBOX1_count = 0
	PC_count = 0
	PS4_bool = False

	#PlayStation4 => PS4
	for console in consoleList:
		if 'PlayStation 4' in console:
			consoleList.remove(console)
			consoleList.append(['PS4'])

	print(consoleList)
	cnt = Counter()
	for console in consoleList:
		cnt[str(console)] += 1
	print(cnt)

	makePieList = list(cnt.items())

	print(makePieList)

	#console and count List
	console_list = [(i[0]) for i in makePieList]
	count_list = [(i[1]) for i in makePieList]
	print(console_list)
	print(count_list)

	#slices = [7,2,1]
	#consoles = ['PS4', 'WIIU', '3DS']
	cols = ['c','m','r','k']

	plt.pie(count_list, labels=console_list, colors=cols, autopct='%1.1f%%')

	plt.xlabel('x')
	plt.ylabel('y')
	plt.title('What console are the most popular games on?\nCheck it out!')
	plt.legend()
	plt.show()
	
getData("http://www.gamerankings.com/")
systemsOwned()
worthPlaying(80)
print("\n")
computeConsolePopularity()

