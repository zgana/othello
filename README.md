# othello.py

Basic text-only implementation of Othello/Reversi.

## Two-player mode

No arguments are required.  'O' goes first.  Moves are input in the format
`[row][column]` or `[column][row]`, i.e. row letter and column number.  Spaces
are allowed but have no effect.

    $ ./othello.py

    --------------------------
    O: 2                  X: 2
    --------------------------
    a ( )( )( )( )( )( )( )( )
    b ( )( )( )( )( )( )( )( )
    c ( )( )( )( )( )( )( )( )
    d ( )( )( )(x)(o)( )( )( )
    e ( )( )( )(o)(x)( )( )( )
    f ( )( )( )( )( )( )( )( )
    g ( )( )( )( )( )( )( )( )
    h ( )( )( )( )( )( )( )( )
       1  2  3  4  5  6  7  8
    O => e6

    --------------------------
    O: 4                  X: 1
    --------------------------
    a ( )( )( )( )( )( )( )( )
    b ( )( )( )( )( )( )( )( )
    c ( )( )( )( )( )( )( )( )
    d ( )( )( )(x)(o)( )( )( )
    e ( )( )( )(o)(o)(o)( )( )
    f ( )( )( )( )( )( )( )( )
    g ( )( )( )( )( )( )( )( )
    h ( )( )( )( )( )( )( )( )
       1  2  3  4  5  6  7  8
    X => 6 f

    --------------------------
    O: 3                  X: 3
    --------------------------
    a ( )( )( )( )( )( )( )( )
    b ( )( )( )( )( )( )( )( )
    c ( )( )( )( )( )( )( )( )
    d ( )( )( )(x)(o)( )( )( )
    e ( )( )( )(o)(x)(o)( )( )
    f ( )( )( )( )( )(x)( )( )
    g ( )( )( )( )( )( )( )( )
    h ( )( )( )( )( )( )( )( )
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
    a (x)(x)(x)(o)(o)(o)(o)(o)
    b (x)(x)(x)(x)(o)(o)(o)(x)
    c (x)(x)(o)(o)(o)(o)(x)(o)
    d (o)(x)(o)(o)(o)(x)(o)(o)
    e (o)(x)(o)(o)(x)(x)(o)(o)
    f (o)(x)(o)(x)(x)(o)(o)(o)
    g (o)(x)(x)(o)(o)(o)(o)(o)
    h (o)(x)(o)(o)(o)(o)(o)(o)
       1  2  3  4  5  6  7  8
    No legal moves remain!
    Player "O" wins by 42 - 22.


## TODO

Known TODO items include:

* Decouple game state engine from presentation — alternative UIs could include
  curses, PyQt/PyGTK, some kinda website, etc.

* Store game history and provide interface for saving the logs to disk.
