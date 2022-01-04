import pygame
from pygame import Surface, image
from pygame import surface
from pygame.locals import *

pygame.init()

black = (0, 0, 0)
blacklight = (40, 40, 40)
white = (255, 255, 255)
whitedeep = (250, 250, 250)
red = (255, 0, 0)
yellow = (255, 255, 0)
graydeep = (64, 64, 64)
gray = (128, 128, 128)
graylight = (246, 246, 246)
silver = (192, 192, 192)
brown = (210, 105, 30)
burlywood = (222, 184, 135)

#Mengatur warna dan ukuran layar
background_color = burlywood
(width, height) = (800, 680)

screen = pygame.display.set_mode((width, height))

#Mengubah warna screen
screen.fill(background_color)

#Menambahkan gambar
image = pygame.image.load('sun.png')
screen.blit(image,(600, 30))


#Membuat Bangunan
pygame.draw.rect(screen, silver,(100, 220, 500, 400))
pygame.draw.rect(screen, black,(100, 618, 500, 5))
pygame.draw.rect(screen, black,(100, 250, 5, 370))
pygame.draw.rect(screen, black,(600, 230, 5, 393))

#Membuat Pintu
pygame.draw.rect(screen, gray,(400, 420, 150, 198))
pygame.draw.rect(screen, black,(400, 415, 154, 5))
pygame.draw.rect(screen, black,(400, 420, 5, 200))
pygame.draw.rect(screen, black,(549, 420, 5, 203))

#Membuat Jendela
pygame.draw.rect(screen, whitedeep,(150, 290, 170, 100))
pygame.draw.rect(screen, black,(150, 290, 170, 5))
pygame.draw.rect(screen, black,(150, 390, 170, 5))
pygame.draw.rect(screen, black,(150, 290, 5, 100))
pygame.draw.rect(screen, black,(320, 290, 5, 105))

#Membuat Garis dalam jendela
pygame.draw.rect(screen, black,(150, 335, 170, 10))
pygame.draw.rect(screen, black,(234, 290, 10, 100))

#Membuat Gagang pintu
pygame.draw.rect(screen, black,(530, 520, 15, 15))

#Membuat Atap
pygame.draw.rect(screen, black,(100, 163, 500, 58))
pygame.draw.rect(screen, black,(200, 100, 300, 68))
pygame.draw.rect(screen, black,(280, 60, 124, 50))
pygame.draw.rect(screen, black,(50, 200, 600, 65))

#Membuat Cerobong 
pygame.draw.rect(screen, brown,(90, 70, 70, 100))

#Membuat Atap kanan kiri
pygame.draw.line(screen, black, (350, 30), (650, 230), 70)
pygame.draw.line(screen, black, (50, 230), (350, 30), 70)


running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    pygame.display.update()

pygame.quit()
