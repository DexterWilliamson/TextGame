import random
import curses

class Entity():
    def __init__(self):
        self.name = ""
    #Base class for all entity types,
    #Name, location, coordinates if needed

class Player():
    def __init__(self, name):
        self.name = name
        self.hp = 10
        self.armor = 0
        self.damage = 2
        self.inventory = {}
        self.specialInventory = {}
        self.location = 0
        self.currentRoom = False
    
    def getItem(self, item, value=False):
        listofspecialitems = {'Helmet': 5, "Sword": 2, "Shield": 1, "Breast Plate": 5}
        if item in listofspecialitems:
            self.specialInventory[item] = listofspecialitems[item]
        else:
            self.inventory[item] = value

    def useItem(self, item):
        self.inventory[item]

    def move(self, direction):
        if direction == "w":
            self.location

    def printInventory(self):
        print(self.inventory)

class Item():
    def __init__(self, name, hp=0, armor=0, dmg=0):
        self.name = name
        self.location = 0
        self.hp = hp
        self.armor = armor
        self.damage = dmg
        self.currentRoom = False

class Map():
    def __init__(self):
        self.map = {}
        self.roomNames = {"startingRoom": "Starting Room", 
                          "bossRoom": "Boss Room", 
                          "mainRoom":"Main Room", 
                          "guestRoom": "Guest Room", 
                          "armory": "Armory", 
                          "laboratory":"Laboratory", 
                          "dungeon": "Dungeon", 
                          "basement": "Basement", 
                          "observatory":"Observatory",
                          "backyard": "Backyard",
                          "attic": "Attic",
                          "diningRoom": "Dining Room",
                          "theatre": "Theatre",
                          "ballRoom": "Ballroom",
                          "bathRoom": "Bathroom",
                          "library": "Library",
                          "office": "Office",
                          "familyRoom": "Family Room",
                          "den": "Den",
                          "computerRoom": "Computer Room",
                          "loft": "Loft"}
        self.itemList = {"Helmet": Item("Helmet", armor=2), "Breast Plate": Item("Breast Plate", armor=2), "Sword": Item("Sword", dmg=2),
                         "Potion": Item("Potion", hp=2), "Super Potion": Item("Super Potion", hp=4), "Shield": Item("Shield", armor=2)}
        
        self.specialItemList = {f"Fragment {i}": Item(f"Fragment {i}") for i in range(3,13)}
    def GenerateMaxRooms(self, rooms=False):
        if rooms == False:
            self.maxRooms = random.randint(13,15)
        else:
            self.maxRooms = rooms
        
        for i in range(0,self.maxRooms):
            doors=1
            maxWidth=random.randint(3,25)
            maxHeight=random.randint(3,25)
            items=False
            if "startingRoom" not in self.map:
                room = "startingRoom"
                maxWidth=random.randint(3,10)
                maxHeight=random.randint(3,10)
            elif "mainRoom" not in self.map:
                room = "mainRoom"
                doors=random.randint(1,4)
            elif "bossRoom" not in self.map:
                room = "bossRoom"
            else:
                room = random.choice(list(self.roomNames))
                while room in self.map:
                    room = random.choice(list(self.roomNames))

                doors = random.randint(1, 4)
                if len(list(self.itemList.keys())) != 0:
                    randomItemChoice = random.choice(list(self.itemList.keys()))
                    items = [self.itemList[randomItemChoice]]
                    del self.itemList[randomItemChoice]
                else:
                    randomItemChoice = random.choice(list(self.specialItemList.keys()))
                    items = [self.specialItemList[randomItemChoice]]
                    del self.specialItemList[randomItemChoice]
            self.map[room] = Room(name=self.roomNames[room], items=items, doors=doors, maxWidth=maxWidth, maxHeight=maxHeight)

            self.map[room].addItems(self.map[room])

    def GenerateDoors(self):
        self.maxDoors = self.maxRooms-1
        roomNames = list(self.map.keys())
        self.doors = {}
        #self.doors = {roomNames[i]+"To"+roomNames[i+1]: Entity() for i in range(0,self.maxDoors) if i in ['startingRoom', 'mainRoom', 'bossRoom']}

        for j,i in enumerate(roomNames):
            name="="
            if i == 'startingRoom':
                connectedRoom = 'mainRoom'
                newName = i+"To"+connectedRoom
                self.doors[newName] = Entity()
                direction, index = self.doorLocationPicker(self.map[i], newName, wall='SOUTH')
                roomB = self.map[connectedRoom]
                self.doors[newName] = Door(number=j,name=name, roomA=self.map[i], roomB=roomB, wallPosRoomA=direction, roomALocation=index)
                self.addDoors(newName)

            elif i == "bossRoom":
                name = "x"
                connectedRoom = random.randint(1,len(roomNames)-1)
                newName = i+"To"+roomNames[connectedRoom]
                self.doors[newName] = Entity()
                direction, index = self.doorLocationPicker(self.map[i], newName)
                roomB = self.map[roomNames[connectedRoom]]
                self.doors[newName] = Door(number=j,name=name, roomA=self.map[i], roomB=roomB, wallPosRoomA=direction, roomALocation=index)
                self.addDoors(newName)

            else:
                for num in range(self.map[i].doors):

                    connectedRoom = random.randint(1,len(roomNames)-1)
                    newName = i+"To"+roomNames[connectedRoom]
                    reverseName = roomNames[connectedRoom]+"To"+i

                    while newName in self.doors or reverseName in self.doors and connectedRoom != i and connectedRoom != 'bossRoom':
                        connectedRoom = random.randint(1,len(roomNames)-1)
                        newName = i+"To"+roomNames[connectedRoom]
                        reverseName = roomNames[connectedRoom]+"To"+i
                    if "boss" in newName:
                        name = "x"

                    self.doors[newName] = Entity()
                    print(self.map[i], newName)
                    try:
                        direction, index = self.doorLocationPicker(self.map[i],newName)
                    except Exception as e:
                        print(e)
                    else:
                        roomB = self.map[roomNames[connectedRoom]]
                
                        self.doors[newName] = Door(number=j, name=name, roomA=self.map[i], roomB=roomB, wallPosRoomA=direction, roomALocation=index)
                        self.addDoors(newName)

    def doorLocationPicker(self,room, doorName, wall=False, pos=False):
        
        for w in room.roomWalls:
            if any(isinstance(x, Entity) for x in room.roomWalls[w]) == False and any(isinstance(x, Door) for x in room.roomWalls[w]) == False and "=" not in room.roomWalls[w]:
                if wall == False:
                    wall = w
                if pos == False:
                    pos = random.randint(1, len(room.roomWalls[w])-1)
                room.roomWalls[wall][pos] = self.doors[doorName]
                print(room.name, wall, pos)
                return wall, pos           

    def addDoors(self, doorName):
        wallA, posA =  self.doors[doorName].wallPosRoomA, self.doors[doorName].roomALocation
        wallB, posB = self.doors[doorName].wallPosRoomB, self.doors[doorName].roomBLocation
        self.doors[doorName].roomA.roomWalls[wallA][posA] = self.doors[doorName]
        self.doors[doorName].roomB.roomWalls[wallB][posB] = self.doors[doorName]

