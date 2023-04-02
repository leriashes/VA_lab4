import numpy as np
import matplotlib.pyplot as plt
import math
import getch

#чтение таблицы из файла
def read_table():
    spisok = []
    table = []

    with open('znacheniya.csv', 'r') as file:
        i = 0
        print('ТАБЛИЦА ЗНАЧЕНИЙ (x и y)')
        for line in file.readlines():
            spisok.append([])
            table.append([])
            spisok[i].append(line[:line.find(';')])
            line = line[line.find(';') + 1:]
            spisok[i].append(line[:-1])

            for j in range(2):
                table[i].append(float(spisok[i][j]))
                j += 1
            i += 1
        

    table.sort()

    for strok in table:
        print(strok[0], end='   ')
        print(strok[1])

    print()

    return table

#чтение иксов из файла
def read_x():
    spisok = []
    xt = []

    with open('fx.csv', 'r') as file:
        i = 0
        for line in file.readlines():
            spisok.append(line[:line.find(';')])
            xt.append([])
            xt[i].append(float(spisok[i]))
            i += 1
        
    xt.sort()

    return xt

#интерполяционный полином Лагранжа
def Lagrange(table):

    n = len(table)
    coef_Lagrange = []

    #вычисление коэффициентов
    for i in range(n):
        coef1 = []
        coef = []

        znam = 1

        if i == 0:
            coef.append(table[1][0] * (-1))
        else:
            coef.append(table[0][0] * (-1))

        coef.append(1)

        for k in range(n):
            if k != i and k != abs(bool(i) - 1):

                coef1 = coef.copy()

                coef.insert(0, 0)

                for j in range(len(coef1)):
                    coef[j] += coef1[j] * table[k][0] * (-1)

            if k != i:
                znam *= (table[i][0] - table[k][0])

        for j in range(len(coef)):
            coef[j] /= znam
            coef[j] *= table[i][1]

        if i == 0:
            for j in range(len(coef)):
                coef_Lagrange.append(coef[j])
        else:
            for j in range(len(coef)):
                coef_Lagrange[j] += coef[j]

    #вывод полинома
    print('\nПолином Лагранжа: ', end='')

    for i in range(n - 1):
        print(coef_Lagrange[len(coef_Lagrange) - 1 - i], ' * (x^', n - i - 1, ') + ', end='', sep='')

    print(coef_Lagrange[0])

    return coef_Lagrange

#интерполяционный полином Ньютона
def Newton(table, f):

    #вычисление разностей
    n = len(table)
    
    f.append([])
    for i in range(n):
        f[0].append(table[i][1])
        

    for i in range(1, n):
        f.append([])
        k = i
        for j in range(n - i):
            f[i].append((f[i - 1][j + 1] - f[i - 1][j])/(table[k][0] - table[j][0]))
            k += 1

    #вывод полинома
    print('\nПолином Ньютона: ', table[0][1], end='')

    for i in range(n - 1):
        print(' + ', end='')
        for j in range(i + 1):
            print('(x - ', end='')
            if table[j][0] < 0:
                print('(', table[j][0], ')', end='', sep='')
            else:
                print(table[j][0], end='')
            print(') * ', end='')

        if f[i + 1][0] < 0:
            print('(', f[i + 1][0], ')', end='', sep='')
        else:
            print(f[i + 1][0], end='')
    
    return

#вычисление результатов путём подстановки в полином Лагранжа
def count_Lagrange(xs, coefs):
    order = len(coefs)

    ys = np.zeros(len(xs))

    ys += coefs[order - 1]

    for i in range(order - 1):
        ys *= xs
        ys += coefs[order - 2 - i]

    return ys

#вычисление результатов путём подстановки в полином Ньютона
def count_Newton(xs, f, table):

    ys = np.zeros(len(xs))
    ys += f[0][0]

    n = len(table)

    s = []

    for i in range(n - 1):
        s.append([])
        for j in range(len(ys)):
            s[i].append(f[i + 1][0])
   
    r = np.zeros(len(xs))

    for i in range(n - 1):
        r = xs - table[i]

        for j in range(n - 2, -1 + i, -1):
            s[j] *= r

    for i in range(n - 1):
        ys += s[i]

    return ys

#вычисление значений функции
def count_function(xs, func):
    ys = []

    for i in range(len(xs)):
        x = xs[i]
        ys.append(eval(func))
    return ys

#поиск максимального отклонения
def count_razn(iy, fy):
    razn = [[0, 0, 0]]
    k = 0

    for i in range(len(iy)):
        r = fy[i] - iy[i]
        if abs(r) > abs(razn[0][2]):
            razn[0][2] = r
            razn[0][0] = i
            razn[0][1] = fy[i]

    for i in range(len(iy)):
        r = fy[i] - iy[i]
        if abs(r) == abs(razn[0][2]) and i != razn[0][0]:
            razn.append([])
            k += 1
            razn[k].append(i)
            razn[k].append(fy[i])
            razn[k].append(r)

    return razn

#метод прогонки
def progonka(table, h):

    n = len(table) - 1

    a = []
    b = []

    for k in range(n - 1):
        i = k + 1

        a.append([])
        
        if k == 0:
            a[k].append(0)
        else:
            a[k].append(h[k])

        a[k].append(2 * (h[k] + h[k + 1]))
        
        if k == n - 2:
            a[k].append(0)
        else:
            a[k].append(h[k + 1])

        b.append(6 * ((table[i + 1][1] - table[i][1]) / h[k + 1] - (table[i][1] - table[i - 1][1]) / h[k]))

    #прямой ход
    v = []
    u = []

    v.append(a[0][2] / a[0][1] * (-1))
    u.append(b[0] / a[0][1])
    
    for i in range(1, n - 2):
        v.append(a[i][2] / (a[i][1] * (-1) - a[i][0] * v[i - 1]))
        u.append((a[i][0] * u[i - 1] - b[i]) / (a[i][1] * (-1) - a[i][0] * v[i - 1]))

    v.append(0)
    u.append((a[n - 2][0] * u[n - 3] - b[n - 2]) / (a[n - 2][1] * (-1) - a[n - 2][0] * v[n - 3]))
    

    #обратный ход
    x = []

    x.append(u[n - 2])

    for i in range(n - 2):
        x.append(v[n - i - 3] * x[i] + u[n - i - 3])

    x.reverse()

    return x

