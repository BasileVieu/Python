import random


def player():
    name = input("Enter your name:")
    print(f"Hello, {name}")
    file = open("rating.txt", "r")
    score = {}
    for line in file:
        score[line.split()[0]] = int(line.split()[1])
    file.close()
    if name not in score:
        score[name] = 0
    return name, score


def option_list():
    option = input()
    if option == "":
        deck = ["paper", "scissors", "rock"]
    else:
        deck = option.split(",")
    print("Okay, let's start")
    return deck


def play_game():
    global user_choice
    global deck
    global score

    computer_choice = random.choice(deck)
    lose = f"Sorry, but computer chose {computer_choice}"
    draw = f"There is a draw ({computer_choice})"
    win = f"Well done. Computer chose {computer_choice} and failed"

    if user_choice == computer_choice:
        game = draw
    else:
        a = deck.index(user_choice)
        final_list = deck[(a + 1):] + deck[:a]
        final_list.insert(len(final_list) // 2, user_choice)
        if final_list.index(computer_choice) < final_list.index(user_choice):
            game = lose
        else:
            game = win

    if game == draw:
        score[name] += 50
    elif game == win:
        score[name] += 100

    print(game)
    return game, score


name, score = player()
deck = option_list()
user_choice = input()

while user_choice != "!exit":
    if user_choice == "!rating":
        print(f"Your rating: {score[name]}")
    elif user_choice not in deck:
        print("Invalid input")
    elif user_choice in deck:
        game, score = play_game()

    user_choice = input()


print("Bye!")