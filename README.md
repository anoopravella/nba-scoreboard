# nba-scoreboard
A program that returns the scores for NBA games to the command line.
Mainly created as an exercise to gain experience web scraping with python and xpath.

## Description
This program will return NBA scores for a given date (beginning from the 2010-2011 season) or for the current day if no date is provided. It scrapes scoreboard data from si.com/nba/scoreboard and returns the current score for games in progress, the final score for finished games, and the scheduled game time for future games. Additionally, it will return the record of the teams involved in each game on that date.

## Python libraries needed
* lxml
* requests
* sys

## Executing the program
* Download the nba-scoreboard.py file
* Run the command below to access the current day's scores
```
python nba-scoreboard.py
```
* Run the command below (replacing "YYYY-MM-DD" with the date you would like to see the scores from) to see a specific date's scores
```
python nba-scoreboard.py YYYY-MM-DD
```
