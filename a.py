"""
x = [ 
    2.6, 3.9, 4.5, 4.0, 3.7, 3.2, 5.7, 4.3, 3.8, 3.6, 
    4.7, 6.1, 6.0, 5.0, 4.5, 6.2, 3.4, 2.9, 3.6, 4.1,
    2.5, 2.8, 3.2, 3.1, 4.6, 5.2, 6.1, 4.5, 4.1, 3.8, 
    7.2, 3.4, 7.9, 3.6, 3.6, 4.8, 5.2, 6.3, 8.2, 5.3,
    3.9, 4.6, 4.5, 5.7, 4.8, 6.9, 6.3, 2.6, 2.5, 6.8,
    8.0, 5.6, 3.9, 4.6, 4.8, 5.9, 6.2, 3.2, 4.5, 5.0      
          ]

y = [
    2.5, 2.5, 2.6, 2.6, 2.8, 2.9, 3.1, 3.2, 3.2, 3.2, 
    3.4, 3.4, 3.6, 3.6, 3.6, 3.6, 3.7, 3.8, 3.8, 3.9,
    3.9, 3.9, 4.0, 4.1, 4.1, 4.3, 4.5, 4.5, 4.5, 4.5,
    4.5, 4.6, 4.6, 4.6, 4.7, 4.8, 4.8, 4.8, 5.0, 5.0,
    5.2, 5.2, 5.3, 5.6, 5.7, 5.7, 5.9, 6.0, 6.1, 6.1,
    6.2, 6.2, 6.3, 6.3, 6.8, 6.9, 7.2, 7.9, 8.0, 8.2]


#a) Ordena los datos en forma creciente.
x = sorted(x)

#b) Determina la frecuencia con que se repite cada valor


#c) Calcula la media aritmética, la moda y la mediana.
po = 0
for n in y:
    po += n

po /= len(y)

me = y[ int(len(y)/2 ) ]

mo = max(set(y), key=y.count)

all_d = list(dict.fromkeys(y))


print(po, me, mo, all_d, len(y) )
"""


def get_data():
    data_open = open("data.txt")
    data_f = list()
    for data in data_open:
        data_f.append(data.replace("\n", ""))
    data_open.close()

    return data_f

#data_open = open("data.txt", "w")


def write_data(*args):
    data_open = get_data()

    for n in range(0, len(data_open)):
        data_open[n] += "\n"

    data_write = open("data.txt", "w")

    for n in range(len(args[0]))

    data_open[args[0]] = args[1] + "\n"

    data_open = "".join(data_open)

    data_write.write(data_open)

    print(data_open)

# "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011101", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011101", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011100", "011101", 

