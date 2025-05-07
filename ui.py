#!/usr/bin/env python3
"""
EduRPG - Text-Based Educational RPG
UI module for terminal interface using Rich library
"""

import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich import box
from rich.text import Text

console = Console()

class UI:
    """UI class for EduRPG
    
    Handles terminal interface using Rich library
    """
    
    def __init__(self):
        """Initialize the UI"""
        self.console = Console()
        self.width = 80  # Default width for panels and tables
    
    def clear(self):
        """Clear the console"""
        self.console.clear()
    
    def print(self, text, style=None):
        """Print text to the console
        
        Args:
            text (str): Text to print
            style (str, optional): Rich style. Defaults to None.
        """
        self.console.print(text, style=style)
    
    def display_title(self):
        """Display the game title"""
        title_art = """
        ______    _       _____  _____   _____  
       |  ____|  | |     |  __ \|  __ \ / ____| 
       | |__   __| |_   _| |__) | |__) | |  __ 
       |  __| / _` | | | |  _  /|  ___/| | |_ |
       | |___| (_| | |_| | | \ \| |    | |__| |
       |______\__,_|\__,_|_|  \_\_|     \_____|
                                               
        [bold cyan]Educational Role-Playing Game[/bold cyan]
        """
        
        self.console.print(Panel(title_art, border_style="bright_blue", width=self.width))
        self.console.print("[italic]Learn, Battle, Grow![/italic]", justify="center")
        self.console.print()
    
    def display_menu(self, title, options):
        """Display a menu and get user choice
        
        Args:
            title (str): Menu title
            options (list): List of menu options
            
        Returns:
            int: Selected option index (0-based)
        """
        self.console.print(Panel(f"[bold]{title}[/bold]", border_style="cyan", width=self.width))
        
        for i, option in enumerate(options, 1):
            self.console.print(f"  [cyan]{i}.[/cyan] {option}")
        
        self.console.print()
        
        # Get user choice
        while True:
            choice = Prompt.ask("Enter your choice", console=self.console)
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return choice_num - 1  # Return 0-based index
                else:
                    self.console.print(f"[red]Please enter a number between 1 and {len(options)}[/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number[/red]")
    
    def get_input(self, prompt_text, default=None):
        """Get user input
        
        Args:
            prompt_text (str): Prompt text
            default (str, optional): Default value. Defaults to None.
            
        Returns:
            str: User input
        """
        return Prompt.ask(prompt_text, console=self.console, default=default)
    
    def get_confirmation(self, prompt_text):
        """Get user confirmation
        
        Args:
            prompt_text (str): Prompt text
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        return Confirm.ask(prompt_text, console=self.console)
    
    def display_player_creation(self):
        """Display player creation screen and get player info
        
        Returns:
            dict: Player info (name, grade)
        """
        self.clear()
        self.display_title()
        
        self.console.print(Panel("[bold]Character Creation[/bold]", border_style="green", width=self.width))
        
        name = self.get_input("Enter your character name")
        
        # Grade selection
        grades = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "College"]
        self.console.print("\n[bold]Select your grade level:[/bold]")
        for i, grade in enumerate(grades, 1):
            self.console.print(f"  [cyan]{i}.[/cyan] Grade {grade}")
        
        while True:
            grade_choice = self.get_input("Enter grade number")
            try:
                grade_idx = int(grade_choice) - 1
                if 0 <= grade_idx < len(grades):
                    grade = grades[grade_idx]
                    break
                else:
                    self.console.print(f"[red]Please enter a number between 1 and {len(grades)}[/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number[/red]")
        
        self.console.print(f"\n[green]Character created: [bold]{name}[/bold] (Grade {grade})[/green]")
        time.sleep(1.5)
        
        return {"name": name, "grade": grade}
    
    def display_player_stats(self, player):
        """Display player stats
        
        Args:
            player (Player): Player object
        """
        # Create a table for player stats
        table = Table(box=box.ROUNDED, width=self.width-4)
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="green")
        
        # Add basic info
        table.add_row("Name", player.name)
        table.add_row("Grade", player.grade)
        table.add_row("Level", str(player.level))
        table.add_row("XP", f"{player.xp}/{player.xp_to_next_level}")
        
        # Add traits
        for trait, value in player.traits.items():
            table.add_row(f"{trait.capitalize()} Trait", str(value))
        
        # Add guild info if applicable
        if player.guild_id:
            table.add_row("Guild", player.guild_id)
        else:
            table.add_row("Guild", "None")
        
        # Display the table in a panel
        self.console.print(Panel(table, title="[bold]Character Stats[/bold]", border_style="bright_blue", width=self.width))
    
    def display_inventory(self, player):
        """Display player inventory
        
        Args:
            player (Player): Player object
        """
        if not player.inventory:
            self.console.print(Panel("Your inventory is empty.", title="[bold]Inventory[/bold]", border_style="yellow", width=self.width))
            return
        
        # Create a table for inventory
        table = Table(box=box.SIMPLE, width=self.width-4)
        table.add_column("Item", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Effect", style="magenta")
        
        for item in player.inventory:
            table.add_row(item["name"], item["description"], item["effect"])
        
        # Display the table in a panel
        self.console.print(Panel(table, title="[bold]Inventory[/bold]", border_style="yellow", width=self.width))
    
    def display_skills(self, player):
        """Display player skills
        
        Args:
            player (Player): Player object
        """
        if not player.skills:
            self.console.print(Panel("You haven't unlocked any skills yet.", title="[bold]Skills[/bold]", border_style="magenta", width=self.width))
            return
        
        # Create a table for skills
        table = Table(box=box.SIMPLE, width=self.width-4)
        table.add_column("Skill", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Requirements", style="magenta")
        
        for skill in player.skills:
            table.add_row(skill["name"], skill["description"], skill["requirements"])
        
        # Display the table in a panel
        self.console.print(Panel(table, title="[bold]Skills[/bold]", border_style="magenta", width=self.width))
    
    def display_combat_start(self, enemy):
        """Display combat start screen
        
        Args:
            enemy (Enemy): Enemy object
        """
        self.clear()
        
        # Display enemy encounter message
        self.console.print(Panel(f"[bold red]A wild {enemy.name} appears![/bold red]", border_style="red", width=self.width))
        
        # Display enemy sprite
        self.console.print(Panel(enemy.sprite, border_style="red", width=self.width))
        
        # Display enemy info
        self.console.print(f"[bold]Subject:[/bold] {enemy.subject}")
        self.console.print(f"[bold]HP:[/bold] {enemy.hp}")
        self.console.print()
        
        # Dramatic pause
        time.sleep(1)
        self.console.print("[bold yellow]Prepare for battle![/bold yellow]")
        time.sleep(1)
    
    def display_question(self, question):
        """Display a question and get user answer
        
        Args:
            question (dict): Question dictionary
            
        Returns:
            str: User answer
        """
        # Display question
        self.console.print(Panel(question["text"], title="[bold]Question[/bold]", border_style="cyan", width=self.width))
        
        # Display options if multiple choice
        if "options" in question and question["options"]:
            for i, option in enumerate(question["options"], 1):
                self.console.print(f"  [cyan]{i}.[/cyan] {option}")
            
            # Get user choice
            while True:
                choice = self.get_input("Enter your answer (number)")
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(question["options"]):
                        return question["options"][choice_num - 1]  # Return the selected option
                    else:
                        self.console.print(f"[red]Please enter a number between 1 and {len(question['options'])}[/red]")
                except ValueError:
                    self.console.print("[red]Please enter a valid number[/red]")
        else:
            # Free response question
            return self.get_input("Enter your answer")
    
    def display_answer_result(self, is_correct, correct_answer=None, explanation=None):
        """Display the result of an answer
        
        Args:
            is_correct (bool): Whether the answer is correct
            correct_answer (str, optional): The correct answer. Defaults to None.
            explanation (str, optional): Explanation of the answer. Defaults to None.
        """
        if is_correct:
            self.console.print(Panel("[bold green]Correct![/bold green]", border_style="green", width=self.width))
        else:
            panel_content = f"[bold red]Incorrect![/bold red]\n\n"
            if correct_answer:
                panel_content += f"The correct answer is: [bold]{correct_answer}[/bold]\n\n"
            if explanation:
                panel_content += f"Explanation: {explanation}"
            
            self.console.print(Panel(panel_content, border_style="red", width=self.width))
        
        time.sleep(1.5)
    
    def display_combat_status(self, player_hp, enemy_hp, enemy_name):
        """Display combat status
        
        Args:
            player_hp (int): Player HP
            enemy_hp (int): Enemy HP
            enemy_name (str): Enemy name
        """
        # Create a table for combat status
        table = Table(box=box.SIMPLE, width=self.width-4)
        table.add_column("Combatant", style="cyan")
        table.add_column("HP", style="green")
        
        table.add_row("You", self._create_hp_bar(player_hp, 100))
        table.add_row(enemy_name, self._create_hp_bar(enemy_hp, enemy_hp if enemy_hp > 0 else 100))
        
        # Display the table in a panel
        self.console.print(Panel(table, title="[bold]Combat Status[/bold]", border_style="red", width=self.width))
    
    def _create_hp_bar(self, current, maximum, width=30):
        """Create an HP bar
        
        Args:
            current (int): Current HP
            maximum (int): Maximum HP
            width (int, optional): Bar width. Defaults to 30.
            
        Returns:
            str: HP bar string
        """
        percentage = current / maximum
        filled_width = int(width * percentage)
        empty_width = width - filled_width
        
        if percentage > 0.6:
            color = "green"
        elif percentage > 0.3:
            color = "yellow"
        else:
            color = "red"
        
        bar = f"[{color}]{'█' * filled_width}[/{color}]{' ' * empty_width} {current}/{maximum}"
        return bar
    
    def display_combat_end(self, victory, xp_gained=0, items_gained=None):
        """Display combat end screen
        
        Args:
            victory (bool): Whether the player won
            xp_gained (int, optional): XP gained. Defaults to 0.
            items_gained (list, optional): Items gained. Defaults to None.
        """
        if victory:
            self.console.print(Panel("[bold green]Victory![/bold green]", border_style="green", width=self.width))
            
            # Display rewards
            rewards_text = f"XP gained: [bold]{xp_gained}[/bold]\n"
            
            if items_gained:
                rewards_text += "\nItems gained:\n"
                for item in items_gained:
                    rewards_text += f"- [cyan]{item['name']}[/cyan]: {item['description']}\n"
            
            self.console.print(Panel(rewards_text, title="[bold]Rewards[/bold]", border_style="yellow", width=self.width))
        else:
            self.console.print(Panel("[bold red]Defeat![/bold red]\n\nDon't worry, you can try again!", border_style="red", width=self.width))
        
        time.sleep(2)
    
    def display_level_up(self, new_level, trait_increases=None):
        """Display level up screen
        
        Args:
            new_level (int): New level
            trait_increases (dict, optional): Trait increases. Defaults to None.
        """
        self.console.print(Panel(f"[bold yellow]Level Up![/bold yellow]\n\nYou are now level [bold]{new_level}[/bold]!", border_style="yellow", width=self.width))
        
        if trait_increases:
            traits_text = "Trait increases:\n"
            for trait, increase in trait_increases.items():
                traits_text += f"- [cyan]{trait.capitalize()}[/cyan]: +{increase}\n"
            
            self.console.print(Panel(traits_text, border_style="cyan", width=self.width))
        
        time.sleep(2)
    
    def display_guild_list(self, guilds):
        """Display list of guilds
        
        Args:
            guilds (list): List of guild dictionaries
            
        Returns:
            int: Selected guild index, or -1 to create new guild, or -2 to cancel
        """
        self.clear()
        
        self.console.print(Panel("[bold]Available Guilds[/bold]", border_style="blue", width=self.width))
        
        if not guilds:
            self.console.print("No guilds available. Create a new one!")
            
            if self.get_confirmation("Create a new guild?"):
                return -1  # Create new guild
            else:
                return -2  # Cancel
        
        # Display guild list
        table = Table(box=box.SIMPLE, width=self.width-4)
        table.add_column("#", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Members", style="magenta")
        table.add_column("Level", style="yellow")
        
        for i, guild in enumerate(guilds, 1):
            table.add_row(
                str(i),
                guild["name"],
                str(len(guild["members"])),
                str(guild["level"])
            )
        
        self.console.print(table)
        self.console.print()
        
        # Options
        self.console.print("[cyan]0.[/cyan] Create a new guild")
        self.console.print("[cyan]C.[/cyan] Cancel")
        self.console.print()
        
        # Get user choice
        while True:
            choice = self.get_input("Enter your choice").lower()
            
            if choice == "c":
                return -2  # Cancel
            
            try:
                choice_num = int(choice)
                if choice_num == 0:
                    return -1  # Create new guild
                elif 1 <= choice_num <= len(guilds):
                    return choice_num - 1  # Return 0-based index
                else:
                    self.console.print(f"[red]Please enter a number between 0 and {len(guilds)}[/red]")
            except ValueError:
                self.console.print("[red]Please enter a valid number or 'C' to cancel[/red]")
    
    def display_guild_creation(self):
        """Display guild creation screen and get guild info
        
        Returns:
            dict: Guild info (name, description)
        """
        self.clear()
        
        self.console.print(Panel("[bold]Guild Creation[/bold]", border_style="blue", width=self.width))
        
        name = self.get_input("Enter guild name")
        description = self.get_input("Enter guild description")
        
        self.console.print(f"\n[green]Guild created: [bold]{name}[/bold][/green]")
        time.sleep(1.5)
        
        return {"name": name, "description": description}
    
    def display_guild_details(self, guild):
        """Display guild details
        
        Args:
            guild (Guild): Guild object
        """
        self.clear()
        
        # Guild info panel
        guild_info = f"[bold]{guild.name}[/bold]\n\n{guild.description}\n\nLevel: {guild.level}\nXP: {guild.xp}/{guild.xp_to_next_level}\nMembers: {len(guild.members)}"
        self.console.print(Panel(guild_info, title="[bold]Guild Info[/bold]", border_style="blue", width=self.width))
        
        # Members table
        if guild.members:
            table = Table(box=box.SIMPLE, width=self.width-4)
            table.add_column("Member", style="cyan")
            table.add_column("Level", style="green")
            
            for member in guild.members:
                table.add_row(member["name"], str(member["level"]))
            
            self.console.print(Panel(table, title="[bold]Members[/bold]", border_style="cyan", width=self.width))
        
        # Active quests
        if guild.quests:
            active_quests = [q for q in guild.quests if not q["completed"]]
            if active_quests:
                quests_table = Table(box=box.SIMPLE, width=self.width-4)
                quests_table.add_column("Quest", style="cyan")
                quests_table.add_column("Progress", style="green")
                quests_table.add_column("Reward", style="yellow")
                
                for quest in active_quests:
                    progress = f"{quest['progress']}/{quest['target']}"
                    quests_table.add_row(quest["name"], progress, quest["reward"])
                
                self.console.print(Panel(quests_table, title="[bold]Active Quests[/bold]", border_style="magenta", width=self.width))
    
    def display_guild_chat(self, chat_history):
        """Display guild chat
        
        Args:
            chat_history (list): List of chat message dictionaries
        """
        self.clear()
        
        self.console.print(Panel("[bold]Guild Chat[/bold]", border_style="green", width=self.width))
        
        if not chat_history:
            self.console.print("No messages yet. Be the first to say something!")
        else:
            # Display chat messages
            for message in chat_history:
                sender = message["sender"]
                text = message["text"]
                timestamp = message["timestamp"]
                
                self.console.print(f"[bold cyan]{sender}[/bold cyan] [dim]({timestamp})[/dim]")
                self.console.print(f"{text}\n")
        
        # Get new message
        new_message = self.get_input("Enter your message (or leave empty to exit)")
        
        return new_message
    
    def display_loading(self, message="Loading...", duration=1.0):
        """Display a loading spinner
        
        Args:
            message (str, optional): Loading message. Defaults to "Loading...".
            duration (float, optional): Duration in seconds. Defaults to 1.0.
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]{task.description}"),
            console=self.console,
            transient=True,
        ) as progress:
            task = progress.add_task(message, total=100)
            for _ in range(100):
                time.sleep(duration / 100)
                progress.update(task, advance=1)


# For testing
if __name__ == "__main__":
    ui = UI()
    
    # Test title display
    ui.clear()
    ui.display_title()
    
    # Test menu
    choice = ui.display_menu("Main Menu", ["New Game", "Load Game", "Options", "Exit"])
    ui.print(f"Selected option: {choice}")
    
    # Test loading
    ui.display_loading("Testing UI components...")