import datetime


# correction of the output form of the final value
def tofixed(numobj, digits=0):
    return f"{numobj:.{digits}f}"


# getting a list of all vertices
def Vertex(mas):
    ans = []
    for i in mas:
        if int(i[1]) not in ans:
            ans.append(int(i[1]))

    return ans


# initialization of the adjacency matrix given as a dictionary
def matrixx(mas, vertex):
    ans = {}
    for i in vertex:
        ans[i] = []
    for i in vertex:
        for j in mas:
            if str(i) == j[1]:

                if int(j[2]) not in ans[i]:
                    ans[i].append(int(j[2]))
                    ans[i].sort()

    return ans


# search for the Hamiltonian path
def hamilton(g, size, pt, path=[]):

    if pt not in set(path):
        path.append(pt)
        if len(path) == size:
            return path
        for pt_next in g.get(pt, []):
            res_path = [i for i in path]
            candidate = hamilton(g, size, pt_next, res_path)
            if candidate is not None:
                return candidate


# reading from a file
def read():
    f = open('text.csv', 'r')
    mas = [[]] * 250
    iterator = 0

    for i in f:
        k = i.splitlines()
        k = k[0].split(';')
        mas[iterator] = k
        iterator += 1
    f.close()
    return mas


# list of trains passing between stations
def ways(mas):
    dic = {}
    for i in mas:
        if (i[1], i[2]) not in dic:
            dic[(i[1], i[2])] = []
            dic[(i[1], i[2])].append(i[0])
        else:
            dic[(i[1], i[2])].append(i[0])
    return dic


# calculation of the fastest path between vertices from the ''path'' list
def time(path, dic, mas):
    tmp_min_time = 0
    min_time = 0
    num_trains = []
    t = ''
    tmp = 0
    previous = 0

    for i in range(len(path) - 1):
        for j in range(len(dic[str(path[i]), str(path[i + 1])])):
            train = dic[str(path[i]), str(path[i + 1])][j]

            for h in mas:
                if str(train) == h[0] and str(path[i]) == h[1] and str(path[i + 1]) == h[2]:

                    if len(num_trains) == 0:
                        dt1 = datetime.datetime.strptime(h[4], "%H:%M:%S")
                        dt2 = datetime.datetime.strptime(h[5], "%H:%M:%S")
                        tmp = (dt2 - dt1).seconds

                        if tmp_min_time == 0 or tmp_min_time > tmp:
                            t = h[0]
                            tmp_min_time = tmp
                            previous = h[5]

                    else:

                        dt1 = datetime.datetime.strptime(h[4], "%H:%M:%S")  # отъезд
                        dt2 = datetime.datetime.strptime(h[5], "%H:%M:%S")  # приезд
                        dt3 = datetime.datetime.strptime(previous, "%H:%M:%S")  # приезд предыдущего

                        tmp = (dt2 - dt1).seconds + (dt1 - dt3).seconds

                        if tmp_min_time == 0 or tmp_min_time > tmp:
                            t = h[0]
                            tmp_min_time = tmp
                            previous = h[5]

        num_trains.append(t)
        min_time += tmp_min_time
        tmp_min_time = 0

    print('min time->', int(min_time/3600), 'hours', int(min_time % 3600/60), 'minutes')
    print('trains->', num_trains)


# counting the cheapest path between vertices from the ''path'' list
def cost(path, dic, mas):
    tmp_min_cost = 0
    min_cost = 0
    num_trains = []
    t = ''
    for i in range(len(path) - 1):
        for j in range(len(dic[str(path[i]), str(path[i + 1])])):
            train = dic[str(path[i]), str(path[i + 1])][j]

            for h in mas:
                if str(train) == h[0] and str(path[i]) == h[1] and str(path[i + 1]) == h[2]:
                    t = h[0]
                    if tmp_min_cost == 0 or tmp_min_cost > float(h[3]):
                        tmp_min_cost = float(h[3])

        num_trains.append(t)
        min_cost += tmp_min_cost
        tmp_min_cost = 0

    print('min cost->', tofixed(min_cost, 2))
    print('trains->', num_trains)
    print('------------------------')


def main():
    mas = read()
    dic = ways(mas)

    vertex = Vertex(mas)
    matrix = matrixx(mas, vertex)
    path = hamilton(matrix, len(vertex), 1909, [])
    path1 = hamilton(matrix, len(vertex), 1981, [])

    cost(path, dic, mas)
    time(path1, dic, mas)


main()