#вычисление значения для интерполяции
def countS(a, b, c, d, xi, x):
    return a + b * (x - xi) + pow(x - xi, 2) * c / 2 + pow(x - xi, 3) * d / 6

#первый вариант работы программы
def variant1():
    table = read_table()
    n = len(table) - 1
    ag = table[0][0]
    bg = table[n - 1][0]

    while(True):
        print('Введите значение x для точки: ', end='')
        xzn = float(input())

        if xzn >= ag and xzn <= bg:
            break

    #h
    h = []
    for i in range(n):
        h.append(table[i + 1][0] - table[i][0])

    
    c = progonka(table, h)
    c.append(0)
    c.insert(0, 0)

    d = []
    b = []

    for i in range(n):
        d.append((c[i + 1] - c[i]) / h[i])
        b.append((h[i] * c[i + 1]) / 2 - d[i] * pow(h[i], 2) / 6 + (table[i + 1][1] - table[i][1]) / h[i])


    for i in range(n):
        if xzn >= table[i][0] and xzn <= table[i + 1][0]:
            result = countS(table[i + 1][1], b[i], c[i + 1], d[i], table[i + 1][0], xzn)
            break

    print('\n\nРезультат: ', result)

    result = 0

    count = 0
    for i in range(n):
        chisl = table[i][1]
        znam = 1
        for j in range(n):
            count += 1
            if (i != j):
                chisl *= xzn - table[j][0]
                znam *= table[i][0] - table[j][0]
        result += chisl / znam

    print('\n\nРезультат (полином Лагранжа): ', result)


    coef_Lagrange = Lagrange(table)

    result1 = coef_Lagrange[len(coef_Lagrange) - 1]
    count = 0

    for i in range(n - 1):
        result1 *= xzn
        result1 += coef_Lagrange[len(coef_Lagrange) - 2 - i]
        count += 1

    print('\nРезультат (полином Лагранжа): ', result1)


    f = []
    Newton(table, f)

    result = table[0][1]
    s = []

    for i in range(1, n):
        s.append(f[i][0])

    for i in range(n - 1):
        r = xzn - table[i][0]

        for j in range(n - 2, -1 + i, -1):
            s[j] *= r

    for i in range(n - 1):
        result += s[i]

    print('\n\nРезультат (полином Ньютона): ', result)

    xt = []
    yt = []

    for i in range(len(table)):
        xt.append(table[i][0])
        yt.append(table[i][1])

    x = np.arange(table[0][0], table[len(table) - 1][0], 0.001)
    plt.plot(x, count_Lagrange(x, coef_Lagrange), 'y')
    plt.plot(x, count_Newton(x, f, xt), 'g')

    plt.plot(xzn, result, 'ro')
    plt.plot(xt, yt, 'bo')
    plt.grid(True)

    plt.xlabel(r'$x$', fontsize=14)
    plt.ylabel(r'$y$', fontsize=14)

    plt.show()

    return

#второй вариант работы прораммы
def variant2():
    print('Введите функцию: y = ', end='')
    func = input()

    table = read_x()

    for i in range(len(table)):
        x = table[i][0]
        table[i].append(eval(func))
        print('x = ', table[i][0], '   y = ', table[i][1], sep='')

    coef_Lagrange = Lagrange(table)

    f = []
    Newton(table, f)

    xt = []
    yt = []

    for i in range(len(table)):
        xt.append(table[i][0])
        yt.append(table[i][1])

    x = np.arange(table[0][0], table[len(table) - 1][0], 0.001)

    ly = count_Lagrange(x, coef_Lagrange)
    plt.plot(x, ly, 'y')
    plt.plot(x, count_Newton(x, f, xt), 'g')
    
    fy = count_function(x, func)
    plt.plot(x, fy, 'r', label=r'f(x)')

    plt.plot(xt, yt, 'bo')
    plt.grid(True)
    plt.legend(loc='best', fontsize=12)

    plt.xlabel(r'$x$', fontsize=14)
    plt.ylabel(r'$y$', fontsize=14)

    razn = count_razn(ly, fy)

    for i in range(len(razn)):
        razn[i][0] = table[0][0] + razn[i][0] * 0.001
        plt.plot([razn[i][0], razn[i][0]], [razn[i][1], razn[i][1] - razn[i][2]], 'orange')

    print('\n\nМаксимальное отклонение: ', abs(razn[0][2]))
    plt.show()
    return

    
while True:
    while True:
        print('Режимы работы:\n1 - по заданной таблице значений определить \n    приближённое значение функции в точке\n2 - по заданной аналитически функции y = f(x) и массиву значений аргумента \n    вычислить таблицу значений функции\n\nВыберите режим работы программы: ', end='')
        variant = input()

        print('\n')
        if len(variant) == 1 and (variant[0] == '1' or variant[0] == '2'):
            if variant == '1':
                variant1()
            else:
                variant2()
            break
    print('\n\nЧтобы продолжить нажмите Enter. Для выхода из программы нажмите любую другую клавишу. ', end='')
    cont = getch.getch()
   
    if cont == '\n' or cont == b'\r':
        print('\n\n')
    else:
        break
