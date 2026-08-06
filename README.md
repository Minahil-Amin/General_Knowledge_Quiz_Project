# The General Knowledge Quiz Game

A beautiful, modern **General Knowledge Quiz Game** built in Python using a state-of-the-art Graphical User Interface (GUI) powered by **CustomTkinter** and **Pillow**.

Designed specifically for beginners, the application logic is fully procedural (using simple variables, functions, and list indexing) and excludes complex object-oriented programming (OOP) or advanced algorithms, making it clean, easy to understand, and highly educational.

---

## Features

- **Modern Glassmorphic Card UI**: Centered cards floating over a custom-rendered blue-to-green gradient.
- **Custom Assets**: Uses AI-generated theme illustration (`quiz.png`) and application icon (`icon.ico`).
- **Interactive Elements**: Beautiful hover states, rounded corners, and animated screen transitions.
- **Instant Visual Feedback**: Option buttons highlight in **green** (Correct) or **red** (Wrong) instantly upon selection.
- **Automatic Transitions**: The quiz automatically proceeds to the next question after a 1.2-second delay.
- **Score System & Achievements**: Smart message and badge allocation depending on final score at the completion screen.
- **Progress Tracking**: Continuous indicator displaying the active question number and current score with a custom progress bar.

---

## File Structure

```text
GeneralKnowledgeQuiz/
│
├── main.py             # Main entry point containing logic and GUI elements
├── requirements.txt    # Required python packages list
├── README.md           # Documentation for project setup and walkthrough
└── assets/             # Asset folder for graphic resources
    ├── quiz.png        # Theme illustration for the home screen
    └── icon.ico        # High-resolution application window icon
```

---

## Requirements

- **Python**: version `3.8` or above.
- **Libraries**:
  - `customtkinter` (for modern UI components)
  - `pillow` (for handling, resizing, and rendering custom image assets)

---

## Installation & Setup

Follow these simple steps to set up and run the project locally on your machine:

1. **Clone or Download the Project**:
   Ensure you have all files in a single folder named `GeneralKnowledgeQuiz`.

2. **Open your Terminal/Command Prompt**:
   Navigate into the folder where the files are located.

3. **Install Dependencies**:
   Run the following command to download and install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Game**:
   Start the application by running:
   ```bash
   python main.py
   ```

---

## Code Logic Breakdown

The code is highly commented to make it perfect for class presentations:
1. **Questions Data List**: Stored in a simple list of dictionaries (`questions`), containing the question text, option choices, and the target index of the correct answer.
2. **State Management**: Uses simple global variables (`score` and `current_question_index`) modified via Python's standard `global` keyword inside event-handling functions.
3. **Screen Transitions**: Accomplished by packing and unpacking standard Tkinter frames (`.pack_forget()` and `.pack()`) dynamically under a helper function `show_screen()`.
4. **Button Disabling**: The options list buttons are set to `"disabled"` immediately when one is selected to avoid double inputs or rapid click spamming.
