money = 550
water = 400
milk = 540
beans = 120
cups = 9

machineOn = 1


def buy():
    choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
    if choice == "1":
        espresso()
    elif choice == "2":
        latte()
    elif choice == "3":
        cappuccino()


def fill():
    global water
    global milk
    global beans
    global cups
    water += int(input("Write how many ml of water do you want to add:"))
    milk += int(input("Write how many ml of milk do you want to add:"))
    beans += int(input("Write how many grams of coffee beans do you want to add:"))
    cups += int(input("Write how many disposable cups of coffee do you want to add:"))


def take():
    global money
    print("I gave you €" + str(money))
    money = 0


def espresso():
    global water
    global beans
    global cups
    global money
    if water < 250:
        print("Sorry, not enough water!")
        return
    elif beans < 16:
        print("Sorry, not enough beans!")
        return
    elif cups < 1:
        print("Sorry, not enough cups!")
        return
    else:
        print("I have enough resources, making you a coffee!")
        water -= 250
        beans -= 16
        cups -= 1
        money += 4


def latte():
    global water
    global milk
    global beans
    global cups
    global money
    if water < 350:
        print("Sorry, not enough water!")
        return
    elif milk < 75:
        print("Sorry, not enough milk!")
        return
    elif beans < 20:
        print("Sorry, not enough beans!")
        return
    elif cups < 1:
        print("Sorry, not enough cups!")
        return
    else:
        print("I have enough resources, making you a coffee!")
        water -= 350
        milk -= 75
        beans -= 20
        cups -= 1
        money += 7


def cappuccino():
    global water
    global milk
    global beans
    global cups
    global money
    if water < 200:
        print("Sorry, not enough water!")
        return
    elif milk < 100:
        print("Sorry, not enough milk!")
        return
    elif beans < 12:
        print("Sorry, not enough beans!")
        return
    elif cups < 1:
        print("Sorry, not enough cups!")
        return
    else:
        print("I have enough resources, making you a coffee!")
        water -= 200
        milk -= 100
        beans -= 12
        cups -= 1
        money += 6


def remaining():
    print("The coffee machine has:")
    print(str(water) + " of water")
    print(str(milk) + " of milk")
    print(str(beans) + " of coffee beans")
    print(str(cups) + " of disposable cups")
    print(str(money) + " of money")


def choose_action():
    action = str(input("Write action (buy, fill, take, remaining, exit) :"))
    if action == "buy":
        buy()
    elif action == "fill":
        fill()
    elif action == "take":
        take()
    elif action == "remaining":
        remaining()
    elif action == "exit":
        global machineOn
        machineOn = 0


while machineOn == 1:
    choose_action()
