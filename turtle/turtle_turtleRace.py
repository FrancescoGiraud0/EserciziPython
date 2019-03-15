import turtle as t
import random
import time

def disegnaTraguardo():
    turtleTraguardo = t.Turtle()
    turtleTraguardo.penup()
    turtleTraguardo.goto(traguardo, DIM_Y/2+20)
    turtleTraguardo.pendown()
    turtleTraguardo.goto(traguardo, -(DIM_Y/2+20))
    turtleTraguardo.hideturtle()

def posizionaTurtle(i_turtle):
    y = float(turtlesNumber//2 - i_turtle) * (DIM_Y/2) / (turtlesNumber/2)
    turtlesList[i_turtle].goto(-((DIM_X/2)-10), y)

MAX_TURTLES = 20
DIM_X, DIM_Y = 600, 600
turtlesList = []
turtlesNumber = 0
vincitore = -1
traguardo = (DIM_X/2)-20

while turtlesNumber<=0 or turtlesNumber>=MAX_TURTLES:
    turtlesNumber = int(input("\n> Inserire numero di turtle in gara: "))

t.setup(DIM_X, DIM_Y+40)
t.colormode(255)
disegnaTraguardo()

for i in range(0,turtlesNumber):
        turtlesList.append(t.Turtle())
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        turtlesList[i].color((b,g,r))
        turtlesList[i].speed(0)
        turtlesList[i].penup()
        posizionaTurtle(i)
        turtlesList[i].pendown()
        turtlesList[i].speed(2)

print("\n", end = "\r")
for timer in reversed(range(1,4)):
    print("> La gara comincia tra %d" %timer, end = "\r")
    time.sleep(1)

print("> VIA!                                   ")

while vincitore<=-1:
    for i in range(0, turtlesNumber):
        step = random.randrange(0,21)
        turtlesList[i].forward(step)
        if turtlesList[i].xcor() > traguardo:
            vincitore = i
            turtlesList.pop(i)
            break

print("\n> Ha vinto la turtle numero %d!" % (vincitore+1))
time.sleep(1)

for perdente in turtlesList:
    perdente.clear()
    perdente.hideturtle()

print("\nPremi un tasto qualsiasi per uscire...")
input()