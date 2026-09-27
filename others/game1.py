import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
LANE_WIDTH = 100
LANES = [100, 200, 300, 400]
KEYS = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)] # Red, Green, Blue, Yellow
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
HIT_ZONE_Y = 700
NOTE_SPEED = 5
SPAWN_RATE = 30  # Lower is faster

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Guitar Hero")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

class Note:
    def __init__(self, lane_index):
        self.lane = lane_index
        self.x = LANES[lane_index]
        self.y = -50
        self.color = COLORS[lane_index]
        self.hit = False

    def move(self):
        self.y += NOTE_SPEED

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x + LANE_WIDTH // 2, self.y), 30)

def main():
    notes = []
    score = 0
    frame_count = 0
    running = True

    while running:
        screen.fill((0, 0, 0))
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                for i in range(len(KEYS)):
                    if event.key == KEYS[i]:
                        # Check if a note is in the hit zone for this lane
                        for note in notes:
                            if note.lane == i and HIT_ZONE_Y - 50 < note.y < HIT_ZONE_Y + 50:
                                note.hit = True
                                notes.remove(note)
                                score += 10
                                break

        # 2. Logic: Spawn Notes
        frame_count += 1
        if frame_count >= SPAWN_RATE:
            lane_index = random.randint(0, 3)
            notes.append(Note(lane_index))
            frame_count = 0

        # 3. Draw Lanes and Hit Zone
        for i, x in enumerate(LANES):
            pygame.draw.rect(screen, GRAY, (x, 0, LANE_WIDTH, SCREEN_HEIGHT), 1)
            # Draw visual target keys
            pygame.draw.circle(screen, COLORS[i], (x + LANE_WIDTH // 2, HIT_ZONE_Y), 35, 2)
            
        # Draw Hit Line
        pygame.draw.line(screen, WHITE, (0, HIT_ZONE_Y), (SCREEN_WIDTH, HIT_ZONE_Y), 3)

        # 4. Update and Draw Notes
        for note in notes[:]:
            note.move()
            note.draw()
            
            # Remove note if it goes off screen
            if note.y > SCREEN_HEIGHT:
                notes.remove(note)
                score -= 5 # Penalty for missing

        # 5. UI (Score)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Instructions
        instr_text = font.render("Keys: D  F  J  K", True, WHITE)
        screen.blit(instr_text, (SCREEN_WIDTH - 200, 10))

        pygame.display.flip()
        clock.tick(50)

    pygame.quit()

if __name__ == "__main__":
    main()