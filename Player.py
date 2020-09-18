from connect4 import Board
import random
"""
Implementation of a Connect-4 Player class

Author: William Clark and Henry Howell
"""


class Player:
    """A type for representing the behavior of a Connect-4 player who decides
    what move to play next by looking a few moves ahead.
    
    Attributes:
    side - a single character string that is either 'X' or 'O'
           (the letter Oh, not the number 0), denoting the side this
           Player will be taking
    ply -  a non-negative integer (i.e., ≥ 0) representing how many moves
           into the future this Player will look in order to evaluate the
           “goodness” of a move
    is_random - a boolean value denoting how this Player will handle situations
                when there exist multiple moves that are equally good.
                If set to True, then this Player will break ties randomly;
                if False, then the Player will choose the left-most column
                among the tied columns.
    """
    GOOD_MOVE = 100
    OKAY_MOVE = 50
    BAD_MOVE = 0
    PLY_END = 0
   
    def __init__(self, side, ply, is_random):
        """Initializes the three attributes of the Player Class.

        Paremeters:
            side - string 'X' or 'O'
            ply - how far ahead into the future the player will
                  look when planning next move
            is_random - how to break ties between best moves
        
        Returns:
            None.
        """
        self.side = side
        self.ply = ply
        self.is_random = is_random
       
    def  __str__(self):
        """Returns a string representation of the Player object that calls it.

        Returns:
            A string containing the instance of the Player object that is
            being played. 

        """
        stringo = ""
        tie_breaker = ""
       
        if self.is_random == True:
            tie_breaker += "randomly"
        else:
            tie_breaker += "deterministically"
       
        stringo += ("Player for " + self.side + ', ply = '
                    + str(self.ply) + ", breaks ties " + tie_breaker)
       
        return stringo
       
    def opponent(self):
        """Returns the side that the opponent is playing on.

        Returns:
            An 'X' if the current Player is an 'O' or vise versa. 

        """
        if self.side == 'X':
            return 'O'
        else:
            return 'X'
       
       
    def evaluate_board(self, board):
        """Evaluates the board to see if a given move will either win or lose
           the game for the player.

           Parameters:
                board - the current state that the connect four board is in.
           Returns:
               A score of either 100, for a winning move, 0, for a losing
               move, or 50, for neither winning or losing move.                               

        """
             
        if board.win_for(self.side) == True: #if the board shows a win for the player side
            return Player.GOOD_MOVE          
        elif board.win_for(self.opponent()) == True: #if the board shows a win for the opponent
            return Player.BAD_MOVE
        else:
            return Player.OKAY_MOVE     #if no one wins return 50

       
    def score_columns(self, board):
        """Returns a list that uses evaluate_board in order to determine
           the column that will produce the most success for the player by
           assessing the oppoenent's countermoves. How many moves to look ahead
           to make is based off the ply number.

           Parameters:
               board - the current state that the connect four board is in.

           Returns:
               initial_scores - a list with the score assessment should the
               Player make a play in a given column

        """
        
        initial_scores = []
        
        
        self.ply = self.ply
       
       
       
        for i in range(board.width):
            initial_scores.append(Player.OKAY_MOVE)  #creates a list of all 50s

        for w in range(len(initial_scores)):

           
            if board.allows_move(w) == False:    #base case if column is full
                initial_scores[w] = Board.INVALID_MOVE  #assigns that col w/ -1        
       
            #base case if either the player or opponent win:
            elif (board.win_for(self.side) == True
                  or board.win_for(not self.side) == True):
                #checks evaluate_board to check what to assign that col with:
                initial_scores[w] = self.evaluate_board(board)
                
               
            elif self.ply < Player.PLY_END:  #if the ply reaches less than 0
                initial_scores[w] = Player.OKAY_MOVE  #assignt that col w/ 50

            else:
                #adds move to determine countermoves:
                board.add_move(w, self.side)
                
                #creates opponent player that acts recursively when called:
                opponent_player = (Player(self.opponent(),
                                          self.ply - 1, self.is_random))
                
                #after assessing each of the countermoves, it takes the max of
                #the countermove list in order to create the final list:
                initial_scores[w] = (Player.GOOD_MOVE -
                                     max(opponent_player.score_columns(board)))
                #deletes the move that countermoves are based off of
                board.delete_move(w)

        return initial_scores


       
    def best_move(self, scores):
        """Receives the initial_scores list from score_columns and if there
           are any duplicated max numbers than uses the Boolean from __str__
           to determine how to break the tie.

           Parameters:
                scores - the list of countermove scores from initial_scores

           Returns:
                The column number of the best move in which to play determined
                either randomly or deterministically
        """
        
        tied_highest = []
        max_score = max(scores)
        for index, value in enumerate(scores):
            if value == max_score:
                tied_highest.append(index)#creates a list of all the max scores
       
        if self.is_random == True:
            return random.choice(tied_highest)
        else:    
            return min(tied_highest)
       
       
           
       
    def next_move(self, board):
        """Puts together the modules of best_move and score_move in order to
           start determining what the next move should be.

        Parameters:
           board - the current state that the connect four board is in.

        Returns:
           Recursively calls to both previous modules
        """
        return self.best_move(self.score_columns(board))

def main():
    """Tester function"""
    pass
    #used pass here as an attempt to get rid of runtime error. 

if __name__ == "__main__":
    main()


