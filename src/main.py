"""
THE LEGEND OF ROBOT - Final Project: Helsinki MOOC (Part 14)
Author: Luis Suárez Afonso
Date: March 2026

A 2D state-based game where a robot must collect 10 coins to buy a sword,
defeat all monsters, and escape through a portal.
"""

import random

import pygame

# ===============================================
# ENTITY MODEL CLASSES (Robot, Monster, Coins...)
# ===============================================


class Robot:
    def __init__(self, window_width, window_height):

        # Image load and hitbox configuration of the robot.
        self.image = pygame.image.load("src/robot.png")
        self.rect = self.image.get_rect()

        # Initial position: Center in the x axis and supported on the y axis.
        self.rect.centerx = window_width // 2
        self.rect.bottom = window_height
        self.velocity = 3

    def move(self, keys, window_width, window_height):

        # Movement management with boundary checking.
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < window_width:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < window_height:
            self.rect.y += self.velocity

    def draw(self, window):

        # Render the robot in it's actual position.
        window.blit(self.image, (self.rect.x, self.rect.y))


class Coin:
    def __init__(self, window_width, window_height):

        # Image load and hitbox configuration of the coins.
        self.image = pygame.image.load("src/coin.png")
        self.rect = self.image.get_rect()
        self.window_width = window_width
        self.window_height = window_height

        # Reset it's position at the start of the game.
        self.reset_position()

    def reset_position(self):

        # Reset it's position in a random location above the window.
        self.rect.x = random.randint(0, self.window_width - self.rect.width)
        self.rect.y = random.randint(-1000, -50)
        self.velocity = random.randint(2, 5)

    def fall(self):

        # Make the coin fall
        self.rect.y += self.velocity

        # If the coin go beyond the window reset it's position.
        if self.rect.top > self.window_height:
            self.reset_position()

    def draw(self, window):

        # Render the coin in it's actual position.
        window.blit(self.image, (self.rect.x, self.rect.y))


class Monster:
    def __init__(self, window_width, window_height):

        # Image load and hitbox configuration of the monsters.
        self.image = pygame.image.load("src/monster.png")
        self.rect = self.image.get_rect()
        self.window_width = window_width
        self.window_height = window_height
        self.velocity = 1

        # Reset it's position at the start of the game.
        self.reset_position()

    def reset_position(self):

        # Reset it's position in a random location above the window.
        self.rect.x = random.randint(0, self.window_width - self.rect.width)
        self.rect.y = random.randint(-500, -100)

    def persecute(self, robot_rect):

        # A simple AI algorithm that make the monster chase the robot.
        if self.rect.x < robot_rect.x:
            self.rect.x += self.velocity
        elif self.rect.x > robot_rect.x:
            self.rect.x -= self.velocity
        if self.rect.y < robot_rect.y:
            self.rect.y += self.velocity
        elif self.rect.y > robot_rect.y:
            self.rect.y -= self.velocity

    def draw(self, window):

        # Render the monster in it's actual position.
        window.blit(self.image, (self.rect.x, self.rect.y))


class Sword:
    def __init__(self, x, y):

        # Hitbox configuration and modeling of the sword.
        self.rect = pygame.Rect(x, y, 16, 44)
        self.color = (192, 192, 192)

        # Relative points to make the model.
        self.relative_points = [
            (x + 0, y + 0),
            (x + 8, y + 10),
            (x + 8, y + 30),
            (x + 16, y + 30),
            (x + 16, y + 38),
            (x + 8, y + 38),
            (x + 4, y + 44),
            (x + -4, y + 44),
            (x + -8, y + 38),
            (x + -16, y + 38),
            (x + -16, y + 30),
            (x + -8, y + 30),
            (x + -8, y + 10),
        ]

    def draw(self, window):

        # Render the sword in the middle of the window.
        pygame.draw.polygon(window, self.color, self.relative_points)


class Door:
    def __init__(self, window_width):

        # Image load and hitbox configuration of door/portal.
        self.image = pygame.image.load("src/door.png")
        self.rect = self.image.get_rect()

        # The position in the top of the window above the sword.
        self.rect.centerx = window_width // 2
        self.rect.y = 0

    def draw(self, window):

        # Render the door in the top of the window.
        window.blit(self.image, (self.rect.x, self.rect.y))


# ===============================================
# MAIN GAME FUNCTIONALITY CLASS
# ===============================================


