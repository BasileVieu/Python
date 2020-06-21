import random

word_list = ["python", "java", "kotlin", "javascript"]
answer = random.choice(word_list)

print("H A N G M A N")

user_choice = input("Type \"play\" to play the game, \"exit\" to quit:")
answer_set = set(answer)
letters_set = set()
guessed = "-" * len(answer)
tries = 8

while tries > 0 and guessed != answer:
    print("\n" + guessed)
    choice = input("Input a letter:")
    if choice == "exit":
        exit()
    elif len(choice) != 1:
        print("You should input a single letter")
    elif choice in letters_set:
        print("You already typed this letter")
    elif not choice.isascii() or not choice.islower():
        print("It is not an ASCII lowercase letter")
    elif choice not in answer_set:
        print("No such letter in the word")
        letters_set.add(choice)
        tries -= 1
    else:
        answer_set.discard(choice)
        letters_set.add(choice)
        count = 0
        for letter in answer:
            if letter not in answer_set:
                guessed = guessed[:count] + letter + guessed[count + 1:]
            count += 1

if guessed != answer:
    print("You are hanged!")
else:
    print("\n" + answer)
    print("You guessed the word!")
    print("You survived!")
