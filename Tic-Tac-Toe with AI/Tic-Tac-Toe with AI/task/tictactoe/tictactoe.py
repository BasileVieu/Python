import random


class TicTacToe:
    def __init__(self):
        self.Bool = True
        self.players = {}
        self.field = ["_" for i in range(9)]
        self.struct = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self.winner = "None"
        self.turn = "player1"
        self.Ask()

    def Ask(self):
        while self.Bool:
            command = input("Input command:").split()
            print(command)

            if len(command) != 3:
                print("Bad parameters!")
                continue

            if command[0] == "exit":
                break

            types = ["user", "easy", "medium", "hard"]

            self.players["player1"] = {"type": command[1], "cell": "X"}
            self.players["player2"] = {"type": command[2], "cell": "O"}

            if self.players["player1"]["type"] not in types \
                    or self.players["player2"]["type"] not in types:
                print("Bad parameters!")
                continue
            else:
                self.Run()
                break

    def GetCoordinates(self, position):
        try:
            return (position[0] - 1) + (9 - (3 * position[1]))
        except ValueError:
            return None

    def CheckWinner(self):
        diff = len([x for x in self.field if x == "X"]) - len([y for y in self.field if y == "O"])
        if diff < -1 or diff > 1:
            return "Impossible"

        list_winners = []

        for move in ["X", "O"]:
            for i in range(9):
                for line in self.LineFrom(i):
                    if line.count(move) == 3:
                        list_winners.append(move)

        if "X" in list_winners and "O" in list_winners:
            return "Impossible"
        elif "X" in list_winners:
            return "X wins"
        elif "O" in list_winners:
            return "O wins"
        elif "_" in self.field:
            return "Game not finished"
        elif "_" not in self.field:
            return "Draw"
        else:
            return "None"

    def LineFrom(self, index):
        return ["".join(self.field[i] for i in line) for line in self.struct if index in line]

    def SearchCaseEasy(self):
        coordinates = random.randint(0, 8)

        while self.field[coordinates] != '_':
            coordinates = random.randint(0, 8)

        return coordinates

    def SearchCaseMedium(self):
        options = [i for i, cell in enumerate(self.field) if cell == "_"]

        win_moves = []
        lose_moves = []

        for move in ["X", "O"]:
            for option in options:
                for line in self.LineFrom(option):
                    if line.count(move) == 2:
                        win_moves.append(option) if move == self.players[self.turn]["cell"] else lose_moves.append(option)

        if len(win_moves) != 0:
            return win_moves[0]

        if len(lose_moves) != 0:
            return lose_moves[0]

        coordinates = random.randint(0, 8)

        while self.field[coordinates] != '_':
            coordinates = random.randint(0, 8)

        return coordinates

    def Minimax(self, new_field, player):
        options = [i for i, cell in enumerate(new_field) if cell == "_"]

        for move in ["X", "O"]:
            for option in options:
                for line in self.LineFrom(option):
                    if line.count(move) == 3:
                        return 10 if move == self.players[player]["cell"] else -10

        if len(options) == 0:
            return 0

        moves = []

        for option in options:
            new_field[option] = self.players[player]["cell"]
            move = {"index": option, "score": self.Minimax(new_field, "player1" if player == "player2" else "player2")}
            new_field[option] = "_"
            moves.append(move)

        best_move = moves[0]

        if player == self.turn:
            best_score = -1000000

            for move in moves:
                if move["score"] > best_score:
                    best_score = move["score"]
                    best_move = move
        else:
            best_score = 1000000

            for move in moves:
                if move["score"] < best_score:
                    best_score = move["score"]
                    best_move = move

        return best_move["index"]

    def SearchCaseHard(self):
        return self.Minimax(self.field, self.turn)

    def UserTurn(self):
        coordinates = self.GetCoordinates([int(number) for number in input("Enter the coordinates:").split()])

        if coordinates is None:
            print("You should enter numbers!")
        elif coordinates < 0 or coordinates > 8:
            print("Coordinates should be from 1 to 3!")
        elif self.field[coordinates] != '_':
            print("This cell is occupied! Choose another one!")
        else:
            self.field[coordinates] = self.players[self.turn]["cell"]

            return

        self.UserTurn()

    def ComputerTurn(self):
        if self.players[self.turn]["type"] == "easy":
            coordinates = self.SearchCaseEasy()
        elif self.players[self.turn]["type"] == "medium":
            coordinates = self.SearchCaseMedium()
        else:
            coordinates = self.SearchCaseHard()

        self.field[coordinates] = self.players[self.turn]["cell"]

        level = self.players[self.turn]["type"]

        print(f"Making move level \"{level}\"")

    def ShowField(self):
        print("---------")
        print(f"| {self.field[0]} {self.field[1]} {self.field[2]} |")
        print(f"| {self.field[3]} {self.field[4]} {self.field[5]} |")
        print(f"| {self.field[6]} {self.field[7]} {self.field[8]} |")
        print("---------""")

    def Run(self):
        self.ShowField()

        while self.winner == "None" or self.winner == "Game not finished":
            print("")

            if self.players[self.turn]["type"] == "user":
                self.UserTurn()
            else:
                self.ComputerTurn()

            self.ShowField()
            self.winner = self.CheckWinner()

            if self.turn == "player1":
                self.turn = "player2"
            else:
                self.turn = "player1"

        print("\n", self.winner)


tic_tac_toe = TicTacToe()
