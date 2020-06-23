cells = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]

print(f"""---------
| {cells[0]} {cells[1]} {cells[2]} |
| {cells[3]} {cells[4]} {cells[5]} |
| {cells[6]} {cells[7]} {cells[8]} |
---------""")

coordinates = 0
winner = "None"
turn = "X"


def Winner(temp_cells):
    global winner
    diff = len([x for x in temp_cells if x == "X"]) - len([y for y in temp_cells if y == "O"])
    if diff < -1 or diff > 1:
        winner = "Impossible"

    list_winners = []
    if temp_cells[0] == temp_cells[1] == temp_cells[2] != "_":
        list_winners.append(temp_cells[0])

    if temp_cells[3] == temp_cells[4] == temp_cells[5] != "_":
        list_winners.append(temp_cells[3])

    if temp_cells[6] == temp_cells[7] == temp_cells[8] != "_":
        list_winners.append(temp_cells[6])

    if temp_cells[0] == temp_cells[3] == temp_cells[6] != "_":
        list_winners.append(temp_cells[0])

    if temp_cells[1] == temp_cells[4] == temp_cells[7] != "_":
        list_winners.append(temp_cells[1])

    if temp_cells[2] == temp_cells[5] == temp_cells[8] != "_":
        list_winners.append(temp_cells[2])

    if temp_cells[0] == temp_cells[4] == temp_cells[8] != "_":
        list_winners.append(temp_cells[0])

    if temp_cells[2] == temp_cells[4] == temp_cells[6] != "_":
        list_winners.append(temp_cells[2])

    if "X" in list_winners and "O" in list_winners:
        winner = "Impossible"
    elif "X" in list_winners:
        winner = "X wins"
    elif "O" in list_winners:
        winner = "O wins"
    elif "_" not in temp_cells:
        winner = "Draw"
    else:
        winner = "None"


while winner != "X wins"\
        and winner != "O wins"\
        and winner != "Draw":
    temp_coordinates = [int(number) for number in input("Enter the coordinates:").split()]
    coordinates = (temp_coordinates[0] - 1) + (9 - (3 * temp_coordinates[1]))
    if coordinates is None:
        print("You should enter numbers!")
    elif coordinates < 0 or coordinates > 8:
        print("Coordinates should be from 1 to 3!")
    elif cells[coordinates] != '_':
        print("This cell is occupied! Choose another one!")
    else:
        cells[coordinates] = turn
        Winner(cells)
        if turn == "X":
            turn = "O"
        else:
            turn = "X"

    print(f"""---------
| {cells[0]} {cells[1]} {cells[2]} |
| {cells[3]} {cells[4]} {cells[5]} |
| {cells[6]} {cells[7]} {cells[8]} |
---------""")

print(winner)
