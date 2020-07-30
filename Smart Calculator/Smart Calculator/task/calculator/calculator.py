class Stack:
    def __init__(self):
        self.size = -1
        self.content = []

    def is_empty(self):
        return True if self.size == -1 else False

    def push(self, elem):
        self.content.append(elem)
        self.size += 1

    def pop(self):
        if not self.is_empty():
            self.size -= 1
            return self.content.pop()
        else:
            return None

    def seek(self):
        if not self.is_empty():
            return self.content[self.size]
        else:
            return None

    def display(self):
        if not self.is_empty():
            return self.content
        else:
            return None


class Calculator:
    def __init__(self):
        self.Bool = True
        self.commands = {"/help": self.ShowHelp, "/exit": self.Exit}
        self.precedence = {"^": 5, "*": 4, "/": 4, "+": 3, "-": 3, "(": 2, ")": 1}
        self.variables = {}
        self.Ask()

    def Ask(self):
        while self.Bool:
            user_input = input()

            if user_input == "":
                continue

            if user_input[0] == "/":
                if user_input in self.commands:
                    self.commands[user_input]()
                else:
                    print("Unknown command")

                continue

            user_input = self.GetFinalInput(user_input)

            if not self.CheckInvalidExpression(user_input):
                print("Invalid expression")
                continue

            if "=" in user_input:
                self.Assignment(user_input)
                continue

            if self.CheckVariables(user_input):
                print(self.variables[user_input[0]])
                continue

            stack = self.GetStack(user_input)
            print(self.CalculateStack(stack))

    def CheckInvalidExpression(self, user_input):
        return False if user_input.count("(") != user_input.count(")")\
                        or user_input.count("*") > 2\
                        or user_input.count("/") > 1 else True

    def GetFinalInput(self, user_input):
        user_input = user_input.replace(" ", "")
        user_input = [user_input[i:i + 1] for i in range(0, len(user_input), 1)]

        temp_user = []

        size = len(user_input) - 1

        temp_bool = True

        for i in range(size):
            if user_input[i].isdigit() \
                    and user_input[i + 1].isdigit():
                temp_user.append(user_input[i] + user_input[i + 1])
                temp_bool = False
                continue

            if temp_bool:
                temp_user.append(user_input[i])

            temp_bool = True

        if temp_bool:
            temp_user.append(user_input[size])

        return temp_user

    def GetStack(self, user_input):
        postfix = []
        stack = Stack()

        for i in user_input:
            if i.isalpha() \
                    or i.isdigit():
                postfix.append(i)
            elif i in "+-*/^":
                while len(stack.content) != 0 and self.precedence[i] <= self.precedence[stack.seek()]:
                    postfix.append(stack.pop())

                stack.push(i)
            elif i is "(":
                stack.push(i)
            elif i is ")":
                o = stack.pop()

                while o != "(":
                    postfix.append(o)
                    o = stack.pop()

        while len(stack.content) != 0:
            postfix.append(stack.pop())

        return postfix

    def CalculateStack(self, stack):
        result = list()

        for item in stack:
            if item.isdigit():
                result.append(int(item))
            elif item.isalpha():
                if item in self.variables:
                    result.append(self.variables[item])
                else:
                    return "Unknown variable"
            else:
                num2 = result.pop()
                num1 = result.pop()

                result.append(self.GetFunction(item)(num1, num2))

        return result[0]

    def ShowHelp(self):
        print("The program calculates operations of numbers")

    def Exit(self):
        print("Bye!")
        self.Bool = False

    def Assignment(self, user_input):
        left = user_input[:user_input.index("=")]
        right = user_input[user_input.index("=") + 1:]

        if len(left) == 1:
            left = left[0]
        else:
            left = "".join(left)

        if len(right) == 1:
            right = right[0]
        else:
            right = "".join(right)

        if not left.isalpha():
            print("Invalid identifier")
            return

        if not right.isalpha():
            if not right.isdigit():
                print("Invalid assignment")
                return
            else:
                self.variables[left] = int(right)
        else:
            if right not in self.variables:
                print("Unknown variable")
                return
            else:
                self.variables[left] = self.variables[right]

    def CheckVariables(self, user_input):
        if len(user_input) != 1 \
                or "=" in user_input:
            return False

        if user_input[0] not in self.variables:
            print("Unknown variable")
            return False

        return True

    def GetFunction(self, operator):
        if operator == "+":
            return lambda x, y: x + y
        elif operator == "-":
            return lambda x, y: x - y
        elif operator == "*":
            return lambda x, y: x * y
        elif operator == "/":
            return lambda x, y: int(x / y)
        elif operator == "^":
            return lambda x, y: x ^ y


calculator = Calculator()
