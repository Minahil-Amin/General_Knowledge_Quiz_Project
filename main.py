"""
General Knowledge Quiz Game
---------------------------
A modern, colorful, and interactive quiz game built with Python and CustomTkinter.
This project uses procedural programming (functions and global state) suitable for beginners.

Features:
- Custom-generated blue-green gradient background.
- Rounded frames, soft shadows, and clean modern typography.
- Smart screen state transitions (Home -> Rules -> Quiz -> End).
- Score tracking, progress bar, and instant visual correct/incorrect button colors.
- Play Again or Exit functionality.
"""

import sys
import os
import customtkinter as ctk
from PIL import Image

# ---------------------------------------------------------
# 1. Global Quiz Configuration and Questions
# ---------------------------------------------------------
# Define the quiz questions in a list of dictionaries.
# Each question contains the text, 4 choices, and the index of the correct answer.
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Rome", "Berlin"],
        "correct": 1  # Paris is at index 1
    },
    {
        "question": "Which planet is called the Red Planet?",
        "options": ["Venus", "Earth", "Mars", "Jupiter"],
        "correct": 2  # Mars is at index 2
    },
    {
        "question": "Which language is used to develop Python programs?",
        "options": ["Python", "HTML", "CSS", "SQL"],
        "correct": 0  # Python is at index 0
    }
]

# Global variables to track the current state of the game
score = 0
current_question_index = 0

# ---------------------------------------------------------
# 2. Gradient Background Helper
# ---------------------------------------------------------
def create_gradient_image(width, height, color1, color2):
    """
    Generates a horizontal linear gradient image between color1 and color2 (RGB tuples).
    This function uses Pillow to construct a 1-pixel high line, interpolating the colors,
    and then scales it to full window size for high performance.
    """
    base = Image.new("RGB", (width, 1))
    for x in range(width):
        ratio = x / width
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        base.putpixel((x, 0), (r, g, b))
    
    # Scale up the 1-pixel tall image to the full window height
    return base.resize((width, height), Image.Resampling.NEAREST)

# ---------------------------------------------------------
# 3. CustomTkinter App Initial Setup
# ---------------------------------------------------------
# Set the look and feel theme of CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize root application window
root = ctk.CTk()
root.title("The General Knowledge Quiz")
root.geometry("900x600")
root.resizable(False, False)

