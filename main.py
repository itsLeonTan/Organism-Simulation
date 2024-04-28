import neat.population
import pygame
import random
import math
import os
import neat

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
    else:
        return '-'

def normalize_angle(angle):
    if angle < 0:
        angle += 360
    elif angle >= 360:
        angle -= 360
    return angle

class Organism:
    def __init__(self, screen_width, screen_height):
        #Colour
        self.r = random.randint(99, 255)
        self.g = random.randint(99, 255)
        self.b = random.randint(99, 255)
        self.radius_color = (self.r, self.g, self.b)
        #Properties
        self.radius = 50  # Radius of the circular organism
        self.rect = pygame.Rect(random.randint(0, screen_width - self.radius*2), random.randint(0, screen_height - self.radius*2), self.radius*2, self.radius*2)
        self.name = map_number_to_letter(self.r) + map_number_to_letter(self.g) + map_number_to_letter(self.b)
        self.tail_length = 50  # Number of segments in the tail
        self.tail_segments = []  # List to store previous positions for the tail
        #Movement
        self.angle = random.randint(0, 360)  # Initial random angle
        self.turn = 0 # (-1: left) (0: center) (1: right)
        self.step_size = 10
        #Senses
        self.search_radius = 250  # Radius within which to search for food
        self.closest_food = None
        self.closest_organism = None
        self.counter = 0
        self.turn_delay = 10
        self.food_consumed = 0  # Track food consumed

    def movement(self, screen_width, screen_height, food_list, organism_list):
        self.tail_segments.append((self.rect.x + self.radius, self.rect.y + self.radius))
        if len(self.tail_segments) > self.tail_length:
            self.tail_segments.pop(0)  # Limit tail length

        global dif, food_min_distance
        self.closest_food = None # Reset
        self.closest_organism = None # Reset
        food_min_distance = float("inf")
        organism_min_distance = float("inf")

        for organism in organism_list:
            if organism != self:
                distance = math.sqrt((self.rect.x - organism.rect.x) ** 2 + (self.rect.y - organism.rect.y) ** 2)
                if distance < organism_min_distance and distance <=self.radius*2:
                    organism_min_distance = distance
                    self.closest_organism = organism

        if self.closest_organism == None:
            for food in food_list:
                distance = math.sqrt((self.rect.x - food.rect.x) ** 2 + (self.rect.y - food.rect.y) ** 2)
                if distance < food_min_distance and distance <= self.search_radius:
                    food_min_distance = distance
                    self.closest_food = food

        if self.closest_food != None:
            # Calculate angle towards closest food
            dx = self.closest_food.rect.x - self.rect.x
            dy = self.closest_food.rect.y - self.rect.y
            dif = normalize_angle(math.degrees(math.atan2(dy, dx))) - self.angle
            '''
            if dif < 0 and abs(dif) < 90:
                self.turn = -1
            elif dif > 0 and abs(dif) < 90:
                self.turn = 1 
            '''
        else:
            dif = 0
        
        if self.closest_organism != None:
            # Calculate angle towards closest organism
            dx = self.rect.x - self.closest_organism.rect.x
            dy = self.rect.y - self.closest_organism.rect.y
            self.angle = math.degrees(math.atan2(dy, dx))

        self.angle = normalize_angle(self.angle)

        rad_angle = math.radians(self.angle)
        dx = self.step_size * math.cos(rad_angle)
        dy = self.step_size * math.sin(rad_angle)
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        if 0 <= new_x <= screen_width - self.rect.width:
            self.rect.x = new_x
        else:
            self.angle = 180 - self.angle
        if 0 <= new_y <= screen_height - self.rect.height:
            self.rect.y = new_y
        else:
            self.angle = 360 - self.angle

        if self.turn == -1:
            self.angle -= 2
        elif self.turn == 1:
            self.angle += 2
        
        '''
        if self.counter == self.turn_delay:
            self.turn = random.randint(-1,1)
            self.counter = 0
            self.turn_delay = random.randint(50, 100)
        elif self.closest_food == None and self.closest_organism == None:
            self.counter += 1
        '''

    def draw(self, screen):
        for i, segment in enumerate(self.tail_segments):
            size = i
            pygame.draw.circle(screen, self.radius_color, segment, size) # draw tail
        pygame.draw.arc(screen, (255, 255, 255), self.rect.inflate(self.search_radius + 200, self.search_radius + 200), math.radians(-self.angle-45), math.radians(-self.angle+45), 5)  # draw search radius (Search angle at 90d)
        pygame.draw.circle(screen, self.radius_color, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)  # Draw organism

        if self.closest_food != None:
            pygame.draw.line(screen, (255, 255, 255), (self.rect.x + self.radius, self.rect.y + self.radius), (self.closest_food.rect.x + self.closest_food.radius, self.closest_food.rect.y + self.closest_food.radius), 5)

