import random
import math
import tkinter

tk = tkinter.Tk()
canvas = tkinter.Canvas(tk, width=500, height=500)
canvas.pack()

#Storing data for cities####################################################

number_of_cities = int(input("For how many cities do you want to find the best route: "))
'''
cities_x = [290, 100, 380, 450, 70, 330, 170, 150, 150, 170, 230, 390, 350, 480, 40, 430, 310, 330, 100, 180,
60, 120, 70, 80, 400, 420, 170, 290, 140, 430, 240, 400, 440, 100, 180, 100, 30, 110, 140, 320]
cities_y = [190, 280, 450, 40, 390, 100, 230, 440, 250, 310, 140, 330, 420, 100, 400, 460, 460, 140, 480, 160,
400, 320, 30, 240, 360, 220, 420, 320, 140, 350, 260, 210, 250, 30, 440, 460, 280, 360, 180, 70]
'''

cities_x = [0]*number_of_cities
cities_y = [0]*number_of_cities
for i in range(number_of_cities):
    cities_x[i] = random.randint(20,480)
    cities_y[i] = random.randint(20,480)

#########################################################################
def draw(path):
    canvas.delete('all')
    for i in range(0,number_of_cities-1):
        first_city = path[i]
        second_city = path[i+1]
        canvas.create_line(cities_x[first_city], cities_y[first_city], cities_x[second_city], cities_y[second_city])
        canvas.create_oval(cities_x[first_city]-2, cities_y[first_city]-2, cities_x[first_city]+2,cities_y[first_city]+2,fill = "red")
    canvas.create_line(cities_x[path[number_of_cities-1]], cities_y[path[number_of_cities-1]], cities_x[path[0]], cities_y[path[0]])
    canvas.create_oval(cities_x[path[number_of_cities-1]]-2, cities_y[path[number_of_cities-1]]-2, cities_x[path[number_of_cities-1]]+2,cities_y[path[number_of_cities-1]]+2, fill = "red")
    tk.update()

def fit(path):
    total = 0
    for i in range(len(path) - 1):
        total += math.sqrt(
            (cities_x[path[i]] - cities_x[path[i + 1]]) ** 2 + (cities_y[path[i]] - cities_y[path[i + 1]]) ** 2)
    total += math.sqrt((cities_x[path[0]] - cities_x[path[-1]]) ** 2 + (cities_y[path[0]] - cities_y[path[-1]]) ** 2)
    return total

def generate1(path):
    children = []
    for i in range(len(path) - 1):
        child = path.copy()
        child[i], child[i+1] = child[i+1], child[i]
        children.append(child)
    return children

def generate2(path):
    children = []
    for i in range(len(path) - 1):
        for j in range(i + 1, len(path)):
            child = path.copy()
            child[i], child[j] = child[j], child[i]
            children.append(child)
    return children

def generate3(path):
    children = []
    for i in range(len(path) - 1):
        for j in range(i + 1, len(path)):
            child = path.copy()
            city = child.pop(i)
            child.insert(j, city)
            children.append(child)
    return children

def generate4(path):
    children = []
    for i in range(len(path) - 1):
        for j in range(i + 1, len(path)):
            child = path.copy()
            child[i:j] = reversed(child[i:j])
            children.append(child)
    return children

def generate5(path):
    children = []
    for i in range(len(path) - 1):
        for j in range(i + 1, len(path)):
            child = path.copy()
            child[i:j] = reversed(child[i:j])
            children.append(child)
            child = path.copy()
            city = child.pop(i)
            child.insert(j, city)
            children.append(child)
    return children

def search(temp,lowest_temp,rate):
    current_path = list(range(number_of_cities))
    random.shuffle(current_path)
    current_distance = float('inf')
    l = 0
    was_all = True
    while temp > lowest_temp and was_all:
        current_distance = fit(current_path)
        children = generate4(current_path)
        found = False
        while not found:
            if not children:
                was_all = False
                break
            else:
                pos_path = random.choice(children).copy()
                children.remove(pos_path)
                pos_distance = fit(pos_path)
                if pos_distance < current_distance or random.random() < math.exp((current_distance-pos_distance)/temp):
                    current_path = pos_path.copy()
                    found = True
        temp = rate*temp
        l += 1
        draw(current_path)
    print("The best route is:", current_path)
    print("Its length is:", current_distance)
    print("Number of iterations:", l)
    return current_distance

#Start the search
s = 0
test = input("Do you want to test? (yes/no): ")
if test == "no":
    search(55.48,1,0.992)
else:
    t = float(input("What should the initial temperature be: "))
    r = float(input("What should the cooling rate be: "))
    m = float(input("What should the minimum temperature be: "))
    num = int(input("Enter the number of calculations: "))
    for i in range(num):
        s +=  search(t,m,r)
    print("The average route length is:", s/num)
tk.mainloop()
