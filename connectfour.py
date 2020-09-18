
import random
"""
Implementation of a Connect-4 Player class

Author: William Clark and Henry Howell
"""

class Board:
    """A type for representing the state and behavior of a Connect-4 board

    Attributes:
        width - an integer denoting the number of columns in the board
        height - an integer denoting the number of rows in the board
        data - a 2D array (i.e. nested list) of characters (strings of length
               1) representing the current state of each cell of the board.
               The only permitted values for each entry are ' ' (for an
               unoccupied cell), 'X' (denoting a peg belonging to player 1),
               and 'O' (denoting a peg belonging to player 2).
    """
    INVALID_MOVE = -1
    

    def __init__(self, width, height):
        """Constructs an empty board of the specified width and height.

        Parameters:
            width - the number of columns in the board (an int >= 1)
            height - the number of rows in the board (an int >= 1)

        Returns:
            None.
        """
        self.width = width
        self.height = height
        self.data = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(' ')
            self.data.append(row)


    def __str__(self):
        """Generates and returns a string representation of this board object

        Returns:
            A string containing an ASCII representation of the current
            state of this Connect-4 board.
        """
        data_string = ""
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                row += "|" + self.data[i][j]
            row += "|\n"
            data_string += row
        data_string += "-" * (2 * self.width + 1)
        data_string += "\n"

        # Column numbers are labeled modulo 10 to keep the characters
        # aligned correctly
        for i in range(self.width):
            data_string += " " + str(i % 10)

        return data_string


    def add_move(self, column, side):
        """Adds a peg of the specified type to the indicated column

        This method mutates the given Board object, by adding a peg
        to the given column, for the specified player (either 'X' or 'O').
        Due to the action of gravity, the peg "drops" from the top of the
        column to come to rest at the first vacant cell in this column.
        Note that this method performs no bounds-checking to ensure that
        'column' is indeed a valid move.

        Args:
            column - the column number to which we wish to add a peg (an int)
            side - the side making this move (either an 'X' or an 'O')

        Returns:
            None.
        """
        row = 0
        # Find the first occupied cell in this column
        while (row < self.height and self.data[row][column] == " "):
            row = row + 1
        # Now add the new peg to the row above it
        row = row - 1
        self.data[row][column] = side


    def clear(self):
        """Resets this board object so it's once again empty

        Returns:
            None.
        """
        for i in range(self.height):
            for j in range(self.width):
                self.data[i][j] = " "


    def set_board(self, move_string):
        """Accepts a string of column numbers and places alternating pegs in
        them.

        For example, b.set_board('012345') would place alternating
        'X's and 'O's on the bottom-most row (starting with an 'X').

        Parameters:
            move_string - a string containing a sequence of moves to play (a
                          sequence of integers)

        Returns:
            None.
        """
        next_side = "X"
        for col_string in move_string:
            col = int(col_string)
            if col >= 0 and col <= self.width:
                self.add_move(col, next_side)
            if next_side == "X":
                next_side = "O"
            else:
                next_side = "X"


    def allows_move(self, column):
        """Returns whether a legal move may be made in the specified column
        of this board.

        The move is legal if and only if the specified column index falls
        within the width of the board and the column is not already full.

        Parameters:
            column - the column number in which we wish to place a peg (an int)

        Returns:
            A boolean value indicating whether 'column' constitutes a legal
            move on the given board
        """
        return (    (column >= 0)
                and (column < self.width)
                and (self.data[0][column] == " "))


    def is_full(self):
        """Returns whether the current board is completely filled up

        Returns:
            A boolean value indicating whether every column in the calling
            Board object has been filled up
        """
        # If at least one of the columns permits a move, then the board is
        # not full
        for i in range(self.width):
            if self.allows_move(i):
                return False
        return True


    def delete_move(self, column):
        """Removes the top-most peg from the specified column

        If the specified column is empty, then this method has no effect.
        Note that no bounds-checking is performed to ensure that column
        is indeed a valid move.

        Parameters:
            column - the column index from which to remove a peg (an int)

        Returns:
            None.
        """
        row = 0
        # Find the first non-empty cell in the specified column
        while (row < self.height and self.data[row][column] == " "):
            row = row + 1

        # If the column is not empty, remove the top peg
        if (row != self.height):
            self.data[row][column] = " "


    def win_for(self, side):
        """Returns whether the current board position represents a win for
        the specified side

        A player wins by getting four-of-a-kind of their own peg type in a
        row. This can happen either horizontally, vertically or diagonally.
        This method checks whether any of these conditions has been met.

        Parameters:
            side - the player for whom we wish to test for wins ('X' or 'O')

        Returns:
            A boolean value indicating whether the specified player has won
        """
        # Testing rows
        for row in range(self.height):
            for col in range(self.width - 3):
                if (    self.data[row][col] == side
                    and self.data[row][col+1] == side
                    and self.data[row][col+2] == side
                    and self.data[row][col+3] == side):
                    return True

        # Testing columns
        for col in range(self.width):
            for row in range(self.height - 3):
                if (    self.data[row][col] == side
                    and self.data[row+1][col] == side
                    and self.data[row+2][col] == side
                    and self.data[row+3][col] == side):
                    return True

        # Testing left diagonal
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if (    self.data[row][col] == side
                    and self.data[row+1][col+1] == side
                    and self.data[row+2][col+2] == side
                    and self.data[row+3][col+3] == side):
                    return True

        # Testing right diagonal
        for row in range(self.height - 3):
            for col in range(3, self.width):
                if (    self.data[row][col] == side
                    and self.data[row+1][col-1] == side
                    and self.data[row+2][col-2] == side
                    and self.data[row+3][col-3] == side):
                    return True

        return False


    def host_game(self):
        """Wrapper method that runs a complete game of Connect-4

        This method "hosts" a game of Connect-4 by gluing together all the
        other methods. Player 'X' gets to go first. The user is prompted
        to enter moves via the terminal, which are then played on the board.
        User input is validated to ensure that only valid column numbers are
        accepted. When the game terminates, the final state of the board
        is printed along with a message indicating which player won (or if
        the game ended in a tie).

        Returns:
            None.
        """
        current_side = "X"
        while (    (not self.win_for("X"))
               and (not self.win_for("O"))
               and (not self.is_full())):
            print()
            print(self)
            print()
            move = Board.INVALID_MOVE
            while not self.allows_move(move):
                move = int(input(current_side + "'s move: "))
            self.add_move(move, current_side)
            if current_side == "X":
                current_side = "O"
            else:
                current_side = "X"

        if self.win_for("X"):
            print("X wins --- congratulations!\n")
        elif self.win_for("O"):
            print("O wins --- congratulations!\n")
        else:
            print("Tied game!\n")

        print()
        print(self)


    def play_game(self, x_player, o_player):
        """Modified wrapper method that manages a game of Connect-4 between two
        players, each of whom can either be an AI or a human

        This is a modified version of the host_game method that allows for
        one or both of the players to be AI agents (i.e., instances of the
        Player class). When an AI agent is chosen, then that agent's next_move
        method is used to generate moves for that player. When a human player
        is chosen, the terminal is used to solicit moves. To set a certain
        player to be an AI player, pass in a Player instance for that
        parameter; to make a player a human, pass in the string 'human' for
        that parameter.

        Args:
            x_player, o_player - the type of the 'X'/'O' player (either a Player
                                 object or the string 'human')

        Returns:
            Nothing
        """
        #from connectfour import Player     #either from connect4_player or connectfour
        
        current_side = "X"
        players = {"X": x_player, "O": o_player}
        while ((not self.win_for("X")) and
               (not self.win_for("O")) and
               (not self.is_full())):
            print()
            print(self)
            print()
            move = Board.INVALID_MOVE
            while not self.allows_move(move):
                if players[current_side] == "human":
                    move = int(input(current_side + "'s move: "))
                else:
                    move = players[current_side].next_move(self)
                    print("Computer playing for " + current_side +
                          " plays at " + str(move))

            self.add_move(move, current_side)
            if current_side == "X":
                current_side = "O"
            else:
                current_side = "X"

        if self.win_for("X"):
            print("X wins --- congratulations!\n")
        elif self.win_for("O"):
            print("O wins --- congratulations!\n")
        else:
            print("Tied game!\n")

        print()
        print(self)

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