import sys
from random import randrange, uniform

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QTableWidget, QApplication, QMainWindow,
                             QPushButton, QLabel, QLineEdit, QTextEdit, QCheckBox, QTableWidgetItem,
                             QStyledItemDelegate)

N = 2


def func(x1, x2):
    return (eval(f"({x1} - 2)**4 + ({x1} - 2*{x2})**2"))


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        pass


class MainWinodow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gens = []
        self.count_gens = None
        self.min_gen = None
        self.max_gen = None
        self.setWindowTitle("Генетический алгоритм")
        self.resize(800, 700)

        self.param = QLabel("Параметры", self)
        self.param.move(100, 10)
        self.param.setFont(QFont("Times", 10))
        self.param.adjustSize()

        self.func_label = QLabel("Функция:", self)
        self.func_label.move(10, 45)
        self.func_label.adjustSize()

        self.func_label_2 = QLabel("(X[1] - 2)^4 + (X[1] - 2*X[2])^2", self)
        self.func_label_2.setFont(QFont("Times", 9))
        self.func_label_2.move(100, 45)
        self.func_label_2.adjustSize()

        self.mutation_label = QLabel("Вероятность мутации (%):", self)
        self.mutation_label.move(10, 80)
        self.mutation_label.adjustSize()

        self.count_hrom = QLabel("Количество хромосом:", self)
        self.count_hrom.move(10, 115)
        self.count_hrom.adjustSize()

        self.min_gen_labal = QLabel("Минимальное значение гена:", self)
        self.min_gen_labal.move(10, 150)
        self.min_gen_labal.adjustSize()

        self.max_gen_label = QLabel("Максимальное значение гена:", self)
        self.max_gen_label.move(10, 185)
        self.max_gen_label.adjustSize()

        self.modify_label = QLabel("Включить модификацию", self)
        self.modify_label.move(10, 220)
        self.modify_label.adjustSize()

        self.mutation_line = QLineEdit(self)
        self.mutation_line.setText("25")
        self.mutation_line.move(220, 75)

        self.count_hrom_line = QLineEdit(self)
        self.count_hrom_line.setText("50")
        self.count_hrom_line.move(220, 110)

        self.min_gen_line = QLineEdit(self)
        self.min_gen_line.setText("-50")
        self.min_gen_line.move(220, 145)

        self.max_gen_line = QLineEdit(self)
        self.max_gen_line.setText("50")
        self.max_gen_line.move(220, 180)

        self.modify_checkbox = QCheckBox(self)
        self.modify_checkbox.move(220, 220)

        self.management = QLabel("Управление", self)
        self.management.move(100, 245)
        self.management.setFont(QFont("Times", 10))
        self.management.adjustSize()

        self.make_hrom = QPushButton("Рассчитать хромосомы", self)
        self.make_hrom.resize(250, 30)
        self.make_hrom.move(30, 285)
        self.make_hrom.clicked.connect(self.generate_hrom)

        self.count_poc = QLabel("Количество поколений:", self)
        self.count_poc.move(10, 330)
        self.count_poc.adjustSize()

        self.count_poc_line = QLineEdit(self)
        self.count_poc_line.setText("100")
        self.count_poc_line.move(220, 325)

        self.make_do = QPushButton("Рассчитать", self)
        self.make_do.resize(250, 30)
        self.make_do.move(30, 365)
        self.make_do.clicked.connect(self.calculate_algo)

        self.res = QLabel("Результаты", self)
        self.res.move(100, 405)
        self.res.setFont(QFont("Times", 10))
        self.res.adjustSize()

        self.best_res_label = QLabel("Лучшее решение:", self)
        self.best_res_label.move(10, 440)
        self.best_res_label.adjustSize()

        self.res_textedit = QTextEdit(self)
        self.res_textedit.resize(320, 170)
        self.res_textedit.move(10, 470)
        self.res_textedit.setEnabled(False)

        self.best_func_label = QLabel("Значение функции:", self)
        self.best_func_label.move(10, 660)
        self.best_func_label.adjustSize()

        self.func_res_line = QLineEdit(self)
        self.func_res_line.move(150, 655)
        self.func_res_line.resize(180, 30)
        self.func_res_line.setEnabled(False)

        self.table = QTableWidget(self)
        self.table.move(350, 20)
        self.table.resize(430, 660)
        self.table.itemChanged.connect(self.item_change)

    def item_change(self, item):
        pass
        ## try:
        ##    self.gens[item.row()][item.column()] = float(item.text())
        ##    res = func(self.gens[item.row()][0], self.gens[item.row()][1])
        ##    self.gens[item.row()][-1] = res
        ##    self.table.setItem(item.row(), 2, QTableWidgetItem(str(res)))
        ## except Exception as exx:
        ##    print(exx)

    def reload_table(self):
        for i in range(self.count_gens):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.gens[i][0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.gens[i][1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.gens[i][2])))

    def mutation(self, chance, a, b):
        if randrange(1, 101) < chance:
            if randrange(0, 2):
                a = uniform(self.min_gen, self.max_gen + 1)
            else:
                b = uniform(self.min_gen, self.max_gen + 1)
        return a, b

    def generate_hrom(self):
        self.count_gens = int(self.count_hrom_line.text())
        self.table.setColumnCount(3)
        self.table.setRowCount(self.count_gens)
        delegate = ReadOnlyDelegate(self)
        self.table.setItemDelegateForColumn(2, delegate)
        self.min_gen = int(self.min_gen_line.text())
        self.max_gen = int(self.max_gen_line.text())
        self.gens = [[uniform(self.min_gen, self.max_gen + 1) for _ in range(N)] for _ in range(self.count_gens)]
        for i in range(self.count_gens):
            self.gens[i].append(func(*self.gens[i]))
        self.reload_table()

    def calculate_algo(self):
        if self.count_gens % 2 == 1:
            self.gens.pop()
            self.count_gens -= 1
        count_of_gener = int(self.count_poc_line.text())
        chance = int(self.mutation_line.text())
        for i in range(count_of_gener):
            for j in range(0, self.count_gens, 2):
                father1, father2 = self.gens[j], self.gens[j + 1]
                self.krossingover(self.modify_checkbox.isChecked(), chance, father1, father2, j)
            self.gens = sorted(self.gens, key=lambda x: x[-1])[:self.count_gens]
        self.reload_table()
        text_for_output = ""
        for i in range(N):
            text_for_output += f"X[{i + 1}] = {self.gens[0][i]}\n"
        self.res_textedit.setText(text_for_output)
        self.func_res_line.setText(str(self.gens[0][-1]))

    def krossingover(self, modify, chance, father1, father2, j):
        if modify:
            a, b = self.mutation(chance, father1[0], father1[1])
            self.gens[j] = [a, b, func(a, b)]

            a, b = self.mutation(chance, father2[0], father2[1])
            self.gens[j + 1] = [a, b, func(a, b)]

            a, b = self.mutation(chance, (father1[0] + father2[0]) / 2, father2[1])
            self.gens.append([a, b, func(a, b)])

            a, b = self.mutation(chance, father2[0], (father1[1] + father2[1]) / 2)
            self.gens.append([a, b, func(a, b)])
        else:
            a, b = self.mutation(chance, father1[0], father1[1])
            self.gens[j] = [a, b, func(a, b)]

            a, b = self.mutation(chance, father2[0], father2[1])
            self.gens[j + 1] = [a, b, func(a, b)]

            a, b = self.mutation(chance, father1[0], father2[1])
            self.gens.append([a, b, func(a, b)])

            a, b = self.mutation(chance, father2[0], father1[1])
            self.gens.append([a, b, func(a, b)])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWinodow()
    ex.show()
    sys.exit(app.exec_())
