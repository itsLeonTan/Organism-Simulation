import pygame
import time
import random
import math

food_list = []
organism_list = []


def overlap_check(lst, var):
    for existing in lst:
        if var.rect.colliderect(existing):
            return True
    return False

class Organism:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("organism.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 20)
        self.rect.y = random.randint(0, screen_height - 20)
        self.angle = random.randint(0, 360)  # Initial random angle
        self.step_size = 1
        self.search_radius = 50  # Radius within which to search for food
        self.closest_food = None
        self.closest_organism = None
        self.radius_color = (0, 255, 0)  
        self.counter = 0
        self.turn_delay = 10

    def movement(self, screen_width, screen_height, food_list, organism_list):
        self.closest_food = None  # Reset
        self.closest_organism = None # Reset
        min_distance = float("inf")

        for organism in organism_list:
            if organism != self:
                distance = math.sqrt((self.rect.x - organism.rect.x)**2 + (self.rect.y - organism.rect.y)**2)
                if distance < min_distance and distance <= self.search_radius:
                    min_distance = distance
                    self.closest_organism = organism

        if self.closest_organism == None:
            for food in food_list:
                distance = math.sqrt((self.rect.x - food.rect.x)**2 + (self.rect.y - food.rect.y)**2)
                if distance < min_distance and distance <= self.search_radius:
                    min_distance = distance
                    self.closest_food = food

        if self.closest_food != None:
            # Calculate angle towards closest food
            dx = self.closest_food.rect.x - self.rect.x
            dy = self.closest_food.rect.y - self.rect.y
            self.angle = math.degrees(math.atan2(dy, dx))
        
        elif self.closest_organism != None:
            # Calculate angle towards closest food
            dx = self.rect.x - self.closest_organism.rect.x
            dy = self.rect.y - self.closest_organism.rect.y
            self.angle = math.degrees(math.atan2(dy, dx))

        rad_angle = math.radians(self.angle)
        dx = self.step_size * math.cos(rad_angle)
        dy = self.step_size * math.sin(rad_angle)
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if 0 <= new_x <= screen_width-self.rect.width:
            self.rect.x = new_x
        else:
            self.angle = 180 - self.angle
        if 0 <= new_y <= screen_height-self.rect.height:
            self.rect.y = new_y
        else:
            self.angle = 360 - self.angle

        if self.counter < self.turn_delay:
            self.counter += 1
        elif self.counter == self.turn_delay:
            self.angle += random.randint(-180,180)
            self.counter = 0
            self.turn_delay = random.randint(50,200)


    def draw_radius(self, screen):
        pygame.draw.circle(screen, self.radius_color, (self.rect.x + 10, self.rect.y + 10), self.search_radius, 1)

def generate_organism(organism_list, screen_width, screen_height):
    num_organism = 10
    for _ in range(num_organism-len(organism_list)):
        new_organism = Organism(screen_width,screen_height)
        if overlap_check(organism_list, new_organism) == True:
            pass
        else:
            organism_list.append(Organism(screen_width, screen_height))

class Food:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("food.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 10)
        self.rect.y = random.randint(0, screen_height - 10)

def generate_food(food_list, screen_width, screen_height):
    num_food = 50

    for _ in range(num_food-len(food_list)):
        new_food = Food(screen_width, screen_height)
        if overlap_check(food_list, new_food) == True:
            pass
        else:
            food_list.append(new_food)

def main():
    pygame.init()
    pygame.display.set_caption("Organism Simulation")
    screen_width = 760
    screen_height = 570
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((0, 0, 0))
    running = True

    generate_organism(organism_list, screen_width, screen_height)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        generate_food(food_list, screen_width, screen_height)

        for organism in organism_list:
            screen.blit(organism.image, organism.rect)
            organism.movement(screen_width, screen_height, food_list, organism_list)  # Move organism towards food
            organism.draw_radius(screen)  # Draw search radius around organism

        for food in food_list:
            screen.blit(food.image, food.rect)

        for food in food_list:
            for organism in organism_list:
                if organism.rect.colliderect(food.rect):
                    food_list.remove(food)
                    # You can add score increment or other actions here


        pygame.display.flip()
        time.sleep(0.01)

if __name__ == "__main__":
    main()
