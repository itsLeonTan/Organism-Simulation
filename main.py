import neat.population
import pygame
import random
import math
import os
import neat
import string

pygame.init()
pygame.display.set_caption("Organism Simulation")
font = pygame.font.Font(None, 24)
base_screen_width = 960  # Original window size
base_screen_height = 600  # Original window size
scale_factor = 3  # Scale factor for pixel density
habitat_screen_width = base_screen_width * scale_factor
habitat_screen_height = base_screen_height * scale_factor

screen = pygame.display.set_mode((base_screen_width, base_screen_height))  # Original window size
habitat_surface = pygame.Surface((habitat_screen_width, habitat_screen_height))
habitat_surface.set_colorkey((0, 0, 0))  # Set transparent color

toggle = [True, True, True] # 0:Leaderboard 1:FOV 2:LOS
alphabet = list(string.ascii_uppercase)
food_list = []
organism_list = []
gen_count = -1

menu_img = pygame.image.load("menu_button.png")
menu_img = pygame.transform.scale(menu_img, (30, 30))
menu = pygame.Rect(10, 10, 30, 30)

def map_number_to_letter(num):
    num -= 100
    num //= 6
    return alphabet[num]

def normalize_angle(angle):
    return angle % 360

class Organism:
    def __init__(self):
        #Colour
        self.r = random.randint(100, 255)
        self.g = random.randint(100, 255)
        self.b = random.randint(100, 255)
        self.radius_color = (self.r, self.g, self.b)
        #Properties
        self.radius = 20  # Radius of the circular organism
        self.rect = pygame.Rect(random.randint(0, habitat_screen_width - self.radius*2), (habitat_screen_height/2 - self.radius), self.radius*2, self.radius*2)
        self.name = map_number_to_letter(self.r) + map_number_to_letter(self.g) + map_number_to_letter(self.b)
        self.tail_length = 10  # Number of segments in the tail
        self.tail_segments = []  # List to store previous positions for the tail
        #Movement
        self.angle = random.randint(0, 360)  # Initial random angle
        self.turn = 0 # (-1: left) (0: center) (1: right)
        self.step_size = 10
        self.move = False
        #Senses
        self.search_radius = 200  # Radius within which to search for food
        self.closest_food = None
        self.food_consumed = 0  # Track food consumed
        self.energy = 1000

    def movement(self):
        self.tail_segments.append((self.rect.x + self.radius, self.rect.y + self.radius))
        if len(self.tail_segments) > self.tail_length:
            self.tail_segments.pop(0)  # Limit tail length

        global dif, food_min_distance
        self.closest_food = None # Reset
        food_min_distance = self.search_radius

        for food in food_list:
            distance = math.hypot(self.rect.x - food.rect.x, self.rect.y - food.rect.y)
            if distance < food_min_distance and distance <= self.search_radius:
                food_min_distance = distance
                self.closest_food = food

        if self.closest_food != None:
            # Calculate angle towards closest food
            dx = self.closest_food.rect.x - self.rect.x
            dy = self.closest_food.rect.y - self.rect.y
            dif = normalize_angle(math.degrees(math.atan2(dy, dx))) - self.angle

            if dif > 180:
                dif = 360-dif
            elif dif < -180:
                dif = 360+dif

            if abs(dif) > 90:
                self.closest_food = None # Reset
                food_min_distance = self.search_radius
                dif = 0    
        else:
            dif = 0

        self.angle = normalize_angle(self.angle)

        rad_angle = math.radians(self.angle)
        dx = self.step_size * math.cos(rad_angle)
        dy = self.step_size * math.sin(rad_angle)
        if self.move == True:
            new_x = self.rect.x + dx
            new_y = self.rect.y + dy

            if 0 <= new_x <= habitat_screen_width - self.rect.width:
                self.rect.x = new_x
            else:
                self.angle = 180 - self.angle
            if 0 <= new_y <= habitat_screen_height - self.rect.height:
                self.rect.y = new_y
            else:
                self.angle = 360 - self.angle

        if self.turn == -1:
            self.angle -= 5
        elif self.turn == 1:
            self.angle += 5

    def draw(self):
        for i, segment in enumerate(self.tail_segments):
            size = i*2
            pygame.draw.circle(habitat_surface, self.radius_color, segment, size) # draw tail
        pygame.draw.circle(habitat_surface, self.radius_color, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)  # Draw organism

        if toggle[1] == True:
            pygame.draw.arc(habitat_surface, (255, 255, 255), self.rect.inflate(self.search_radius*1.5, self.search_radius*1.5), math.radians(-self.angle-90), math.radians(-self.angle+90), 5)  # draw search radius
        if self.closest_food != None and toggle[2] == True:
            pygame.draw.line(habitat_surface, (255, 255, 255), (self.rect.x + self.radius, self.rect.y + self.radius), (self.closest_food.rect.x + self.closest_food.radius, self.closest_food.rect.y + self.closest_food.radius), 5)

