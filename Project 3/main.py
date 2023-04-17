import random
import copy
import time
from properties import *

MAX_ROUNDS = 1000

'''
Initializing game board with builtin dictionary data structure
* Game's rule for this version of Monopoly:
    1. Eliminated Chances and Community chest cards.
    2. No Trade and Auction.
    3. No double dice rule(i mean if 3 times happend then player should go to jail).
    4. One action per turn.
    5. No color(it means streets dont have any color and if player landed on a street can buy it and build house and hotels for it).
    6. No sell option(yet).
    7. if player land on 'Go Jail' goes to 'jail' and must give 100$ and start the game from there
'''
class stats:
    def __init__(self, id, location, balance, jail, ownedP, ownedRR, ownedUT):
        self.id = id # store the id of each player (int: 1 , 2)
        self.location = location  # store the location of the player (string or index of dictionary)
        self.balance = balance  # store the amount of money the player has (int data)
        self.jail = jail  # store whether the player is in jail or not (bool data) (for future updates!!)
        self.ownedP = ownedP  # store the properties that the player has bought (list of property names or index)
        self.ownedRR = ownedRR  # store the railroads that the player has bought (list of railroad names or index)
        self.ownedUT = ownedUT  # store the utilities that the player has bought (list of utility names or index)

# set up players with stats class
players = {}
for count in range(1, 3):
     players.update({count: stats(count, 0, 1500, False, [],[], [])})

number_of_players = 2
current_player = 1
player_left = number_of_players
round_num = 0

# defining some important functions:
# roll dice return a tuple of two numbers that they generated randomly.
def roll_dice():
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    return (dice1, dice2)

# updates players location.
def move_player(player, rolls): 
    current_location = player.location
    
    roll = rolls[0] + rolls[1]
    
    # calculate the new location by adding the roll to the current location
    new_location = (current_location + roll) % 34
    
    # update the player's location
    player.location = new_location

def is_terminal(player):
     if player.balance <= 0:
         return True
     return False

def purchase(player):
     prop_type = properties[player.location]["type"]
     owner_id  = properties[player.location]["owner"]

     if  prop_type in ["property", "railroad", "utility"] and owner_id == "none":
          properties[player.location]["owner"] =  player.id
          player.balance -= properties[player.location]["price"]
          
          if prop_type == "property":
               player.ownedP.append(player.location)
          
          elif prop_type == "railroad":
               player.ownedRR.append(player.location) 

          elif prop_type == "utility":
               player.ownedUT.append(player.location) 
     
     elif owner_id != "none":
          raise ValueError("This propertie is owned by other player(ownership error)")
    
     else:
          raise ValueError("You can't buy this place(type error)")

def charge_rent(player):
     rent = properties[player.location]["rent"]
     owner_id = properties[player.location]["owner"]

     if owner_id != "none" and owner_id != player.id:
          if properties[player.location]["hotels"] == 0:
               player.balance = player.balance - (rent + 10*properties[player.location]["houses"])
               players[owner_id].balance = players[owner_id].balance + (rent + 10*properties[player.location]["houses"])
          else:
               player.balance = player.balance - (rent + 10*(properties[player.location]["houses"] + 1))
               players[owner_id].balance = players[owner_id].balance + (rent + 10*(properties[player.location]["houses"] + 1))
      

def build_house(player, property):
     # Check if the property belongs to the player and is a valid property to build on
     if property in player.ownedP and properties[property]["houses"] < 4:
          
          # Check if the player has enough money to build a house
          if player.balance >= properties[property]["hPrice"]:
               # Subtract the cost of the house from the player's balance
               player.balance -= properties[property]["hPrice"]
               # Increase the number of houses on the property by 1
               properties[property]["houses"] += 1
     
def build_hotel(player, property):
     if property in player.ownedP and properties[property]["type"] == "property" and properties[property]["houses"] == 4:
          if player.balance >= properties[property]["hPrice"]:
               player.balance -= properties[property]["hPrice"]
               properties[property]["houses"] = 0
               properties[property]["houses"] = True
     
def switch_player(current_player):
     if current_player == 1:
          current_player = 2
     else:
          current_player = 1
     return current_player

def get_valid_actions(player):
     actions = []

     if properties[player.location]["name"] in ["Go", "Just Visiting/Jail", "Free Parking"]:
          actions.append(all_actions[0])
          
     elif properties[player.location]["name"] == "Go To Jail":
          actions.append(all_actions[6])

     # Check if player is on a property
     elif properties[player.location]["type"] in ["property", "railroad", "utility"]:
          # Check if the property is unowned
          if properties[player.location]["owner"] == "none":
               # Add the "BUY_PROP" action
               actions.append(all_actions[0])
               actions.append(all_actions[1])

          elif properties[player.location]["owner"] != player.id:
               # Add the "PAY_RENT" action
               actions.append(all_actions[2])
          elif properties[player.location]["type"] == "property":
               # Add the "BUILD_HOUSE" or "BUILD_HOTEL" action
               if player.balance >= properties[player.location]["hPrice"] and properties[player.location]["houses"] < 4:
                    # Add the "BUILD_HOUSE" action
                    actions.append(all_actions[0])
                    actions.append(all_actions[4])
          
               # Check if player has enough money to build a hotel
               elif player.balance >= properties[player.location]["hPrice"]:
                    # Add the "BUILD_HOTEL" action
                    actions.append(all_actions[0])
                    actions.append( all_actions[5])
     
     # Check if player is on tax
     elif properties[player.location]["type"] == "tax":
          # Add the "PAY_TAX" action
          actions.append(all_actions[3])

     return actions

