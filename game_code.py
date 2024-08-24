import pygame
import sys
import random
import webbrowser

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Security Awareness Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)             # Standard Blue
CYAN = (0, 255, 255)           # Cyan
MAGENTA = (255, 0, 255)        # Magenta
YELLOW = (255, 255, 0)         # Yellow
ORANGE = (255, 165, 0)         # Orange
PURPLE = (128, 0, 128)         # Purple
PINK = (255, 192, 203)         # Light Pink
LIGHT_GRAY = (211, 211, 211)   # Light Gray
DARK_GRAY = (169, 169, 169)    # Dark Gray
BROWN = (165, 42, 42)          # Brown
TURQUOISE = (64, 224, 208)     # Turquoise
VIOLET = (238, 130, 238)       # Violet
LIME = (50, 205, 50)           # Lime Green
INDIGO = (75, 0, 130)          # Indigo
TEAL = (0, 128, 128)           # Teal


# Font
font = pygame.font.Font(None, 36)

# Load sounds
correct_sound = pygame.mixer.Sound('sounds/correct.wav')
incorrect_sound = pygame.mixer.Sound('sounds/incorrect.wav')
bg_music = pygame.mixer.music.load('sounds/bgm.mp3')
pygame.mixer.music.play(-1)  # Loop the music

# Load images
background_image = pygame.image.load('images/bgimage.jpeg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
hacker_image = pygame.image.load('images/hacker.png')
hacker_image = pygame.transform.scale(hacker_image, (200, 200))  # Resize as needed
user_image = pygame.image.load('images/user.png')
user_image = pygame.transform.scale(user_image, (200, 200))  # Resize as needed

# Positions for interactive images
hacker_rect = pygame.Rect(50, HEIGHT - 200, 150, 150)
user_rect = pygame.Rect(WIDTH - 200, HEIGHT - 200, 150, 150)

# Health settings
hacker_health = 100
user_health = 100

# Define questions and answers
questions = [

    {
        "question": "Which is the strongest password?",
        "options": ["123456", "Password123", "$tr0ngP@ssw0rd!"],
        "correct": "$tr0ngP@ssw0rd!",
        "explanation": "Strong passwords include letters, numbers, and symbols."
    },
    {
        "question": "A stranger asks for your personal info. Will you share it?",
        "options": ["Yes", "No"],
        "correct": "No",
        "explanation": "Never share personal information with strangers."
    },
    {
        "question": "What should you do if you receive an unexpected attachment?",
        "options": ["Open it immediately", "Delete it", "Scan it with antivirus"],
        "correct": "Scan it with antivirus",
        "explanation": "Always scan unexpected attachments with antivirus software."
    },
    {
        "question": "What is two-factor authentication?",
        "options": ["A second password", "An additional security step", "A password manager"],
        "correct": "An additional security step",
        "explanation": "Two-factor authentication adds an additional layer of security beyond just a password."
    },
    {
        "question": "What is the best practice for handling software updates?",
        "options": ["Ignore updates until they become mandatory", "Install updates as soon as they are available", "Only install updates if you encounter issues"],
        "correct": "Install updates as soon as they are available",
        "explanation": "Installing updates promptly ensures that you receive the latest security patches and bug fixes, reducing vulnerabilities."
    },
    {
        "question": "What should you do if you suspect your computer is infected with malware?",
        "options": ["Continue using it normally", "Disconnect it from the internet and run a security scan", "Try to fix the issue yourself without professional help"],
        "correct": "Disconnect it from the internet and run a security scan",
        "explanation": "Disconnecting from the internet prevents further spread of the malware, while a security scan can help identify and remove it."
    },
    {
        "question": "How can you protect sensitive data when using public Wi-Fi?",
        "options": ["Use a virtual private network (VPN)", "Turn off Wi-Fi when not in use", "Access sensitive data only during daylight hours"],
        "correct": "Use a virtual private network (VPN)",
        "explanation": "A VPN encrypts your internet connection, making it more secure when accessing sensitive information over public Wi-Fi."
    },
    {
        "question": "What should you do before disposing of an old computer or hard drive?",
        "options": ["Delete all files and perform a factory reset", "Just throw it away without any further action", "Physically destroy the hard drive or use data-wiping software"],
        "correct": "Physically destroy the hard drive or use data-wiping software",
        "explanation": "Properly destroying or wiping the hard drive ensures that sensitive data cannot be recovered by unauthorized individuals."
    },
    {
        "question": "How can you recognize a secure website?",
        "options": ["The URL begins with 'http'", "The URL begins with 'https' and has a padlock icon", "The website has a lot of advertisements"],
        "correct": "The URL begins with 'https' and has a padlock icon",
        "explanation": "The 'https' and padlock icon indicate that the website uses encryption to protect your data during transmission."
    },
    {
        "question": "What is a common indicator of a scam phone call?",
        "options": ["A call from an unknown number asking for personal information", "A call from a known contact with a request", "A call with a friendly and informative message"],
        "correct": "A call from an unknown number asking for personal information",
        "explanation": "Scam calls often come from unknown numbers and request personal information. Be cautious and verify the caller's identity before sharing any information."
    },
    {
        "question": "What should you do if you receive an email from an unfamiliar source with an urgent request?",
        "options": ["Click on any links provided to verify the request", "Delete the email and report it as phishing", "Reply to the email asking for more details"],
        "correct": "Delete the email and report it as phishing",
        "explanation": "It's safer to delete and report suspicious emails to prevent potential phishing attempts and protect your information."
    },
    {
        "question": "Which action can help prevent identity theft?",
        "options": ["Using strong and unique passwords for each account", "Keeping all your passwords in a text file on your computer", "Sharing passwords with trusted friends"],
        "correct": "Using strong and unique passwords for each account",
        "explanation": "Strong and unique passwords for each account help protect your personal information and reduce the risk of identity theft."
    },
    {
        "question": "What should you do if you are unsure about the safety of a website?",
        "options": ["Enter your information to see if it's safe", "Contact the website's customer service for verification", "Check for online reviews and security ratings"],
        "correct": "Check for online reviews and security ratings",
        "explanation": "Online reviews and security ratings can help determine the safety of a website before you enter any personal information."
    },
    {
        "question": "What is a good practice for creating a strong password?",
        "options": ["Using easily memorable words", "Combining letters, numbers, and special characters", "Using the same password for multiple accounts"],
        "correct": "Combining letters, numbers, and special characters",
        "explanation": "A strong password should be complex and difficult to guess, incorporating a mix of letters, numbers, and symbols."
    },
    {
        "question": "What should you do if your computer prompts you to install unfamiliar software?",
        "options": ["Install it immediately", "Ignore the prompt", "Research the software and verify its legitimacy"],
        "correct": "Research the software and verify its legitimacy",
        "explanation": "Installing unknown software can introduce malware. Verify its legitimacy before proceeding."
    },
    {
        "question": "What is the purpose of a firewall?",
        "options": ["To improve internet speed", "To block unauthorized access to a network", "To increase computer storage"],
        "correct": "To block unauthorized access to a network",
        "explanation": "A firewall helps protect your network by filtering incoming and outgoing traffic to block unauthorized access."
    },
    {
        "question": "How can you avoid falling victim to social engineering attacks?",
        "options": ["Be skeptical of unsolicited requests for personal information", "Share information only with trusted individuals", "Verify the identity of the requester before responding"],
        "correct": "Be skeptical of unsolicited requests for personal information",
        "explanation": "Social engineering attacks often rely on tricking individuals into disclosing personal information. Always verify the legitimacy of requests."
    },
    {
        "question": "What should you do if you suspect that your email account has been compromised?",
        "options": ["Change your password immediately", "Ignore the suspicion", "Contact your email provider and ask them to monitor your account"],
        "correct": "Change your password immediately",
        "explanation": "Changing your password immediately helps secure your account and prevent unauthorized access."
    },
    {
        "question": "How can you protect your personal information on social media?",
        "options": ["Share as much information as possible", "Set your profile to private and be cautious with what you share", "Accept friend requests from everyone"],
        "correct": "Set your profile to private and be cautious with what you share",
        "explanation": "Limiting the visibility of your profile and being careful about what you share can help protect your personal information."
    },
    {
        "question": "What is phishing?",
        "options": ["A type of computer virus", "A method of tricking individuals into providing personal information", "A way to protect your data"],
        "correct": "A method of tricking individuals into providing personal information",
        "explanation": "Phishing involves tricking individuals into providing personal information through deceptive emails or websites."
    },
    {
        "question": "What is a VPN used for?",
        "options": ["To encrypt your internet connection", "To speed up your internet", "To back up your data"],
        "correct": "To encrypt your internet connection",
        "explanation": "A VPN encrypts your internet connection, enhancing security and privacy while you browse the web."
    },
    {
        "question": "Why is it important to have antivirus software installed on your computer?",
        "options": ["To improve computer performance", "To detect and remove malware", "To update your operating system"],
        "correct": "To detect and remove malware",
        "explanation": "Antivirus software helps protect your computer by detecting and removing malicious software that could compromise your security."
    },
    {
        "question": "What should you do if you receive a suspicious text message asking for personal information?",
        "options": ["Reply to the message with the requested information", "Ignore the message", "Report it to your mobile carrier and delete it"],
        "correct": "Report it to your mobile carrier and delete it",
        "explanation": "Reporting suspicious messages to your mobile carrier helps prevent potential scams and keeps your information safe."
    },
    {
        "question": "What is a common feature of a secure password manager?",
        "options": ["It stores passwords in plain text", "It uses encryption to protect stored passwords", "It only stores passwords for one account"],
        "correct": "It uses encryption to protect stored passwords",
        "explanation": "A secure password manager uses encryption to protect your passwords and keep them safe from unauthorized access."
    },
    {
        "question": "How should you handle sensitive data in emails?",
        "options": ["Send it without encryption", "Use encryption and secure methods for transmission", "Share it in plain text"],
        "correct": "Use encryption and secure methods for transmission",
        "explanation": "Encrypting sensitive data ensures that it is protected from unauthorized access during transmission."
    },
    {
        "question": "What is the primary goal of cybersecurity?",
        "options": ["To create software", "To protect data and systems from threats", "To improve internet speed"],
        "correct": "To protect data and systems from threats",
        "explanation": "Cybersecurity aims to protect data, systems, and networks from various threats and vulnerabilities."
    },
    {
        "question": "What is a common sign of a computer virus infection?",
        "options": ["Slow performance and unexpected crashes", "Increased battery life", "Improved internet speed"],
        "correct": "Slow performance and unexpected crashes",
        "explanation": "Common signs of a virus infection include slow performance, frequent crashes, and unusual behavior."
    },
    {
        "question": "What should you do if you accidentally click on a suspicious link?",
        "options": ["Close the browser immediately and run a security scan", "Ignore it and continue using the computer", "Click on more links to investigate"],
        "correct": "Close the browser immediately and run a security scan",
        "explanation": "Closing the browser and running a security scan can help prevent potential threats from spreading."
    },
    {
        "question": "What is a common method used to protect sensitive information on a computer?",
        "options": ["Using encryption", "Leaving files unprotected", "Sharing passwords with colleagues"],
        "correct": "Using encryption",
        "explanation": "Encryption protects sensitive information by converting it into a secure format that can only be accessed with the correct key."
    },
    {
        "question": "What action should you take if you find a lost device containing sensitive information?",
        "options": ["Keep it and try to use it", "Report it to the appropriate authorities or the device's owner", "Discard it without further action"],
        "correct": "Report it to the appropriate authorities or the device's owner",
        "explanation": "Reporting a lost device helps ensure that any sensitive information it contains is secured and returned to its rightful owner."
    },
    {
        "question": "What is the role of regular software updates?",
        "options": ["To add new features only", "To fix security vulnerabilities and improve functionality", "To change the user interface"],
        "correct": "To fix security vulnerabilities and improve functionality",
        "explanation": "Regular software updates address security vulnerabilities and enhance overall functionality."
    },
    {
        "question": "How can you ensure your online transactions are secure?",
        "options": ["Use public Wi-Fi for transactions", "Check for 'https' in the URL and use trusted websites", "Share your payment details with anyone who asks"],
        "correct": "Check for 'https' in the URL and use trusted websites",
        "explanation": "Secure online transactions should be conducted on websites with 'https' and a padlock icon to ensure data protection."
    }
]

# Font
font = pygame.font.Font(None, 48)  # Standard font size
title_font = pygame.font.Font(None, 100)  # Larger font for the title
button_font = pygame.font.Font(None, 50)  # Font for buttons
question_font = pygame.font.Font(None, 60)  # Font for questions
explanation_font = pygame.font.Font(None, 45)  # Font for explanations

# Music state
music_on = True

# Screen sizes
screen_sizes = [(1024, 768), (800, 600), (1280, 720)]
current_screen_size_index = 0



# Centered text function
def render_text_centered(text, y_pos, color=BLACK, use_question_font=False, font_type=None):
    font_to_use = font_type if font_type else (question_font if use_question_font else font)
    text_surface = font_to_use.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y_pos))
    screen.blit(text_surface, text_rect)



