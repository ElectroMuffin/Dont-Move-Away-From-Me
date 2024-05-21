import tkinter as tk
import pygame
import random
import math
import os
from time import time

# Initialize pygame mixer
pygame.mixer.init()

# Get the current directory
current_directory = os.path.dirname(__file__)

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Variable to track whether the game is running
game_running = False

# Initialize the final score window variable
final_score_window = None

# Read personal best score from file
def read_personal_best():
    try:
        with open("PB.txt", "r") as file:
            personal_best = int(file.read())
    except FileNotFoundError:
        personal_best = 0
    return personal_best

# Write new personal best score to file
def write_personal_best(new_best):
    with open("PB.txt", "w") as file:
        file.write(str(new_best))

# Function to create the Toplevel window for displaying the GIF
def create_error_window():
    global game_running
    if not game_running:
        game_running = True
        # Create a Toplevel window for displaying the GIF
        error_window = tk.Toplevel()
        error_window.title("Keep the cursor on me!")  # Change the title
        error_window.geometry("400x300")  # Set initial dimensions (width: 400, height: 300)

        # Define parameters for movement
        speed = 5  # The speed
        move_interval = 20  # Update interval in milliseconds

        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Choose a random angle between right and up
        angle = random.uniform(math.pi / 6, math.pi / 3)  # Angle between 30 and 60 degrees (in radians)

        # Calculate direction components using trigonometry
        direction_x = math.cos(angle)
        direction_y = -math.sin(angle)  # Make y negative to move upwards

        # Variables for timer and score
        start_time = None
        score = 0

        # Function to update the elapsed time
        def update_time():
            nonlocal start_time
            if start_time is not None:
                elapsed = time() - start_time
                elapsed_seconds = int(elapsed)
                elapsed_time.set(f"Time: {elapsed_seconds:02}")
                error_window.after(1000, update_time)  # Call update_time() again after 1 second

        # Function to move the window around the screen
        def move_error_window():
            nonlocal direction_x, direction_y, start_time, score
            current_x = error_window.winfo_x()
            current_y = error_window.winfo_y()

            # Calculate new position
            new_x = current_x + direction_x * speed
            new_y = current_y + direction_y * speed

            # Check if the window hits the edges of the screen
            if new_x <= 0 or new_x >= screen_width - error_window.winfo_width():
                direction_x *= -1
            if new_y <= 0 or new_y >= screen_height - error_window.winfo_height():
                direction_y *= -1

            # Convert new position to integers
            new_x = int(new_x)
            new_y = int(new_y)

            # Move the window
            error_window.geometry(f"+{new_x}+{new_y}")

            # Check if cursor is on the window
            x, y = root.winfo_pointerxy()
            if (error_window.winfo_rootx() <= x <= error_window.winfo_rootx() + error_window.winfo_width()) and \
               (error_window.winfo_rooty() <= y <= error_window.winfo_rooty() + error_window.winfo_height()):
                error_window.config(bg="green")
                if start_time is None:
                    start_time = time()
                    update_time()
            else:
                error_window.config(bg="SystemButtonFace")
                if start_time is not None:
                    score = int(time() - start_time)
                start_time = None
                show_final_score_window(score)

            # Schedule next movement
            error_window.after(move_interval, move_error_window)

        # Function to stop window movement when cursor leaves
        def stop_move_error_window(event):
            error_window.destroy()

        # Bind the window movement to cursor entering
        error_window.bind("<Enter>", lambda event: move_error_window())

        # Bind the window movement stop when cursor leaves
        error_window.bind("<Leave>", stop_move_error_window)

        # Load and play the sound in a loop
        sound_path = os.path.join(current_directory, "sneaky-snitch.wav")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)  # Play in a loop

        # Label to display elapsed time with larger font
        elapsed_time = tk.StringVar()
        time_label = tk.Label(error_window, textvariable=elapsed_time, font=("Arial", 16))
        time_label.pack()

# Function to display the final score window
def show_final_score_window(score):
    global final_score_window
    if not final_score_window:
        final_score_window = tk.Toplevel()
        final_score_window.title("Final Score")
        final_score_window.geometry("200x150")

        # Read personal best score from file
        personal_best = read_personal_best()

        # Check if the current score is higher than the personal best
        if score > personal_best:
            personal_best = score
            # Write new personal best score to file
            write_personal_best(personal_best)

        # Display score and personal best
        final_score_label = tk.Label(final_score_window, text=f"Score: {score}\nPersonal Best: {personal_best}")
        final_score_label.pack()

        # Create Quit button
        quit_button = tk.Button(final_score_window, text="Quit", command=lambda: quit_game(final_score_window))
        quit_button.pack()

        # Create Play Again button
        play_again_button = tk.Button(final_score_window, text="Play Again", command=lambda: restart_game(final_score_window))
        play_again_button.pack()

# Function to quit the game
def quit_game(window):
    global final_score_window
    window.destroy()
    del final_score_window
    thanks_window = tk.Toplevel()
    thanks_window.title("Thanks for playing")
    thanks_window.geometry("200x100")
    thanks_label = tk.Label(thanks_window, text="Thanks for playing :)\n-@electromuffin (on YT)")
    thanks_label.pack()

# Function to restart the game
def restart_game(window):
    global game_running, final_score_window
    game_running = False
    final_score_window.destroy()
    final_score_window = None
    window.destroy()
    del window
    create_error_window()

# Spawn the initial window
create_error_window()

# Run the tkinter event loop
root.mainloop()
