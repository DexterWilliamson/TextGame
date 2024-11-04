#Dexter Williamson

# Starter Code


# IMPORTANT: When submitting to Sense, do not modify any code above this line or the function signature below.

def navigate(current_room: str, user_input: str, rooms):
    err_msg = ''
    item = ''
    
    # Conditional statement to see if code is a Direction, 
    # an "Exit", or invalid command 
    

    # else if user_input is "Exit", then 
    # next_room equals the exit sentinel
    # and err_msg is the goodbye text
    if user_input == 'Exit':
        item = 'exit'
        err_msg = "Thanks for playing."
    
    elif user_input[0] == 'get':
        if len(rooms[current_room]) > 1:
            if user_input[1] in rooms[current_room][1]:
                item = rooms[current_room][1]
                del rooms[current_room][1]
                err_msg = f"You got a {item}"
            else:
                err_msg = 'Item not in this room'
        else:
            err_msg = 'Item not in this room.'

    # else the command isn't recognized
    # err_msg informs user of invalid command
    # and lists out valid commands
    else:
        err_msg = "That is not a valid direction. You need to enter one of: " +\
        str(rooms["Directions"]+["Exit"]) + "."
        
    # Do not modify anything below this line. 
    return item, err_msg

def show_status(room, player, rooms): 
    print(f"\nYou are in the {room}\nValid moves:\n\n{', '.join([f'go {i}'for i in list(rooms[room][0].keys())] + ['Exit'])}\nInventory: {player['inventory']}")
    if len(rooms[room]) > 1:
        print(f"You see a {rooms[room][1]}")
    print(f'-'*25)

def get_new_state(direction_from_user, current_room, rooms):
    next_room = current_room
    err_msg = ''
    
    # Conditional statement to see if code is a Direction, 
    # an "Exit", or invalid command 
    if direction_from_user in rooms["Directions"]:

        # Check if user_input is listed in the subdictionary
        # of current_room keys

        # if so, then update the next_rom to the value
        # in the current_room subdictionary user_input value 
        if direction_from_user in rooms[current_room][0]:
            next_room = rooms[current_room][0][direction_from_user]

        # Else inform player the direction isn't possible
        # in this room
        else:
            err_msg = "You bumped into a wall."
    else:
        err_msg = "That is not a valid direction. You need to enter one of: " +\
        str(rooms["Directions"]+["Exit"]) + "."
    return next_room, err_msg
def show_instructions():  
   #print a main menu and the commands
   print("Insomnia Nightmares Game\nCollect 13 items to win the game, or be beaten by the evil Dr. Sleepwell.\nMove commands: go South, go North, go East, go West\nAdd to Inventory: get 'item name'\n")

def main():

    rooms = {"Starting Location": [{"South":"Gallary"}],
          "Gallary": [{'North': "Starting Location",'South': "Dining Hall",'East':"Sitting Room",'West':"Tea Room"}, "Backpack"],
          "Sitting Room": [{"North": "Study", "West": "Gallary"}, "Boots"],
         "Study": [{"North": "Green Room", "South": "Sitting Room"}, "Book"],
         "Green Room": [{"West": "Bed Room", "South": "Study"}, "Potion"],
         "Dining Hall": [{"North": "Gallary", "South": "Kitchen", "East":"Closet"},"Gauntlets"],
         "Kitchen" : [{"North": "Dining Hall"},"Sword"],
         "Closet": [{"West": "Dining Hall"},"Helmet"],
         "Tea Room": [{"North": "Armory", "East": "Gallary"},"Shield"],
         "Armory" : [{"North": "Bed Room", "South": "Tea Room", "West": "Master Bedroom"},"Chest Plate"],
         "Master Bedroom" : [{"East": "Armory"},"Diary"],
         "Bed Room" : [{"North": "Bathroom", "South": "Armory", "East": "Green Room"},"Pillow"],
         "Bathroom" : [{"South": "Bed Room", "East": "Secret Passage"},"Special Glasses"],
         "Secret Passage" : [{"East" : "Boss Room"},"Gloves"],
         "Boss Room": [{"West":"Secret Passage"}],
         "Directions" :['North', 'South', 'East', 'West']}
    
# Used this to create a gameplay loop
    # Sets the room variable to "Great Hall"
    room = "Starting Location"

    # While room doesn't equal exit
    # get user input and provide valid inputs
    # based on the room the player is in
    # send user_input to the navigate function
    player = {"inventory": []}
    show_instructions()
    while room != "exit":
        if room == "Boss Room" and len(player["inventory"]) != 13:
            print("You have been put to sleep!\nYou lose!")
            break
        elif room == "Boss Room" and len(player["inventory"] == 13):
            print("You defeated Dr. Sleepwell!\n")
            break
        else:
            
            show_status(room, player, rooms)
            user_input = input(f"Enter your move: \n> ")
            user_input = user_input.split(' ')

            # Used some string formating to correct user_input
            # so the game is more forgiving

            # Check if the move command has "go" before a diretion is input
            # also check to see if the list has more than one element
            # so it can be used
            if user_input[0].lower() == 'go' and len(user_input) > 1:
                room, err = get_new_state(user_input[1], room, rooms)
                print("\n", err)
        
            elif user_input[0].capitalize() == "Exit":
                room, err = navigate(room, user_input[0].capitalize(), rooms)
                print("\n", err)

            elif user_input[0].lower() == 'get' and len(user_input) > 1:
                item, err = navigate(room, user_input, rooms)
                if item != "":
                    player["inventory"].append(item)
                print("\n", err)

            else:
                print('Unknown Input')

if __name__ == "__main__":

    main()  



