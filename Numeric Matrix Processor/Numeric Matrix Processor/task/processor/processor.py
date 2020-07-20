def num(x):
    try:
        return int(x)
    except ValueError:
        return float(x)


class Matrix:
    def __init__(self, matrix=None, index=""):
        self.matrix = matrix
        if self.matrix is None:
            self.row, self.column = map(int, input(f"Enter size of {index}matrix:").split())
            print(f"Enter {index}matrix:")
            self.matrix = [list(map(num, input().split())) for i in range(self.row)]

    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.matrix)

    def __add__(self, other):
        if type(other) is Matrix and self.CheckDimensionForAdd(other.matrix):
            return Matrix([[self.matrix[x][y] + other.matrix[x][y] for y in range(self.column)] for x in range(self.row)])
        else:
            return "ERROR"

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Matrix([[self.matrix[x][y] * other for y in range(self.column)] for x in range(self.row)])
        elif type(other) is Matrix:
            if self.CheckDimensionForMul(other.matrix):
                result = []

                for x in range(0, self.row):
                    result.append([])
                    for y in range(0, other.column):
                        result[x].append(0)
                        for k in range(0, self.column):
                            result[x][y] += self.matrix[x][k] * other.matrix[k][y]

                return Matrix(matrix=result)
        else:
            return "The operation cannot be performed."

    def __rmul__(self, other):
        return self.__mul__(other)

    def GetMinor(self, i, j):
        return [row[:j] + row[j + 1:] for row in (self.matrix[:i] + self.matrix[i + 1:])]

    def CheckDimensionForAdd(self, matrix):
        return True if len(self.matrix) == len(matrix) and len(self.matrix[0]) == len(matrix[0]) else False

    def CheckDimensionForMul(self, matrix):
        return True if len(self.matrix[0]) == len(matrix) else False

    def CheckDimensionForDeterminant(self):
        return True if len(self.matrix) == len(self.matrix[0]) else False


class Processor:
    def __init__(self):
        self.Bool = True
        self.Ask()

    def Ask(self):
        while self.Bool:
            print("1. Add matrices")
            print("2. Multiply matrix by a constant")
            print("3. Multiply matrices")
            print("4. Transpose matrix")
            print("5. Calculate a determinant")
            print("6. Inverse matrix")
            print("0. Exit")
            choice = input("Your choice:")

            if choice == "1":
                self.AddMatrices()
            elif choice == "2":
                self.MultiplyMatrixConstant()
            elif choice == "3":
                self.MultiplyMatrices()
            elif choice == "4":
                self.ChoiceTransposeMatrix()
            elif choice == "5":
                self.CalculateDeterminant()
            elif choice == "6":
                self.InverseMatrix()
            else:
                print("Bye!")
                break

    def AddMatrices(self):
        mat1 = Matrix(index="first ")
        mat2 = Matrix(index="second ")
        print("The result is:")
        print(mat1 + mat2)
        print("")

    def MultiplyMatrixConstant(self):
        mat = Matrix()
        constant = num(input("Enter constant:"))
        print("The result is:")
        print(mat * constant)
        print("")

    def MultiplyMatrices(self):
        mat1 = Matrix(index="first ")
        mat2 = Matrix(index="second ")
        print("The result is:")
        print(mat1 * mat2)
        print("")

    def ChoiceTransposeMatrix(self):
        print("1. Main diagonal")
        print("2. Side diagonal")
        print("3. Vertical line")
        print("4. Horizontal line")
        choice = input("Your choice:")

        if choice == "1":
            self.TransposeMatrixMainDiagonal()
        elif choice == "2":
            self.TransposeMatrixSideDiagonal()
        elif choice == "3":
            self.TransposeMatrixVerticalLine()
        elif choice == "4":
            self.TransposeMatrixHorizontalLine()

    def TransposeMatrixMainDiagonal(self):
        mat = Matrix()

        result = [[mat.matrix[y][x] for y in range(mat.column)] for x in range(mat.row)]

        print("The result is:")
        print(Matrix(matrix=result))

    def TransposeMatrixSideDiagonal(self):
        mat = Matrix()

        result = [[mat.matrix[mat.row - y][mat.column - x] for y in range(1, mat.column + 1)] for x in range(1, mat.row + 1)]

        print("The result is:")
        print(Matrix(matrix=result))

    def TransposeMatrixVerticalLine(self):
        mat = Matrix()

        result = [[mat.matrix[x][mat.column - y] for y in range(1, mat.column + 1)] for x in range(0, mat.row)]

        print("The result is:")
        print(Matrix(matrix=result))

    def TransposeMatrixHorizontalLine(self):
        mat = Matrix()

        result = [[mat.matrix[mat.row - x][y] for y in range(0, mat.column)] for x in range(1, mat.row + 1)]

        print("The result is:")
        print(Matrix(matrix=result))

    def determinant_recursive(self, matrix=None, total=0):
        indices = list(range(len(matrix)))

        if len(matrix) == len(matrix[0]) == 1:
            return matrix[0][0]

        if len(matrix) == len(matrix[0]) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        for fc in indices:
            sub_matrix = matrix
            sub_matrix = sub_matrix[1:]
            height = len(sub_matrix)

            for i in range(height):
                sub_matrix[i] = sub_matrix[i][0:fc] + sub_matrix[i][fc + 1:]

            sign = (-1) ** (fc % 2)
            sub_det = self.determinant_recursive(sub_matrix)
            total += sign * matrix[0][fc] * sub_det

        return total

    def CalculateDeterminant(self):
        mat = Matrix()

        if mat.CheckDimensionForDeterminant():
            print("The result is:")
            print(self.determinant_recursive(matrix=mat.matrix))
        else:
            print("The operation can not be performed.")

    def FindCofactors(self, mat):
        result = []

        for x in range(0, len(mat.matrix)):
            row = []
            for y in range(0, len(mat.matrix[0])):
                minor = mat.GetMinor(x, y)
                row.append(((-1) ** (x + y)) * self.determinant_recursive(minor))
            result.append(row)

        return result

    def InverseMatrix(self):
        mat = Matrix()

        if mat.CheckDimensionForDeterminant():
            det = self.determinant_recursive(matrix=mat.matrix)
        else:
            print("The operation can not be performed.")
            return

        if det == 0:
            print("This matrix doesn't have an inverse.")
            return

        cofactors = self.FindCofactors(mat)

        cofactors = [[cofactors[y][x] for y in range(len(cofactors[0]))] for x in range(len(cofactors))]

        for x in range(0, len(mat.matrix)):
            for y in range(0, len(mat.matrix[0])):
                cofactors[x][y] = cofactors[x][y] / det

        print("The result is:")
        print(Matrix(cofactors))


processor = Processor()