class Game:
    def __init__(self):

        # Pygame initializing.
        pygame.init()

        # Create the window of the program.
        self.width, self.height = 640, 480
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Legend of Robot")

        # Other configurations like the font of the text and the clock cycles of CPU.
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        # Starts a new game.
        self.new_game()

    def new_game(self):  # Function that stars a new game

        # Resets all the values to start a new game.
        self.points = 0
        self.have_sword = False
        self.game_active = True
        self.win = False
        self.game_over = False

        # Create the robot
        self.robot = Robot(self.width, self.height)

        # Create the coins using a list comprehension.
        self.coins = [Coin(self.width, self.height) for i in range(6)]

        # Create the monsters using a list comprehension.
        self.monsters = [Monster(self.width, self.height) for i in range(2)]

        # Create the sword.
        self.sword = Sword(self.width // 2, self.height // 2)

        # Create the door.
        self.door = Door(self.width)

    def update(self):  # Function that updates the game

        # Freeze the game if is not active.
        if not self.game_active:
            return

        # Register of the keys pressed.
        keys = pygame.key.get_pressed()

        # Move the robot depending on the keys pressed.
        self.robot.move(keys, self.width, self.height)

        for coin in self.coins:
            # The coin fall.
            coin.fall()

            # If touch the robot coins +1 and reset it's position.
            if coin.rect.colliderect(self.robot.rect):
                self.points += 1
                coin.reset_position()

        # If you get 10 coins, clear all the coins in the window.
        if self.points == 10:
            self.coins = []

        # If you have 10 or more points you can buy the sword with 10 coins.
        if self.points >= 10 and not self.have_sword:
            if self.sword.rect.colliderect(self.robot.rect):
                self.have_sword = True
                self.sword.rect.y = -1000
                self.points -= 10

        for monster in self.monsters[:]:  # Using slices to don't have mutable problems.
            monster.persecute(self.robot.rect)
            if monster.rect.colliderect(self.robot.rect):
                # If you touch the monster without the sword you get a game over.
                if not self.have_sword:
                    self.game_active = False
                    self.game_over = True
                else:
                    # If you have the sword and touch the monster you kill them.
                    self.monsters.remove(monster)

        # After killing the monsters touching the portal make you win.
        if len(self.monsters) == 0:
            if self.door.rect.colliderect(self.robot.rect):
                self.game_active = False
                self.win = True

    def draw(self):  # Function that render all models in the game.

        # Fill the window with a green colour.
        self.window.fill((100, 150, 100))

        # Render the robot.
        self.robot.draw(self.window)

        # Render the coins.
        for coin in self.coins:
            coin.draw(self.window)

        # Render the sword.
        if self.points >= 10 and not self.have_sword:
            self.sword.draw(self.window)

        # Render the monsters.
        for monster in self.monsters:
            monster.draw(self.window)

        # Render the door.
        if len(self.monsters) == 0:
            self.door.draw(self.window)

        # Render of the puntuation Coins and Enemies remaining.
        points_text = self.font.render(f"Coins: {self.points}", True, (255, 255, 255))
        enemies_text = self.font.render(
            f"Enemies: {len(self.monsters)}", True, (255, 255, 255)
        )
        self.window.blit(points_text, (10, 10))
        self.window.blit(enemies_text, (self.width - 150, 10))

        # If the game is not active show the messages YOU WIN! or GAME OVER! and give you the option to restart.
        if not self.game_active:
            font = pygame.font.SysFont("Arial", 36)
            if self.win:
                msg = font.render("YOU WIN! Press R to Restart", True, (0, 255, 0))
            elif self.game_over:
                msg = font.render("GAME OVER! Press R to Restart", True, (255, 0, 0))

            # Make the msg in the middle of the window.
            if self.win or self.game_over:
                text_rect = msg.get_rect(center=(self.width // 2, self.height // 2))
                self.window.blit(msg, text_rect)

        # Update the window.
        pygame.display.flip()

    def read_events(self):  # Function that read all the inputs of the player.

        # Read all events in the game.
        for event in pygame.event.get():
            # Quit the game if you close the window.
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Detect the keys pressed by the player.
            if event.type == pygame.KEYDOWN:
                # If the 'R' key is pressed, start a new game
                if not self.game_active and event.key == pygame.K_r:
                    self.new_game()

    def execute(self):  # Function that execute the program.

        # Do a loop: Read -> Update -> Draw.
        while True:
            self.read_events()
            self.update()
            self.draw()

            # Make the game run at 60 clock ticks.
            self.clock.tick(60)


if __name__ == "__main__":  # Game execution.
    game = Game()
    game.execute()
