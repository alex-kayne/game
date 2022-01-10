from time import time
def gen(s): # КЛЮЧЕВОЙ ПРИКОЛ ГЕНЕРАТОРА, ЧТО ПОСЛЕ ВЫЗОВА NEXT(), ПРОГРАММА ОПЯТЬ ПОЛУЧАЕТ КОНТРОЛЬ НАД ПОТОКОМ.
    # ВЫПОЛНЕНИЕ ВОВЗВРАЩАЕТСЯ В ТО МЕСТО, ГДЕ БЫЛ ВЫЗВАН NEXT
    # ГЕНЕРАТОР ЭТО ИМЕННО ФУНКЦИЯ - ОНА ВЫПОЛНЯЕТСЯ
    for i in s:
        yield i

g = gen('oleg')


def gen_filename():
    while True:
        pattern = 'file-{}.jpeg'
        t = int(time() * 1000)
        yield pattern.format(str(t))

        print('test') # разница между генератором и обычной функцией не только в том, что return -> yield, есть next,
        # но и в том, что после yield ыполнение функции не прерывается. код останавливается на yield - сдвиг происходит до след yield


def yield_loop(): # МОЖЕТ БЫТЬ НЕСКОЛЬКО СОБЫТИЙ
    while True:
        yield 1
        yield 2
        yield 3

y = yield_loop()


def gen2(n):
    for i in range(n):
        yield i

g1 = gen('oleg')
g2 = gen2(4)

tasks = [g1, g2]

while True:
    task = tasks.pop(0)
    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration and IndexError:
        pass