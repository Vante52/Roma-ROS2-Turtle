#!/usr/bin/env python3
import sys
import termios
import tty
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

msg = """
🤖 Controla a ROMA!
---------------------------
Movimiento (WASD o Flechas):
        w / ↑
   a / ←   s / ↓   d / →

Espacio: Freno de emergencia
q / Esc: Salir
---------------------------
"""

# Diccionario de teclas -> (Linear X, Angular Z)
moveBindings = {



    
    'w': (1.0, 0.0),
    's': (-1.0, 0.0),
    'a': (0.0, 1.0),
    'd': (0.0, -1.0),
    '\x1b[A': (1.0, 0.0),  # Flecha Arriba
    '\x1b[B': (-1.0, 0.0), # Flecha Abajo
    '\x1b[C': (0.0, -1.0), # Flecha Derecha
    '\x1b[D': (0.0, 1.0),  # Flecha Izquierda
}

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    if key == '\x1b': # Si es una flecha, lee los siguientes 2 bytes
        key += sys.stdin.read(2)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = rclpy.create_node('teleop_wasd')
    publisher = node.create_publisher(Twist, 'cmd_vel', 10)
    
    speed = 0.5 # Velocidad lineal (m/s)
    turn = 1.0  # Velocidad de giro (rad/s)
    
    print(msg)
    try:
        while True:
            key = getKey(settings)
            
            x = 0.0
            th = 0.0
            
            if key in moveBindings:
                x = moveBindings[key][0]
                th = moveBindings[key][1]
            elif key == ' ': # Freno
                x = 0.0
                th = 0.0
            elif key == 'q' or key == '\x1b': # Salir
                break
                
            # Construir y enviar el mensaje ROS
            twist = Twist()
            twist.linear.x = x * speed
            twist.angular.z = th * turn
            publisher.publish(twist)

    except Exception as e:
        print(e)
    finally:
        # Al salir, asegurar que el robot se detenga
        twist = Twist()
        publisher.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
