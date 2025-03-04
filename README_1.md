# AOthello

By Ophelia Sin

## Usage

Invoke the game with 

$ java -jar othello.jar [options]

and start the client with 

$ python3 sdks/python/client.py 1337 localhost 

Here I specify the listening port and the webserver port as I have run into some issues when I don't specify them. 

## Concept 

The algorithm used in this client is a greedy algorithm, where the player will select the move that can flip the most number of pieces at the time.  