def evaluate_utility(player):
     net_worth = 0
     for prop_loc in player.ownedP:
          net_worth += properties[prop_loc]["price"]
          if properties[prop_loc]["hotels"] == 0:
               net_worth += properties[prop_loc]["rent"]+ 10*properties[prop_loc]["houses"]
          else:
               net_worth += properties[prop_loc]["rent"]+ 10*(properties[prop_loc]["houses"] + 1)
     
     for rr_loc in player.ownedRR:
          net_worth += properties[rr_loc]["price"]
          net_worth += properties[rr_loc]["rent"]
     
     for ut_loc in player.ownedUT:
          net_worth += properties[ut_loc]["price"]
          net_worth += properties[ut_loc]["rent"]
          
     net_worth += player.balance

     return net_worth


def transition(players: dict, properties: dict, current_player: int, action):
     new_properties = copy.deepcopy(properties)
     new_players = copy.deepcopy(players)

     # Execute action
     if action == all_actions[0]: # Do nothing
          pass

     elif action == all_actions[1]: # Buy property
          new_players[current_player].balance -= new_properties[new_players[current_player].location]["price"]
          new_players[current_player].ownedP.append(new_players[current_player].location)
          new_properties[new_players[current_player].location]["owner"] = new_players[current_player].id

     elif action == all_actions[2]: # Pay rent
          charge_rent(new_players[current_player])
          
     elif action == all_actions[3]: # Pay tax
          new_players[current_player].balance -= new_properties[new_players[current_player].location]["tax_price"]
          
     elif action == all_actions[4]: # Build house
          build_house(new_players[current_player], new_players[current_player].location)
          
     elif action == all_actions[5]: # Build hotel
          build_hotel(new_players[current_player], new_players[current_player].location)
          
     elif action == all_actions[6]: # Jail free
          new_players[current_player].location = 8
          new_players[current_player].balance -= 100
     
     return new_players, new_properties

def expectiminimax(players: dict, properties: dict, depth: int, is_max: bool, chance: bool=False, current_player: int=0):
     best_action = None

     if is_terminal(players[current_player]) or depth == 0:
          return evaluate_utility(players[current_player]), None
     
     elif is_max:
          max_value = float("-inf")
          actions = get_valid_actions(players[current_player])

          for action in actions:
               new_players, new_properties = transition(players, properties, current_player, action)
               next_player = switch_player(current_player)
               value, _ = expectiminimax(new_players, new_properties, depth-1, False, True, next_player)
               if value > max_value:
                    max_value = value
                    best_action = action

          return max_value, best_action
     
     elif is_max == False:
          min_value = float("inf")
          actions = get_valid_actions(players[current_player])
          
          for action in actions:
               new_players, new_properties = transition(players, properties, current_player, action)
               next_player = switch_player(current_player)
               value, _ = expectiminimax(new_players, new_properties, depth-1, True, True, next_player)
               
               if value < min_value:
                    min_value = value
                    best_action = action

          return min_value, best_action
     
     else:
          total_value = 0
          for dice in range(2,13):
               new_players, new_properties = transition(players, properties, current_player, action)
               next_player = switch_player(current_player)
               value, _ = expectiminimax(new_players, new_properties, depth-1, False, False, next_player)
               total_value += value*probability[dice]

          return total_value, None


start_time = time.time()

while round_num <= MAX_ROUNDS:
     
     # Print current game state
     print("========================================================================================")
     print(f"Round {round_num}:")
     print(f"Player {current_player}'s turn")
     print("Player's status:")
     print(f"Player location: {players[current_player].location} , Player Balance: {players[current_player].balance} , Properties: {players[current_player].ownedP} , RailRoad: {players[current_player].ownedRR} , Utility: {players[current_player].ownedUT}")

     # Roll the dice
     rolls = roll_dice()
     roll_res = rolls[0] + rolls[1]
     print(f"Player {current_player} rolled {rolls[0]} + {rolls[1]} = {roll_res}")

     # Update player location and handle passing Go
     players[current_player].location += roll_res
     if players[current_player].location >= 33:
          players[current_player].location -= 33
          players[current_player].balance += 200
          print(f"Player {current_player} passed Go and collected $200")

     # Use expectiminimax to choose the best action for the current player
     _, best_action = expectiminimax(players, properties, 4, True, True, current_player)
     print(f"Player {current_player} chose action: {best_action}")

     # Update game state based on the chosen action
     players, properties = transition(players, properties, current_player, best_action)

     # Check if the game has ended
     if is_terminal(players[current_player]):
          print("Game over!")
          break

     # Switch to the next player
     current_player = switch_player(current_player)
     round_num += 1
print("========================================================================================")


end_time = time.time()

# Print the final game state
print("Final game state:")

for i in range(1,3):
     print(f"Player Balance: {players[i].balance} , Properties: {players[i].ownedP} , RailRoad: {players[i].ownedRR} , Utility: {players[i].ownedUT}")

print(f"Player 1's net worth: {evaluate_utility(players[1])}")
print(f"Player 2's net worth: {evaluate_utility(players[2])}")

print(f"Time spend to finish the game: {str(end_time - start_time)}")


