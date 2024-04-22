import pygame
import time
import random
import math

food_list = []
organism_list = []

def map_number_to_letter(number):
    if 100 <= number <= 105:
        return 'A'
    elif 106 <= number <= 111:
        return 'B'
    elif 112 <= number <= 117:
        return 'C'
    elif 118 <= number <= 123:
        return 'D'
    elif 124 <= number <= 129:
        return 'E'
    elif 130 <= number <= 135:
        return 'F'
    elif 136 <= number <= 141:
        return 'G'
    elif 142 <= number <= 147:
        return 'H'
    elif 148 <= number <= 153:
        return 'I'
    elif 154 <= number <= 159:
        return 'J'
    elif 160 <= number <= 165:
        return 'K'
    elif 166 <= number <= 171:
        return 'L'
    elif 172 <= number <= 177:
        return 'M'
    elif 178 <= number <= 183:
        return 'N'
    elif 184 <= number <= 189:
        return 'O'
    elif 190 <= number <= 195:
        return 'P'
    elif 196 <= number <= 201:
        return 'Q'
    elif 202 <= number <= 207:
        return 'R'
    elif 208 <= number <= 213:
        return 'S'
    elif 214 <= number <= 219:
        return 'T'
    elif 220 <= number <= 225:
        return 'U'
    elif 226 <= number <= 231:
        return 'V'
    elif 232 <= number <= 237:
        return 'W'
    elif 238 <= number <= 243:
        return 'X'
    elif 244 <= number <= 249:
        return 'Y'
    elif 250 <= number <= 255:
        return 'Z'


class Organism:
    def __init__(self, screen_width, screen_height):
        self.radius = 10  # Radius of the circular organism
        self.rect = pygame.Rect(random.randint(0, screen_width - self.radius*2), random.randint(0, screen_height - self.radius*2), self.radius*2, self.radius*2)
        self.angle = random.randint(0, 360)  # Initial random angle
        self.step_size = 1
        self.search_radius = 50  # Radius within which to search for food
        self.closest_food = None
        self.closest_organism = None
        self.counter = 0
        self.turn_delay = 10
        self.food_consumed = 0  # Track food consumed

        self.r = random.randint(99,255)
        self.g = random.randint(99,255)
        self.b = random.randint(99,255)
        self.radius_color = (self.r, self.g, self.b)

        self.name = map_number_to_letter(self.r)+map_number_to_letter(self.g)+map_number_to_letter(self.b)

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
        pygame.draw.circle(screen, self.radius_color, (self.rect.x + self.radius, self.rect.y + self.radius), self.search_radius, 1)

class Food:
    def __init__(self, screen_width, screen_height):
        self.radius = 5  # Radius of the circular food
        self.rect = pygame.Rect(random.randint(0, screen_width - self.radius*2), random.randint(0, screen_height - self.radius*2), self.radius*2, self.radius*2)
        self.radius_color = (255,0,0)

def overlap_check(lst, var):
    for existing in lst:
        if var.rect.colliderect(existing):
            return True
    return False

def generate_organism(organism_list, screen_width, screen_height):
    num_organism = 3
    for _ in range(num_organism-len(organism_list)):
        new_organism = Organism(screen_width,screen_height)
        if overlap_check(organism_list, new_organism) == True:
            pass
        else:
            organism_list.append(new_organism)

def generate_food(food_list, screen_width, screen_height):
    num_food = 50

    for _ in range(num_food-len(food_list)):
        new_food = Food(screen_width, screen_height)
        if overlap_check(food_list, new_food) == True:
            pass
        else:
            food_list.append(new_food)

def render_leaderboard(screen, font, organism_list):
    sorted_organisms = sorted(organism_list, key=lambda x: x.food_consumed, reverse=True)
    for i, organism in enumerate(sorted_organisms):
        leaderboard_entry = font.render(f"{organism.name}: {organism.food_consumed} food", True, (255, 255, 255))
        screen.blit(leaderboard_entry, (screen.get_width() - 150, 50 + i * 30))

def main():
    pygame.init()
    pygame.display.set_caption("Organism Simulation")
    screen_width = 760
    screen_height = 570
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((0, 0, 0))
    running = True

    generate_organism(organism_list, screen_width, screen_height)

    font = pygame.font.Font(None, 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        generate_food(food_list, screen_width, screen_height)

        for organism in organism_list:
            pygame.draw.circle(screen, organism.radius_color, (organism.rect.x + organism.radius, organism.rect.y + organism.radius), organism.radius)  # Draw circular organism
            organism.movement(screen_width, screen_height, food_list, organism_list)  # Move organism towards food
            organism.draw_radius(screen)  # Draw search radius around organism

        for food in food_list:
            pygame.draw.circle(screen, food.radius_color, (food.rect.x + food.radius, food.rect.y + food.radius), food.radius)  # Draw circular food

        render_leaderboard(screen, font, organism_list)  # Render leaderboard

        for food in food_list:
            for organism in organism_list:
                if organism.rect.colliderect(food.rect):
                    food_list.remove(food)
                    organism.food_consumed += 1  # Increment food consumed
        pygame.display.flip()
        time.sleep(0.01)

if __name__ == "__main__":
    main()
