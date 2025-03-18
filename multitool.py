import os
import sys
import shutil
import time
import threading
import itertools
import questionary
import getpass
import webbrowser
from colorama import init, Fore, Style
from rich.console import Console

init(autoreset=True)
username = getpass.getuser()
console = Console()

# Loading Spinner
def loading_spinner():
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not loading_spinner.done:
        sys.stdout.write(f'\r{Fore.RED}Loading {Fore.LIGHTGREEN_EX}{next(spinner)} ')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 20 + '\r')
    sys.stdout.flush()

loading_spinner.done = False

def animate_loading(duration=1.0):
    loading_spinner.done = False
    spinner_thread = threading.Thread(target=loading_spinner)
    spinner_thread.start()
    time.sleep(duration)
    loading_spinner.done = True
    spinner_thread.join()

def get_terminal_width(default_width=80):
    try:
        width = shutil.get_terminal_size().columns
        return max(80, width)
    except Exception:
        return default_width

def set_cmd_title_and_color():
    if os.name == 'nt':
        os.system('title Modern Multitool Hub && color 0A')

def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def smooth_gradient_print(text, start_color, end_color):
    steps = len(text) - 1 if len(text) > 1 else 1
    r_start, g_start, b_start = start_color
    r_end, g_end, b_end = end_color
    gradient_text = "".join(
        f'\033[38;2;{int(r_start + (r_end - r_start) * (i / steps))};'
        f'{int(g_start + (g_end - g_start) * (i / steps))};'
        f'{int(b_start + (b_end - b_start) * (i / steps))}m{char}'
        for i, char in enumerate(text)
    )
    print(gradient_text + Style.RESET_ALL)

def center_text(text, width=None):
    return text.center(width or get_terminal_width())

ASCII_LOGO = r"""
 ▄▄▄██▀▀▀▄▄▄        █████  
   ▒██  ▒████▄    ▒██▓  ██▒
   ░██  ▒██  ▀█▄  ▒██▒  ██░
▓██▄██▓ ░██▄▄▄▄██ ░██  █▀ ░
 ▓███▒   ▓█   ▓██▒░▒███▒█▄ 
 ▒▓▒▒░   ▒▒   ▓▒█░░░ ▒▒░ ▒ 
 ▒ ░▒░    ▒   ▒▒ ░ ░ ▒░  ░ 
 ░ ░ ░    ░   ▒      ░   ░ 
 ░   ░        ░  ░    ░    
              JAQLIV                  
"""

def print_ascii_logo():
    width = get_terminal_width()
    for line in ASCII_LOGO.splitlines():
        smooth_gradient_print(center_text(line, width), current_gradient_start, current_gradient_end)

TOOLS = {
    '1': {'name': 'Guns.lol', 'function': 'open_guns_lol', 'page': 1},
    '2': {'name': 'GitHub', 'function': 'open_github', 'page': 1},
    '3': {'name': 'Settings', 'function': 'show_settings', 'page': 1},
    '4': {'name': 'Exit', 'function': 'exit_tool', 'page': 1},
}

# Globale Farbvariablen
current_gradient_start = (0, 255, 255)  # Cyan
current_gradient_end = (255, 69, 0)     # Orange

# Erweiterte Farbpalette
COLOR_SCHEMES = {
    "Cyan to Orange (Default)": [(0, 255, 255), (255, 69, 0)],
    "Purple to Pink": [(128, 0, 128), (255, 105, 180)],
    "Blue to Green": [(0, 0, 255), (0, 255, 0)],
    "Red to Yellow": [(255, 0, 0), (255, 255, 0)],
    "Green to Cyan": [(0, 128, 0), (0, 255, 255)],
    "Magenta to Yellow": [(255, 0, 255), (255, 255, 0)],
    "Blue to Purple": [(0, 0, 255), (128, 0, 128)],
    "Gold to Red": [(255, 215, 0), (255, 0, 0)],
    "Teal to Lime": [(0, 128, 128), (50, 205, 50)],
    "Navy to Cyan": [(0, 0, 128), (0, 255, 255)],
    "Crimson to Pink": [(220, 20, 60), (255, 192, 203)],
    "Forest to Yellow": [(34, 139, 34), (255, 255, 0)],
    "Violet to Orange": [(238, 130, 238), (255, 165, 0)],
    "Indigo to Cyan": [(75, 0, 130), (0, 255, 255)],
    "Coral to Blue": [(255, 127, 80), (0, 0, 255)]
}