# Set window icon if available
icon_path = os.path.join("assets", "icon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Generate and set the blue-to-green gradient background
# Neon Navy Blue: (10, 25, 47) -> Neon Dark Teal/Green: (6, 78, 59)
bg_pil_image = create_gradient_image(900, 600, (10, 25, 47), (6, 78, 59))
bg_image = ctk.CTkImage(light_image=bg_pil_image, dark_image=bg_pil_image, size=(900, 600))

# Display the gradient background image using a full-screen Label
bg_label = ctk.CTkLabel(master=root, image=bg_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a central container card frame to overlay all screens
# This gives the game a modern, centered floating card aesthetic.
card_frame = ctk.CTkFrame(
    master=root,
    width=720,
    height=480,
    corner_radius=20,
    fg_color="#0f172a",  # slate-900 (solid color to provide contrast against the background)
    border_color="#334155",  # slate-700 subtle border
    border_width=2
)
card_frame.place(relx=0.5, rely=0.5, anchor="center")
# Prevent the card frame from shrinking to fit its contents
card_frame.pack_propagate(False)

# ---------------------------------------------------------
# 4. Navigation and Transitions
# ---------------------------------------------------------
def show_screen(screen_name):
    """
    Hides all screen frames and displays the requested one inside the central card.
    """
    # Hide all content frames
    home_frame.pack_forget()
    rules_frame.pack_forget()
    quiz_frame.pack_forget()
    end_frame.pack_forget()
    
    # Show the requested screen frame
    if screen_name == "home":
        home_frame.pack(fill="both", expand=True, padx=20, pady=20)
    elif screen_name == "rules":
        rules_frame.pack(fill="both", expand=True, padx=20, pady=20)
    elif screen_name == "quiz":
        quiz_frame.pack(fill="both", expand=True, padx=20, pady=20)
        start_quiz_game()
    elif screen_name == "end":
        end_frame.pack(fill="both", expand=True, padx=20, pady=20)
        display_end_results()

# ---------------------------------------------------------
# 5. Quiz Logic Functions
# ---------------------------------------------------------
def start_quiz_game():
    """
    Resets the quiz variables and starts the quiz from the first question.
    """
    global score, current_question_index
    score = 0
    current_question_index = 0
    display_question()

def display_question():
    """
    Loads and displays the active question, option list, and updates progress indicators.
    """
    global current_question_index
    
    # Get current question data
    q_data = questions[current_question_index]
    
    # Update question text label
    question_label.configure(text=q_data["question"])
    
    # Reset and configure options buttons
    for i in range(4):
        option_buttons[i].configure(
            text=f"  {chr(65 + i)}.   {q_data['options'][i]}",  # E.g., "A. London"
            fg_color="#1e293b",       # default option background
            hover_color="#334155",    # default option hover
            state="normal"            # re-enable clicking
        )
    
    # Update progress indicator text
    progress_text_label.configure(text=f"Question {current_question_index + 1} of {len(questions)}")
    
    # Update current score indicator
    score_indicator_label.configure(text=f"Score: {score}")
    
    # Update progress bar (value ranges from 0.0 to 1.0)
    progress_val = (current_question_index + 1) / len(questions)
    progress_bar.set(progress_val)

def select_option(selected_idx):
    """
    Checks the user's choice, highlights the buttons, increments score, and schedules next question.
    """
    global score, current_question_index
    
    # Disable all option buttons immediately to prevent multiple rapid clicks
    for btn in option_buttons:
        btn.configure(state="disabled")
        
    q_data = questions[current_question_index]
    correct_idx = q_data["correct"]
    
    # Check if correct
    if selected_idx == correct_idx:
        score += 1
        # Highlight selected button in green (Correct)
        option_buttons[selected_idx].configure(
            fg_color="#10b981",
            hover_color="#10b981"
        )
    else:
        # Highlight selected button in red (Wrong)
        option_buttons[selected_idx].configure(
            fg_color="#ef4444",
            hover_color="#ef4444"
        )
        # Highlight correct answer button in green so user learns
        option_buttons[correct_idx].configure(
            fg_color="#10b981",
            hover_color="#10b981"
        )
        
    # Show active score update
    score_indicator_label.configure(text=f"Score: {score}")
    
    # Move to the next question automatically after 1.2 seconds (1200 ms)
    root.after(1200, move_to_next)

def move_to_next():
    """
    Increments index and decides whether to load next question or navigate to end screen.
    """
    global current_question_index
    current_question_index += 1
    
    if current_question_index < len(questions):
        display_question()
    else:
        show_screen("end")

def display_end_results():
    """
    Configures and displays the score details and dynamic messages on the End Screen.
    """
    global score
    
    # Show score summary
    end_score_label.configure(text=f"Your Score: {score} / {len(questions)}")
    
    # Customize message and visual appearance based on performance
    if score == 3:
        emoji = "🎉 🏆 🎉"
        feedback = "Excellent!\nPerfect Score!"
        color = "#10b981"  # emerald green
    elif score == 2:
        emoji = "✨ ⭐ ✨"
        feedback = "Great Job!"
        color = "#3b82f6"  # modern blue
    elif score == 1:
        emoji = "👍 😊 👍"
        feedback = "Good Try!"
        color = "#f59e0b"  # golden amber
    else:
        emoji = "📚 💪 📚"
        feedback = "Keep Practicing!"
        color = "#ef4444"  # crimson red
        
    end_emoji_label.configure(text=emoji)
    end_feedback_label.configure(text=feedback, text_color=color)

def exit_application():
    """
    Closes the Tkinter root window and exits the script.
    """
    root.destroy()
    sys.exit()

# ---------------------------------------------------------
# 6. Building UI Screens inside Card Container
# ---------------------------------------------------------

# =========================================================
# A. HOME SCREEN FRAME
# =========================================================
home_frame = ctk.CTkFrame(master=card_frame, fg_color="transparent")

# Load and place the quiz illustration logo
quiz_logo_img = Image.open(os.path.join("assets", "quiz.png"))
ctk_logo = ctk.CTkImage(light_image=quiz_logo_img, dark_image=quiz_logo_img, size=(160, 160))

logo_label = ctk.CTkLabel(master=home_frame, image=ctk_logo, text="")
logo_label.pack(pady=(15, 10))

# Game Main Title
home_title = ctk.CTkLabel(
    master=home_frame,
    text="THE GENERAL KNOWLEDGE QUIZ",
    font=("Helvetica", 28, "bold"),
    text_color="#f8fafc"
)
home_title.pack(pady=5)

# Game Subtitle
home_subtitle = ctk.CTkLabel(
    master=home_frame,
    text="Test your knowledge with fun questions!",
    font=("Helvetica", 15, "italic"),
    text_color="#94a3b8"
)
home_subtitle.pack(pady=(0, 20))

# Buttons frame (horizontal layout)
home_buttons_frame = ctk.CTkFrame(master=home_frame, fg_color="transparent")
home_buttons_frame.pack(pady=10)

btn_start_quiz = ctk.CTkButton(
    master=home_buttons_frame,
    text="🚀  Start Quiz",
    font=("Helvetica", 15, "bold"),
    width=160,
    height=45,
    corner_radius=12,
    fg_color="#0ea5e9",
    hover_color="#0284c7",
    command=lambda: show_screen("rules")
)
btn_start_quiz.pack(side="left", padx=15)

btn_exit_game = ctk.CTkButton(
    master=home_buttons_frame,
    text="❌  Exit",
    font=("Helvetica", 15, "bold"),
    width=160,
    height=45,
    corner_radius=12,
    fg_color="#ef4444",
    hover_color="#dc2626",
    command=exit_application
)
btn_exit_game.pack(side="left", padx=15)


# =========================================================
# B. QUIZ RULES SCREEN FRAME
# =========================================================
rules_frame = ctk.CTkFrame(master=card_frame, fg_color="transparent")

# Rules Title
rules_title = ctk.CTkLabel(
    master=rules_frame,
    text="📋  Quiz Rules",
    font=("Helvetica", 26, "bold"),
    text_color="#f8fafc"
)
rules_title.pack(pady=(20, 15))

# Rules List Container
rules_list_frame = ctk.CTkFrame(master=rules_frame, fg_color="#1e293b", corner_radius=15, border_width=1, border_color="#334155")
rules_list_frame.pack(fill="x", padx=40, pady=10)

rules_text = (
    "• There are 3 questions.\n\n"
    "• Every correct answer gives 1 point.\n\n"
    "• No negative marking.\n\n"
    "• Final score will be displayed at the end.\n\n"
    "• Click Start to begin."
)
rules_label = ctk.CTkLabel(
    master=rules_list_frame,
    text=rules_text,
    font=("Helvetica", 14),
    justify="left",
    text_color="#cbd5e1"
)
rules_label.pack(padx=25, pady=20)

# Rules buttons frame
rules_buttons_frame = ctk.CTkFrame(master=rules_frame, fg_color="transparent")
rules_buttons_frame.pack(pady=20)

btn_rules_start = ctk.CTkButton(
    master=rules_buttons_frame,
    text="🎬  Start",
    font=("Helvetica", 15, "bold"),
    width=140,
    height=42,
    corner_radius=12,
    fg_color="#10b981",
    hover_color="#059669",
    command=lambda: show_screen("quiz")
)
btn_rules_start.pack(side="left", padx=15)

btn_rules_back = ctk.CTkButton(
    master=rules_buttons_frame,
    text="⬅️  Back",
    font=("Helvetica", 15, "bold"),
    width=140,
    height=42,
    corner_radius=12,
    fg_color="#475569",
    hover_color="#334155",
    command=lambda: show_screen("home")
)
btn_rules_back.pack(side="left", padx=15)


# =========================================================
# C. QUIZ PLAY SCREEN FRAME
# =========================================================
quiz_frame = ctk.CTkFrame(master=card_frame, fg_color="transparent")

# Quiz Header Info (Progress + Score)
quiz_header_frame = ctk.CTkFrame(master=quiz_frame, fg_color="transparent")
quiz_header_frame.pack(fill="x", padx=15, pady=(10, 5))

progress_text_label = ctk.CTkLabel(
    master=quiz_header_frame,
    text="Question 1 of 3",
    font=("Helvetica", 14, "bold"),
    text_color="#94a3b8"
)
progress_text_label.pack(side="left")

score_indicator_label = ctk.CTkLabel(
    master=quiz_header_frame,
    text="Score: 0",
    font=("Helvetica", 14, "bold"),
    text_color="#38bdf8"
)
score_indicator_label.pack(side="right")

# Progress bar
progress_bar = ctk.CTkProgressBar(
    master=quiz_frame,
    height=8,
    corner_radius=4,
    progress_color="#0ea5e9",
    fg_color="#334155"
)
progress_bar.pack(fill="x", padx=15, pady=(5, 20))
progress_bar.set(0.0)

# Question Display Card Frame
q_card_frame = ctk.CTkFrame(master=quiz_frame, fg_color="#1e293b", height=90, corner_radius=12)
q_card_frame.pack(fill="x", padx=15, pady=(0, 15))
q_card_frame.pack_propagate(False)

question_label = ctk.CTkLabel(
    master=q_card_frame,
    text="Question loading...",
    font=("Helvetica", 18, "bold"),
    text_color="#f8fafc",
    wraplength=600
)
question_label.pack(expand=True, padx=20, pady=10)

# Options frame (4 vertical buttons)
options_frame = ctk.CTkFrame(master=quiz_frame, fg_color="transparent")
options_frame.pack(fill="both", expand=True, padx=15, pady=0)

# Dynamically construct 4 option buttons and append them to option_buttons list
option_buttons = []
for i in range(4):
    btn = ctk.CTkButton(
        master=options_frame,
        text="",
        font=("Helvetica", 15, "bold"),
        height=45,
        corner_radius=10,
        fg_color="#1e293b",
        hover_color="#334155",
        text_color="#cbd5e1",
        anchor="w",
        border_width=1,
        border_color="#334155",
        command=lambda idx=i: select_option(idx)
    )
    btn.pack(fill="x", pady=5)
    option_buttons.append(btn)


# =========================================================
# D. END SCREEN FRAME
# =========================================================
end_frame = ctk.CTkFrame(master=card_frame, fg_color="transparent")

# Large emoji representing achievements
end_emoji_label = ctk.CTkLabel(
    master=end_frame,
    text="🎉",
    font=("Helvetica", 54)
)
end_emoji_label.pack(pady=(20, 10))

# Completion Title
end_title = ctk.CTkLabel(
    master=end_frame,
    text="Quiz Completed!",
    font=("Helvetica", 28, "bold"),
    text_color="#f8fafc"
)
end_title.pack(pady=5)

# Score display
end_score_label = ctk.CTkLabel(
    master=end_frame,
    text="Your Score: 0 / 3",
    font=("Helvetica", 20, "bold"),
    text_color="#38bdf8"
)
end_score_label.pack(pady=5)

# Dynamic feedback message box
end_feedback_label = ctk.CTkLabel(
    master=end_frame,
    text="Excellent!",
    font=("Helvetica", 22, "bold"),
)
end_feedback_label.pack(pady=(5, 20))

# End screen buttons container
end_buttons_frame = ctk.CTkFrame(master=end_frame, fg_color="transparent")
end_buttons_frame.pack(pady=10)

btn_play_again = ctk.CTkButton(
    master=end_buttons_frame,
    text="🔄  Play Again",
    font=("Helvetica", 15, "bold"),
    width=150,
    height=45,
    corner_radius=12,
    fg_color="#10b981",
    hover_color="#059669",
    command=lambda: show_screen("home")
)
btn_play_again.pack(side="left", padx=15)

btn_end_exit = ctk.CTkButton(
    master=end_buttons_frame,
    text="❌  Exit",
    font=("Helvetica", 15, "bold"),
    width=150,
    height=45,
    corner_radius=12,
    fg_color="#ef4444",
    hover_color="#dc2626",
    command=exit_application
)
btn_end_exit.pack(side="left", padx=15)

# ---------------------------------------------------------
# 7. Start the application
# ---------------------------------------------------------
# Default landing screen is the Home screen
show_screen("home")

# Run the Tkinter main event loop
root.mainloop()
