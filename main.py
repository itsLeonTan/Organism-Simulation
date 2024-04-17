import pygame
import time
import random
import math

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
        self.radius_color = (0, 255, 0)  # Red color for the radius

    def move_with_angle(self, screen_width, screen_height, food_list):
        self.closest_food = None  # Reset closest_food
        min_distance = float("inf")
        for food in food_list:
            distance = math.sqrt((self.rect.x - food.rect.x)**2 + (self.rect.y - food.rect.y)**2)
            if distance < min_distance and distance <= self.search_radius:
                min_distance = distance
                self.closest_food = food

        if self.closest_food:
            # Calculate angle towards closest food
            dx = self.closest_food.rect.x - self.rect.x
            dy = self.closest_food.rect.y - self.rect.y
            self.angle = math.degrees(math.atan2(dy, dx))

        rad_angle = math.radians(self.angle)
        dx = self.step_size * math.cos(rad_angle)
        dy = self.step_size * math.sin(rad_angle)
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if 0 <= new_x <= screen_width - 20 and 0 <= new_y <= screen_height - 20:
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            # Change direction if reaching screen boundaries
            self.angle = random.randint(0, 360)  # Change to a new random angle

    def draw_radius(self, screen):
        pygame.draw.circle(screen, self.radius_color, (self.rect.x + 10, self.rect.y + 10), self.search_radius, 1)

def generate_organism(screen_width, screen_height):
    organism_list = []
    num_organism = 1
    for _ in range(num_organism):
        organism_list.append(Organism(screen_width, screen_height))
    return organism_list

class Food:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("food.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 10)
        self.rect.y = random.randint(0, screen_height - 10)

def generate_food(screen_width, screen_height):
    food_list = []
    num_food = 20
    for _ in range(num_food):
        food_list.append(Food(screen_width, screen_height))
    return food_list

def main():
    pygame.init()
    pygame.display.set_caption("minimal program")
    screen_width = 760
    screen_height = 570
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((0, 0, 0))
    running = True

    food_list = generate_food(screen_width, screen_height)
    organism_list = generate_organism(screen_width, screen_height)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for organism in organism_list:
            screen.blit(organism.image, organism.rect)
            organism.move_with_angle(screen_width, screen_height, food_list)  # Move organism towards food
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
