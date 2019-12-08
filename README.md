# othello.py

Basic text-only implementation of Othello/Reversi.

## Two-player mode

No arguments are required.  'O' goes first.  Moves are input in the format `i j`,
i.e. integer-space-integer.

    $ ./othello.py

    --------------------------
    O: 2                  X: 2
    --------------------------
    1 ( )( )( )( )( )( )( )( )
    2 ( )( )( )( )( )( )( )( )
    3 ( )( )( )( )( )( )( )( )
    4 ( )( )( )(x)(o)( )( )( )
    5 ( )( )( )(o)(x)( )( )( )
    6 ( )( )( )( )( )( )( )( )
    7 ( )( )( )( )( )( )( )( )
    8 ( )( )( )( )( )( )( )( )
       1  2  3  4  5  6  7  8 
    O => 5 6

    --------------------------
    O: 4                  X: 1
    --------------------------
    1 ( )( )( )( )( )( )( )( )
    2 ( )( )( )( )( )( )( )( )
    3 ( )( )( )( )( )( )( )( )
    4 ( )( )( )(x)(o)( )( )( )
    5 ( )( )( )(o)(o)(o)( )( )
    6 ( )( )( )( )( )( )( )( )
    7 ( )( )( )( )( )( )( )( )
    8 ( )( )( )( )( )( )( )( )
       1  2  3  4  5  6  7  8 
    X => 6 6

    --------------------------
    O: 3                  X: 3
    --------------------------
    1 ( )( )( )( )( )( )( )( )
    2 ( )( )( )( )( )( )( )( )
    3 ( )( )( )( )( )( )( )( )
    4 ( )( )( )(x)(o)( )( )( )
    5 ( )( )( )(o)(x)(o)( )( )
    6 ( )( )( )( )( )(x)( )( )
    7 ( )( )( )( )( )( )( )( )
    8 ( )( )( )( )( )( )( )( )
       1  2  3  4  5  6  7  8 

    [...]


## Computer player

Naive (minimal look-ahead) computer players are implemented.  The computer can
stand in for player 'O', player 'X', or both.  There are several options that
have been only just barely tested:

    $ ./othello.py --rand-X         # choose randomly from legal moves
    $ ./othello.py --best-X         # flip as many pieces as possible
    $ ./othello.py --skill-X=1.0    # tune preference for large flip counts

The latter option produces random move selection based on `n_flips**skill`,
where `skill` is a non-zero float.  I haven't yet performed any statistical
analyses to determine the relative performance of these various settings.

Here's one example of a computer-vs-computer match and the resulting final
state:

    $ ./othello.py --best-O --rand-X

    [...]

    --------------------------
    O: 42                X: 22
    --------------------------
    1 (o)(o)(o)(o)(o)(o)(o)(o)
    2 (x)(x)(x)(x)(x)(x)(x)(o)
    3 (x)(x)(x)(o)(o)(x)(x)(o)
    4 (o)(o)(x)(o)(x)(o)(x)(o)
    5 (o)(x)(x)(x)(o)(o)(x)(o)
    6 (o)(o)(o)(o)(x)(o)(x)(o)
    7 (o)(o)(x)(o)(o)(o)(o)(o)
    8 (o)(o)(o)(o)(o)(o)(o)(o)
       1  2  3  4  5  6  7  8 
    No legal moves remain!
    Player "O" wins by 42 - 22.


## TODO

Known TODO items include:

* Decouple game state engine from presentation — alternative UIs could include
  curses, PyQt/PyGTK, some kinda website, etc.

* Store game history and provide interface for saving the logs to disk.
