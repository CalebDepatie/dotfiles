#!/usr/bin/env python3

# curses should be installed by default on unix
import curses
import os
import sys
import subprocess

# TODO: Clean up the code

# Config variable setup
config = {}
config['size'] = os.get_terminal_size()
config['home_path'] = '~/'
config['packages'] = ['atom', 'kitty', 'zsh']
config['devtools'] = ['meson', 'llvm']
config['font'] = 'https://download.jetbrains.com/fonts/JetBrainsMono-1.0.3.zip?_ga=2.59111342.2034427416.1593382366-1719389182.1592084656'
uname = os.uname()
if "Ubuntu" in uname[3]:
    config['install'] = 'apt install'
    config['download'] = 'wget'
else:
    print("Undefined OS. Please update installer.py")
    sys.exit()

# Useful functions
def quit_curses():
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    curses.curs_set(1)
def centre_string(string, x):
    screen.addstr(x, int((config['size'][0]/2)-(len(string)/2)), string)
def centre_styled_string(string, x, args):
    screen.addstr(x, int((config['size'][0]/2)-(len(string)/2)), string, args)
def selected_option(cursor, index):
    if cursor != index:
        return curses.color_pair(2)
    else:
        return curses.A_STANDOUT | curses.color_pair(3)
# I just like this look, TODO: should have the [] be useful
def install_output(message, y, ok):
    if ok:
        screen.addstr(y, 1, "[ OK ]", curses.A_BOLD | curses.color_pair(1))
        x = 8
    else:
        screen.addstr(y, 1, "[ FAILED ]", curses.A_BOLD | curses.color_pair(1))
        x = 12
    screen.addstr(y, x, message, curses.color_pair(2))
    screen.refresh()

screen = curses.initscr()
curses.start_color()
curses.cbreak()
curses.noecho()
screen.keypad(True)

curses.curs_set(0)

# Setup colour pairs
curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

def install():
    y = 3
    screen.clear()
    centre_styled_string("Dotfiles Installer", 1, curses.A_BOLD | curses.color_pair(1))
    screen.refresh()
    total_items_to_install = len(config['packages']) + len(config['devtools']) + 1 + 4 # Font(1) + dotfiles(4)
    total_items_installed = 0 # TODO: Progress bar
    # Install base packages
    for package in config['packages']:
        subprocess.run([config['install'] + ' ' + package], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)

    install_output("Packages Installed", y++, True)

    # Font install
    subprocess.run(['wget -q --output-document=font.zip ' + config['font']], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)
    subprocess.run(['unzip -o font.zip'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)
    subprocess.run(['mv -u JetBrainsMono-1.0.3 /usr/share/fonts/'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)
    subprocess.run(['fc-cache -f -v'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)
    subprocess.run(['rm font.zip'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)

    install_output("Font Installed", y++, True)

    # TODO: Add Oh-My-Zsh installation

    # Move config files to proper places
    # TODO: Change this to sym linking
    subprocess.run(['mv -u configs/.bashrc ~/'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)
    subprocess.run(['mv -u configs/.zshrc ~/'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)
    subprocess.run(['mv -u configs/kitty.conf ~/.config/kitty/'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)
    subprocess.run(['mv -u configs/atom/config.cson ~/.atom/'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)
    subprocess.run(['mv -u configs/atom/accentsui-modified-ui ~/.atom/packages'], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)

    install_output("Dotfiles Installed", y++, True)

    # Install full dev environment
    # TODO: Install atom packages
    for package in config['devtools']:
        subprocess.run([config['install'] + ' ' + package], shell=True, executable='/bin/bash', stdout=subprocess.DEVNULL)

    install_output("Dev Tools Intalled", y++, True)

    centre_styled_string("Press Any Button to Return", y++, curses.A_BOLD | curses.color_pair(1))

    c = screen.getch()

# Enum for handling the different options to make it easy to add more
# TODO: Finish the custom install
from enum import IntEnum
class options(IntEnum):
    INSTALL = 1
    CUSTOM_INSTALL = 3
    QUIT = 2

def handle_options(x):
    if x == options.INSTALL:
        install()
    elif x == options.CUSTOM_INSTALL:
        pass
    elif x == options.QUIT:
        quit_curses()
        sys.exit()


def main_page():
    end = False
    cursor = 1
    total_options = options.QUIT # Quit should always be the last option
    while not end:
        # Setup main install page
        screen.clear()
        centre_styled_string("Dotfiles Installer", 1, curses.A_BOLD | curses.color_pair(1))
        centre_styled_string("[ Full Install ]", 4, selected_option(cursor, options.INSTALL))
        #centre_styled_string("[ Custom Install ]", 6, selected_option(cursor, options.CUSTOM_INSTALL))
        centre_styled_string("[ Quit ]", 6, selected_option(cursor, options.QUIT))
        screen.refresh()
        # Handle key input
        c = screen.getch()
        if c == curses.KEY_UP:
            cursor-=1
            if cursor <= 0:
                cursor = total_options
        elif c == curses.KEY_DOWN:
            cursor+=1
            if cursor >= total_options+1:
                cursor = 1
        elif c == 10: # ASCII Enter key
            handle_options(cursor)

main_page()

# Exit the installer here in case something broke
quit_curses()
