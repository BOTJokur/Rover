import RPi.GPIO as GPIO
from time import sleep
import pygame
from pygame.locals import K_a, K_d, K_w, K_s
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

GPIO.setwarnings(False)

pygame.init()
screen = pygame.display.set_mode((320,240))
#setting the variables NOTE: 1 = BOTTOM MOTOR 2 = TOP MOTOR
resetAngle1 = 100
resetAngle2 = 165
resetTime = 1
runtime = 0.5
servoPIN1 = 17
servoPIN2 = 27
increment = 20
lowestangle = 5
maxangle = 180
angle1 = resetAngle1
angle2 = resetAngle2

GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)
p2 = GPIO.PWM(servoPIN2, 50)
p2.start(0)
p1 = GPIO.PWM(servoPIN1, 50)
p1.start(0)

GPIO.setup(18, GPIO.OUT) #OUTPUT1
GPIO.setup(24, GPIO.OUT) #OUTPUT2
GPIO.setup(14, GPIO.OUT) #OUTPUT3
GPIO.setup(2, GPIO.OUT)  #OUTPUT4
           


quit = False

def SetAngle1(angle): #Code for making the bottom servo motor servo turn in the direction we want
    duty = angle/18+2
    GPIO.output(servoPIN1, 1)
    p1.ChangeDutyCycle(duty)
    sleep(runtime)
    GPIO.output(servoPIN1, 0)
    p1.ChangeDutyCycle(0)

def SetAngle2(angle): #Code for making the top servo motor servo turn in the direction we want
    duty = angle/18+2
    GPIO.output(servoPIN2, 1)
    p2.ChangeDutyCycle(duty)
    sleep(runtime)
    GPIO.output(servoPIN2, 0)
    p2.ChangeDutyCycle(0)


while not quit:  
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: #Whenever A is pressed, the servo motor controlling the camera will turn the camera LEFT 20 degrees
                    if angle1 <= maxangle:
                       angle1 = angle1 + increment
                       SetAngle1(angle1)
                if event.key == pygame.K_d: #Whenever D is pressed, the servo motor controlling the camera will turn the camera RIGHT 20 degrees
                    if angle1 >= lowestangle:
                       angle1 = angle1 - increment
                       SetAngle1(angle1)
                if event.key == pygame.K_s: #Whenever S is pressed, the servo motor controlling the camera will turn the camera DOWN 20 degrees
                    if angle2 <= maxangle:
                       angle2 = angle2 + increment
                       SetAngle2(angle2)
                if event.key == pygame.K_w: #Whenever W is pressed, the servo motor controlling the camera will turn the camera UP 20 degrees
                    if angle2 >= lowestangle:
                       angle2 = angle2 - increment
                       SetAngle2(angle2)
                if event.key == pygame.K_x: #Whenever X is pressed, both the servo motors will go back to their default state (makes the camera look straight forward)
                    SetAngle1(resetAngle1, resetTime)
                    SetAngle2(resetAngle2, resetTime)
                    angle1 = resetAngle1
                    angle2 = resetAngle2
                if event.key == pygame.K_UP: #Moves the rover forward when the UP arrow is pressed
                    GPIO.output(18, 1)
                    GPIO.output(14, 1)
                    print("FORWARDS")
                    
                if event.key == pygame.K_DOWN: #Moves the rover backwards when the DOWN arrow is pressed
                    GPIO.output(24, 1)
                    GPIO.output(2, 1)
                    print("BACKWARDS")
                    
                if event.key == pygame.K_LEFT: #Rotates the rover left when the LEFT arrow is pressed
                    GPIO.output(14, 1)
                    GPIO.output(2, 1)
                    print("LEFT")
                if event.key == pygame.K_RIGHT: #Rotates the rover right when the RIGHT arrow is pressed
                    GPIO.output(18, 1)
                    GPIO.output(24, 1)
                    print("RIGHT")
            elif event.type == pygame.KEYUP: #When no buttons are pressed, the rover stops moving
                GPIO.output(18, 0)
                GPIO.output(24, 0)
                GPIO.output(14, 0)
                GPIO.output(2, 0)
