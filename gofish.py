import random 
from time import sleep
from itertools import combinations
from itertools import product
import copy 

def invalid(): 
    return "That is not a valid entry. Try again."


def end_game(players_cards,players_not_cards,all_cards,how_many_cards): 
    print()
    print()
    print("OH NO")
    print("Someone has been a nincompoop! The game no longer makes sense. See if you can work out what has gone wrong.")
    print("The cards we knew each player had are: {}".format(players_cards))
    print()
    print("And the suits we knew players definitely didn't have, were: {}".format(players_not_cards))
    print("And the number of cards each player has: {}".format(how_many_cards))
    print()
    for i in range(len(all_cards)): 
        print("There were {0} cards in the {1}s suit left in the pack.".format(len(all_cards[i]),i+1))
    print("That's the end of the game!")
    print()
    print()
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


def choose_stuff(player,players,players_cards,players_not_cards,all_cards): 
    if player == "User": 
        if len(players) > 2:
            choose_player = True
            while choose_player:
                player_choose = input("Enter the number (as a digit from 1 to {}) of the computer player that you'd like to ask a question to:  ".format(len(players)-1))
                if int(player_choose)-float(player_choose) == 0 and int(player_choose) > 0 and int(player_choose) < len(players):
                    validated_player = "Computer {}".format(player_choose)
                    choose_player = False
                else:
                    print(invalid())
        else: 
            validated_player = "Computer 1"   
        choose_suit = True
        while choose_suit:
            suit_choose = input("Enter the number (as a digit from 1 to {}) of the suit you'd like to ask about:  ".format(len(players)))
            if int(suit_choose)-float(suit_choose) == 0 and int(suit_choose) > 0 and int(suit_choose) < len(players)+1:
                validated_suit = int(suit_choose)
                choose_suit = False
            else:
                print(invalid())
    else: 
        validated_player = random.choice([i for i in players if i != player])
        validated_suit = random.choice(possible_suits(player,players_cards,players_not_cards,all_cards))    
    print("The player {0} has chosen to ask player {1} if they have the suit {2}".format(player,validated_player,validated_suit)) 
    return validated_player,validated_suit


def possible_suits(player,players_cards,players_not_cards,all_cards): 
    possible_suits = []
    for suit in range(1,len(all_cards)+1): 
        if suit in players_cards[player]: 
            possible_suits.append(suit)
        else: 
            if len(all_cards[suit-1])>0:
                if suit not in players_not_cards[player]:
                        possible_suits.append(suit)
    return possible_suits


def can_player_take(suit,player,players_cards,players_not_cards,all_cards,how_many_cards):
    space_left = how_many_cards[player] - len(players_cards[player])
    if suit in possible_suits(player,players_cards,players_not_cards,all_cards):
        can_take = space_left
    else: 
        can_take = 0
    return can_take


def reply(suit,chosen_player,players_cards,players_not_cards,all_cards): 
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
    return validated_response
       
        
def go(player,players,players_cards,players_not_cards,all_cards,how_many_cards):  
    chosen_player,suit = choose_stuff(player,players,players_cards,players_not_cards,all_cards)
    if suit in possible_suits(player,players_cards,players_not_cards,all_cards): 
        if suit not in players_cards[player]:
            players_cards[player].append(all_cards[suit-1].pop(0))
    else: 
        return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
    sleep(3)
    print()
    print("After ASKING:")
    print("Cards we know each player has:{}".format(players_cards))
    print("Suits we know each player does not have are:{}".format(players_not_cards))
    print("Number of cards each player has: {}".format(how_many_cards))
    print()
    sleep(8)
    validated_response = reply(suit,chosen_player,players_cards,players_not_cards,all_cards)
    if validated_response == "Y":
        if suit not in possible_suits(chosen_player,players_cards,players_not_cards,all_cards): 
            return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
    else: 
        if suit in players_cards[chosen_player]:
            return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
        else: 
            count = 0 
            for person in players: 
                if person != chosen_player:
                    count += can_player_take(suit,person,players_cards,players_not_cards,all_cards,how_many_cards)
            if count < len(all_cards[suit-1]):
                return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
            else:
                if suit not in players_not_cards[chosen_player]:
                    players_not_cards[chosen_player].append(suit)         
    if validated_response == "Y":
        how_many_cards[chosen_player] -= 1
        how_many_cards[player] += 1
        if suit in players_cards[chosen_player]:
            players_cards[chosen_player].remove(suit)
            players_cards[player].append(suit)     
        else:
            players_cards[player].append(all_cards[suit-1].pop(0))     
    print()
    sleep(3)
    print("After REPLYING:")
    print("Cards we know each player has:{}".format(players_cards))
    print("Suits we know each player does not have are:{}".format(players_not_cards))
    print("Number of cards each player has: {}".format(how_many_cards))
    print()
    sleep(8)
    total_cards = 0
    for person in players: 
        total_cards += how_many_cards[person]
    if total_cards != len(players)*4: 
        print("Ooops this game is broken")
 

