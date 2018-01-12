from lxml import html
import requests
import sys

# function to remove spaces, newlines, and other undesirable characters from strings
def clean_data (raw_list, destination_list) :
	for element in raw_list :
		element = element.replace('\n', '')
		element = element.replace('\x95', '')
		element = element.strip()
		destination_list.append(element)

	return destination_list

# main program

# processing arguments, error checking and handling
if len(sys.argv) > 2 :
	print ('Error')
	print ('USAGE: nba-scoreboard.py [date in YYYY-MM-DD form]')
	sys.exit(0)
elif len(sys.argv) == 2 :
	url = 'https://www.si.com/nba/scoreboard?date=%s' % sys.argv[1]
else :
	url = 'https://www.si.com/nba/scoreboard'


page = requests.get(url, headers={'User-Agent': 'nbaScoresRobot/1.0 (aravella1@gmail.com)'})

tree = html.fromstring(page.text)

# initializing variables
awayTeamsCityProcessed = []
awayTeamsRecordProcessed = []

homeTeamsCityProcessed = []
homeTeamsRecordProcessed = []

gameStatus = []
awayScores = []
homeScores = []

# scraping city, team name, and team record data
awayTeamsCityRaw = tree.xpath('//div[@class="teams"]/div[1]/div[2]/div[1]/a/text()')
awayTeamsName = tree.xpath('//div[@class="teams"]/div[1]/div[2]/a[2]/span/text()')
awayTeamsRecordRaw = tree.xpath('//div[@class="teams"]/div[1]/div[2]/span/text()')

homeTeamsCityRaw = tree.xpath('//div[@class="teams"]/div[3]/div[2]/div[1]/a/text()')
homeTeamsName = tree.xpath('//div[@class="teams"]/div[3]/div[2]/a[2]/span/text()')
homeTeamsRecordRaw = tree.xpath('//div[@class="teams"]/div[3]/div[2]/span/text()')

# cleaning up city and record data
awayTeamsCityProcessed = clean_data(awayTeamsCityRaw, awayTeamsCityProcessed)
homeTeamsCityProcessed = clean_data(homeTeamsCityRaw, homeTeamsCityProcessed)
awayTeamsRecordProcessed = clean_data(awayTeamsRecordRaw, awayTeamsRecordProcessed)
homeTeamsRecordProcessed = clean_data(homeTeamsRecordRaw, homeTeamsRecordProcessed)


# games in progress
if tree.xpath('//span[@class="status-active uppercase"]/text()') :
	
	clocks = tree.xpath('//span[@class="status-active uppercase"]/text()')
	gameStatus = clean_data(clocks, gameStatus)

	awayScoresRaw = tree.xpath("//span[@class='status-active uppercase']/../../../div[2]/div/div[1]/div/div[1]/div[3]/div/text()")
	awayScores = clean_data(awayScoresRaw, awayScores)

	homeScoresRaw = tree.xpath("//span[@class='status-active uppercase']/../../../div[2]/div/div[1]/div/div[3]/div[3]/div/text()")
	homeScores = clean_data(homeScoresRaw, homeScores)

# games not yet started
if tree.xpath('//div[@class="float-left status-container"]/strong/text()') :
	
	times = tree.xpath('//div[@class="float-left status-container"]/strong/text()')
	gameStatus = clean_data(times, gameStatus)

	clean_times = []
	clean_times = clean_data(times, clean_times)
	clean_times = list(filter(None, clean_times))

	for time in clean_times :
		awayScores.append('-')
		homeScores.append('-')
	
# games ended
if tree.xpath('//div[@class="status-final"]/text()') :

	finals = tree.xpath('//div[@class="status-final"]/text()')
	gameStatus = clean_data(finals, gameStatus)

	awayScoresRaw = tree.xpath('//div[@class="status-final"]/../../../div[2]/div/div[1]/div/div[1]/div[3]/div/text()')
	awayScores = clean_data(awayScoresRaw, awayScores)

	homeScoresRaw = tree.xpath('//div[@class="status-final"]/../../../div[2]/div/div[1]/div/div[3]/div[3]/div/text()')
	homeScores = clean_data(homeScoresRaw, homeScores)


gameStatus = list(filter(None, gameStatus))		# remove empty strings from list

# prints the scoreboard
for awayCity, homeCity, awayTeam, homeTeam, awayRecord, homeRecord, status, awayScore, homeScore in zip(awayTeamsCityProcessed, homeTeamsCityProcessed, awayTeamsName, homeTeamsName, awayTeamsRecordProcessed, homeTeamsRecordProcessed, gameStatus, awayScores, homeScores) :
	print ('{0:50} {1:10}'.format(awayCity + ' ' + awayTeam + ' ' + awayRecord, awayScore))
	print ('{0:50} {1:10}'.format(homeCity + ' ' + homeTeam + ' ' + homeRecord, homeScore))
	print (status + '\n')