# Dynamische Farben für questionary
def get_custom_style():
    start_hex = rgb_to_hex(*current_gradient_start)
    end_hex = rgb_to_hex(*current_gradient_end)
    mid_r = int((current_gradient_start[0] + current_gradient_end[0]) / 2)
    mid_g = int((current_gradient_start[1] + current_gradient_end[1]) / 2)
    mid_b = int((current_gradient_start[2] + current_gradient_end[2]) / 2)
    mid_hex = rgb_to_hex(mid_r, mid_g, mid_b)
    return questionary.Style([
        ("question", f"bold {start_hex}"),
        ("answer", mid_hex),
        ("pointer", end_hex),
        ("selected", f"bold {end_hex}"),
        ("input", mid_hex),
        ("highlighted", end_hex),
        ("instruction", mid_hex),
        ("text", f"bold {start_hex}"),
        ("prompt", start_hex),
    ])

def print_menu(page=1):
    global current_gradient_start, current_gradient_end
    os.system('cls' if os.name == 'nt' else 'clear')
    width = get_terminal_width()
    print_ascii_logo()

    border_top = "╓" + "─" * (width - 2) + "╖"
    border_bottom = "╙" + "─" * (width - 2) + "╜"
    smooth_gradient_print(border_top, current_gradient_start, current_gradient_end)
    smooth_gradient_print(center_text("MODERN MULTITOOL HUB", width), current_gradient_start, current_gradient_end)
    smooth_gradient_print(center_text("For educational purposes only", width), current_gradient_start, current_gradient_end)
    smooth_gradient_print(border_bottom, current_gradient_start, current_gradient_end)
    print()

    menu_items = [
        "[01] Guns.lol",
        "[02] GitHub",
        "[03] Settings",
        "[04] Exit"
    ]

    # Berechne die Länge des längsten Menüeintrags
    max_length = max(len(item) for item in menu_items)
    
    # Füge Rahmen hinzu
    menu_with_border = []
    menu_with_border.append("┌" + "─" * (max_length + 8) + "┐")
    
    for item in menu_items:
        centered_item = f"│    {item}" + " " * (max_length - len(item) + 4) + "│"
        menu_with_border.append(centered_item)
    
    menu_with_border.append("└" + "─" * (max_length + 8) + "┘")
    
    # Zentriere und drucke das Menü mit Farbverlauf
    for item in menu_with_border:
        smooth_gradient_print(center_text(item, width), current_gradient_start, current_gradient_end)
    
    print()

# Tool-Funktionen
def open_guns_lol():
    print()
    animate_loading(0.3)
    smooth_gradient_print(center_text("Opening Guns.lol...", get_terminal_width()), 
                         current_gradient_start, current_gradient_end)
    webbrowser.open("https://guns.lol/jaqliv")
    smooth_gradient_print(center_text("Redirected to https://guns.lol/jaqliv!", get_terminal_width()), 
                         current_gradient_start, current_gradient_end)

def open_github():
    print()
    animate_loading(0.3)
    smooth_gradient_print(center_text("Opening GitHub Repository...", get_terminal_width()), 
                         current_gradient_start, current_gradient_end)
    webbrowser.open("https://github.com/JAQLIV")

