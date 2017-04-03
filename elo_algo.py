import numpy
import math



def update_scores(r1, r2, winner, tourneySize):
	"""This function calculates updated player scores
	Requires: Elo ranking of player 1 and 2, a number in winner that indicates who won
		1 for player1, 2 for player2, and the number of entrants for the tourney
	Modifies: Nothing
	Effects: Returns updated scores for r1 and r2
	"""
	#simplification of current ratings
	R1 = math.pow(10,r1/400)
	R2 = math.pow(10,r2/400)
	#expected score for each player after match
	E1 = R1/(R1 + R2)
	E2 = R2/(R1 + R2)
	#mod the winner with 2 to get the actual score for p1
	result1 = winner % 2
	#subtract 1 from the winner to get actual score for p2
	result2 = winner - 1
	#modification factor
	k = 5 * math.log(tourneySize,2) 
	#result calculations
	newR1 = r1 + k * (result1 - E1)
	newR2 = r2 + k * (result2 - E2)
	return newR1, newR2




print ("Quick test with numbers 2400 and 2000")
r1 = 2400
r2 = 2000
tourneySize = 100
newR1, newR2 = update_scores(r1,r2, 1, tourneySize)
print("r1 = " + str(newR1) + " r2 = " + str(newR2))
newR1, newR2 = update_scores(r1,r2, 2, tourneySize)
print("r1 = " + str(newR1) + " r2 = " + str(newR2))




