from lxml import html
import requests
import sys


# main program

if len(sys.argv) > 2 :
	print ('Error')
	print ('USAGE: nba-scoreboard.py [date in YYYY-MM-DD form]')
	sys.exit(0)
elif len(sys.argv) == 2 :
	url = 'https://www.si.com/nba/scoreboard?date=%s' % sys.argv[1]
else :
	url = 'https://www.si.com/nba/scoreboard'


page = requests.get(url, headers={'User-Agent': 'nbScoresRobot/1.0 (aravella1@gmail.com)'})

tree = html.fromstring(page.text)

# initializing variables
awayTeamsCityProcessed = []
awayTeamsRecordProcessed = []

homeTeamsCityProcessed = []
homeTeamsRecordProcessed = []

gameStatus = []
awayScores = []
homeScores = []


awayTeamsCityRaw = tree.xpath('//div[@class="teams"]/div[1]/div[2]/div[1]/a/text()')
awayTeamsName = tree.xpath('//div[@class="teams"]/div[1]/div[2]/a[2]/span/text()')
awayTeamsRecordRaw = tree.xpath('//div[@class="teams"]/div[1]/div[2]/span/text()')

homeTeamsCityRaw = tree.xpath('//div[@class="teams"]/div[3]/div[2]/div[1]/a/text()')
homeTeamsName = tree.xpath('//div[@class="teams"]/div[3]/div[2]/a[2]/span/text()')
homeTeamsRecordRaw = tree.xpath('//div[@class="teams"]/div[3]/div[2]/span/text()')

for city in awayTeamsCityRaw :
	city = city.replace('\n', '')
	city = city.strip()
	awayTeamsCityProcessed.append(city)

for city in homeTeamsCityRaw :
	city = city.replace('\n', '')
	city = city.strip()
	homeTeamsCityProcessed.append(city)

for record in awayTeamsRecordRaw :
	record = record.replace('\n', '')
	record = record.strip()
	awayTeamsRecordProcessed.append(record)

for record in homeTeamsRecordRaw :
	record = record.replace('\n', '')
	record = record.strip()
	homeTeamsRecordProcessed.append(record)


# games in progress
if tree.xpath('//div[@class="status-active uppercase"]/text()') :
	clocks = tree.xpath('//span[@class="status-active uppercase"]/text()')

	for clock in clocks :
		clock = clock.replace('\n', '')
		clock = clock.replace('\x95', '')
		clock = clock.strip()
		gameStatus.append(clock)


	awayScoresRaw = tree.xpath("//div[@class='status-active uppercase']/../../../div[2]/div/div[1]/div/div[1]/div[3]/div/text()")

	for score in awayScoresRaw :
		score = score.replace('\n', '')
		score = score.strip()
		awayScores.append(score)

	homeScoresRaw = tree.xpath("//div[@class='status-active uppercase']/../../../div[2]/div/div[1]/div/div[3]/div[3]/div/text()")

	for score in homeScoresRaw :
		score = score.replace('\n', '')
		score = score.strip()
		homeScores.append(score)

# games not yet started
if tree.xpath('//div[@class="float-left status-container"]/strong/text()') :
	times = tree.xpath('//div[@class="float-left status-container"]/strong/text()')
	
	for time in times :
		time = time.replace('\n', '')
		time = time.strip()
		gameStatus.append(time)

		awayScores.append('-')
		homeScores.append('-')

# games ended
if tree.xpath('//div[@class="status-final"]/text()') :
	finals = tree.xpath('//div[@class="status-final"]/text()')

	for final in finals :
		final = final.replace('\n', '')
		final = final.strip()
		gameStatus.append(final)


	awayScoresRaw = tree.xpath('//div[@class="status-final"]/../../../div[2]/div/div[1]/div/div[1]/div[3]/div/text()')

	for score in awayScoresRaw :
		score = score.replace('\n', '')
		score = score.strip()
		awayScores.append(score)

	homeScoresRaw = tree.xpath('//div[@class="status-final"]/../../../div[2]/div/div[1]/div/div[3]/div[3]/div/text()')

	for score in homeScoresRaw :
		score = score.replace('\n', '')
		score = score.strip()
		homeScores.append(score)




gameStatus = list(filter(None, gameStatus))		# remove empty strings from list


for awayCity, homeCity, awayTeam, homeTeam, awayRecord, homeRecord, status, awayScore, homeScore in zip(awayTeamsCityProcessed, homeTeamsCityProcessed, awayTeamsName, homeTeamsName, awayTeamsRecordProcessed, homeTeamsRecordProcessed, gameStatus, awayScores, homeScores) :
	print ('{0:50} {1:10}'.format(awayCity + ' ' + awayTeam + ' ' + awayRecord, awayScore))
	print ('{0:50} {1:10}'.format(homeCity + ' ' + homeTeam + ' ' + homeRecord, homeScore))
	print (status + '\n')