def show_settings():
    global current_gradient_start, current_gradient_end
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_ascii_logo()
        width = get_terminal_width()
        
        settings_border_top = "┌" + "─" * (width - 20) + "┐"
        settings_border_bottom = "└" + "─" * (width - 20) + "┘"
        
        smooth_gradient_print(center_text(settings_border_top, width), current_gradient_start, current_gradient_end)
        smooth_gradient_print(center_text("│ SETTINGS MENU │".center(width - 20), width), 
                             current_gradient_start, current_gradient_end)
        smooth_gradient_print(center_text(settings_border_bottom, width), current_gradient_start, current_gradient_end)
        print()
        
        choice = questionary.select(
            "Choose an option:",
            choices=[
                "Change Color Scheme",
                "Back to Main Menu"
            ],
            style=get_custom_style()
        ).ask()
        
        if choice == "Change Color Scheme":
            os.system('cls' if os.name == 'nt' else 'clear')
            print_ascii_logo()
            
            color_border_top = "┌" + "─" * (width - 20) + "┐"
            color_border_bottom = "└" + "─" * (width - 20) + "┘"
            
            smooth_gradient_print(center_text(color_border_top, width), current_gradient_start, current_gradient_end)
            smooth_gradient_print(center_text("│ COLOR SCHEMES │".center(width - 20), width), 
                                 current_gradient_start, current_gradient_end)
            smooth_gradient_print(center_text(color_border_bottom, width), current_gradient_start, current_gradient_end)
            print()
            
            color_choices = list(COLOR_SCHEMES.keys())
            
            color = questionary.select(
                "Select a gradient color scheme:",
                choices=color_choices,
                style=get_custom_style()
            ).ask()
            
            if color in COLOR_SCHEMES:
                current_gradient_start, current_gradient_end = COLOR_SCHEMES[color]
                
                os.system('cls' if os.name == 'nt' else 'clear')
                print_ascii_logo()
                smooth_gradient_print(center_text(f"Color scheme changed to {color}!", width), 
                                     current_gradient_start, current_gradient_end)
                time.sleep(1.5)
        
        elif choice == "Back to Main Menu":
            return

def exit_tool():
    width = get_terminal_width()
    animate_loading(0.5)
    smooth_gradient_print(center_text("Exiting... Goodbye!", width), current_gradient_start, current_gradient_end)
    time.sleep(0.5)
    sys.exit()

def run_tool():
    set_cmd_title_and_color()
    current_page = 1
    while True:
        print_menu(current_page)
        width = get_terminal_width()
        
        # Zentriere den Eingabeprompt
        prompt_text = f"┌──({username}@ModernMultitoolHub)─[~/main]"
        prompt_arrow = " └─$"
        
        # Wir berechnen Offset für den Pfeil basierend auf der Breite
        prompt_offset = (width - len(prompt_text) - len(prompt_arrow)) // 2
        centered_prompt = " " * prompt_offset + prompt_text + "\n" + " " * prompt_offset + prompt_arrow
        
        choice = questionary.text(
            centered_prompt,
            qmark="",
            style=get_custom_style(),
        ).ask()

        if choice.lower() == 'e':
            exit_tool()

        elif choice in TOOLS:
            tool = TOOLS[choice]
            if tool['page'] == current_page:
                if tool['function'] == 'open_guns_lol':
                    open_guns_lol()
                elif tool['function'] == 'open_github':
                    open_github()
                elif tool['function'] == 'show_settings':
                    show_settings()
                elif tool['function'] == 'exit_tool':
                    exit_tool()
            else:
                animate_loading(0.3)
                smooth_gradient_print(center_text("Invalid page selection!", width), 
                                     current_gradient_start, current_gradient_end)
        else:
            animate_loading(0.3)
            smooth_gradient_print(center_text("Invalid Choice. Please Select a Valid Option", width), 
                                 current_gradient_start, current_gradient_end)

        if choice.lower() not in ['e']:
            print()
            smooth_gradient_print(center_text("Press 'Enter' to Continue...", width), 
                                 current_gradient_start, current_gradient_end)
            input()
        
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    run_tool()