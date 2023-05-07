import pygame
import math, random

# Initialize pygame font module
pygame.font.init()

# Set the window width and height
width, height = 1200, 800

# Create a window with the given dimensions
win = pygame.display.set_mode((width, height))

# Set the window title to "Pong"
pygame.display.set_caption("Pong")

# Create two font objects for displaying the score and the winner
score = pygame.font.SysFont('timesnewroman', 40)
winner = pygame.font.SysFont('timesnewroman', 100)

# Define some color constants
white_ = (255, 255, 255)
black_ = (0, 0, 0)
red_ = (255, 0, 0)

# Define some game constants
paddle_vel = 7
pong_speed = 5
pong_vel = pygame.math.Vector2(pong_speed, 0)
pong_vel_x, pong_vel_y = 1,1
max_bounce_angle = math.pi / 2

# Define the game borders
center_border = pygame.Rect(width//2, 0, 10, height)
top_border = pygame.Rect(0, 0, width, 10)
bottom_border = pygame.Rect(0, height - 10, width, 10)

# Define the paddles
paddle_width, paddle_height = 5, 75
paddle_margin = 50

# Define user events for when the ball goes off the left or right side of the screen
pong_off_left = pygame.USEREVENT + 1
pong_off_right = pygame.USEREVENT + 2

# Define the size of the ball
pong_width, pong_height = 10, 10


def draw_window(left_paddle, right_paddle, pong, left_score, right_score):
    win.fill(black_)
    # create score text surfaces for the left and right scores, with the score and a white color
    left_score_text = score.render("Score: " + str(left_score), 1, white_)
    right_score_text = score.render("Score: " + str(right_score), 1, white_)

    # blit (draw) the score text surfaces onto the window, with the top-left corner of the left score at position (10, 10),
    # and the top-right corner of the right score at position (width - right_score_text.get_width() - 10, 10)
    win.blit(left_score_text, (10, 10))
    win.blit(right_score_text, (width - right_score_text.get_width() - 10, 10))

    # draw rectangles for the center, top, and bottom borders of the game window, using the white color
    pygame.draw.rect(win, white_, center_border)
    pygame.draw.rect(win, white_, top_border)
    pygame.draw.rect(win, white_, bottom_border)

    # draw rectangles for the left and right paddles, using the white color
    pygame.draw.rect(win, white_, left_paddle)
    pygame.draw.rect(win, white_, right_paddle)

    # draw a rectangle for the pong ball, using the red color
    pygame.draw.rect(win, red_, pong)

    # update the display
    pygame.display.update()

def draw_winner(text):
    draw_text = winner.render(text, 1, white_)
    win.blit(draw_text, (width//2 - draw_text.get_width() /2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def left_handle_movement(keys, left_paddle):
    # If the "W" key is pressed and moving the paddle up won't go out of bounds
    if keys[pygame.K_w] and left_paddle.y - paddle_vel > 0: 
        left_paddle.y -= paddle_vel  # Move the left paddle up by paddle_vel

    # If the "S" key is pressed and moving the paddle down won't go out of bounds
    if keys[pygame.K_s] and left_paddle.y + paddle_vel + left_paddle.height < height: 
        left_paddle.y += paddle_vel  # Move the left paddle down by paddle_vel

def right_handle_movement(keys, right_paddle):
    # If the up arrow key is pressed and moving the paddle up won't go out of bounds
    if keys[pygame.K_UP] and right_paddle.y - paddle_vel > 0: 
        right_paddle.y -= paddle_vel  # Move the right paddle up by paddle_vel

    # If the down arrow key is pressed and moving the paddle down won't go out of bounds
    if keys[pygame.K_DOWN] and right_paddle.y + paddle_vel + right_paddle.height < height: 
        right_paddle.y += paddle_vel  # Move the right paddle down by paddle_vel

# This function handles the movement of the pong ball and detects collisions with the paddles and borders
# physics created with inspiration and aid of ChatGPT
def pong_handle_movement(pong, left_paddle, right_paddle, pong_direction):
    
    # Define global variables for the velocity of the pong ball
    global pong_vel, pong_vel_x, pong_vel_y

    # Check if the pong ball has gone off the screen on the left or right side
    if pong.x < -10:
        # Create an event to notify the game that the pong ball has gone off the screen on the right side
        pygame.event.post(pygame.event.Event(pong_off_right))
    elif pong.x > 1200:
        # Create an event to notify the game that the pong ball has gone off the screen on the left side
        pygame.event.post(pygame.event.Event(pong_off_left))
    else: 
        # If the pong ball is still on the screen, update its position based on its velocity and direction
        if pong_direction == 0:
            pong.x += pong_vel_x
            pong.y += pong_vel_y
        elif pong_direction == 1:
            pong.x -= pong_vel_x
            pong.y += pong_vel_y
        elif pong_direction == 2:
            pass # In case we want to add diagonal movement later on

    # Check for collisions with the left paddle
    if left_paddle.colliderect(pong):
        # Calculate the distance between the center of the pong ball and the center of the paddle
        distance = (pong.y + pong_height/2) - (left_paddle.y + paddle_height/2)
        # Calculate the relative distance as a value between -1 and 1
        relative_distance = distance / (paddle_height/2)
        # Calculate the angle at which the pong ball should bounce off the paddle
        angle = relative_distance * max_bounce_angle
        # Reverse the direction of the pong ball
        pong_direction = 1 - pong_direction
        # Calculate the new x and y velocity components based on the bounce angle and speed
        pong_vel_x = pong_speed * math.cos(angle)
        pong_vel_y = -pong_speed * math.sin(angle)
        # Update the velocity vector of the pong ball
        pong_vel = pygame.math.Vector2(pong_vel_x, pong_vel_y)
    
    # Check for collisions with the right paddle (similar to the left paddle)
    elif right_paddle.colliderect(pong):
        distance = (pong.y + pong_height/2) - (right_paddle.y + paddle_height/2)
        relative_distance = distance / (paddle_height/2)
        angle = relative_distance * max_bounce_angle
        pong_direction = 1 - pong_direction
        pong_vel_x = -pong_speed * math.cos(angle)
        pong_vel_y = -pong_speed * math.sin(angle)
        pong_vel = pygame.math.Vector2(pong_vel_x, pong_vel_y)

    # Check for collisions with the top or bottom border
    elif top_border.colliderect(pong) or bottom_border.colliderect(pong):
        # Reverse the y-direction of the velocity vector of the pong ball
        pong_vel_y = -pong_vel_y
        pong_vel = pygame.math.Vector2(pong_vel_x, pong_vel_y)

    # Scale the velocity vector to the desired speed and update the position of the pong ball
    pong_vel.scale_to_length(pong_speed)
    pong.move_ip(pong_vel)

    # Return the current direction of the pong ball
    return pong_direction

# Define the main function
def main():
    # Initialize the scores to 0 for both players
    left_score, right_score = 0, 0
    
    # Set the initial position of the paddles
    left_paddle_x = paddle_margin
    left_paddle_y = height // 2 - paddle_height // 2
    right_paddle_x = width - paddle_margin - paddle_width
    right_paddle_y = height // 2 - paddle_height // 2
    
    # Create a rectangle object for each paddle
    left_paddle = pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height)
    right_paddle = pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height)
    
    # Set the initial position of the ball
    pong = pygame.Rect(600, 400, pong_width, pong_height)
    
    # Randomly choose the direction of the ball to start with
    pong_direction = random.randint(0,1)
    
    # Create a clock object to limit the game's framerate
    clock = pygame.time.Clock()
    
    # Set the game loop to run
    run = True
    while run:
        # Limit the framerate to 60 fps
        clock.tick(60)
        
        # Check for user input events
        for event in pygame.event.get():
            # If the user quits the game, set the loop to stop and quit pygame
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            # If the ball goes off the left or right side of the screen, increment the corresponding player's score,
            # reset the ball to the center of the screen, and delay the game for 250 milliseconds
            if event.type in [pong_off_left, pong_off_right]:
                if event.type == pong_off_left:
                    left_score += 1
                else:
                    right_score += 1
                pong.x, pong.y = 600, 400
                pygame.time.delay(250)

        
        # Check if either player has won
        winner_text = ""
        if left_score > 5 or right_score > 5:
            # If the left player has won, set the winner text to "Left Wins"
            if left_score > 5:
                winner_text = "Left Wins"
            # If the right player has won, set the winner text to "Right Wins"
            else:
                winner_text ="Right Wins"
            # Draw the winner text on the screen and break out of the game loop
            draw_winner(winner_text)
            break
        
        # Check for user input from the keyboard and move the paddles accordingly
        keys = pygame.key.get_pressed()
        left_handle_movement(keys, left_paddle)
        right_handle_movement(keys, right_paddle)
        
        # Move the ball and check if it has collided with a paddle or gone off the edge of the screen
        pong_direction = pong_handle_movement(pong, left_paddle, right_paddle, pong_direction)
        
        # Draw the game window with the updated positions of the paddles, ball, and scores
        draw_window(left_paddle, right_paddle, pong, left_score, right_score)
    
    # Call the main function to start the game
    main()

if __name__ == "__main__":
    main()