def render_wrapped_text(text, y_pos, color=BLACK, font_type=font, max_width=WIDTH - 100):
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        test_surface = font_type.render(test_line, True, color)
        if test_surface.get_width() > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line
    
    lines.append(current_line)
    
    for i, line in enumerate(lines):
        text_surface = font_type.render(line, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y_pos + i * font_type.get_height()))
        screen.blit(text_surface, text_rect)



# Draw button
def draw_button(text, y_pos, color, font_type=button_font):
    text_surface = font_type.render(text, True, WHITE)
    text_width = text_surface.get_width() + 40
    text_height = text_surface.get_height() + 20
    
    button_rect = pygame.Rect(WIDTH // 2 - text_width // 2, y_pos - text_height // 2, text_width, text_height)
    
    pygame.draw.rect(screen, color, button_rect, border_radius=15)
    
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    
    return button_rect





# Draw health bar
def draw_health_bar(health, max_health, x, y):
    bar_width = 20
    bar_height = 100
    fill = (health / max_health) * bar_height
    pygame.draw.rect(screen, BLACK, (x, y - bar_height, bar_width, bar_height), 2)  # Draw border
    pygame.draw.rect(screen, RED if health <= max_health / 2 else GREEN, (x, y - fill, bar_width, fill))  # Draw fill


def toggle_music():
    global music_on
    if music_on:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    music_on = not music_on

def change_screen_size():
    global WIDTH, HEIGHT, screen
    global current_screen_size_index
    WIDTH, HEIGHT = screen_sizes[current_screen_size_index]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Security Awareness Game")

def settings_screen():
    global current_screen_size_index

    screen.blit(background_image, (0, 0))
    render_text_centered("Settings", 150, WHITE)

    # Music On/Off
    music_button_text = "Turn Music Off" if music_on else "Turn Music On"
    music_button = draw_button(music_button_text, 300, GRAY)

    # Screen Size Options
    screen_size_text = f"Screen Size: {screen_sizes[current_screen_size_index][0]}x{screen_sizes[current_screen_size_index][1]}"
    screen_size_button = draw_button(screen_size_text, 400, GRAY)

    # Back Button
    back_button = draw_button("Back to Menu", HEIGHT - 100, GRAY)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if music_button.collidepoint(event.pos):
                    toggle_music()
                    music_button_text = "Turn Music Off" if music_on else "Turn Music On"
                    screen.blit(background_image, (0, 0))
                    render_text_centered("Settings", 150, WHITE)
                    music_button = draw_button(music_button_text, 300, GRAY)
                    screen_size_text = f"Screen Size: {screen_sizes[current_screen_size_index][0]}x{screen_sizes[current_screen_size_index][1]}"
                    screen_size_button = draw_button(screen_size_text, 400, GRAY)
                    back_button = draw_button("Back to Menu", HEIGHT - 100, GRAY)
                    pygame.display.flip()
                elif screen_size_button.collidepoint(event.pos):
                    current_screen_size_index = (current_screen_size_index + 1) % len(screen_sizes)
                    change_screen_size()
                    screen.blit(background_image, (0, 0))
                    render_text_centered("Settings", 150, WHITE)
                    music_button_text = "Turn Music Off" if music_on else "Turn Music On"
                    music_button = draw_button(music_button_text, 300, GRAY)
                    screen_size_text = f"Screen Size: {screen_sizes[current_screen_size_index][0]}x{screen_sizes[current_screen_size_index][1]}"
                    screen_size_button = draw_button(screen_size_text, 400, GRAY)
                    back_button = draw_button("Back to Menu", HEIGHT - 100, GRAY)
                    pygame.display.flip()
                elif back_button.collidepoint(event.pos):
                    waiting = False
                    main_menu()

link_rects = {
    "Website": pygame.Rect(0, 0, 0, 0),
    "LinkedIn": pygame.Rect(0, 0, 0, 0),
    "GitHub": pygame.Rect(0, 0, 0, 0)
}

def credits_screen():
    screen.blit(background_image, (0, 0))
    render_text_centered("Credits", 150, WHITE, font_type=button_font)
    
    # Load logo images
    website_logo = pygame.image.load('images/website_logo.png')  # Replace with your logo file path
    linkedin_logo = pygame.image.load('images/linkedin_logo.png')  # Replace with your logo file path
    github_logo = pygame.image.load('images/github_logo.png')  # Replace with your logo file path

    # Resize logos if needed
    website_logo = pygame.transform.scale(website_logo, (100, 100))
    linkedin_logo = pygame.transform.scale(linkedin_logo, (100, 100))
    github_logo = pygame.transform.scale(github_logo, (100, 100))

    # Display logos and define clickable areas
    website_rect = pygame.Rect(WIDTH // 2 - 150, 250, 100, 100)
    linkedin_rect = pygame.Rect(WIDTH // 2 - 50, 250, 100, 100)
    github_rect = pygame.Rect(WIDTH // 2 + 50, 250, 100, 100)

    screen.blit(website_logo, website_rect.topleft)
    screen.blit(linkedin_logo, linkedin_rect.topleft)
    screen.blit(github_logo, github_rect.topleft)

    # Store clickable areas for each logo
    link_rects["Website"] = website_rect
    link_rects["LinkedIn"] = linkedin_rect
    link_rects["GitHub"] = github_rect
    
    # Display text for names (optional)
    render_text_centered("Developed by Naveen", 400, WHITE)
    
    # Back Button
    back_button = draw_button("Back to Menu", HEIGHT - 100, GRAY)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    waiting = False
                    main_menu()
                else:
                    for link, rect in link_rects.items():
                        if rect.collidepoint(event.pos):
                            if link == "Website":
                                webbrowser.open("https://workwithnaveen7.github.io/Naveen-portfolio-website/")
                            elif link == "LinkedIn":
                                webbrowser.open("https://www.linkedin.com/in/naveenkumar54321")
                            elif link == "GitHub":
                                webbrowser.open("https://github.com/workwithnaveen7")



# Main Menu
def main_menu():
    screen.blit(background_image, (0, 0))

    # Create larger font for the title
    larger_title_font = pygame.font.Font(None, 100)  # Ensure this line is creating the font

    # Render the title with the larger font
    title_text_surface = larger_title_font.render("Security Awareness Game", True, LIME)
    title_text_rect = title_text_surface.get_rect(center=(WIDTH // 2, 200))
    screen.blit(title_text_surface, title_text_rect)

    # Add a subtitle below the title
    subtitle_font = pygame.font.Font(None, 50)  # Subtitle font
    subtitle_text_surface = subtitle_font.render("Test Your Knowledge and Stay Safe Online!", True, WHITE)
    subtitle_text_rect = subtitle_text_surface.get_rect(center=(WIDTH // 2, 300))
    screen.blit(subtitle_text_surface, subtitle_text_rect)

    # Add decorative lines
    #pygame.draw.line(screen, BLACK, (150, 180), (850, 180), 5)  # Line above the title
    pygame.draw.line(screen, BLACK, (150, 260), (850, 260), 5)  # Line below the subtitle

    # Add buttons
    start_button = draw_button("Start Game", 500, GRAY, font_type=button_font)
    settings_button = draw_button("Settings", 600, GRAY, font_type=button_font)
    credits_button = draw_button("Credits", 700, GRAY, font_type=button_font)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting = False
                elif settings_button.collidepoint(event.pos):
                    settings_screen()
                elif credits_button.collidepoint(event.pos):
                    credits_screen()



# Handle player input
def handle_input(scenario, *buttons):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.collidepoint(event.pos):
                        button_index = buttons.index(button)
                        return button_index  # Return the index of the selected option

# Game Scenario
def game_scenario(question_data):
    global hacker_health, user_health
    screen.blit(background_image, (0, 0))
    
    render_wrapped_text(question_data["question"], 150, color=WHITE, font_type=question_font)
    
    buttons = []
    y_pos = 350  # Adjust the y position for the options
    for i, option in enumerate(question_data["options"]):
        button = draw_button(option, y_pos + i * 80, GRAY)  # Adjust spacing between options
        buttons.append(button)
    
    screen.blit(hacker_image, hacker_rect.topleft)
    screen.blit(user_image, user_rect.topleft)

    draw_health_bar(hacker_health, 100, hacker_rect.left - 30, hacker_rect.top + 25)
    draw_health_bar(user_health, 100, user_rect.right + 10, user_rect.top + 25)
    
    pygame.display.flip()
    selected_index = handle_input(question_data["question"], *buttons)
    
    correct = question_data["options"][selected_index] == question_data["correct"]
    if correct:
        hacker_health -= 20
    else:
        user_health -= 20
    
    return correct, question_data["explanation"]



# Display feedback
def display_feedback(correct, explanation=""):
    global score
    screen.fill(WHITE)
    if correct:
        feedback = font.render("Correct!", True, GREEN)
        correct_sound.play()
        score += 1
    else:
        feedback = font.render("Incorrect!", True, RED)
        incorrect_sound.play()
    
    screen.blit(feedback, feedback.get_rect(center=(WIDTH // 2, 250)))
    
    score_display = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_display, score_display.get_rect(center=(WIDTH // 2, 300)))
    
    render_wrapped_text(explanation, 350, BLACK, font_type=explanation_font)
    
    pygame.display.flip()
    pygame.time.wait(3000)



# Game Over Screen
def game_over():
    screen.blit(background_image, (0, 0))
    if hacker_health <= 0:
        render_text_centered("You Win!", 200, GREEN, font_type=title_font)
    elif user_health <= 0:
        render_text_centered("You Lose!", 200, RED, font_type=title_font)
    
    restart_button = draw_button("Restart", 400, GRAY, font_type=button_font)
    quit_button = draw_button("Quit", 500, GRAY, font_type=button_font)
    
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    main()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Main Game Loop
def main():
    global score, hacker_health, user_health
    score = 0
    hacker_health = 100
    user_health = 100
    main_menu()
    
    # Randomly select and display scenarios
    while hacker_health > 0 and user_health > 0:
        question_data = random.choice(questions)
        correct, explanation = game_scenario(question_data)
        display_feedback(correct, explanation)
    
    game_over()

if __name__ == "__main__":
    main()


