#!/usr/bin/env python3
"""
EduRPG - Text-Based Educational RPG
Guild module for collaborative features
"""

import time
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

class Guild:
    """Guild class for collaborative gameplay"""
    
    def __init__(self, name, description, leader_id):
        """Initialize a new guild
        
        Args:
            name (str): Guild name
            description (str): Guild description
            leader_id (str): User ID of the guild leader
        """
        self.id = str(uuid.uuid4())[:8]  # Generate a short unique ID
        self.name = name
        self.description = description
        self.leader_id = leader_id
        self.members = {leader_id: "Leader"}  # User ID -> Role mapping
        self.quests = []  # List of active quests
        self.completed_quests = []  # List of completed quests
        self.chat_history = []  # List of chat messages
        self.created_at = time.time()
        self.xp = 0  # Guild XP
        self.level = 1  # Guild level
    
    def add_member(self, user_id, role="Member"):
        """Add a member to the guild
        
        Args:
            user_id (str): User ID to add
            role (str, optional): Role to assign. Defaults to "Member".
            
        Returns:
            bool: True if added, False if already a member
        """
        if user_id in self.members:
            return False
        
        self.members[user_id] = role
        return True
    
    def remove_member(self, user_id):
        """Remove a member from the guild
        
        Args:
            user_id (str): User ID to remove
            
        Returns:
            bool: True if removed, False if not a member or is leader
        """
        if user_id not in self.members or user_id == self.leader_id:
            return False
        
        del self.members[user_id]
        return True
    
    def change_role(self, user_id, new_role):
        """Change a member's role
        
        Args:
            user_id (str): User ID to change
            new_role (str): New role to assign
            
        Returns:
            bool: True if changed, False if not a member
        """
        if user_id not in self.members:
            return False
        
        self.members[user_id] = new_role
        return True
    
    def add_quest(self, quest):
        """Add a quest to the guild
        
        Args:
            quest (dict): Quest data
        """
        self.quests.append(quest)
    
    def complete_quest(self, quest_id):
        """Mark a quest as completed
        
        Args:
            quest_id (str): ID of the quest to complete
            
        Returns:
            bool: True if completed, False if not found
        """
        for i, quest in enumerate(self.quests):
            if quest["id"] == quest_id:
                completed_quest = self.quests.pop(i)
                completed_quest["completed_at"] = time.time()
                self.completed_quests.append(completed_quest)
                
                # Add XP to guild
                self.gain_xp(completed_quest["xp_reward"])
                
                return True
        
        return False
    
    def add_chat_message(self, user_id, user_name, message):
        """Add a chat message to the guild
        
        Args:
            user_id (str): ID of the user sending the message
            user_name (str): Name of the user sending the message
            message (str): Message content
        """
        self.chat_history.append({
            "user_id": user_id,
            "user_name": user_name,
            "message": message,
            "timestamp": time.time()
        })
        
        # Limit chat history to last 100 messages
        if len(self.chat_history) > 100:
            self.chat_history = self.chat_history[-100:]
    
    def gain_xp(self, amount):
        """Add XP to the guild and check for level up
        
        Args:
            amount (int): Amount of XP to add
            
        Returns:
            bool: True if guild leveled up, False otherwise
        """
        self.xp += amount
        
        # Check for level up (simple formula: level * 1000 XP needed)
        if self.xp >= self.level * 1000 and self.level < 50:  # Max level 50
            self.level += 1
            return True
        
        return False
    
    def to_dict(self):
        """Convert guild data to dictionary for saving
        
        Returns:
            dict: Guild data as dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "leader_id": self.leader_id,
            "members": self.members,
            "quests": self.quests,
            "completed_quests": self.completed_quests,
            "chat_history": self.chat_history,
            "created_at": self.created_at,
            "xp": self.xp,
            "level": self.level
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a guild from dictionary data
        
        Args:
            data (dict): Guild data
            
        Returns:
            Guild: New guild instance
        """
        guild = cls(data["name"], data["description"], data["leader_id"])
        guild.id = data["id"]
        guild.members = data["members"]
        guild.quests = data["quests"]
        guild.completed_quests = data["completed_quests"]
        guild.chat_history = data["chat_history"]
        guild.created_at = data["created_at"]
        guild.xp = data["xp"]
        guild.level = data["level"]
        return guild


