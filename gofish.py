import random 
from time import sleep
from itertools import combinations
from itertools import product
import copy 


def invalid(): 
    return "That is not a valid entry. Try again."


#If someone makes a mistake such that there is a paradox in the game this function is called.
def end_game(players_cards,players_not_cards,all_cards,how_many_cards): 
    print()
    print()
    print("OH NO")
    print("Someone has been a nincompoop! The game no longer makes sense. See if you can work out what has gone wrong.")
    print()
    print("The cards we knew each player had: {}".format(players_cards))
    print("And the suits we knew players definitely didn't have: {}".format(players_not_cards))
    print("And the number of cards each player has: {}".format(how_many_cards))
    print()
    print("That's the end of the game!")
    print()
    return "end"    


def make_players(number): 
    players = ["User"] + ["Computer {0}".format(i) for i in range(1,number)]
    return players


#The suits are named after the positive integers from 1 to the number of players in the game.
def make_cards(players):
    card_suits = [i for i in range(1,len(players)+1)] 
    all_cards = []
    for suit in card_suits: 
        all_of_one_suit = [suit]*4    
        all_cards.append(all_of_one_suit)
    return all_cards


#Returns a list of suits that could (definitely or possibly) be in the hand of a particualr player. 
def possible_suits(player,players_cards,players_not_cards,all_cards): 
    possible_suits = []
    for suit in range(1,len(all_cards)+1):      
    #A particular suit gets added to the list if:
    
        #The suit is in the cards we know the player defintiely has (initialised line 312 - 325). 
        if suit in players_cards[player]: 
            possible_suits.append(suit)
        
        #Or if there are some cards of that suit left unallocated, and the suit is not in the list of suits the player definitely doesn't have (initialised line 312 - 325).
        else: 
            if len(all_cards[suit-1])>0:
                if suit not in players_not_cards[player]:
                        possible_suits.append(suit)
    return possible_suits



def choose_stuff(player,players,players_cards,players_not_cards,all_cards): 
    
    #If it is the user's go: 
    if player == "User": 
        
        #User chooses which of the computer players to ask (if there is more than one computer player)
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
            
        #And the user chooses a suit to ask about.
        choose_suit = True
        while choose_suit:
            suit_choose = input("Enter the number (as a digit from 1 to {}) of the suit you'd like to ask about:  ".format(len(players)))
            if int(suit_choose)-float(suit_choose) == 0 and int(suit_choose) > 0 and int(suit_choose) < len(players)+1:
                validated_suit = int(suit_choose)
                choose_suit = False
            else:
                print(invalid())
                
    #If it is a computer player's go: 
    else: 
        #The computer chooses a player that is not them.
        validated_player = random.choice([i for i in players if i != player])
        
        #And then chooses a suit
        validated_suit = random.choice(possible_suits(player,players_cards,players_not_cards,all_cards))
    
    #Printing and returning the two choices.
    print("The player '{0}' has chosen to ask player '{1}' if they have the suit {2}.".format(player,validated_player,validated_suit)) 
    return validated_player,validated_suit



def reply(suit,chosen_player,players_cards,players_not_cards,all_cards): 
    
    #If the user is the chosen player they choose if they have the suit they're being asked about.
    if chosen_player == "User":
        choose_response = True
        while choose_response:
            response_choose = input("Enter Y for Yes, and N for No: ").upper()
            if response_choose not in ["Y","N"]: 
                print(invalid())
            else: 
                validated_response = response_choose
                choose_response = False 
    
    #If a computer player is the chosen player:
    else:
        #The computer replies yes if the suit is in the cards we know they definitely have.
        if suit in players_cards[chosen_player]:
            validated_response = "Y"
            
        #If it's not a suit they defintely have, but one they possibly have, they get to chose their response randomly (yes, this means the computer may make a 'human-like' mistake, and cause a paradox!)
        elif suit in possible_suits(chosen_player,players_cards,players_not_cards,all_cards):
            validated_response = random.choice(["Y","N"])
        else: 
            validated_response = "N"  
    
    #Printing and returning the chosen player's response
    if validated_response == "Y": 
        words = "do"
    else: 
        words = "don't"  
    print("The player '{0}' has said they {1} have a card of the {2}s suit.".format(chosen_player,words,suit))
    return validated_response



 #This function checks if the hands of all the players are 'determined'. The hands are determined if there is only one possible way the cards can be held by the players.
