#!/usr/bin/env python3
"""
EduRPG - Text-Based Educational RPG
Main entry point for the terminal application
"""

import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm

# Import game modules
from player import Player
from combat import CombatSystem
from guild import GuildSystem
from database import Database
from ui import UI

# Initialize console
console = Console()

class Game:
    """Main game class for EduRPG"""
    
    def __init__(self):
        """Initialize the game"""
        self.ui = UI()
        self.db = Database()
        self.player = None
        self.combat = None
        self.guild = None
        self.running = True
    
    def start(self):
        """Start the game"""
        self.ui.display_title()
        self.main_menu()
    
    def main_menu(self):
        """Display the main menu"""
        while self.running:
            choice = self.ui.display_main_menu()
            
            if choice == "new_game":
                self.new_game()
            elif choice == "load_game":
                self.load_game()
            elif choice == "guild":
                if self.player:
                    self.guild_menu()
                else:
                    console.print("[yellow]You need to start or load a game first![/yellow]")
            elif choice == "help":
                self.help_menu()
            elif choice == "exit":
                self.exit_game()
    
    def new_game(self):
        """Create a new game"""
        name = Prompt.ask("[bold cyan]Enter your character name[/bold cyan]")
        grade_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "college"]
        grade = self.ui.select_option("Select your grade", grade_options)
        
        self.player = Player(name, grade)
        self.combat = CombatSystem(self.player)
        self.guild = GuildSystem(self.player, self.db)
        
        console.print(f"\n[green]Welcome, {name}! You are now a Level 1 student in grade {grade}.[/green]")
        time.sleep(1)
        self.game_menu()
    
    def load_game(self):
        """Load a saved game"""
        # This would connect to Firebase to load saved games
        console.print("[yellow]Loading game...[/yellow]")
        # Placeholder for loading functionality
        console.print("[red]No saved games found. Please start a new game.[/red]")
    
    def game_menu(self):
        """Display the game menu"""
        while self.player and self.running:
            choice = self.ui.display_game_menu(self.player)
            
            if choice == "battle":
                self.combat.start_battle()
            elif choice == "profile":
                self.ui.display_profile(self.player)
            elif choice == "guild":
                self.guild_menu()
            elif choice == "save":
                self.save_game()
            elif choice == "main_menu":
                if Confirm.ask("Return to main menu? Your progress will be lost if not saved"):
                    break
    
    def guild_menu(self):
        """Display the guild menu"""
        console.print("[yellow]Guild system coming soon![/yellow]")
    
    def save_game(self):
        """Save the current game"""
        console.print("[yellow]Saving game...[/yellow]")
        # Placeholder for saving functionality
        console.print("[green]Game saved successfully![/green]")
    
    def help_menu(self):
        """Display the help menu"""
        self.ui.display_help()
    
    def exit_game(self):
        """Exit the game"""
        if self.player:
            if Confirm.ask("Exit game? Your progress will be lost if not saved"):
                self.running = False
        else:
            self.running = False
        console.print("[green]Thank you for playing EduRPG![/green]")


if __name__ == "__main__":
    game = Game()
    try:
        game.start()
    except KeyboardInterrupt:
        console.print("\n[yellow]Game interrupted. Exiting...[/yellow]")
    except Exception as e:
        console.print(f"\n[red]An error occurred: {e}[/red]")
    sys.exit(0)