class GuildSystem:
    """System for managing guilds and quests"""
    
    def __init__(self, player, database):
        """Initialize the guild system
        
        Args:
            player: Player object
            database: Database object for persistence
        """
        self.player = player
        self.db = database
        self.guilds = {}  # Guild ID -> Guild object mapping
        self.quest_templates = self._load_quest_templates()
    
    def _load_quest_templates(self):
        """Load quest templates
        
        Returns:
            list: List of quest templates
        """
        # This would normally load from a database or file
        # For now, we'll use a small sample of quest templates
        return [
            {
                "name": "Math Marathon",
                "description": "Solve 50 math questions collectively",
                "subject": "math",
                "goal": {"type": "answer_questions", "count": 50, "subject": "math"},
                "time_limit": 86400,  # 24 hours in seconds
                "min_level": 1,
                "xp_reward": 500,
                "item_reward": {"name": "Advanced Calculator", "type": "tool", "subject": "math", "effect": {"trait_bonus": {"math": 10}}}
            },
            {
                "name": "Science Sprint",
                "description": "Answer 30 science questions with at least 80% accuracy",
                "subject": "science",
                "goal": {"type": "answer_questions", "count": 30, "subject": "science", "min_accuracy": 0.8},
                "time_limit": 43200,  # 12 hours in seconds
                "min_level": 3,
                "xp_reward": 300,
                "item_reward": {"name": "Lab Equipment", "type": "tool", "subject": "science", "effect": {"trait_bonus": {"science": 8}}}
            },
            {
                "name": "Historical Hunt",
                "description": "Find answers to 20 historical questions",
                "subject": "history",
                "goal": {"type": "answer_questions", "count": 20, "subject": "history"},
                "time_limit": 172800,  # 48 hours in seconds
                "min_level": 2,
                "xp_reward": 400,
                "item_reward": {"name": "Ancient Artifact", "type": "tool", "subject": "history", "effect": {"trait_bonus": {"history": 9}}}
            },
            {
                "name": "Multi-Subject Challenge",
                "description": "Answer questions from all subjects",
                "subject": "all",
                "goal": {"type": "answer_questions", "count": 15, "subject": "all"},
                "time_limit": 86400,  # 24 hours in seconds
                "min_level": 5,
                "xp_reward": 600,
                "item_reward": {"name": "Knowledge Orb", "type": "artifact", "subject": "all", "effect": {"xp_bonus": 0.1}}
            },
        ]
    
    def create_guild(self, name, description):
        """Create a new guild
        
        Args:
            name (str): Guild name
            description (str): Guild description
            
        Returns:
            Guild: The created guild
        """
        # Create the guild with the player as leader
        guild = Guild(name, description, self.player.name)  # Using player name as ID for simplicity
        
        # Add to local cache
        self.guilds[guild.id] = guild
        
        # Save to database
        self._save_guild(guild)
        
        # Update player's guild
        self.player.join_guild(guild.id)
        
        console.print(f"[bold green]Guild '{name}' created successfully![/bold green]")
        return guild
    
    def join_guild(self, guild_id):
        """Join an existing guild
        
        Args:
            guild_id (str): ID of the guild to join
            
        Returns:
            bool: True if joined, False if already in guild or guild not found
        """
        # Check if guild exists
        guild = self._get_guild(guild_id)
        if not guild:
            console.print(f"[bold red]Guild with ID {guild_id} not found![/bold red]")
            return False
        
        # Check if player is already in a guild
        if self.player.guild_id:
            console.print(f"[bold yellow]You are already in a guild. Leave it first.[/bold yellow]")
            return False
        
        # Add player to guild
        if guild.add_member(self.player.name):  # Using player name as ID for simplicity
            # Update player's guild
            self.player.join_guild(guild_id)
            
            # Save guild to database
            self._save_guild(guild)
            
            console.print(f"[bold green]You have joined the guild '{guild.name}'![/bold green]")
            return True
        else:
            console.print(f"[bold yellow]You are already a member of this guild.[/bold yellow]")
            return False
    
    def leave_guild(self):
        """Leave the current guild
        
        Returns:
            bool: True if left, False if not in a guild
        """
        # Check if player is in a guild
        if not self.player.guild_id:
            console.print(f"[bold yellow]You are not in a guild.[/bold yellow]")
            return False
        
        # Get the guild
        guild = self._get_guild(self.player.guild_id)
        if not guild:
            # Guild not found, but player thinks they're in it
            # Clear the player's guild ID anyway
            self.player.leave_guild()
            return True
        
        # Check if player is the leader
        if guild.leader_id == self.player.name:  # Using player name as ID for simplicity
            if Confirm.ask("You are the leader of this guild. Leaving will delete the guild. Are you sure?"):
                # Delete the guild
                self._delete_guild(guild.id)
                
                # Clear player's guild ID
                self.player.leave_guild()
                
                console.print(f"[bold yellow]You have left and deleted the guild '{guild.name}'.[/bold yellow]")
                return True
            else:
                return False
        else:
            # Remove player from guild
            guild.remove_member(self.player.name)  # Using player name as ID for simplicity
            
            # Save guild to database
            self._save_guild(guild)
            
            # Clear player's guild ID
            self.player.leave_guild()
            
            console.print(f"[bold yellow]You have left the guild '{guild.name}'.[/bold yellow]")
            return True
    
    def list_guilds(self):
        """List all available guilds
        
        Returns:
            list: List of guild dictionaries
        """
        # This would normally query the database
        # For now, we'll just return the local cache
        guilds_list = [guild.to_dict() for guild in self.guilds.values()]
        
        # Display guilds in a table
        table = Table(title="Available Guilds")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Members")
        table.add_column("Level")
        
        for guild in guilds_list:
            table.add_row(
                guild["id"],
                guild["name"],
                str(len(guild["members"])),
                str(guild["level"])
            )
        
        console.print(table)
        return guilds_list
    
    def view_guild(self, guild_id=None):
        """View details of a guild
        
        Args:
            guild_id (str, optional): ID of the guild to view. Defaults to player's guild.
            
        Returns:
            dict: Guild data, or None if not found
        """
        # Use player's guild if not specified
        if not guild_id:
            guild_id = self.player.guild_id
        
        # Check if player is in a guild
        if not guild_id:
            console.print(f"[bold yellow]You are not in a guild.[/bold yellow]")
            return None
        
        # Get the guild
        guild = self._get_guild(guild_id)
        if not guild:
            console.print(f"[bold red]Guild with ID {guild_id} not found![/bold red]")
            return None
        
        # Display guild details
        console.print(Panel(f"{guild.description}", title=f"Guild: {guild.name} (Level {guild.level})")
        )
        
        # Display members
        table = Table(title="Members")
        table.add_column("Name")
        table.add_column("Role")
        
        for member_id, role in guild.members.items():
            table.add_row(member_id, role)  # Using player name as ID for simplicity
        
        console.print(table)
        
        # Display active quests
        if guild.quests:
            console.print("\n[bold]Active Quests:[/bold]")
            for quest in guild.quests:
                console.print(f"- {quest['name']}: {quest['description']}")
        
        return guild.to_dict()
    
    def start_quest(self, template_index):
        """Start a new quest for the guild
        
        Args:
            template_index (int): Index of the quest template to use
            
        Returns:
            dict: The started quest, or None if failed
        """
        # Check if player is in a guild
        if not self.player.guild_id:
            console.print(f"[bold yellow]You are not in a guild.[/bold yellow]")
            return None
        
        # Get the guild
        guild = self._get_guild(self.player.guild_id)
        if not guild:
            console.print(f"[bold red]Guild not found![/bold red]")
            return None
        
        # Check if template index is valid
        if template_index < 0 or template_index >= len(self.quest_templates):
            console.print(f"[bold red]Invalid quest template index![/bold red]")
            return None
        
        # Get the template
        template = self.quest_templates[template_index]
        
        # Check if guild meets level requirement
        if guild.level < template["min_level"]:
            console.print(f"[bold red]Guild level too low! Need level {template['min_level']}.[/bold red]")
            return None
        
        # Create the quest
        quest = {
            "id": str(uuid.uuid4())[:8],  # Generate a short unique ID
            "name": template["name"],
            "description": template["description"],
            "subject": template["subject"],
            "goal": template["goal"],
            "progress": 0,
            "started_at": time.time(),
            "expires_at": time.time() + template["time_limit"],
            "xp_reward": template["xp_reward"],
            "item_reward": template["item_reward"],
            "started_by": self.player.name  # Using player name as ID for simplicity
        }
        
        # Add to guild
        guild.add_quest(quest)
        
        # Save guild to database
        self._save_guild(guild)
        
        console.print(f"[bold green]Quest '{quest['name']}' started![/bold green]")
        console.print(f"[green]{quest['description']}[/green]")
        
        return quest
    
    def update_quest_progress(self, quest_id, progress_amount):
        """Update progress on a quest
        
        Args:
            quest_id (str): ID of the quest to update
            progress_amount (int): Amount of progress to add
            
        Returns:
            bool: True if updated, False if not found or already completed
        """
        # Check if player is in a guild
        if not self.player.guild_id:
            return False
        
        # Get the guild
        guild = self._get_guild(self.player.guild_id)
        if not guild:
            return False
        
        # Find the quest
        for quest in guild.quests:
            if quest["id"] == quest_id:
                # Update progress
                quest["progress"] += progress_amount
                
                # Check if quest is completed
                if quest["progress"] >= quest["goal"]["count"]:
                    # Complete the quest
                    guild.complete_quest(quest_id)
                    
                    # Give reward to player
                    self.player.add_to_inventory(quest["item_reward"])
                    
                    console.print(f"[bold green]Quest '{quest['name']}' completed![/bold green]")
                    console.print(f"[green]Reward: {quest['item_reward']['name']}[/green]")
                else:
                    console.print(f"[green]Quest progress updated: {quest['progress']}/{quest['goal']['count']}[/green]")
                
                # Save guild to database
                self._save_guild(guild)
                
                return True
        
        return False
    
    def send_chat_message(self, message):
        """Send a chat message to the guild
        
        Args:
            message (str): Message content
            
        Returns:
            bool: True if sent, False if not in a guild
        """
        # Check if player is in a guild
        if not self.player.guild_id:
            console.print(f"[bold yellow]You are not in a guild.[/bold yellow]")
            return False
        
        # Get the guild
        guild = self._get_guild(self.player.guild_id)
        if not guild:
            console.print(f"[bold red]Guild not found![/bold red]")
            return False
        
        # Add message to chat history
        guild.add_chat_message(self.player.name, self.player.name, message)  # Using player name as ID and display name
        
        # Save guild to database
        self._save_guild(guild)
        
        return True
    
    def view_chat(self):
        """View the guild chat history
        
        Returns:
            list: Chat history, or None if not in a guild
        """
        # Check if player is in a guild
        if not self.player.guild_id:
            console.print(f"[bold yellow]You are not in a guild.[/bold yellow]")
            return None
        
        # Get the guild
        guild = self._get_guild(self.player.guild_id)
        if not guild:
            console.print(f"[bold red]Guild not found![/bold red]")
            return None
        
        # Display chat history
        console.print(Panel(title=f"Guild Chat: {guild.name}"))
        
        if not guild.chat_history:
            console.print("[italic]No messages yet.[/italic]")
        else:
            for message in guild.chat_history:
                console.print(f"[bold]{message['user_name']}:[/bold] {message['message']}")
        
        return guild.chat_history
    
    def _get_guild(self, guild_id):
        """Get a guild by ID
        
        Args:
            guild_id (str): Guild ID to get
            
        Returns:
            Guild: The guild, or None if not found
        """
        # Check local cache first
        if guild_id in self.guilds:
            return self.guilds[guild_id]
        
        # Try to load from database
        guild_data = self.db.get_guild(guild_id)
        if guild_data:
            guild = Guild.from_dict(guild_data)
            self.guilds[guild_id] = guild  # Add to cache
            return guild
        
        return None
    
    def _save_guild(self, guild):
        """Save a guild to the database
        
        Args:
            guild (Guild): Guild to save
        """
        # Update local cache
        self.guilds[guild.id] = guild
        
        # Save to database
        self.db.save_guild(guild.to_dict())
    
    def _delete_guild(self, guild_id):
        """Delete a guild
        
        Args:
            guild_id (str): ID of the guild to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        # Remove from local cache
        if guild_id in self.guilds:
            del self.guilds[guild_id]
        
        # Delete from database
        return self.db.delete_guild(guild_id)