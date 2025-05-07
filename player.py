#!/usr/bin/env python3
"""
EduRPG - Text-Based Educational RPG
Player module for character management and progression
"""

import json
from rich.console import Console

console = Console()

class Player:
    """Player class for EduRPG"""
    
    def __init__(self, name, grade):
        """Initialize a new player
        
        Args:
            name (str): Player's name
            grade (str): Player's grade level (1-12 or 'college')
        """
        self.name = name
        self.grade = grade
        self.level = 1
        self.xp = 0
        self.traits = {
            "math": 0,
            "science": 0,
            "history": 0,
            "language": 0,
            "arts": 0
        }
        self.inventory = []
        self.skills = []
        self.guild_id = None
        
        # Initialize level thresholds
        self.level_thresholds = self._generate_level_thresholds()
    
    def _generate_level_thresholds(self):
        """Generate XP thresholds for each level
        
        Returns:
            dict: Level thresholds with level as key and XP required as value
        """
        thresholds = {}
        for level in range(1, 51):  # Max level 50
            # Exponential growth formula: base_xp * (growth_factor ^ (level - 1))
            thresholds[level] = int(100 * (1.5 ** (level - 1)))
        return thresholds
    
    def gain_xp(self, amount, subject=None):
        """Add XP to the player and check for level up
        
        Args:
            amount (int): Amount of XP to add
            subject (str, optional): Subject to add trait points to. Defaults to None.
        
        Returns:
            bool: True if player leveled up, False otherwise
        """
        self.xp += amount
        
        # Add trait points if subject is specified
        if subject and subject in self.traits:
            self.traits[subject] += amount // 10  # 10% of XP goes to trait
        
        # Check for level up
        leveled_up = False
        while self.level < 50 and self.xp >= self.level_thresholds[self.level + 1]:
            self.level += 1
            leveled_up = True
            console.print(f"[bold green]🎉 Level Up! You are now Level {self.level}![/bold green]")
            
            # Check for skill unlocks
            new_skills = self._check_skill_unlocks()
            for skill in new_skills:
                console.print(f"[bold cyan]🔓 New Skill Unlocked: {skill}[/bold cyan]")
        
        return leveled_up
    
    def _check_skill_unlocks(self):
        """Check if any new skills are unlocked at the current level
        
        Returns:
            list: List of newly unlocked skills
        """
        new_skills = []
        
        # Define skills that unlock at specific levels and trait requirements
        skill_requirements = {
            "Math Mastery I": {"level": 5, "trait": {"math": 50}},
            "Science Explorer": {"level": 5, "trait": {"science": 50}},
            "History Buff": {"level": 5, "trait": {"history": 50}},
            "Language Expert": {"level": 5, "trait": {"language": 50}},
            "Creative Genius": {"level": 5, "trait": {"arts": 50}},
            "Math Mastery II": {"level": 10, "trait": {"math": 100}},
            "Scientific Method": {"level": 10, "trait": {"science": 100}},
            "Historical Analysis": {"level": 10, "trait": {"history": 100}},
            "Linguistic Mastery": {"level": 10, "trait": {"language": 100}},
            "Artistic Vision": {"level": 10, "trait": {"arts": 100}},
            "Math Prodigy": {"level": 20, "trait": {"math": 200}},
            "Scientific Genius": {"level": 20, "trait": {"science": 200}},
            "Historical Scholar": {"level": 20, "trait": {"history": 200}},
            "Polyglot": {"level": 20, "trait": {"language": 200}},
            "Master Artist": {"level": 20, "trait": {"arts": 200}},
        }
        
        # Check each skill
        for skill_name, requirements in skill_requirements.items():
            if (
                skill_name not in self.skills and
                self.level >= requirements["level"]
            ):
                # Check trait requirements
                meets_trait_req = True
                for trait_name, trait_value in requirements["trait"].items():
                    if self.traits.get(trait_name, 0) < trait_value:
                        meets_trait_req = False
                        break
                
                if meets_trait_req:
                    self.skills.append(skill_name)
                    new_skills.append(skill_name)
        
        return new_skills
    
    def add_to_inventory(self, item):
        """Add an item to the player's inventory
        
        Args:
            item (dict): Item to add to inventory
        """
        self.inventory.append(item)
        console.print(f"[green]Added {item['name']} to your inventory![/green]")
    
    def remove_from_inventory(self, item_name):
        """Remove an item from the player's inventory
        
        Args:
            item_name (str): Name of the item to remove
            
        Returns:
            dict: The removed item, or None if not found
        """
        for i, item in enumerate(self.inventory):
            if item["name"] == item_name:
                removed_item = self.inventory.pop(i)
                console.print(f"[yellow]Removed {item_name} from your inventory.[/yellow]")
                return removed_item
        
        console.print(f"[red]Item {item_name} not found in inventory.[/red]")
        return None
    
    def join_guild(self, guild_id):
        """Join a guild
        
        Args:
            guild_id (str): ID of the guild to join
        """
        self.guild_id = guild_id
        console.print(f"[green]You have joined a new guild![/green]")
    
    def leave_guild(self):
        """Leave the current guild"""
        if self.guild_id:
            self.guild_id = None
            console.print(f"[yellow]You have left your guild.[/yellow]")
        else:
            console.print(f"[yellow]You are not in a guild.[/yellow]")
    
    def get_xp_to_next_level(self):
        """Get the amount of XP needed to reach the next level
        
        Returns:
            int: XP needed for next level, or 0 if at max level
        """
        if self.level >= 50:  # Max level
            return 0
        
        next_level_xp = self.level_thresholds[self.level + 1]
        return next_level_xp - self.xp
    
    def get_progress_percentage(self):
        """Get the progress percentage to the next level
        
        Returns:
            float: Percentage progress to next level (0-100)
        """
        if self.level >= 50:  # Max level
            return 100.0
        
        current_level_xp = self.level_thresholds[self.level]
        next_level_xp = self.level_thresholds[self.level + 1]
        xp_for_this_level = next_level_xp - current_level_xp
        xp_gained_in_level = self.xp - current_level_xp
        
        return min(100.0, (xp_gained_in_level / xp_for_this_level) * 100)
    
    def to_dict(self):
        """Convert player data to dictionary for saving
        
        Returns:
            dict: Player data as dictionary
        """
        return {
            "name": self.name,
            "grade": self.grade,
            "level": self.level,
            "xp": self.xp,
            "traits": self.traits,
            "inventory": self.inventory,
            "skills": self.skills,
            "guild_id": self.guild_id
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a player from dictionary data
        
        Args:
            data (dict): Player data
            
        Returns:
            Player: New player instance
        """
        player = cls(data["name"], data["grade"])
        player.level = data["level"]
        player.xp = data["xp"]
        player.traits = data["traits"]
        player.inventory = data["inventory"]
        player.skills = data["skills"]
        player.guild_id = data["guild_id"]
        return player
    
    def save_to_file(self, filename):
        """Save player data to a JSON file
        
        Args:
            filename (str): File to save to
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
            return True
        except Exception as e:
            console.print(f"[red]Error saving player data: {e}[/red]")
            return False
    
    @classmethod
    def load_from_file(cls, filename):
        """Load player data from a JSON file
        
        Args:
            filename (str): File to load from
            
        Returns:
            Player: New player instance, or None if error
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except Exception as e:
            console.print(f"[red]Error loading player data: {e}[/red]")
            return None