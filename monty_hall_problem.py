from tkinter import *
import tkinter.messagebox
import random
import os


# defining the game class
class MontyHallGame:
    def __init__(self):
        self.window = Tk()  # initializing the gui window
        self.window.title("Monty Hall Game")  # setting the title for the window
        self.doorColor = "#242582"
        self.doorNum = 0
        self.gifts = ["car", "goat", "goat"]
        self.selectedDoor = ""
        self.btns = []
        self.changedDoorWins = 0
        self.changedDoorLoss = 0
        self.maintainedDoorWins = 0
        self.maintainedDoorLoss = 0


        # creating a menu bar
        menubar = Menu(self.window)  # initializing the menu bar
        self.window.config(menu=menubar)  # displaying the menu bar

        # Create a pull-down menu, and add it to the menu bar
        operationMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=operationMenu)
        operationMenu.add_command(label="Help", command=self.help)
        operationMenu.add_command(label="About", command=self.about)
        operationMenu.add_separator()
        operationMenu.add_command(label="Exit", command=self.exit)

        # frame for welcome message and game instructions
        frame0 = Frame(self.window)
        frame0.grid(row=1, column=1, sticky=W)  # frame is in row 1 and column 1 and sticking to the West
        self.msgCanvas = Canvas(frame0, width=800, height=200, bg="white")  # canvas is inside the frame0
        self.msgCanvas.pack()
        self.welcomeMsg = self.msgCanvas.create_text(400, 20, fill="#f64c72", font="Helvetica 15 bold",
                                                     text="Welcome to the Monty Hall Game!")

        # button that starts game
        self.startGameBtn = Button(self.msgCanvas, fg="white", bg="blue", text="Start Game", command=self.startGame)
        self.startGameBtn.place(x=350, y=40)

        self.instructionMsg1 = self.msgCanvas.create_text(400, 155, fill="#553d67", text="")
        self.firstDoorChoice = self.msgCanvas.create_text(400, 90, fill="#553d67", text="")
        self.secondDoorChoice = self.msgCanvas.create_text(400, 120, fill="#553d67", text="")
        self.instructionMsg2 = self.msgCanvas.create_text(400, 170, fill="#553d67", text="")

        # creating frame1 inside window. This frame contains the doors
        frame1 = Frame(self.window)
        frame1.grid(row=2, column=1)  # placing frame1 in row 2 and column 1

        self.canvas = Canvas(frame1, width=800, height=400, bg="white")
        self.canvas.pack()

        self.btn1 = Button(self.canvas, bg="#47201d", text="Door 1", padx=60, pady=145, state="disabled", command=lambda: self.setDoorNum(1),
                      fg="white")
        self.btn1.place(x=80, y=35)

        door1 = self.canvas.create_rectangle(65, 25, 260, 348, tags="door1", fill="#683835")

        self.btn2 = Button(self.canvas, bg="#47201d", text="Door 2", padx=60, pady=145, state="disabled", command=lambda: self.setDoorNum(2),
                      fg="white")
        self.btn2.place(x=335, y=35)
        door2 = self.canvas.create_rectangle(320, 25, 510, 348, tags="door2", fill="#683835")

        self.btn3 = Button(self.canvas, bg="#47201d", text="Door 3", padx=60, pady=145, state="disabled", command=lambda: self.setDoorNum(3),
                      fg="white")
        self.btn3.place(x=575, y=35)
        door3 = self.canvas.create_rectangle(565, 25, 750, 348, tags="door3", fill="#683835")

        self.btns.append(self.btn1)
        self.btns.append(self.btn2)
        self.btns.append(self.btn3)



        self.window.mainloop()  # sets window's event loop

    # function to open help menu
    def help(self):
        tkinter.messagebox.showinfo("Game Instruction", "The Monty Hall Problem\n"
                                                        "You are presented with 3 doors.\nAt first you need to choose "
                                                        "one.\nAfter you've chosen a door the host will show you a "
                                                        "different door where there's a goat.\nAt that point you need "
                                                        "to choose whether you want to keep your choice, or change it.")

    # function to open about menu
    def about(self):
        tkinter.messagebox.showinfo("About Monty Hall", "This game was made by Ohad")

    # function to exit game
    def exit(self):
        exit = tkinter.messagebox.askyesno("Exit", "Are you sure you've had enough?")
        if exit:
            self.window.quit()

    # function to detect door number clicked
    def setDoorNum(self, num):
        self.doorNum = num
        # self.setDoorColor("purple", num)
        self.msgCanvas.itemconfigure(self.firstDoorChoice,
                                     text="Your first choice: Door " + str(num))
        self.gameControl(self.doorNum)

    # function to get door number clicked
    def getDoorNum(self):
        return self.doorNum

    # setting door colors
    def setDoorColor(self, color, doornum):
        if doornum == 1:
            self.btn1["bg"] = color
        elif doornum == 2:
            self.btn2["bg"] = color
        elif doornum == 3:
            self.btn3["bg"] = color

    '''def getDoorColor(self):
        return self.doorColor'''

    def getNewOption(self, newDoorNum):
        self.msgCanvas.itemconfigure(self.secondDoorChoice,
                                     text="Your second choice: Door " + str(newDoorNum))
        if self.selectedDoor == "goat":
            if self.doorNum == newDoorNum:
                self.maintainedDoorLoss += 1
                self.msgCanvas.itemconfigure(self.instructionMsg2,
                                             text="Sorry you lost!")

            else:
                self.changedDoorWins += 1
                self.msgCanvas.itemconfigure(self.instructionMsg2,
                                             text="Great you won!")

        elif self.selectedDoor == "car":
            if self.doorNum == newDoorNum:
                self.maintainedDoorWins += 1
                self.msgCanvas.itemconfigure(self.instructionMsg2,
                                             text="Great you won!")

            else:
                self.changedDoorLoss += 1
                self.msgCanvas.itemconfigure(self.instructionMsg2,
                                             text="Sorry you lost!")

        self.msgCanvas.itemconfigure(self.instructionMsg1, text="")
        self.btn1["state"] = "disabled"
        self.btn2["state"] = "disabled"
        self.btn3["state"] = "disabled"
        self.startGameBtn["text"] = "Restart Game"

        i = 0  # keep track of the doors
        for gift in self.gifts:
            if gift == "car":
                self.btns[i]["bg"] = "#2fa376"
            else:
                self.btns[i]["bg"] = "white"

            self.btns[i]["text"] = "  " + gift.upper()

            i += 1

    # function to start game
    def startGame(self):
        os.system('cls')
        print("Scoreboard:\n")
        print("Door maintained:")
        print("Won: ", self.maintainedDoorWins)
        print("Lost: ", self.maintainedDoorLoss, "\n")
        print("Door switched:")
        print("Won: ", self.changedDoorWins)
        print("Lost: ", self.changedDoorLoss)

        # shuffling gifts
        random.shuffle(self.gifts)
        self.msgCanvas.itemconfigure(self.instructionMsg1,
                                     text="Choose a door")
        self.msgCanvas.itemconfigure(self.instructionMsg2,
                                     text="")
        self.msgCanvas.itemconfigure(self.firstDoorChoice,
                                     text="")
        self.msgCanvas.itemconfigure(self.secondDoorChoice,
                                     text="")
        self.btn1["state"] = "normal"
        self.btn1["bg"] = "#242582"
        self.btn1["text"] = "Door 1"
        self.btn1["command"] = lambda: self.setDoorNum(1)

        self.btn2["state"] = "normal"
        self.btn2["bg"] = "#242582"
        self.btn2["text"] = "Door 2"
        self.btn2["command"] = lambda: self.setDoorNum(2)

        self.btn3["state"] = "normal"
        self.btn3["bg"] = "#242582"
        self.btn3["text"] = "Door 3"
        self.btn3["command"] = lambda: self.setDoorNum(3)

        self.startGameBtn["text"] = "Restart Game"


    def gameControl(self, doorNum):
        # copying list into giftCopy for later computations
        giftsCopy = [x for x in self.gifts]
        '''# getting door number selected
        doorNum = self.getDoorNum()'''

        # checking for first door/gift selected
        # if 0 < doorNum < 4:  # making sure that door number is from 1-3
        doorIndex = self.doorNum - 1  # calculating index of door/gift from door number chosen
        self.selectedDoor = self.gifts[doorIndex]  # content of selected door
        if self.selectedDoor == "goat":  # if door selected contains goat
            giftsCopy[doorIndex] = "air"  # replacing selected gift with air in the copied list
            moderatorDoor = giftsCopy.index("goat")  # moderator chooses door with other goat
            self.moderatorsChoice = moderatorDoor + 1

            # setting instruction text
            self.msgCanvas.itemconfigure(self.instructionMsg1, text="Moderator opens door " + str(self.moderatorsChoice))

            # disable button
            if self.moderatorsChoice == 1:
                self.btn1["state"] = "disabled"
                self.setDoorColor("white", 1)
            elif self.moderatorsChoice == 2:
                self.btn2["state"] = "disabled"
                self.setDoorColor("white", 2)
            elif self.moderatorsChoice == 3:
                self.btn3["state"] = "disabled"
                self.setDoorColor("white", 3)

        elif self.selectedDoor == "car":  # if door selected contains car
            giftsCopy[doorIndex] = "air"  # replacing selected gift with air in the copied list
            if random.randint(1, 3) == 1:  # randomly choosing the first or second occurrence of goat for moderator
                # when randint == 1 getting first occurrence of goat
                moderatorDoor = giftsCopy.index("goat")
            else:  # getting last occurrence of goat
                moderatorDoor = len(giftsCopy) - 1 - giftsCopy[::-1].index("goat")

            self.moderatorsChoice = moderatorDoor + 1

        # setting instruction text
        self.msgCanvas.itemconfigure(self.instructionMsg1, text="Moderator opens door " + str(self.moderatorsChoice))

        # disable button
        if self.moderatorsChoice == 1:
            self.btn1["state"] = "disabled"
            self.btn1["text"] = "GOAT"
            self.setDoorColor("white", 1)
        elif self.moderatorsChoice == 2:
            self.btn2["state"] = "disabled"
            self.btn2["text"] = "GOAT"
            self.setDoorColor("white", 2)
        elif self.moderatorsChoice == 3:
            self.btn3["state"] = "disabled"
            self.btn3["text"] = "GOAT"
            self.setDoorColor("white", 3)

        self.msgCanvas.itemconfigure(self.instructionMsg2, text="Click on the same door to maintain your choice or on "
                                                                "the other door to switch")

        self.btn1["command"] = lambda: self.getNewOption(1)
        self.btn2["command"] = lambda: self.getNewOption(2)
        self.btn3["command"] = lambda: self.getNewOption(3)


MontyHallGame()