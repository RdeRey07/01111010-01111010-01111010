from controller import Robot, Keyboard

tilesize = 0.05

robot = Robot() 
timeStep = int(robot.getBasicTimeStep())

wheel_left = robot.getDevice("wheel1 motor")
wheel_right = robot.getDevice("wheel2 motor")

wheel_left.setPosition(float('inf'))
wheel_right.setPosition(float('inf'))

d1 = robot.getDevice("distance sensor1")
d1.enable(timeStep)

d2 = robot.getDevice("distance sensor2")
d2.enable(timeStep)

keyboard = Keyboard()
keyboard.enable(timeStep)

wheel_left.setVelocity(6.28)
wheel_right.setVelocity(6.28)

velocidad = 4.0
lastv = 1  
cnt = 0
def avanzar():
    wheel_left.setVelocity(velocidad)
    wheel_right.setVelocity(velocidad)

def retroceder():
    wheel_left.setVelocity(-velocidad)
    wheel_right.setVelocity(-velocidad)

    
while robot.step(timeStep) != -1:
    distancia1 = d1.getValue()
    distancia2 = d2.getValue()
    
    if lastv == 0:  
        retroceder()
        if distancia1 <= 0.1:
            cnt += 1
            
            lastv = 1
            
            
    elif lastv == 1:  
        avanzar()
        if distancia2 <= 0.1:
            cnt += 1

            lastv = 0
            
        
    if cnt == 6:
        wheel_left.setVelocity(0)
        wheel_right.setVelocity(0)
        break


    #https://github.com/RdeRey07/01111010-01111010-01111010