import random

class board_game():
    
    def __init__(self):
        self.board = ["-" for a in range(3)]
        self.board[0] = "O"
        
    def shuffle(self):
        random.shuffle(self.board)
        
    def __str__(self):
        return f'board game is ready'



class Player():
    
    def __init__(self, name):
        self.name = name    
        
    def __str__(self):
        return f'{self.name}'


class Chips():
    
    def __init__(self):
        self.chips = 100
        self.bet = 0
        
    def bet_win(self):
        self.chips += self.bet

    def bet_loss(self):
        self.chips -= self.bet


def bet(chips):
    
    chips.bet = int(input('Place your bet: '))

def guess():
    
    guess = int(input('Please quess a nut from 0 to 2: '))
    return guess

from datetime import datetime
def save_game(name, chips):
    
    name = player.name
    chips = chips.chips
    date = datetime.now()
    
    with open('C:\Coding\Python\Python_Projects\saved_games.txt', 'a+') as f:
        f.write(f'player: {name} with {chips} of chips on {date}\n')

player = Player("Ales")
table = board_game()
players_chips = Chips()
print(table)

while True:

    players_bet = bet(players_chips)
    player_guess = guess()
    table.shuffle()

    if table.board[player_guess] == "O":
        print('you win')
        players_chips.bet_win()
        print(f'player {player.name} has {players_chips.chips}')
    else:
        print('you lose')
        players_chips.bet_loss()
        print(f'player {player.name} has {players_chips.chips}')

    game_on = input('Do you want to play again? y or n: ')
    
    if game_on == 'n':      
        save = input('Do you want to save game? y or n: ')
        if save == 'y':
            save_game(player, players_chips)
        else:
            pass
        break
