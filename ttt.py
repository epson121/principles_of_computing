"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# Change as desired
NTRIALS = 10    # Number of trials to run
MCMATCH = 1.0  # Score for squares played by the machine player
MCOTHER = 1.0  # Score for squares played by the other player
SCORES = []
# Add your functions here.
def mc_trial(board, player):
    """
    Docs
    """
    while board.check_win() == None:
        empty = board.get_empty_squares()
        rand_sq = empty[random.randrange(len(empty))]
        board.move(rand_sq[0], rand_sq[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    Docs
    """
    if board.check_win() == provided.DRAW:
        return
    winner = board.check_win()
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            square = board.square(row, col)
            if square == winner:
                scores[row][col] += MCMATCH if winner == player else MCOTHER
            elif square == provided.EMPTY:
                continue
            else:
                scores[row][col] -= MCMATCH if winner == player else MCOTHER

def get_best_move(board, scores):
    """
    Docs
    """
    res = {}
    empties = board.get_empty_squares()
    print empties
    print scores
    idx = 0
    jdx = 0
    for elem in empties:
        #for col in range(len(empties)):
        res[elem] = scores[idx][jdx]
        if jdx + 1 == 3:
            jdx = 0
            idx += 1
        else:
            jdx += 1
    print "ITEMS: " + str(res.items())
    result = [key for key,val in res.items() if val == max(res.values())]
    print "RESULT: " + str(result)
    return random.choice(result)

def mc_move(board, player, trials):
    """
    Docs
    """
    global SCORES
    #This function takes a current board, which
    #player the machine player is, and the number
    #of trials to run. The function should use the
    #Monte Carlo simulation described above to return
    #a move for the machine player in the form of a
    #(row, column) tuple. Be sure to use the other
    #functions you have written!

    #Start with the current board.
    #Repeat for the desired number of trials:
    first_sc = [0 for i in range(board.get_dim())]
    SCORES = [first_sc for i in range(board.get_dim())]
    trial_board = board.clone()
    while trials >= 0:
        #Play an entire game by just randomly choosing a move for each player.
        mc_trial(trial_board, player)
        #Score the resulting board.
        mc_update_scores(SCORES, trial_board, player)
        trials -= 1
    #print SCORES
    bemti = get_best_move(board, SCORES)
    #print "BEST MOVE: " + str(bm)
    return bemti
        #Add the scores to a running total across all trials.
        #To select a move, randomly choose one of the empty squares on the board that has the maximum score.

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(mc_move, NTRIALS, False)
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