class Food:
    def __init__(self, screen_width, screen_height):
        self.radius = 25  # Radius of the circular food
        self.rect = pygame.Rect(random.randint(0, screen_width - self.radius * 2),
                                random.randint(0, screen_height - self.radius * 2), self.radius * 2, self.radius * 2)
        self.radius_color = (255, 0, 0)

def overlap_check(lst, var):
    for existing in lst:
        if var.rect.colliderect(existing):
            return True
    return False

# function for testing
def generate_organism(organism_list, screen_width, screen_height):
    num_organism = 10
    for _ in range(num_organism - len(organism_list)):
        new_organism = Organism(screen_width, screen_height)
        if overlap_check(organism_list, new_organism) == True:
            pass
        else:
            organism_list.append(new_organism)

def generate_food(food_list, screen_width, screen_height):
    num_food = 50

    for _ in range(num_food - len(food_list)):
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

def main(genomes, config):
    nets = []
    ge = []
    organism_list = [] # clear the list

    pygame.init()
    pygame.display.set_caption("Organism Simulation")
    base_screen_width = 960  # Original window size
    base_screen_height = 600  # Original window size
    scale_factor = 6  # Scale factor for pixel density

    screen = pygame.display.set_mode((base_screen_width, base_screen_height))  # Original window size
    habitat_surface = pygame.Surface((base_screen_width * scale_factor, base_screen_height * scale_factor))
    habitat_surface.set_colorkey((0, 0, 0))  # Set transparent color
    font = pygame.font.Font(None, 24)

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

        new_organism = Organism(base_screen_width * scale_factor, base_screen_height * scale_factor)
        if overlap_check(organism_list, new_organism) == True:
            pass
        else:
            organism_list.append(new_organism)

    for _ in range(5000):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        habitat_surface.fill((0, 0, 0))  # Clear the habitat surface

        generate_food(food_list, base_screen_width * scale_factor, base_screen_height * scale_factor)

        for x, organism in enumerate(organism_list):
            organism.movement(base_screen_width * scale_factor, base_screen_height * scale_factor, food_list, organism_list)
            organism.draw(habitat_surface)

            output = nets[x].activate((dif, food_min_distance))
            if output[0] > 0.5:
                organism.turn = -1
            if output[1] > 0.5:
                organism.turn = 0
            if output[2] > 0.5:
                organism.turn = 1

        for food in food_list:
            pygame.draw.circle(habitat_surface, food.radius_color, (food.rect.x + food.radius, food.rect.y + food.radius), food.radius)

        scaled_surface = pygame.transform.scale(habitat_surface, (base_screen_width, base_screen_height))

        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(scaled_surface, (0, 0))  # Draw the scaled surface on the screen

        render_leaderboard(screen, font, organism_list)

        for food in food_list:
            for x, organism in enumerate(organism_list):
                if organism.rect.colliderect(food.rect):
                    food_list.remove(food)
                    organism.food_consumed += 1  # Increment food consumed
                    ge[x].fitness += 1
                    break # to prevent food from being consumed twice
        pygame.display.flip()
        pygame.time.delay(10)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_config.txt")
    run(config_path)


#=========
def main_test():
    pygame.init()
    pygame.display.set_caption("Organism Simulation")
    base_screen_width = 960  # Original window size
    base_screen_height = 600  # Original window size
    scale_factor = 6  # Scale factor for pixel density

    screen = pygame.display.set_mode((base_screen_width, base_screen_height))  # Original window size
    habitat_surface = pygame.Surface((base_screen_width * scale_factor, base_screen_height * scale_factor))
    habitat_surface.set_colorkey((0, 0, 0))  # Set transparent color

    generate_organism(organism_list, base_screen_width * scale_factor, base_screen_height * scale_factor)

    font = pygame.font.Font(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        habitat_surface.fill((0, 0, 0))  # Clear the habitat surface

        generate_food(food_list, base_screen_width * scale_factor, base_screen_height * scale_factor)

        for organism in organism_list:
            organism.movement(base_screen_width * scale_factor, base_screen_height * scale_factor, food_list, organism_list)
            organism.draw(habitat_surface)

        for food in food_list:
            pygame.draw.circle(habitat_surface, food.radius_color, (food.rect.x + food.radius, food.rect.y + food.radius), food.radius)

        scaled_surface = pygame.transform.scale(habitat_surface, (base_screen_width, base_screen_height))

        screen.fill((0, 0, 0))  # Clear the screen
        screen.blit(scaled_surface, (0, 0))  # Draw the scaled surface on the screen

        render_leaderboard(screen, font, organism_list)

        for food in food_list:
            for organism in organism_list:
                if organism.rect.colliderect(food.rect):
                    food_list.remove(food)
                    organism.food_consumed += 1  # Increment food consumed
                    break # to prevent food from being consumed twice
        pygame.display.flip()
        pygame.time.delay(10)