from controller import Robot, GPS, DistanceSensor, Gyro, Motor


robot = Robot()
timeStep = int(robot.getBasicTimeStep())


wheel_left = Motor("wheel1 motor")
wheel_right = Motor("wheel2 motor")
wheel_left.setPosition(float('inf'))
wheel_right.setPosition(float('inf'))


gps = GPS("gps")
gps.enable(timeStep)


ds_front = DistanceSensor("distance sensor1")
ds_front.enable(timeStep)

ds_left = DistanceSensor("distance sensor2")
ds_left.enable(timeStep)

ds_right = DistanceSensor("distance sensor3")
ds_right.enable(timeStep)


gyro = Gyro("gyro")
gyro.enable(timeStep)


vel_avance = 6.28
vel_retroceso = -6.28
vel_giro = 1.0  

estado = "avanzar"
cnt_pasos = 0
pasos_por_baldosa = 0
baldosa_inicial = None

baldosa_inicial_coords = None
distancia_tolerancia = 0.1  


def print_sensor_telemetry():
    pos = gps.getValues()
    gyro_angle = gyro.getValues()[1]  
    distancia_frontal = ds_front.getValue()
    distancia_izquierda = ds_left.getValue()
    distancia_derecha = ds_right.getValue()
    
    print(f"GPS Position: X={pos[0]:.2f}, Y={pos[1]:.2f}, Z={pos[2]:.2f}")
    print(f"Gyro Angle: {gyro_angle:.2f} degrees")
    print(f"Distance Sensor - Front: {distancia_frontal:.2f} units")
    print(f"Distance Sensor - Left: {distancia_izquierda:.2f} units")
    print(f"Distance Sensor - Right: {distancia_derecha:.2f} units")
    print(f"Current State: {estado}")
    print("---------------------------")



def avanzar():
    wheel_left.setVelocity(vel_avance)
    wheel_right.setVelocity(vel_avance)


def retroceder():
    wheel_left.setVelocity(vel_retroceso)
    wheel_right.setVelocity(vel_retroceso)


def girar_izquierda():
    wheel_left.setVelocity(vel_giro)
    wheel_right.setVelocity(-vel_giro)


def girar_derecha():
    wheel_left.setVelocity(-vel_giro)
    wheel_right.setVelocity(vel_giro)


while robot.step(timeStep) != -1:
    pos = gps.getValues()
    distancia_frontal = ds_front.getValue()
    distancia_izquierda = ds_left.getValue()
    distancia_derecha = ds_right.getValue()
    
    print_sensor_telemetry()
    
    if estado == "avanzar":
        if distancia_frontal > 0.1:
            avanzar()
        else:
            retroceder()
            estado = "retroceder"

    elif estado == "retroceder":
        if distancia_izquierda > 0.1:
            girar_izquierda()
            estado = "girando_izquierda"
        elif distancia_derecha > 0.1:
            girar_derecha()
            estado = "girando_derecha"
        else:
            avanzar()
            estado = "avanzar"

    elif estado == "girando_izquierda":
        if distancia_izquierda > 0.3:
            girar_izquierda()
        elif distancia_derecha > 0.3:
            girar_derecha()
        else:
            avanzar()
            estado = "avanzar"


    elif estado == "girando_derecha":
        if distancia_derecha > 0.3:
            girar_derecha()
        elif distancia_izquierda > 0.3:
            girar_izquierda()
        
        else:
            avanzar()
            estado = "avanzar"

    if (baldosa_inicial_coords is None or
        (abs(pos[0] - baldosa_inicial_coords[0]) < distancia_tolerancia and
         abs(pos[2] - baldosa_inicial_coords[1]) < distancia_tolerancia)):
        baldosa_inicial_coords = pos[0], pos[2]


wheel_left.setVelocity(0)
wheel_right.setVelocity(0)


#https://github.com/RdeRey07/01111010-01111010-01111010