def is_it_determined(players,players_cards,players_not_cards,all_cards,how_many_cards):
    space_left = []
    for player in players:
        if how_many_cards[player] - len(players_cards[player]) > 0:
            space_left.append(how_many_cards[player] - len(players_cards[player]))
        else:
            space_left.append(0)                                                      
    poss_cards_everyone = []
    for i in range(len(players)): 
        poss_cards_for_each_player = []
        if space_left[i] > 0:
            for m in range(len(all_cards)): 
                if m+1 in possible_suits(players[i],players_cards,players_not_cards,all_cards): 
                    poss_cards_for_each_player += all_cards[m]            
        else: 
            poss_cards_for_each_player = []   
        poss_cards_everyone.append(poss_cards_for_each_player)
    all_combs = []
    for i in range(len(players)):     
        combs = set(combinations(poss_cards_everyone[i],int(space_left[i])))
        all_combs.append(combs)   
    card_arrangements = list(product(*all_combs, repeat=1))
    correct_card_arrangement = []                          
    count = 0
    for i in range(len(card_arrangements)):
        dummy_poss_cards = copy.deepcopy(poss_cards_everyone)
        for pg in range(len(players)):
            for card in card_arrangements[i][pg]:
                for pl in range(len(players)):
                    if pl != pg: 
                        if card in dummy_poss_cards[pl]:
                            dummy_poss_cards[pl].remove(card)
        list_2 = []
        for person in range(len(players)):
            list_1 =[]
            for cell in card_arrangements[i][person]:
                list_1.append(cell)
            list_2.append(list_1)
        if dummy_poss_cards == list_2: 
           count += 1
           correct_card_arrangement.append(list_2)
    if count > 1:
        determined = "no"
        return determined,"nothing"
    elif count == 1:
        determined = "yes"
        correct_cards = dict(zip(players,correct_card_arrangement))
        return determined,correct_cards
    else:
        print("It thinks there is not a way of the cards now being allocated. Something has gone wrong with the game.")
        return end_game(players_cards,players_not_cards,all_cards,how_many_cards),"nothing"
        
    
def play_the_game(number):   
    players = make_players(number)
    all_cards = make_cards(players)    
    how_many_cards = {}
    for player in players: 
        how_many_cards[player] = 4
    players_cards = {}
    for player in players:
        players_cards[player] = []   
    players_not_cards = {}
    for player in players: 
        players_not_cards[player] = []
    play = True 
    while play:
        for player in players: 
            print("NEXT GO:")
            status = go(player,players,players_cards,players_not_cards,all_cards,how_many_cards)
            if status == "end":
                game = "end"
            else:
                determined = is_it_determined(players,players_cards,players_not_cards,all_cards,how_many_cards)
                if determined[0] == "yes":
                    print("The game is now determined. So the player {0} is the winner as they had the last go.".format(player))
                    print("The cards we knew each player had are: {}".format(players_cards))
                    print("The suits we knew each player definitely didn't have are:{}".format(players_not_cards))
                    print("And we can see here how many cards each player has: {}".format(how_many_cards))
                    print("There is only way the cards we don't explicitly know about can be held at this moment. The remaining cards are allocated as such: {}".format(determined[1]))
                    print()
                    game = "end"
                    break
                elif determined[0] == "end":
                    game = "end"
                    break
                else: 
                    for suit in range(1,number+1):
                        who_can_have_it = []
                        for human in players:
                            if suit in possible_suits(human,players_cards,players_not_cards,all_cards):
                                who_can_have_it.append(1)
                        if sum(who_can_have_it) == 1:
                            winner = players[who_can_have_it.index(1)]
                            winning_suit = suit
                            print("We have a winner! {0} must have all the {1}s".format(winner,suit))
                            print("The cards we knew each player had are: {}".format(players_cards))
                            print("The suits we knew each player definitely didn't have are:{}".format(players_not_cards))
                            print("And we can see here how many cards each player has: {}".format(how_many_cards))
                            game = "end"
                            break
                        else: 
                            game = "keep going"
                            print()
        if game == "end":
            play = False 
                                         
    
def start_the_game(): 
    print("Welcome to the game 'Quantum Go Fish'. This is a f***ing ridiculous game that has taken over my life for the last couple of days. The rules are here: https://stacky.net/wiki/index.php?title=Quantum_Go_Fish")
    sleep(3)
    print()
    print("Read the rules before you play the game so you know what's going on.In my version the suits are already named. They are named after the positive integers from 1 up to the number of players in the game.")
    print()
    print("The computer players might make mistakes that end the game for everyone just like a human might, but they are not actually trying to win the game, like a human is. It may run slowly with more than three players.")
    print()
    sleep(3)
    play_again = True
    while play_again:
        get_number = True
        while get_number:
            number_of_players = input("Now choose how many players (atleast 2) that you'd like to have in the game, including yourself: ")
            print()
            if int(number_of_players) - float(number_of_players) == 0 and int(number_of_players)>1:
                number = int(number_of_players)
                get_number = False
            else: 
                print(invalid())   
        play_the_game(number) 
        print()
        keep_playing = True 
        while keep_playing:
            keep_playing_choose = input("Enter Y to play again. Enter N to exit the game: ").upper()
            if keep_playing_choose not in ["Y","N"]:
                print(invalid())
            else: 
                if keep_playing_choose == "N":
                    play_again = False 
                else: 
                    print()
                    print()
                keep_playing = False                                      
    return "game over"
    
start_the_game()
