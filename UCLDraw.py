#! python3

import sys
import enum
import random
class Country(enum.Enum):
	ENG = 1,
	NED = 2,
	SPA = 3,
	GER = 4,
	FRA = 5,
	ITA = 6,
	POR = 7,
	AUS = 8



class Team:
	def __init__(self, name, country, group, isWinner):
		self.name = name
		self.country = country
		self.group = group
		self.isWinner = isWinner
		self.isSelected = False

	def setIsSelected(self, value):
		self.isSelected = value

teams = [Team("Manchester City", Country.ENG, "A", True), Team("Liverpool", Country.ENG, "B", True), Team("Ajax", Country.NED, "C", True),
			Team("Real Madrid", Country.SPA, "D", True), Team("Bayern Munich", Country.GER, "E", True), Team("Manchester United", Country.ENG, "F", True),
			Team("Lille", Country.FRA, "G", True), Team("Juventus", Country.ITA, "H", True), Team("PSG", Country.FRA, "A", False), Team("Athletico Madrid", Country.SPA, "B", False),
			Team("Sporting Lisbon", Country.POR, "C", False), Team("Inter Milan", Country.ITA, "D", False), Team("Benfica", Country.POR, "E", False), Team("Villareal", Country.SPA, "F", False),
			Team("Salzburg", Country.AUS, "G", False), Team("Chelsea", Country.ENG, "H", False)]

def drawTeam(teams):
	drawIndex = random.randrange(0, len(teams))
	return teams[drawIndex]

def printTeamArr(teams):
	for team in teams:
		print(team.name)

def getValidOpponents(team):
	validOpponents = [opponent for opponent in teams if not opponent.isSelected]
	validOpponents = [opponent for opponent in validOpponents if opponent.isWinner != team.isWinner]
	validOpponents = [opponent for opponent in validOpponents if opponent.country != team.country]
	validOpponents = [opponent for opponent in validOpponents if opponent.group != team.group]
	return validOpponents

def checkFutureMatchesValid(validOpponents):
	#Now check for future problems
	finalOpponents = []
	if ( len(validOpponents) == 1):
		print("Inside the one valid opponent check")
		return [validOpponents[0]]

	for opponent in validOpponents:
		print("Lets check if we select" + opponent.name)
		opponent.setIsSelected(True)
		runnersUp = [team for team in teams if (not team.isWinner)]
		remainingRunnersUp = [remainingRunnerUp for remainingRunnerUp in runnersUp if not remainingRunnerUp.isSelected]
		singleOpponentsDict = {}
		fullListOpponents = []
		validOpponent = True
		for runnerUp in remainingRunnersUp:

			opponents = getValidOpponents(runnerUp)
			if(len(opponents) == 0):
				validOpponent = False
				continue
			else:
				#Make full array of all opponents of remaining teams and make sure
				for opponentTeam in opponents:
					fullListOpponents.append(opponentTeam)
				if(len(opponents) == 1):
					singleOpponentsDict[runnerUp] = opponents[0].name
		
		if (len(singleOpponentsDict.keys()) != len(set(singleOpponentsDict.values())) ):
			print("failed A")
			opponent.setIsSelected(False)
			continue
		#Check set of fullListOppontents is same length of the reminaing group winners
		if (len(set(fullListOpponents)) != getNumNotSelectedWinners()):
			print("failed B")
			print("full list size: " + str(len(set(fullListOpponents))))
			print("numNotSelected: " + str(getNumNotSelectedWinners()))
			opponent.setIsSelected(False)
			continue
		
		if(validOpponent):
			print("success")
			finalOpponents.append(opponent)	

		opponent.setIsSelected(False)

	return finalOpponents

def getNumNotSelectedWinners():
	winners = [team for team in teams if team.isWinner]
	numNotSelected = len([team for team in winners if (not team.isSelected)])
	return numNotSelected

def completeDraw(winners, runnersUp):
	print("What is our winners:")
	matchesDict = {}
	for winner in winners:
		print(winner.name)
		matchesDict[winner.name] = {}

	for draw_num in range(len(winners)):
		# filter out selected teams each iteration
		filterredWinners = [team for team in winners if not team.isSelected]
		runnersUp = [team for team in runnersUp if not team.isSelected]

		print("The number of winners to draw from: " + str(len(filterredWinners)))
		winner = drawTeam(filterredWinners)
		winner.setIsSelected(True)
		print("Team we drew from pot 1 is:" + winner.name)
		opponents = getValidOpponents(winner)
		print("What are the opponents we send to future check: ")
		for o in opponents:
			print(o.name)
		validOpponents = checkFutureMatchesValid(opponents)
		print("The number of runners up to draw from: " + str(len(validOpponents)))
		match = drawTeam(validOpponents)
		match.setIsSelected(True)
		print("Our match is: " + match.name)
		matchesDict[winner.name][match.name] = 1
	return matchesDict

def simulation(winners, runnersUp, numDraws):
	countTotalMatches = {}
	for winner in winners:
		countTotalMatches[winner.name] = {}
	for simualtedDraw in range(numDraws):
		print("We are on simulated draw number: " + str(simualtedDraw) )


		matches = completeDraw(winners, runnersUp)
		for winner in matches:
			for match in matches[winner]:
				if match in countTotalMatches[winner]:
					countTotalMatches[winner][match] += 1
				else:
					countTotalMatches[winner][match] = 1
		resetTeamsSelected()
	return countTotalMatches

def resetTeamsSelected():
	for team in teams:
		team.setIsSelected(False)

def main():
	winners = [team for team in teams if (team.isWinner)]
	runnersUp = [team for team in teams if (not team.isWinner)]
	numberDraws = int(sys.argv[1])
	finalCounts = simulation(winners, runnersUp, numberDraws )
	print(finalCounts)


if __name__ == '__main__':
	main()





