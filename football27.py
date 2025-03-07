import pygame
import random
import math
import time

# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("1v1 Football Game")

# Colors
WHITE = (255, 255, 255)
DARK_GREEN = (34, 139, 34)  # Original grass field color
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BALL_COLOR = (255, 255, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Field boundaries
FIELD_BORDER = 10
GOAL_WIDTH = 80
GOAL_HEIGHT = 100
PENALTY_WIDTH = 160
PENALTY_HEIGHT = 200

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self, keys, up, down, left, right):
        if keys[up] and self.rect.y > FIELD_BORDER:
            self.rect.y -= self.speed
        if keys[down] and self.rect.y < height - FIELD_BORDER - 40:
            self.rect.y += self.speed
        if keys[left] and self.rect.x > FIELD_BORDER:
            self.rect.x -= self.speed
        if keys[right] and self.rect.x < width - FIELD_BORDER - 40:
            self.rect.x += self.speed

# Ball class
# Ball class with circular shape and black outline
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = 10  # Radius of the ball
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(width // 2, height // 2))
        self.x_speed = 0
        self.y_speed = 0
        self.draw_ball()

    def draw_ball(self):
        """Draws the circular ball with a black outline."""
        self.image.fill((0, 0, 0, 0))  # Transparent background
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius)  # White fill
        pygame.draw.circle(self.image, BLACK, (self.radius, self.radius), self.radius, 2)  # Black outline

    def update(self):
        """Updates the ball position and keeps it inside boundaries."""
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.x_speed *= 0.98
        self.y_speed *= 0.98

        # Keep the ball inside boundaries
        if self.rect.x < FIELD_BORDER:
            self.rect.x = FIELD_BORDER
            self.x_speed = -self.x_speed
        if self.rect.x > width - FIELD_BORDER - self.radius * 2:
            self.rect.x = width - FIELD_BORDER - self.radius * 2
            self.x_speed = -self.x_speed
        if self.rect.y < FIELD_BORDER:
            self.rect.y = FIELD_BORDER
            self.y_speed = -self.y_speed
        if self.rect.y > height - FIELD_BORDER - self.radius * 2:
            self.rect.y = height - FIELD_BORDER - self.radius * 2
            self.y_speed = -self.y_speed



# AI movement
class AI(Player):
    def move_ai(self, ball):
        if abs(self.rect.x - ball.rect.x) > 30:
            if self.rect.x < ball.rect.x:
                self.rect.x += 4
            if self.rect.x > ball.rect.x:
                self.rect.x -= 4

        if abs(self.rect.y - ball.rect.y) > 30:
            if self.rect.y < ball.rect.y:
                self.rect.y += 4
            if self.rect.y > ball.rect.y:
                self.rect.y -= 4

        # AI Pass Ball Randomly
        if random.randint(0, 100) > 98:
            ball.x_speed = random.choice([-3, 3])
            ball.y_speed = random.choice([-3, 3])

