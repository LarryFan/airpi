import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
GREEN_PRESSED = (0, 255, 0)
RED = (200, 0, 0)
RED_PRESSED = (255, 0, 0)
BLUE = (0, 0, 200)
BLUE_PRESSED = (0, 0, 255)
GRAY = (200, 200, 200)

# Button positions and dimensions
button_width = 120
button_height = 60
up_button_center = (100, 60)
hover_button_center = (100, 130)
down_button_center = (100, 200)
pause_center = (240, 220)
pause_dimensions = (80, 40)

balloon = pygame.image.load("/home/pi/Documents/balloon_test/helpers/balloon2-removebg.png")
balloon = pygame.transform.scale(balloon, (50, 50)) 
balloon_width = 20
balloon_rect = balloon.get_rect()
balloon_rect.centerx = balloon_width

# Button states
states = ("Hover", "Up", "Down")


def draw_buttons_and_indicators(screen, font_big, font_small, state_counter, altitude, temperature, humidity, active_counter, paused, connected):
    """Draw the buttons and indicators on the screen."""
    screen.fill(BLACK)
    state = states[state_counter]

    balloon_height = 240 - (240 * altitude / 60)
    balloon_rect.bottom = balloon_height
    screen.blit(balloon, balloon_rect)

    # Draw "Up" Button
    up_button_rect = pygame.Rect(0, 0, button_width, button_height)
    up_button_rect.center = up_button_center
    if state == "Up" and not paused:
        pygame.draw.ellipse(screen, GREEN_PRESSED, up_button_rect)
    else:
        pygame.draw.ellipse(screen, GREEN, up_button_rect)
    up_text = font_small.render("Up", True, WHITE)
    up_rect = up_text.get_rect(center=up_button_center)
    screen.blit(up_text, up_rect)

    # Draw "Hover" Button
    hover_button_rect = pygame.Rect(0, 0, button_width, button_height)
    hover_button_rect.center = hover_button_center
    if state == "Hover" and not paused:
        pygame.draw.ellipse(screen, BLUE_PRESSED, hover_button_rect)
    else:
        pygame.draw.ellipse(screen, BLUE, hover_button_rect)
    hover_text = font_small.render("Hover", True, WHITE)
    hover_rect = hover_text.get_rect(center=hover_button_center)
    screen.blit(hover_text, hover_rect)

    # Draw "Down" Button
    down_button_rect = pygame.Rect(0, 0, button_width, button_height)
    down_button_rect.center = down_button_center
    if state == "Down" and not paused:
        pygame.draw.ellipse(screen, RED_PRESSED, down_button_rect)
    else:
        pygame.draw.ellipse(screen, RED, down_button_rect)
    down_text = font_small.render("Down", True, WHITE)
    down_rect = down_text.get_rect(center=down_button_center)
    screen.blit(down_text, down_rect)

    # Draw Pause Button
    pause_text = font_small.render("Pause", True, WHITE)
    pause_rect = pause_text.get_rect(center=pause_center)
    screen.blit(pause_text, pause_rect)

    # Draw altitude, temperature, and time indicators
    altitude_text = font_small.render(f"ALT: {altitude:.1f} in", True, WHITE)
    temperature_text = font_small.render(f"TEMP: {temperature:.1f} C", True, WHITE)
    humidity_text = font_small.render(f"HUM: {humidity:.1f} %", True, WHITE)
    flight_time_text = font_small.render(f"TIME: {active_counter:.1f} s", True, WHITE)

    right_margin = 10
    altitude_rect = altitude_text.get_rect(topright=(screen.get_width() - right_margin, 40))
    temperature_rect = temperature_text.get_rect(topright=(screen.get_width() - right_margin, 80))
    humidity_rect = humidity_text.get_rect(topright=(screen.get_width() - right_margin, 120))
    flight_time_rect = flight_time_text.get_rect(topright=(screen.get_width() - right_margin, 160))

    screen.blit(altitude_text, altitude_rect)
    screen.blit(temperature_text, temperature_rect)
    screen.blit(humidity_text, humidity_rect)
    screen.blit(flight_time_text, flight_time_rect)

    if connected:
        status_text = font_small.render(f"ONLINE!", True, WHITE)
    else:
        status_text = font_small.render(f"OFFLINE", True, WHITE)

    status_rect = status_text.get_rect(topleft=(100, 0))
    screen.blit(status_text, status_rect)

    pygame.display.flip()
