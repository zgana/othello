#!/usr/bin/env python3

from argparse import ArgumentParser
import re

import numpy as np

class OthelloError(ValueError): pass
class IllegalMove(OthelloError): pass
class InvalidMove(OthelloError): pass

class Space:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.neighbors = {}
        self.player = ''

    def find_neighbors(self, grid):
        N = len(grid)
        neighbors = self.neighbors
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                I, J = self.i + di, self.j + dj
                if not (0 <= I < N and 0 <= J < N):
                    neighbors[di,dj] = None
                else:
                    neighbors[di,dj] = grid[I,J]

    def set(self, player, force=False):
        flips = self.checkmove(player, force=force)
        self.player = player
        for space in flips:
            space.player = player

    def checkmove(self, player, force=False):
        if self.player and not force:
            raise IllegalMove(f'space ({self.i}, {self.j}) already occupied by {self.player}')
        dirs = [(-1,0), (1,0), (0,-1), (0,1)]
        goods = []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                n = self.next(di,dj)
                if n and n.player and n.player != player:
                    goods.append(n)
        if not goods and not force:
            raise IllegalMove(f'illegal move: must place adjacent to opponent')
        flips = []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                cur = self
                chain = [cur]
                while cur.next(di,dj):
                    cur = cur.next(di,dj)
                    if not cur.player:
                        break
                    chain.append(cur)
                    if cur.player == player:
                        break
                if chain[-1].player == player:
                    for space in chain[1:-1]:
                        flips.append(space)
        if not flips and not force:
            raise IllegalMove(f'illegal move: must sandwich opponent')
        return flips

    def next(self, di, dj):
        return self.neighbors[di,dj]


class Board:

    def __init__(self, N=8, othello=True):
        self.othello = othello
        self.N = N
        self.grid = np.array([
            [Space(i, j) for j in range(N)]
            for i in range(N)
        ])
        for space in np.ravel(self.grid):
            space.find_neighbors(self.grid)
        if othello:
            self('O', 3, 4, force=True)
            self('X', 3, 3, force=True)
            self('O', 4, 3, force=True)
            self('X', 4, 4, force=True)

    def __getitem__(self, *x):
        return self.grid.__getitem__(*x)

    def playergrid(self):
        grid, N = self.grid, self.N
        return np.array([
            [grid[i,j].player for j in range(N)]
            for i in range(N) ])

    def __str__(self):
        grid, N = self.grid, self.N
        lines = [''.join('({:1})'.format(grid[i,j].player) for j in range(N))
                  for i in range(N)]
        lines += ['  ' + ''.join(' {} '.format(i+1) for i in range(N))]
        for (i,line) in enumerate(lines[:-1]):
            lines[i] = '{} '.format(chr(ord('a') + i)) + line
        return '\n'.join(lines)

    def __call__(self, player, i, j, force=False):
        self[i,j].set(player, force=force)


class Game:

    def __init__(self, N=8, othello=True,
                 skill_X=0, skill_O=0,
                 best_X=False, best_O=False,
                 rand_X=False, rand_O=False):
        self.board = Board(N=N, othello=othello)
        self.cur_player = 'O'
        self.auto = ''
        if skill_X or best_X or rand_X:
            self.auto += 'X'
        if skill_O or best_O or rand_O:
            self.auto += 'O'
        self.skill = dict(X=skill_X, O=skill_O)
        self.best = dict(X=best_X, O=best_O)
        self.rand = dict(X=rand_X, O=rand_O)
        print(self.auto)

    def move(self, s):
        try:
            rows = re.findall('[a-h]', s)
            assert len(rows) == 1
            i = ord(rows[0]) - ord('a')
            cols = re.findall('[1-8]', s)
            assert len(cols) == 1
            j = int(cols[0]) - 1
        except Exception as e:
            raise InvalidMove(f'could not parse move: "{s}"') from e
        player = self.cur_player
        self.board(player, i, j)
        self.toggleplayer()

    def toggleplayer(self):
        self.cur_player = 'X' if self.cur_player == 'O' else 'O'
        return self.cur_player

    def score(self):
        pgrid = self.board.playergrid()
        O = np.sum(pgrid == 'O')
        X = np.sum(pgrid == 'X')
        return O, X


    def __str__(self):
        O, X = self.score()
        hO = 'O: {}'.format(O)
        hX = 'X: {}'.format(X)
        lO = len(hO)
        lX = len(hX)
        width = 2 + 3 * self.board.N
        header = hO + (width - lO - lX) * ' ' + hX
        div = width * '-'
        out = '\n'.join([div, header, div, str(self.board).lower()])
        return out

    def get_legal_moves(self, player):
        board = self.board
        N = board.N
        moves = []
        n_flips = []
        for i in range(N):
            for j in range(N):
                try:
                    f = board[i,j].checkmove(player)
                    moves.append((i,j))
                    n_flips.append(len(f))
                except IllegalMove:
                    pass
        return moves, np.array(n_flips)

    def play(self):
        orig_player = player = self.cur_player
        print(self)
        hasmoves = self.get_legal_moves(player)[0]
        if not hasmoves:
            player = self.toggleplayer()
            hasmoves = self.get_legal_moves(player)[0]
            if hasmoves:
                print(f'Player "{orig_player}" has no moves; passing to Player "{player}"')
            else:
                print(f'No legal moves remain!')
                self.endgame()
                return

        try:
            if player in self.auto:
                m = self.autoplay()
            else:
                m = input(f'{player} => ')
        except EOFError:
            print('\nGame Ended.')
            self.endgame()
            return
        if m in 'quit'[:len(m)] or m == '':
            print('\nGame Ended.')
            self.endgame()
            return
        print()
        try:
            self.move(m)
        except OthelloError as e:
            print(e)
            pass
        self.play()

    def autoplay(self):
        player = self.cur_player
        moves, n_flips = self.get_legal_moves(player)
        if self.skill[player]:
            p = n_flips ** self.skill[player]
            p /= p.sum()
            i, j = moves[np.random.choice(len(moves), p=p)]
        if self.best[player]:
            i, j = moves[np.argmax(n_flips)]
        else:
            i, j = moves[np.random.choice(len(moves))]
        move = f'{i+1} {j+1}'
        move = f'{chr(ord("a")+i)} {j+1}'
        print(f'{player} => {move} (*computer player*)')
        return move



    def endgame(self):
        O, X = self.score()
        if O == X:
            print(f'Final score is a tie: {O} - {X}.')
        elif O > X:
            print(f'Player "O" wins by {O} - {X}.')
        else:
            print(f'Player "X" wins by {X} - {O}.')


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--skill-O', default=0, type=float)
    parser.add_argument('--best-O', default=False, action='store_true')
    parser.add_argument('--rand-O', default=False, action='store_true')
    parser.add_argument('--skill-X', default=0, type=float)
    parser.add_argument('--best-X', default=False, action='store_true')
    parser.add_argument('--rand-X', default=False, action='store_true')
    opts = parser.parse_args()

    auto = dict(skill_X=opts.skill_X, skill_O=opts.skill_O,
                best_X=opts.best_X, best_O=opts.best_O,
                rand_X=opts.rand_X, rand_O=opts.rand_O)
    g = Game(**auto)
    g.play()