class Food:
    def __init__(self):
        self.radius = 10  # Radius of the circular food
        self.rect = pygame.Rect(random.randint(0, habitat_screen_width - self.radius * 2),
                                random.randint(0, habitat_screen_height - self.radius * 2), self.radius * 2, self.radius * 2)
        self.radius_color = (255, 0, 0)

    def draw(self):
        pygame.draw.circle(habitat_surface, self.radius_color, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)        

def generate_food():
    num_food = 50

    for _ in range(num_food - len(food_list)):
        new_food = Food()
        if pygame.Rect.collidelist(new_food.rect, food_list) != -1:
            pass
        else:
            food_list.append(new_food)

def render_leaderboard(screen):
    sorted_organisms = sorted(organism_list, key=lambda x: x.food_consumed, reverse=True)
    for i, organism in enumerate(sorted_organisms):
        leaderboard_entry = font.render(f"{organism.name}: {organism.food_consumed} food", True, (organism.r, organism.g, organism.b))
        screen.blit(leaderboard_entry, (screen.get_width() - 150, 50 + i * 30))

def menu_list():
    leaderboard = pygame.Surface((130, 30))
    if toggle[0] == True: leaderboard.fill('green')
    else: leaderboard.fill('red')
    text_L = font.render("Leaderboard", True, (0, 0, 0))
    leaderboard.blit(text_L, (10,7))

    field_of_vision = pygame.Surface((130, 30))
    if toggle[1] == True: field_of_vision.fill('green')
    else: field_of_vision.fill('red')
    text_FOV = font.render("Field of Vision", True, (0, 0, 0))
    field_of_vision.blit(text_FOV, (10,7))

    line_of_sight = pygame.Surface((130, 30))
    if toggle[2] == True: line_of_sight.fill('green')
    else: line_of_sight.fill('red')
    text_LOS = font.render("Line of Sight", True, (0, 0, 0))
    line_of_sight.blit(text_LOS, (10,7))

    while True:
        screen.blit(leaderboard, (50, 100))
        screen.blit(field_of_vision, (50, 150))
        screen.blit(line_of_sight, (50, 200))
        screen.blit(menu_img, menu)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if menu.collidepoint(x, y):
                    return
                elif leaderboard.get_rect(topleft=(50,100)).collidepoint(x, y):
                    if toggle[0] == True:
                        toggle[0] = False
                        leaderboard.fill('red')
                        leaderboard.blit(text_L, (10,7))
                    else:
                        toggle[0] = True
                        leaderboard.fill('green')
                        leaderboard.blit(text_L, (10,7))
                elif field_of_vision.get_rect(topleft=(50,150)).collidepoint(x, y):
                    if toggle[1] == True:
                        toggle[1] = False
                        field_of_vision.fill('red')
                        field_of_vision.blit(text_FOV, (10,7))
                    else:
                        toggle[1] = True
                        field_of_vision.fill('green')
                        field_of_vision.blit(text_FOV, (10,7))
                elif line_of_sight.get_rect(topleft=(50,200)).collidepoint(x, y):
                    if toggle[2] == True:
                        toggle[2] = False
                        line_of_sight.fill('red')
                        line_of_sight.blit(text_LOS, (10,7))
                    else:
                        toggle[2] = True
                        line_of_sight.fill('green')
                        line_of_sight.blit(text_LOS, (10,7))
                
def main(genomes, config):
    nets = []
    ge = []
    organism_list.clear()
    food_list.clear()
    global gen_count
    gen_count += 1

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

        new_organism = Organism()
        organism_list.append(new_organism)

    for _ in range(2000):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if menu.collidepoint(x, y):
                    menu_list()

        if len(organism_list) <= 5:
            continue

        habitat_surface.fill((0, 0, 0))  # Clear the habitat surface
        screen.fill((0, 0, 0))  # Clear the screen
        generate_food()

        for x, organism in enumerate(organism_list):
            organism.movement()
            organism.draw()

            output = nets[x].activate((dif/90, food_min_distance/organism.search_radius))
            if output[0] < -0.8:
                organism.turn = -1
            elif output[0] > 0.8:
                organism.turn = 1
            else:
                organism.turn = 0
            if output[1] > 0:
                organism.move = True
            else:
                organism.move = False

            pos = pygame.Rect.collidelist(organism.rect, food_list)
            if pos != -1:
                food_list.pop(pos)
                organism.food_consumed += 1
                #organism.energy += 200
                ge[x].fitness += 1
            
            '''
            organism.energy -= 1
            if organism.energy < 0 and len(organism_list)> 5:
                organism_list.pop(x)
                nets.pop(x)
                ge.pop(x)'''

        for food in food_list:
            food.draw()
        
        scaled_surface = pygame.transform.scale(habitat_surface, (base_screen_width, base_screen_height))
        screen.blit(scaled_surface, (0, 0))  # Draw the scaled surface on the screen
        
        if toggle[0] == True: render_leaderboard(screen)

        screen.blit(menu_img, menu)
        generation_text = font.render(f"Gen {gen_count}", True, (255, 255, 255))
        screen.blit(generation_text, (20, screen.get_height() - 30))
        pygame.display.flip()
        #pygame.time.delay(10)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,1000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_config.txt")
    run(config_path)