class Door():
    def __init__(self, number, roomA, roomB, name="=", wallPosRoomA=False, wallPosRoomB=False, roomALocation=False, roomBLocation=False):
        self.name = name
        self.number = number 
        self.roomA = roomA
        self.roomB = roomB
        self.wallPosRoomA = wallPosRoomA
        self.wallPosRoomB = wallPosRoomB
        self.roomBLocation = roomBLocation
        self.roomALocation = roomALocation

        if self.roomALocation == False:
            self.roomALocation = self.wallPosRoomA[1]
        if self.wallPosRoomB == False:
            self.automaticLocation()
        if self.roomBLocation == False:
            self.roomBLocation = random.randint(1, len(self.roomB.roomWalls[self.wallPosRoomB])-1)

        self.roomStartingPosition = [0,0]

    def generateNewPosition(self):
        pass

    def useDoor(self, player):
        if player.currentRoom == self.roomA:
            self.roomStartingPosition = self.playerLocation(self.wallPosRoomB, self.roomB, self.roomBLocation)
            self.roomB.addElement(player,room=self.roomB, xLocation=self.roomStartingPosition[1], yLocation=self.roomStartingPosition[0])
        elif player.currentRoom == self.roomB:
            self.roomStartingPosition = self.playerLocation(self.wallPosRoomA, self.roomA, self.roomALocation)
            self.roomA.addElement(player, room=self.roomA,xLocation=self.roomStartingPosition[1], yLocation=self.roomStartingPosition[0])
        else:
            print('idk man')
    
    def playerLocation(self, nextRoomStartingDirection, room, location):
        print(location)
        if nextRoomStartingDirection == "NORTH":
            newLocation = [0, location-1]
        if nextRoomStartingDirection == "SOUTH":
            newLocation = [room.roomHeight-1, location-1]
        if nextRoomStartingDirection == "WEST":
            newLocation = [location, 0]
        if nextRoomStartingDirection == "EAST":
            newLocation = [location, room.roomWidth-1]
        return newLocation

    def automaticLocation(self):
        if self.wallPosRoomA == "NORTH":
            self.wallPosRoomB = "SOUTH"
        if self.wallPosRoomA == "SOUTH":
            self.wallPosRoomB = "NORTH"
        if self.wallPosRoomA == "WEST":
            self.wallPosRoomB = "EAST"
        if self.wallPosRoomA == "EAST":
            self.wallPosRoomB = "WEST"