def is_it_determined(players,players_cards,players_not_cards,all_cards,how_many_cards):
    
    #First find how many more cards each player can have allocated to them.
    space_left = []
    for player in players:
        space_left.append(how_many_cards[player] - len(players_cards[player]))       
        
    #Find for each player, the list of cards that could possibly be allocated to them.
    poss_cards_everyone = []
    for i in range(len(players)): 
        poss_cards_for_each_player = []
        if space_left[i] > 0:
            for m in range(len(all_cards)): 
                if m+1 in possible_suits(players[i],players_cards,players_not_cards,all_cards): 
                    poss_cards_for_each_player += all_cards[m]
                    
        #If the player has no space for more cards they get an empty list here instead.
        else: 
            poss_cards_for_each_player = []   
        poss_cards_everyone.append(poss_cards_for_each_player)
        
    #Find for each player, all the ways the remaining cards could be allocated to them. That is, all the different ways of choosing the number of cards they need to complete their hand, from their possible cards.    
    all_combs = []
    for i in range(len(players)):     
        combs = set(combinations(poss_cards_everyone[i],int(space_left[i])))
        all_combs.append(combs) 
        
    #Find all the different results that come from each player choosing one of their possible allocations of remaining cards.
    card_arrangements = list(product(*all_combs, repeat=1))
    
    #Lots of these results/card arrangements are not possible as the players' allocations are not mututally compatible. The code below works out how many of the arragements are possible.
    
    correct_card_arrangement = []                          
    count = 0
    for i in range(len(card_arrangements)):
        dummy_poss_cards = copy.deepcopy(poss_cards_everyone)
        for pg in range(len(players)):
            
            #We do this by for each card a particular player is hypothetically given, removing it from the possible cards of each of the other players. 
            for card in card_arrangements[i][pg]:
                for pl in range(len(players)):
                    if pl != pg: 
                        if card in dummy_poss_cards[pl]:
                            dummy_poss_cards[pl].remove(card)
                            
        #Turning the card arrangements into list form.
        list_2 = []
        for person in range(len(players)):
            list_1 =[]
            for cell in card_arrangements[i][person]:
                list_1.append(cell)
            list_2.append(list_1)
        
        #Possible/consistent card arrangements would give a set of possible cards that is identical to the card arrangement itself. Because in this situation each player's redundant cards are used by someone else, and the cards they need to be allocated are not being taken by someone else. 
        if dummy_poss_cards == list_2: 
           count += 1
           correct_card_arrangement.append(list_2)
    
    #If there is more than one possible arrangement, the hands are not determined.
    if count > 1:
        determined = "no"
        return determined,"nothing"
    
    #If there is exactly one, the hands are determined.
    elif count == 1:
        determined = "yes"
        correct_cards = dict(zip(players,correct_card_arrangement[0]))
        return determined,correct_cards
    
    #If there are none or fewer, this means the last person who replied created a paradox and the game ends.
    else:
        return end_game(players_cards,players_not_cards,all_cards,how_many_cards),"nothing"
        
        
       
    
#This function make a player's 'go' happen.        
def go(player,players,players_cards,players_not_cards,all_cards,how_many_cards):  
    
    #The player whose go it is chooses a player to ask and a suit to ask about.
    chosen_player,suit = choose_stuff(player,players,players_cards,players_not_cards,all_cards)
    
    #If the suit they ask about is one they possibly but not definitely have, it becomes one they definitely have, unless they have no more cards left unidentified. In that case, the game ends.
    if suit in possible_suits(player,players_cards,players_not_cards,all_cards): 
        if suit not in players_cards[player]:
            if how_many_cards[player] > len(players_cards[player]):
                players_cards[player].append(all_cards[suit-1].pop(0))
            else:
                return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
            
    #If that suit is not in their possible suits, in which case they've created a paradox and ended the gane.     
    else: 
        return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
    
    #Check for more sutble paradoxes by checking it's possible for all the cards to be consistenly allocated in atleast one way at this point. Game will end if not.
    determined_after_choices = is_it_determined(players,players_cards,players_not_cards,all_cards,how_many_cards)
    if determined_after_choices[0] == "end":
        return "end"
    
    sleep(3)
    print()
    print("After ASKING:")
    print("Cards we know each player has:{}".format(players_cards))
    print("Suits we know each player does not have:{}".format(players_not_cards))
    print("Number of cards each player has: {}".format(how_many_cards))
    print()
    sleep(6)
    
    #The chosen player makes their response
    validated_response = reply(suit,chosen_player,players_cards,players_not_cards,all_cards)
    
    #If they say yes:
    if validated_response == "Y":
        
        #But it's not one of their possible suits, the game ends:
        if suit not in possible_suits(chosen_player,players_cards,players_not_cards,all_cards): 
            return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
        
        #Or if it one of their possible suits we accept their response of yes, giving them a copy of it if they don't already have one in their definite cards.
        else: 
            if suit not in players_cards[chosen_player]:
                if how_many_cards[player] > len(players_cards[player]):
                    players_cards[chosen_player].append(all_cards[suit-1].pop(0))  
                else: 
                    return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
        
    #If they say no:
    else:   
        #And it's a suit we know they definitely have, the game ends.
        if suit in players_cards[chosen_player]:
            return end_game(players_cards,players_not_cards,all_cards,how_many_cards)
        
        else: 
            #Otherwise, we accept their decision to not have that suit, and if it's not already in the list of suits they definiely don't have then the suit gets added to that list.
                if suit not in players_not_cards[chosen_player]:
                    players_not_cards[chosen_player].append(suit) 
                    
    #Now check for more subtle paradoxes by checking it's possible after the response for all the cards to be consistenly allocated in atleast one way. Game will end if not.
    determined_after_reply = is_it_determined(players,players_cards,players_not_cards,all_cards,how_many_cards)
    if determined_after_reply[0] == "end":
        return "end"
    
                    
    #If the chosen player says yes (and the game doesn't end), then they give the asking player a card of that suit. 
    if validated_response == "Y":
        
        #this changes how many cards the chosen player and asking player have.
        how_many_cards[chosen_player] -= 1
        how_many_cards[player] += 1
        
        #This takes a card of the suit from the chosen player and gives it to the asking player.
        players_cards[chosen_player].remove(suit)
        players_cards[player].append(suit)      
            
    print()
    sleep(3)
    print("After REPLYING:")
    print("Cards we know each player has:{}".format(players_cards))
    print("Suits we know each player does not have:{}".format(players_not_cards))
    print("Number of cards each player has: {}".format(how_many_cards))
    print()
    sleep(6)
    
    #Checking the programme: shouldn't print anything if there are no code mistakes.
    total_cards = 0
    for person in players: 
        total_cards += how_many_cards[person]
    if total_cards != len(players)*4: 
        print("Ooops this game is broken")
 
    