# Draw field
def draw_field():
    screen.fill(DARK_GREEN)
    
     # Boundaries
    pygame.draw.rect(screen, WHITE, (FIELD_BORDER, FIELD_BORDER, width - 2 * FIELD_BORDER, height - 2 * FIELD_BORDER), 5)
    
    # Center line
    pygame.draw.line(screen, WHITE, (width // 2, FIELD_BORDER), (width // 2, height - FIELD_BORDER), 5)
    
    # Center circle
    pygame.draw.circle(screen, WHITE, (width // 2, height // 2), 60, 5)
    
    # Penalty areas
    pygame.draw.rect(screen, WHITE, (FIELD_BORDER, height // 2 - PENALTY_HEIGHT // 2, PENALTY_WIDTH, PENALTY_HEIGHT), 3)
    pygame.draw.rect(screen, WHITE, (width - FIELD_BORDER - PENALTY_WIDTH, height // 2 - PENALTY_HEIGHT // 2, PENALTY_WIDTH, PENALTY_HEIGHT), 3)
    
    # Goal areas
    pygame.draw.rect(screen, WHITE, (FIELD_BORDER, height // 2 - GOAL_HEIGHT // 2, GOAL_WIDTH, GOAL_HEIGHT), 3)
    pygame.draw.rect(screen, WHITE, (width - FIELD_BORDER - GOAL_WIDTH, height // 2 - GOAL_HEIGHT // 2, GOAL_WIDTH, GOAL_HEIGHT), 3)
    
    # Goals
    pygame.draw.rect(screen, BLACK, (FIELD_BORDER, height // 2 - GOAL_HEIGHT // 2, GOAL_WIDTH, GOAL_HEIGHT), 5)  # Left goal
    pygame.draw.rect(screen, BLACK, (width - FIELD_BORDER - GOAL_WIDTH, height // 2 - GOAL_HEIGHT // 2, GOAL_WIDTH, GOAL_HEIGHT), 5)  # Right goal
    
    # Penalty arcs# Penalty arcs (fixing their position and angle)
    pygame.draw.arc(screen, WHITE, (FIELD_BORDER + PENALTY_WIDTH - 50, height // 2 - 50, 100, 100), 1.5 * math.pi, 0.5 * math.pi, 3) 
    # Left penalty arc
    pygame.draw.arc(screen, WHITE, (width - FIELD_BORDER - PENALTY_WIDTH - 50, height // 2 - 50, 100, 100), 0.5 * math.pi, 1.5 * math.pi, 3) 
    # Right penalty arc
def show_winner(text):
    font = pygame.font.Font(None, 50)
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (width // 2 - 100, height // 2))
    pygame.display.flip()
    pygame.time.delay(2000)

def game_over_screen(winner):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text_surface = font.render(winner, True, WHITE)
    play_again = pygame.font.Font(None, 40).render("Press ENTER to Play Again", True, WHITE)
    quit_game = pygame.font.Font(None, 40).render("Press ESC to Quit", True, WHITE)
    screen.blit(text_surface, (width // 2 - 100, height // 2 - 50))
    screen.blit(play_again, (width // 2 - 160, height // 2 + 20))
    screen.blit(quit_game, (width // 2 - 120, height // 2 + 70))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Restart the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Game variables
def game_loop():
      running=True
  
  
      player = Player(200, height // 2, BLUE)
      ai = AI(600, height // 2, RED)
      ball = Ball()
      player_score, ai_score = 0, 0
      start_time = time.time()
        # Initialize the timer when the game starts

      while running:
          # Process events to prevent "Not Responding"
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                 running = False
                 pygame.quit()
                 exit()

          draw_field()
    
          keys = pygame.key.get_pressed()
    
    # Player movement
          player.move(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
    
    # AI movement
          ai.move_ai(ball)
    
    # Ball stealing and passing
          if keys[pygame.K_SPACE] and player.rect.colliderect(ball.rect):
              ball.x_speed = 4 if player.rect.x < ball.rect.x else -4
              ball.y_speed = 4 if player.rect.y < ball.rect.y else -4

          if keys[pygame.K_p]:
              ball.x_speed = 6 if player.rect.x < width // 2 else -6
              ball.y_speed = random.choice([-3, 3])
    
    # Goal detection
          if ball.rect.x <= FIELD_BORDER + GOAL_WIDTH and height // 3 < ball.rect.y < height // 3 + GOAL_HEIGHT:
             ai_score += 1
             ball.rect.center = (width // 2, height // 2)
             ball.x_speed, ball.y_speed = 0, 0

          if ball.rect.x >= width - FIELD_BORDER - GOAL_WIDTH and height // 3 < ball.rect.y < height // 3 + GOAL_HEIGHT:
             player_score += 1
             ball.rect.center = (width // 2, height // 2)
             ball.x_speed, ball.y_speed = 0, 0

    # Update ball movement after checking collisions
          ball.update()

    # Draw elements
          screen.blit(player.image, player.rect)
          screen.blit(ai.image, ai.rect)
          screen.blit(ball.image, ball.rect)
    
    # Display scores
          font = pygame.font.Font(None, 36)
          elapsed_time = int(time.time() - start_time)
          remaining_time = max(0, 180 - elapsed_time)  # 3-minute countdown
          score_text = font.render(f"Player: {player_score}  AI: {ai_score}  Time: {remaining_time}s", True, WHITE)
          screen.blit(score_text, (width // 2 - 120, 20))

          pygame.display.flip()
          clock.tick(30)
          pygame.time.delay(10)  # Reduce CPU usage
          if remaining_time == 0:
                winner_text = "Draw!" if player_score == ai_score else ("Player Wins!" if player_score > ai_score else "AI Wins!")
                if game_over_screen(winner_text):
                    break  # Restart game
while True:
   game_loop()

