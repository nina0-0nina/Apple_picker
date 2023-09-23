# imports
########################################################################
import random
import pygame
from operator import itemgetter
########################################################################

# Set up the game window
########################################################################
pygame.init()
screen_width = 1024
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Apple Picker")
########################################################################

# Define some constants
########################################################################
# Wall laser
wall_laser_y = 150

good_apple_color = (0, 255, 0)
bad_apple_color = (255, 0, 0)
lever_color = (0, 0, 255)
laser_color = (200, 0, 0)
apple_radius = 20
lever_width = 100
lever_height = 10
apple_speed = 5
game_duration = 120 # in seconds

max_lever_displacement = 20

# Define some variables
########################################################################
good_apple_count = 0
bad_apple_count = 0

bad_apple_value = -3
good_apple_value = 1
score = 0
game_start_time = pygame.time.get_ticks()
########################################################################

# Define some functions
########################################################################
def draw_laser_scan(x_pos, obstacle_height=0):
    pygame.draw.rect(screen, laser_color, (x_pos + lever_width/2, obstacle_height, 1, screen_height))  

def draw_side_laser_sensor(y_pos):
    pygame.draw.rect(screen, lever_color, (0, y_pos - 5, 5, 10))

def draw_lever(x_pos):
    pygame.draw.rect(screen, lever_color, (x_pos, screen_height - lever_height, lever_width, lever_height))

def draw_apple(x_pos, y_pos, color):
    pygame.draw.circle(screen, color, (x_pos, y_pos), apple_radius)

def generate_apple():
    x_pos = random.randint(apple_radius, screen_width - apple_radius)
    y_pos = 0
    if random.random() < 0.2: # 20% chance of generating a bad apple
        color = bad_apple_color
    else:
        color = good_apple_color
    return (x_pos, y_pos, color)

def detect_collision(apple, lever_pos):
    x_pos, y_pos, color = apple
    if y_pos + apple_radius >= screen_height - lever_height and x_pos >= lever_pos and x_pos <= lever_pos + lever_width:
        return True
    else:
        return False


def find_apple_in_laser_range(x_pos, apples):
    closest_apple = None
    lever_center = x_pos + lever_width/2
    for apple in apples:
      # Choose closest in height
      if abs(apple[0] - lever_center) < apple_radius:
        closest_apple = max(closest_apple, apple, key=lambda a: 0 if a is None else a[1]) 
        
    return closest_apple

def draw_wall_laser_scan(y_pos, obstacle_dist=screen_width):
    pygame.draw.rect(screen, laser_color, (0, y_pos, obstacle_dist, 1))
         
def find_apple_in_side_laser_range(y_pos, apples):
    closest_apple = None
    side_laser_center = y_pos
    for apple in apples:
      # Choose closest in height
      if abs(apple[1] - side_laser_center) < apple_radius:
        closest_apple = max(closest_apple, apple, key=lambda a: 0 if a is None else a[1]) 
        
    return closest_apple

########################################################################

# World model
########################################################################
class WorldModel:
    def __init__(self):
        self.apples = []

    def Division1(self,lever_pos):
        if lever_pos >= 0 and lever_pos <= 170:
            print('partição1')
            division = 1
            return division
        else:
            return False
        
    def Division2(self, lever_pos):
        if lever_pos >= 171 and lever_pos <= 341:
            print('partição2')
            division = 2
            return division
        else:
            return False

    def Division3(self, lever_pos):
        if lever_pos >= 342 and lever_pos <= 512:
            print('partição3')
            division = 3
            return division
        else:
            return False

    def Division4(self, lever_pos):
        if lever_pos >= 513 and lever_pos <= 683:
            print('partição4')
            division = 4
            return division
        else:
            return False

    def Division5(self, lever_pos):
        if lever_pos >= 684 and lever_pos <=854:
            print('partição5')
            division = 5
            return division
        else:
            return False

    def Division6(self, lever_pos):
        if lever_pos >= 855 and lever_pos <=1024:
            print('partição6')
            division = 6
            return division
        else:
            return False
        
    def which_division(self, lever_pos):
        if self.Division1(lever_pos) == 1:
            division = 1
            return division
        elif self.Division2(lever_pos) == 2:
            division = 2
            return division
        elif self.Division3(lever_pos) == 3:
            division = 3
            return division
        elif self.Division4(lever_pos) == 4:
            division = 4
            return division
        elif self.Division5(lever_pos) == 5:
            division = 5
            return division
        elif self.Division6(lever_pos) == 6:
            division = 6
            return division

    def updatelist(self, apples):
        self.apples = apples

    def sortlist(self):
        if not self.apples:
            return None, None
        
        sorted_ap = sorted(self.apples, key=itemgetter(0))
        return sorted_ap 
  
    def closestapple(self):
        sorted_apples = self.sortlist()
        if not sorted_apples:
            return None, None
        
        closest_apple = sorted_apples[0]
        if closest_apple is None:
            return None, None
        
        apple_x = closest_apple[0]
        color = closest_apple[2]
        return apple_x, color

########################################################################

