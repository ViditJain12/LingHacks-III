import pygame
import random
import math

# Initialising of pygame and needs to written in every game or else pygame will not work
pygame.init()

# Makes a screen of width by height
screen = pygame.display.set_mode((800, 600))

# Setting the title and the icon of the screen
pygame.display.set_caption("Space Invader")
image = pygame.image.load("spaceship.png")
pygame.display.set_icon(image)


# Loading an image in the screen of the game for the player
player_Img = pygame.image.load("space.png")
playerX = 370  # Coordinates of the image -> X axis
playerY = 480  # Coordinates of the image -> Y axis
playerX_Change = 0  # New coordinates to be made if any movement key is pressed for -> X axis
playerY_Change = 0  # New coordinates to be made if any movement key is pressed for -> Y axis

# Loading an image in the screen of the game for the enemies
enemy_Img = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_Of_Enemies = 6

for enemies in range(num_Of_Enemies):
    enemy_Img.append(pygame.image.load("space-invaders.png"))
    enemyX.append(random.randint(0, 800 - 64))
    enemyY.append(random.randint(25, 200))
    enemyX_Change.append(0.25)
    enemyY_Change.append(30)

# Loading an image in the screen of the game for the bullet
bullet_Img = pygame.image.load("bullet.png")
bulletX = 0  # The X coordinate of the bullet will remain at stop and will change according to X coordinate of the ship
bulletY = 0  # The bullet will have its initial position at stop and will change according to Y coordinate of the ship
bulletX_Change = 0  # The bullet is not moving left or right
bulletY_Change = 0.40  # The bullet will move in the upward direction with speed of 0.35
bullet_state = "Ready"  # Ready states mean the bullet is not visible and is ready to be fired

# Score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)  # Font name and its size
textX = 10
textY = 10


# Function for displaying the score
def show_score(x, y):
    # Text to be displayed, value in string to be displayed, if true then rendered, color of the font
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))     # Rendering the score
    screen.blit(score_value, (x, y))    # Displaying the score on the screen after it has been rendered


def Game_Over():
    font_2 = pygame.font.Font("freesansbold.ttf", 62)
    game_over_text = font_2.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(game_over_text, (180, 240))
    font_3 = pygame.font.Font("freesansbold.ttf", 45)
    final_score = game_over_text = font_3.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(game_over_text, (300, 300))


# Function for adding the loaded image of the player on the screen with its coordinates
def player(x, y):
    screen.blit(player_Img, (x, y))


# Function for adding the loaded image of the enemy on the screen with its coordinates
def enemy(x, y, enemies):
    screen.blit(enemy_Img[enemies], (x, y))


def fire_bullet(x, y):  # Function to be called when we press the space key
    global bullet_state
    bullet_state = "Fire"  # Bullet is ready to fire
    t = x + 16.00
    screen.blit(bullet_Img, (int(t), int(y)))  # Bullet appears at the center of the spaceship


# Function to detect collision
def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance < 27:
        return True
    else:
        return False


# The whole game is written inside a while loop and will execute until the game window has been closed
# Anything that needs to happen inside the game and change according to user input has to be inside of the while loop
running = True
while running:
    # Fills the color of the screen according to RGB
    screen.fill((128, 102, 255))
    # Checks all of the events in the system
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the event of pressing the x on the screen is clicked, the game stops
            running = False  # By making the while loop false and then it is not longer needed to be executed

        # If any key is pressed. If yes it will see which one and will shift the image according to it
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                playerX_Change = -0.32
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                playerX_Change = 0.32
            if event.key in (pygame.K_UP, pygame.K_w):
                playerY_Change = -0.32
            if event.key in (pygame.K_DOWN, pygame.K_s):
                playerY_Change = 0.32
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    # Gets the current X and Y coordinates and stores it in the variables
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        # If key has been released. If yes which one and will stop the image at the place it is currently at
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_d, pygame.K_a):
                playerX_Change = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                playerY_Change = 0

    # Updated coordinates of the image in the screen
    # Putting a boundary for the screen to prevent the image from going beyond the screen
    playerX += playerX_Change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 800 - 64:  # The image itself is 64 bits so we subtract 800 from it
        playerX = 800 - 64

    playerY += playerY_Change
    if playerY <= 300:  # The image of the player does not go beyond the coordinates of the enemy
        playerY = 300
    elif playerY >= 600 - 64:  # The image itself is 64 bits so we subtract 800 from it
        playerY = 600 - 64

    # Enemy movement
    for enemies in range(num_Of_Enemies):
        # Game Over
        if enemyY[enemies] >= playerY:
            for j in range(num_Of_Enemies):
                enemyY[j] = 1000
                playerY = 1000
                playerX = 1000
                textX = 1000
                textY = 1000
            Game_Over()
            break

        enemyX[enemies] += enemyX_Change[enemies]
        if enemyX[enemies] <= 0:
            enemyX_Change[enemies] = 0.25
            enemyY[enemies] += enemyY_Change[enemies]
        elif enemyX[enemies] >= 800 - 64:
            enemyX_Change[enemies] = -0.25
            enemyY[enemies] += enemyY_Change[enemies]

        if enemyY[enemies] >= 600 - 64:  # To prevent the enemy to go beyond the height of the screen
            enemyY[enemies] = 600 - 64

            # Collision
        collisions = collision(enemyX[enemies], enemyY[enemies], bulletX, bulletY)
        if collisions:
            bulletY = 0
            bullet_state = "Ready"
            score += 5
            enemyX[enemies] = random.randint(0, 800 - 64)
            enemyY[enemies] = random.randint(25, 200)

        enemy(enemyX[enemies], enemyY[enemies], enemies)

    # -> Bullet movement
    # Bullet resetting after reaching the end of the screen to its default position
    if bulletY <= 0:
        bulletY = 0
        bullet_state = "Ready"

    # Checking if bullet state is ready to fire and if yes, then the bullet fires from the spaceship
    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(int(playerX), int(playerY))
    show_score(textX, textY)

    # Important line written in every game to update the window of the game with every single event and changes occurred
    pygame.display.update()