def play_the_game(number):  
    
    #Making and intialising things we need in the game
    
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
        
        #Players take turns to have a go.
        for player in players: 
            print("NEXT GO:")
            status = go(player,players,players_cards,players_not_cards,all_cards,how_many_cards)
            
            #If there is not a paradox (end_game), we check if the hands are determined.   
            if status == "end":
                game = "end"
                break
            else:
                determined = is_it_determined(players,players_cards,players_not_cards,all_cards,how_many_cards)
                if determined[0] == "yes":
                    print("DETERMINED:")
                    print("The hands are now determined. So the player '{0}' is the winner as they had the last go.".format(player))
                    print()
                    print("The cards we knew each player had: {}".format(players_cards))
                    print("The suits we knew each player definitely didn't have:{}".format(players_not_cards))
                    print("And the number of cards each player has: {}".format(how_many_cards))
                    print()
                    print("There is only one possible way the remaining cards (the cards we don't explicitly know the location of) can be arranged at this moment. The remaining cards must have been allocated as such: {}".format(determined[1]))
                    print()
                    game = "end"
                    break
                elif determined[0] == "end":
                    game = "end"
                    break
                    
                #if the game is not determined we then check if any of the players have won by having all four cards of the same suit.
                else: 
                    for suit in range(1,number+1):
                        who_can_have_it = []
                        
                        #For any suit, each player who could have that suit is allocated a 1.
                        for human in players:
                            if suit in possible_suits(human,players_cards,players_not_cards,all_cards):
                                who_can_have_it.append(1)
                                
                        #If only one player gets allocated a 1, that means they have all the cards of that suit.(If there are no cards left unallocated from a suit, that suits gets removed from the possible cards of all the other players).
                        if sum(who_can_have_it) == 1:
                            winner = players[who_can_have_it.index(1)]
                            winning_suit = suit
                            
                            print("We have a winner! '{0}' must have all the {1}s, therefore they are the winner.".format(winner,suit))
                            print("The cards we knew each player had are: {}".format(players_cards))
                            print("The suits we knew each player definitely didn't have are:{}".format(players_not_cards))
                            print("And the number of cards each player has are: {}".format(how_many_cards))
                            game = "end"
                        else: 
                            game = "keep going"
                            print()
                        if game == "end": 
                            break
        if game == "end":
            play = False 
       
    
  
 #This is the function to call to start the game.
def start_the_game(): 
    print("Welcome to the game 'Quantum Go Fish'. The rules are here: https://stacky.net/wiki/index.php?title=Quantum_Go_Fish")
    sleep(3)
    print()
    print("Read the rules before you play the game so you know what's going on. In my version the suits are already named. They are named after the positive integers from 1 up to the number of players in the game.")
    print()
    print("The computer players might make mistakes that end the game for everyone just like a human might, but they are not actually trying to win the game, like a human is. It may run slowly with more than three players.")
    print()
    sleep(3)
    play_again = True
    while play_again:
        
        #The User chooses how many players to have in the game.
        get_number = True
        while get_number:
            number_of_players = input("Now choose how many players (atleast 2) that you'd like to have in the game, including yourself: ")
            print()
            if int(number_of_players) - float(number_of_players) == 0 and int(number_of_players)>1:
                number = int(number_of_players)
                get_number = False
            else: 
                print(invalid()) 
                
        #The game is played.
        play_the_game(number) 
        print()
        
        #User is asked if they want to play again.
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