# Agent
########################################################################
class Agent:
    def __init__(self, wm, max_lever_displacement, arena_width):
        # modelo de mundo
        self.worldmodel = wm
        # O maximo de unidades que voce pode se mover na decisao
        self.max_lever_displacement = max_lever_displacement 
        # Tamanho da arena
        self.arena_width = arena_width
        # Speed
        self.lever_posicao = 1
  
    def lever_movimento(self, pos):
        # Nova posicao
        new_pos = pos + (self.lever_posicao * self.max_lever_displacement)
        # Lever ficar indo e voltando na tela
        if new_pos >= (self.arena_width - lever_width) or new_pos <= 0:
            self.lever_posicao *= -1 # Inverte a direção
        return new_pos

    def bad_apple_division(self, lever_pos, apple_x):
        division = wm.which_division(lever_pos)
        apple_division = wm.which_division(apple_x)
        if apple_division == division:
            return True


    def bad_apple_detour(self, lever_pos, apple_x):
        division = wm.which_division(lever_pos)
        apple_division = wm.which_division(apple_x)
        if apple_division == division:
            return min(lever_pos + self.max_lever_displacement / 2, self.arena_width - lever_width)

    def decision(self, lever_pos, laser_scan):
        apple_x, color = wm.closestapple()
        if apple_x is not None and color is not None:
            # se é vermelha e está no mesmo quadrante
            if color == bad_apple_color:
                # se a posição da maçã vermelha for menor que a posição do lever + metade da largura do lever
                if self.bad_apple_division(lever_pos, apple_x):
                # if apple_x < lever_pos + lever_width/2:
                    #encontrou maçã vermelha 
                    print("vermelha")

                    return self.bad_apple_detour(lever_pos, apple_x)
                    #return min(lever_pos + self.max_lever_displacement / 2, self.arena_width - lever_width)
                    
            elif color == good_apple_color:
                # Move towards the good apple if it's above the lever
                if apple_x > lever_pos + lever_width / 2:
                    return min(lever_pos + self.max_lever_displacement, self.arena_width - lever_width)
                # Move towards the good apple if it's below the lever
                else:
                    return max(lever_pos - self.max_lever_displacement, 0)

            #     else:
            #         return max(lever_pos - self.max_lever_displacement, 0)
            #         # return min(lever_pos - self.max_lever_displacement, 20)
            # elif color == good_apple_color: 
            #         if apple_x > lever_pos + lever_width/2:
            #             print("verde")
            #             return min(lever_pos + self.max_lever_displacement, self.arena_width - lever_width)
            #             # return min(lever_pos + self.max_lever_displacement, self.arena_width - lever_width)
            #         else:
            #             return max(lever_pos - self.max_lever_displacement, 0)
            #             # return max(lever_pos - self.max_lever_displacement, 0)
        # else:
        #     return self.lever_movimento(lever_pos)
        return self.lever_movimento(lever_pos)
########################################################################      

# Main game loop
########################################################################
wm = WorldModel()
agent = Agent(wm, max_lever_displacement, screen_width)

running = True
apples = []
lever_pos = screen_width / 2
closest_apple = None
closest_s_apple = None
decisions_count = 0
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    closest_apple = find_apple_in_side_laser_range(lever_pos, apples)
    # closest_apple = find_apple_in_laser_range(lever_pos, apples)
 
    closest_apple_distance = None
    if closest_apple is not None:
      closest_apple_distance = {
      	"distance": closest_apple[0] - apple_radius,
      	"color": "red" if closest_apple[2] == (255, 0, 0) else "green"
      }    
        
    #print(f"{closest_apple_distance=} with data {closest_apple=}")  
    desired_lever_pos = agent.decision(lever_pos, closest_apple_distance)
    if abs(lever_pos - desired_lever_pos) > lever_width/2 + max_lever_displacement:
      print("Max lever displacement exceeded")
    else: 
      lever_pos = desired_lever_pos
    
    wm.updatelist(apples)
      
    # Draw the lever    
    draw_lever(lever_pos)
    draw_laser_scan(lever_pos, 0 if closest_apple is None else closest_apple[1])
    draw_wall_laser_scan(wall_laser_y,  screen_width if closest_s_apple is None else closest_s_apple[0])
    draw_side_laser_sensor(wall_laser_y)
    
    # Generate apples
    if random.random() < 0.05: # 5% chance of generating an apple in each frame
        apple = generate_apple()
        if apple[2] == good_apple_color:
            good_apple_count += 1
        else:
            bad_apple_count += 1
        apples.append(apple)

    # Move apples and detect collisions
    novel_apples = []
    for idx,apple in enumerate(apples):
        x_pos, y_pos, color = apple
        y_pos += apple_speed
        if detect_collision(apple, lever_pos):
            if color == good_apple_color:
                score += good_apple_value
            else:
                score += bad_apple_value
        elif y_pos >= screen_height: 
            pass
        else:
            novel_apples.append((x_pos, y_pos, color))
            draw_apple(x_pos, y_pos, color)
    apples = novel_apples
            
    # Draw the score
    score_text = "Score: " + str(score)
    font = pygame.font.SysFont("Arial", 32)
    score_surface = font.render(score_text, True, (0, 0, 0))
    screen.blit(score_surface, (10, 10))

    # Check if the game is over
    elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000
    #if elapsed_time >= game_duration:
    #    running = False
    
    decisions_count += 1  
    if decisions_count >= 3441: # Aproximadamente dois minutos
      running = False

    time_surface = font.render("Time (s): " + str(elapsed_time), True, (0, 0, 0))
    screen.blit(time_surface, (200, 10))

    # Update the display
    pygame.display.update()
    pygame.time.wait(int(1000/30))
    #pygame.time.wait(500)
########################################################################

# Finished game - score
########################################################################
print(f"Number of decisions {decisions_count}")

# Show the final score
final_score_text = "Final score: " + str(score)
print(f"score: {score}")
font = pygame.font.SysFont("Arial", 64)
final_score_surface = font.render(final_score_text, True, (0, 0, 0))
final_score_rect = final_score_surface.get_rect(center=(screen_width/2, screen_height/2))
screen.blit(final_score_surface, final_score_rect)
pygame.display.update()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Quit the game
pygame.quit()    
########################################################################