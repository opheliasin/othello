# AOthello

By Ophelia Sin

## Usage

Invoke the game with 

    $ java -jar othello.jar [options]

and start the client with 

    $ python3 sdks/python/client.py 1337 localhost 

Here I specified the listening port and the webserver port as I ran into some issues when I don't do so.

I am using Python 3.7 and Java 17.

## Concept  
For each round, the player traverses through the entire game board. 

At each empty cell, the player checks all 8 directions to find an opponent's piece. If an opponent's piece is found in one direction, the player will keep traversing in the same direction to find its own piece (until it gets to its own piece or an empty cell or goes out of bounds). If it can find its own piece, it'll tally the number of pieces it can potentially flip if placing the piece in that empty cell. It'll then traverse another direction to see if it can flip more pieces under the same criteria. 

The algorithm used by this player is a greedy algorithm. After traversing the whole game board, the player will select the move (the cell to place the new piece) that can flip the most number of pieces at the time. 

## Assumptions and Constraints
- In this implementation, we only used the strategy of finding the move that flips the most number of pieces.
- I've tried implementing the approach "Limit the number of disks you flip over early in the game" specifieid in this [wikihow article](https://www.wikihow.com/Play-Othello), but it performed worse than the simple greedy approach.
- If more time was available, I would like to explore implementing other algorithms mentioned in the article, like "Wait to place disks in spaces where your opponent can’t play". 