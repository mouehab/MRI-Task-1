import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import enum
import sys



class Modes(enum.Enum):
    recovery = 1 
    decay =  2
    precession = 3


magVector=[1,1,1]
magVector1=[None]*2
xVector=[]
yVector=[]

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.grid()

# magVectorZ=[0.01,0.01,1]
magVectorZ=[1,1,1]
xVector=[]
yVector=[]
zVector=[]
tVector=[]
t=0

def data_gen(mode, angle):
    magVector1=[None]*3
    magVectorXY=[None]*3
    t=0
    df=10
    magVectorXY[0]=magVector[0]*math.cos(angle)
    magVectorXY[1]=magVector[1]*math.cos(angle)
    magVectorXY[2]=magVector[2]*math.cos(angle)

    while(magVector1[0]!=0 or magVector1[1]!=0):
        E1 = math.exp(-t/100)
        E2 = math.exp(-t/600)
        A= np.array([[E2,0,0],[0,E2,0],[0,0,E1]])
        B= np.array([0, 0, 1-E1])
        phi =2*math.pi*df*t/1000
        Rz=np.array([[math.cos(phi),-math.sin(phi),0],[math.sin(phi),math.cos(phi),0],[0, 0, 1]])
        Afb = np.matmul(A,Rz)
        magVector1 =np.matmul(Afb,magVectorXY)+B
        
        if(mode ==Modes.recovery):
            yield t, magVector1[2]
            t = t+10
        elif(mode == Modes.decay):
            yield t, np.sqrt(np.square(magVector1[0])+np.square(magVector1[1]))
            t = t+10
        elif(mode == Modes.precession):
            yield magVector1[0], magVector1[1]
            t = t+10
        else: print("errorrrr")           

def init():
    ax.set_ylim(-2.0,2.0)
    ax.set_xlim(-2.0, 2.0)
    del xVector[:]
    del yVector[:]
    line.set_data(xVector, yVector)
    return line,



def run(data):
    # update the data
    t, y = data
    xVector.append(t)
    yVector.append(y)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ax.figure.canvas.draw()
    line.set_data(xVector, yVector)
        
    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    if y >= ymax:
        ax.set_ylim(ymin, 2*ymax)
        ax.figure.canvas.draw()
    
    line.set_data(xVector, yVector)

    return line,

def main(*args, **kwargs):
    Index = Modes[sys.argv[1]]
    theta = float(sys.argv[2])
    print(Index)
    print(theta)
   
    ani = animation.FuncAnimation(fig, run, data_gen(Index,theta), blit=False, interval=10,
                              repeat=True, init_func=init)
    plt.show()

if __name__ == '__main__':
    main()