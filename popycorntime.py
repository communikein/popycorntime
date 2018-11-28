import urllib2
import json
from bs4 import BeautifulSoup
from qbittorrent import Client

torrents_url = "http://eztv.it"
qbittorrent_conf = {
	'ip' : '127.0.0.1',
	'port' : '8080',
	'username' : 'admin',
	'password' : 'administrator'
}

def color_string(text, color):
	result = "\x1b[1;3{color}m{text}\x1b[0m".format(color=color, text=text)
	return result

def error_message(message):
	error_message = color_string('\n\n!!!!\nERROR: ' + message + '\n!!!!\n\n', 1)
	return error_message

def prompt_exit():
	choice = raw_input(color_string("Are you sure? (y/n): ", 1))
	if choice.lower() == "y" or choice == '':
		sys.exit(0)

def input_wrapper(prompt, color=7):
	text = color_string(prompt, color)
	choice = raw_input(text)

	return choice


def watch_movie(torrent_link):
	try:
		qb = Client('http://' + qbittorrent_conf['ip'] + ':' + qbittorrent_conf['port'] + '/')

		qb.login(qbittorrent_conf['username'], qbittorrent_conf['password'])
		qb.download_from_link(torrent_link)
	except:
		print(error_message("You must enable qBittorrent Web UI for this to work."))


"""
	Fetches a show mapping $name.
"""
def check_tv_show(name):
	name = name.lower()
	terms = name.split(' ')

	print("Downloading list of TV Shows...")

	req = urllib2.Request(torrents_url + "/js/search_shows1.js", headers={'User-Agent' : "Magic Browser"}) 
	response = urllib2.urlopen(req).read()
	temp = response[response.index("[") : response.index("]") + 1]
	tv_shows = json.loads(temp)

	print("Found " + str(len(tv_shows)) + " TV Shows!")

	results = []
	if len(tv_shows) == 0:
		print("ERROR API!")

	else:
		for tv_show in tv_shows:
			tv_show_name = tv_show['text'].lower()
		
			for word in terms:
				if word in tv_show_name:
					results.append(tv_show)
					break

	if len(results) == 0:
		raise TVShowNotFound('The TV Show "%s" has not been found. '.join(terms), None)

	return results

"""
	load the data, create a dictionary structure with all seasons,
	episodes, magnet.
"""
def load_tv_show_data(tv_show_id):
	tv_show_url = torrents_url + "/search/?q2=" + str(tv_show_id)
	req = urllib2.Request(tv_show_url, headers={'User-Agent' : "Magic Browser"})
	response = urllib2.urlopen(req).read()
	soup = BeautifulSoup(response, 'html.parser')

	episodes = []
	temp = soup.findAll('a', attrs={'class': 'magnet'})
	
	print("Found " + str(len(temp)) + " episodes.")
	for ep in temp:
		episodes.append({'link' : ep['href'], 'title' : ep['title']})

	cont = 0
	for episode in episodes:
		index = color_string(text=str(cont + 1), color=3)
		tv_show_title = color_string(text=episode['title'], color=3)
		print(index + ' ## ' + tv_show_title)
		cont += 1

	return episodes

def search_show():
	term = input_wrapper("Enter title of the show: ")
	if term is '':
		print("No results! :/")
		return 0

	print("Looking for TV Shows like \"" + term + "\" ...")
	result = check_tv_show(term)

	print("")

	for tv_show in result:
		episodes = load_tv_show_data(tv_show['id'])

		if episodes is None:
			print("No results! :/")
			return 0

	user_input = ''
	while user_input == '':
		try:
			user_input = input_wrapper("Choose episode #: ")
			int(user_input)
		except ValueError:
			print(error_message('Type in the number of the episode you want to download.'))
			user_input = ''

	selected = int(user_input)
	torrent_link = episodes[selected - 1]['link']
	tv_show_title = episodes[selected - 1]['title']
	print("Link to the torrent: " + episodes[selected - 1]['link'])

	code = watch_movie(torrent_link)

	return 0


while True:
	i = input_wrapper("Do you want to search for a TV Show? (y/n)")

	if i == 'y' or i == '':
		search_show()
	else:
		break