class Room():
    def __init__(self, name, maxHeight, maxWidth, doors=1, items=False, enemies=False, player=False):
        self.roomHeight = maxHeight
        self.roomWidth = maxWidth
        self.name = name
        self.items = items
        self.roomMap = [['.' for j in range(self.roomWidth)] for i in range(self.roomHeight)]
        self.roomWalls = {"NORTH":[i for i in (f"|{'-'*(self.roomWidth)}|")], "SOUTH":[i for i in (f"|{'-'*(self.roomWidth)}|")], "EAST":['|' for i in range(self.roomHeight)], "WEST":['|' for i in range(self.roomHeight)]}
        self.doors = doors

    def addItems(self, room):
        if self.items != False:
            for i in self.items:
                self.addElement(i, room=room)

    def pingDoors(self):
        for i in self.roomWalls:
            for j in i:
                if "=" in j:
                    return True

    def displayRoom(self):
        print(self.name.center(self.roomWidth))
        barCounter = 0
        for i in self.roomWalls["NORTH"]:
            if isinstance(i, Door):
                print(i.name, end='')
            else:
                if i == '|':
                    barCounter += 1
                if barCounter == 2:
                    print(i)
                else:
                    print(i, end='')
        for num,i in enumerate(self.roomMap):
            if isinstance(self.roomWalls["WEST"][num], Door):
                print(self.roomWalls["WEST"][num].name, end='')
            else:
                print(self.roomWalls["WEST"][num], end='')
            for j in i:
                if isinstance(j, Player) or isinstance(j, Item):
                    print(j.name[0],end='')
                elif isinstance(j,list):
                    print(j[0].name[0],end='')
                else:
                    print(f'{j}',end='')
            if isinstance(self.roomWalls["EAST"][num], Door):
                print(self.roomWalls["EAST"][num].name)
            else:
                print(self.roomWalls["EAST"][num])

        for i in self.roomWalls["SOUTH"]:
            if isinstance(i, Door):
                print(i.name, end='')
            else:
                print(i, end='')
        print('\n')

    def addElement(self, element, room=False, xLocation=False, yLocation=False):
        if isinstance(element, Item):
            if xLocation == False:
                xLocation = random.randint(0,self.roomWidth-1)
            if yLocation == False:
                yLocation = random.randint(0,self.roomHeight-1)
        else:
            if xLocation == False and xLocation != 0:
                xLocation = random.randint(0,self.roomWidth-1)
            if yLocation == False and yLocation != 0:
                yLocation = random.randint(0,self.roomHeight-1)

        if room != False:
            element.currentRoom = room

        element.currentRoom.roomMap[yLocation][xLocation] = element
        element.location = [yLocation, xLocation]

    def gridCheck(self, currentLocation, movement, element, direction):
        if direction == "NORTH" or direction == "SOUTH":
            newLocation = [currentLocation[0] + movement, currentLocation[1]]
        if direction == "WEST" or direction == "EAST":
            newLocation = [currentLocation[0],currentLocation[1] + movement]
            
        if newLocation[0] < 0 and direction == 'NORTH':
                if isinstance(self.roomWalls[direction][element.location[1]+1], Door):
                    return self.roomWalls[direction][element.location[1]+1]
                else:
                    print("Can't move through walls")
                    return currentLocation
                    
        elif newLocation[1] < 0 and direction == "WEST":
                if isinstance(self.roomWalls[direction][element.location[0]], Door):
                    print("door West")
                    return self.roomWalls[direction][element.location[0]]
                else:
                    print("Can't move through walls")
                    return currentLocation

        elif newLocation[0] > self.roomHeight-1 and direction == "SOUTH":
                if isinstance(self.roomWalls[direction][element.location[1]+1], Door):
                    print("door South")
                    return self.roomWalls[direction][element.location[1]+1]
                
                else:
                    print("Can't move through walls")
                    return currentLocation
                
        elif newLocation[1] > self.roomWidth-1 and direction == "EAST":
                if isinstance(self.roomWalls[direction][element.location[0]], Door):
                    return self.roomWalls[direction][element.location[0]]
                
                else:
                    print("Can't move through walls")
                    return currentLocation
  
        elif isinstance(self.roomMap[newLocation[0]][newLocation[1]], Item):
            print(self.roomMap[newLocation[0]][newLocation[1]].name)
            return newLocation

        else:
            return newLocation
        
    def updateElement(self, element, direction):

        if direction == 'W':
            if isinstance(self.roomMap[element.location[0]][element.location[1]], list):
                self.roomMap[element.location[0]][element.location[1]] = self.roomMap[element.location[0]][element.location[1]][1]
            else:    
                self.roomMap[element.location[0]][element.location[1]] = '.'
            element.location = self.gridCheck(element.location, -1, element, 'NORTH')
            if isinstance(element.location, Door):
               element.location.useDoor(element)

            elif isinstance(self.roomMap[element.location[0]][element.location[1]], Item):
                self.roomMap[element.location[0]][element.location[1]] = [element, self.roomMap[element.location[0]][element.location[1]]]

            else:
                self.roomMap[element.location[0]][element.location[1]] = element

        elif direction == 'A':
            

            if isinstance(self.roomMap[element.location[0]][element.location[1]], list):
                self.roomMap[element.location[0]][element.location[1]] = self.roomMap[element.location[0]][element.location[1]][1]
            else:    
                self.roomMap[element.location[0]][element.location[1]] = '.'

            element.location = self.gridCheck(element.location, -1, element, 'WEST')
            if isinstance(element.location,Door):
                element.location.useDoor(element)

            elif isinstance(self.roomMap[element.location[0]][element.location[1]], Item):
                self.roomMap[element.location[0]][element.location[1]] = [element, self.roomMap[element.location[0]][element.location[1]]]

            else:
                self.roomMap[element.location[0]][element.location[1]] = element

        elif direction == 'S':
            if isinstance(self.roomMap[element.location[0]][element.location[1]], list):
                self.roomMap[element.location[0]][element.location[1]] = self.roomMap[element.location[0]][element.location[1]][1]
            else:    
                self.roomMap[element.location[0]][element.location[1]] = '.'

            element.location = self.gridCheck(element.location, 1, element, 'SOUTH')

            if isinstance(element.location, Door):
               element.location.useDoor(element)

            elif isinstance(self.roomMap[element.location[0]][element.location[1]], Item):
                self.roomMap[element.location[0]][element.location[1]] = [element, self.roomMap[element.location[0]][element.location[1]]]

            else:
                self.roomMap[element.location[0]][element.location[1]] = element

        elif direction == 'D':
            if isinstance(self.roomMap[element.location[0]][element.location[1]], list):
                self.roomMap[element.location[0]][element.location[1]] = self.roomMap[element.location[0]][element.location[1]][1]
            else:    
                self.roomMap[element.location[0]][element.location[1]] = '.'

            element.location = self.gridCheck(element.location, 1, element, 'EAST')
            if isinstance(element.location, Door):
                element.location.useDoor(element)

            elif isinstance(self.roomMap[element.location[0]][element.location[1]], Item):
                self.roomMap[element.location[0]][element.location[1]] = [element, self.roomMap[element.location[0]][element.location[1]]]

            else:
                self.roomMap[element.location[0]][element.location[1]] = element

        elif isinstance(self.roomMap[element.location[0]][element.location[1]], list) and direction[0] == 'get':
            if direction[1] == self.roomMap[element.location[0]][element.location[1]][1].name:
                element.inventory[self.roomMap[element.location[0]][element.location[1]][1].name] = self.roomMap[element.location[0]][element.location[1]][1]
                self.roomMap[element.location[0]][element.location[1]] = self.roomMap[element.location[0]][element.location[1]][0]
                print(element.inventory.keys())
        else:
            print('Unknown Command')

class GameLoop():
    def __init__(self):
        userInput = input("Enter Name: ")
        player = Player(userInput)
        map.map["startingRoom"].addElement(player, room=map.map["startingRoom"], xLocation=1, yLocation=1)

        while player.hp > 0 and userInput != "quit":
            player.currentRoom.displayRoom()
            userInput = input()
            if userInput.lower() == 'quit':
                break
            if userInput in ["w",'a', 's', 'd']:
                player.currentRoom.updateElement(player, userInput.upper())

            if userInput == 'i':
                player.printInventory()
                
            userInput = userInput.split(" ", 1)
            if userInput[0] == 'get':
                player.currentRoom.updateElement(player, userInput)

                #print available items in numbered list
                #accept input to select specific items or all items

            

if __name__ == "__main__":
    map = Map()

    map.GenerateMaxRooms()
    map.GenerateDoors()
    #map["mainRoom"] = Room("Main Room", 10, 15, items=[Item('Potion'), Item('Helmet')])
    #map["startingRoom"] = Room("Starting Room", 5,5)

    print("Welcome to Apnea!")
    print("Please enter an option from the list below.")
    print('1. Play\n2. Quit')
    userInput = input('Select: ')
    if int(userInput) == 1 or userInput == "Play":
        GameLoop()


