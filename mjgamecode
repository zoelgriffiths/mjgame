import random 
from time import sleep

def invalid(): 
    return "That is not a valid entry. Try again."

def end_game(players_cards,players_not_cards,all_cards): 
    print()
    print()
    print("OH NO")
    print("Someone has been a nincompoop! The game no longer makes sense.See if you can work out what.")
    print("Before the last request, the players' cards were: {}".format(players_cards))
    print()
    print("And the cards players definitely didn't have, were: {}".format(players_not_cards))
    print()
    for i in range(len(all_cards)): 
        print("There were {0} cards in the {1}s suit left in the pack.".format(len(all_cards[i]),i+1))
    print("That's the end of the game!")
    return "end"    

def make_players(number): 
    players = ["User"] + ["Computer {0}".format(i) for i in range(1,number)]
    return players

def make_cards(players):
    card_suits = [i for i in range(1,len(players)+1)] 
    all_cards = []
    for suit in card_suits: 
        all_of_one_suit = [suit]*4    
        all_cards.append(all_of_one_suit)
    return all_cards

def validate_player_choice(choose): 
    if int(choose) >= 1 and int(choose) <= len(players)-1: 
        return choose
        
def validate_choice(choose):
    if choose in ["Y","N"]:
        return choose 

def choose_stuff(players,player,players_cards,players_not_cards,all_cards): 
    if player == "User": 
        if len(players) > 2:
            choose_player = True
            while choose_player:
                player_choose = input("Enter the number (as a digit from 1 to {}) of the computer player that you'd like to ask a question to:  ".format(len(players)-1))
                try:
                    if int(player_choose) > 0 and int(player_choose) < len(players):
                        validated_player = "Computer {}".format(int(player_choose))
                        choose_player = False
                    else: 
                        print(invalid())
                except: 
                    print(invalid())
        else: 
            validated_player = "Computer 1"   
        choose_suit = True
        while choose_suit:
            suit_choose = input("Enter the number (as a digit from 1 to {}) of the suit you'd like to ask about:  ".format(len(players)))
            try:
                if int(suit_choose) > 0 and int(suit_choose) < len(players)+1:
                    validated_suit = int(suit_choose)
                    choose_suit = False
                else:
                    print(invalid())
            except: 
                print(invalid())
    else: 
        validated_player = random.choice([i for i in players if i != player])
        validated_suit = random.choice(possible_suits(player,players_cards,players_not_cards,all_cards))   
    print("The player {0} has chosen to ask player {1} if they have the suit {2}".format(player,validated_player,validated_suit))
    return validated_player,validated_suit

def possible_suits(player,players_cards,players_not_cards,all_cards): 
    possible_suits = []
    for suit in [i for i in range(1,len(players_cards)+1)]: 
        if suit in players_cards[player]: 
            possible_suits.append(suit)
        else: 
            if len(players_cards[player]) < 4: 
                if len(all_cards[suit-1])>0:
                    if suit not in players_not_cards[player]:
                        possible_suits.append(suit)
    return possible_suits
   
def can_player_take(player,suit,players_cards,players_not_cards,all_cards):
    space_left = 4 - len(players_cards[player])
    if suit in possible_suits(player,players_cards,players_not_cards,all_cards):
        can_take = space_left
    else: 
        can_take = 0
    return can_take
     
        
def go(players,player,players_cards,players_not_cards,all_cards):  
    chosen_player,suit = choose_stuff(players,player,players_cards,players_not_cards,all_cards)
    if suit in possible_suits(player,players_cards,players_not_cards,all_cards): 
        if suit not in players_cards[player]:
            players_cards[player].append(all_cards[suit-1].pop(0))
    else: 
        return end_game(players_cards,players_not_cards,all_cards)
    if chosen_player == "User":
        choose_response = True
        while choose_response:
            response_choose = input("Enter Y for Yes, and N for No: ").upper()
            if response_choose not in ["Y","N"]: 
                print(invalid())
            else: 
                validated_response = response_choose
                choose_response = False        
    else:
        if suit in players_cards[chosen_player]:
            validated_response = "Y"
        elif suit in possible_suits(chosen_player,players_cards,players_not_cards,all_cards):
            validated_response = random.choice(["Y","N"])
        else: 
            validated_response = "N"
            
    if validated_response == "Y": 
        words = "do"
    else: 
        words = "don't"
    print("The player {0} has said they {1} have a card of the {2}s suit.".format(chosen_player,words,suit))

    if validated_response == "Y":
        if suit in possible_suits(chosen_player,players_cards,players_not_cards,all_cards): 
            if suit not in players_cards[chosen_player]:
                players_cards[chosen_player].append(all_cards[suit-1].pop(0)) 
        else: 
            return end_game(players_cards,players_not_cards,all_cards)
    else: 
        if suit in players_cards[chosen_player]:
            return end_game(players_cards,players_not_cards,all_cards)
        else: 
            count = 0 
            for person in players: 
                if person != chosen_player:
                    count += can_player_take(person,suit,players_cards,players_not_cards,all_cards)
            if count < len(all_cards[suit-1]):
                return end_game(players_cards,players_not_cards,all_cards)
            else:
                players_not_cards[chosen_player].append(suit)
    

def play_the_game(number=2): 
    
    play_again=True 
    while play_again:
        players = make_players(number)
        all_cards = make_cards(players)
    
        players_cards = {}
        for player in players:
            players_cards[player] = []
        
        players_not_cards = {}
        for player in players: 
            players_not_cards[player] = []
    
    
        play = True 
        while play:
            for player in players: 
                print("NEXT GO")
                status = go(players,player,players_cards,players_not_cards,all_cards)
                sleep(3)
                print()
                print()
                if status == "end": 
                    keep_playing = True 
                    while keep_playing:
                        keep_playing_choose = input("Enter Y to play again. Enter N to exit the game: ").upper()
                        if keep_playing_choose not in ["Y","N"]:
                            print(invalid())
                        else: 
                            if keep_playing_choose == "N":
                                play = False
                                play_again = False 
                            keep_playing = False 
                            play = False     
    return "game over"
    
    
play_the_game(3)  
    
