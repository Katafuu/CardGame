import random
import csv

deck = []

for suit in ['red', 'black', 'yellow']:
    for val in range(1, 11):
        card = [suit, val]
        deck.append(card)
        # We are now creating the cards. To do this, we create a nested for loop that creates a new card every loop then adds it to the deck list, i chose range(1,11) as there are 10 cards per colour
random.shuffle(deck)


# Using the shuffle function from the random library to shuffle the cards

class players():
    def __init__(self, name):
        self.name = ''
        self.hand = []
        # each player will have a name and a hand of cards

    def drawCard(self):
        self.hand.insert(0, deck.pop())
        # this code will take the first item from the deck and add it to the player's hand

    def showHand(self):
        for card in self.hand:
            print(card)
            # this will tell us all the cards that the player is holding by looping through the hand and printing each item

    def showColor(self):
        for card in self.hand:
            return card[0]
        # this will tell us the color and of the last card added to the player's hand, 0 is the location of the colour and 1 is the second value, which is the location of the number

    def showNum(self):
        for card in self.hand:
            return card[1]


def signup():
    accnum = int(input("How many accounts would you like to sign up?"))
    for x in range(accnum):
        # creating accounts by asking for a username and password, then opening a csv file and using the csv library to write a row to it
        username = input("Enter username:\n")
        password = input("Enter password:\n")
        with open("credentials.csv", "a") as file:
            csvwriter = csv.writer(file)
            creds = [username, password]
            # combining the user and pass in a list before writing it
            csvwriter.writerow(creds)


def login():
    global loggedin
    global loggedin1
    # this is to check if both accounts are logged in, if its 0, then they are not logged in and if it's 1 then they are logged in.
    loggedin = 0
    loggedin1 = 0
    rows = []
    with open("credentials.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)
        # next function used to skip the header
        for row in csvreader:
            rows.append(row)
            # extracting the data and translating it into a 2d list so that it can  be easier for the program to read
    while loggedin == 0:
        usernamein = input("Enter your username:\n")
        passwordin = input("Enter your password:\n")
        if [usernamein, passwordin] in rows:
            # checking if the inputted user and pass is in the 2d list of usernames and passwords
            print("Succesfully logged in!")
            global username
            # this global is so that we can use this name later in the game
            username = usernamein
            loggedin = 1
        else:
            print("Incorrect Credentials!")
    while loggedin1 == 0:
        # same thing as the last block of code, just for the second player
        usernamein = input("Enter Player 2's username:\n")
        passwordin = input("Enter Player 2's password:\n")
        if [usernamein, passwordin] in rows:
            print("Succesfully logged in!")
            global username2
            username2 = usernamein
            loggedin1 = 1
        else:
            print("Incorrect Credentials!")


def play():
    try:
        if loggedin == 0 or loggedin1 == 0:
            print("Please login first -------\n")
            login()
    except:
        print("You are not logged in!")

    player1 = players(username)
    player2 = players(username2)

    def game():
        # creating a function for the game itself so that we can loop through it without using a while loop, as it kept getting stuck, this function is called after every turn
        player1.drawCard()
        player2.drawCard()
        if len(deck) == 0:
            # checks if the game has finished, once all the cards have been used
            print("Game End")
            if len(player1.hand) > len(player2.hand):
                winner, cardnums = username, len(player1.hand)
                print(username + " is the winner with " + str(cardnums) + " cards.\nHis hand:\n")
                for card in player1.hand:
                    print(*card, sep=",")

            else:
                winner, cardnums = username, len(player2.hand)
                print(username2 + " is the winner with " + str(cardnums) + " cards.\nHis hand:\n")
                for card in player2.hand:
                    print(*card, sep=",")
            winnerdata = [winner, cardnums]
            with open("winners.csv", "a") as f:
                header = ["username", "score"]
                csvwriter = csv.writer(f)
                csvwriter.writerow(winnerdata)
        elif player1.showColor() == 'red' and player2.showColor() == 'black' and len(deck) > 0:
            input("Press enter to continue\n")
            print(username + " Got:" + player1.showColor().title(), player1.showNum(), "which beats",
                  player2.showColor().title(), str(player2.showNum()))
            player1.hand.append(player2.hand.pop())
            game()
        elif player1.showColor() == 'yellow' and player2.showColor() == 'red':
            input("Press enter to continue\n")
            print(username + " Got:" + player1.showColor().title(), player1.showNum(),
                  "which beats " + player2.showColor().title(), str(player2.showNum()))
            player1.hand.append(player2.hand.pop(-1))
            game()
        elif player1.showColor() == 'black' and player2.showColor() == 'yellow':
            input("Press enter to continue\n")
            print(username + " Got:" + player1.showColor().title(), player1.showNum(),
                  "which beats " + player2.showColor().title(), player2.showNum())
            player1.hand.append(player2.hand.pop(-1))
            game()
        elif player1.showColor() == player2.showColor():
            input("Press enter to continue\n")
            print("It's a color tie! Both got " + player1.showColor())
            if player1.showNum() > player2.showNum():
                print("But " + username + " got a higher number of: " + str(player1.showNum()))
            else:
                print("But " + username2 + " got a higher number of: " + str(player2.showNum()))
            game()
        else:
            input("Press enter to continue\n")
            print(username2 + " Got:" + player2.showColor().title(), player2.showNum(),
                  "which beats " + player1.showColor().title(), player1.showNum())
            player2.hand.append(player1.hand.pop(-1))
            game()

    game()


gameinprogress = 0

while gameinprogress != 1:
    choice = input("1) Sign Up\n2) Login\n3) Play\n4) Exit\n")
    if choice == "1":
        signup()
    elif choice == "2":
        login()
    elif choice == "3":
        gameinprogress = 1
        play()
    elif choice == "4":
        break
    else:
        print("Invalid input")


