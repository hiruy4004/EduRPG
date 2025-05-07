#!/usr/bin/env python3
"""
EduRPG - Text-Based Educational RPG
Database module for Firebase integration
"""

import os
import json
from pathlib import Path
from rich.console import Console

# Optional Firebase imports - will be used if Firebase is configured
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

console = Console()

class Database:
    """Database class for EduRPG
    
    Handles data persistence using either Firebase (online) or local JSON files (offline)
    """
    
    def __init__(self, use_firebase=True):
        """Initialize the database connection
        
        Args:
            use_firebase (bool, optional): Whether to use Firebase. Defaults to True.
        """
        self.use_firebase = use_firebase and FIREBASE_AVAILABLE
        self.db = None
        self.local_data_dir = Path("data")
        
        if self.use_firebase:
            self._initialize_firebase()
        else:
            self._initialize_local_storage()
    
    def _initialize_firebase(self):
        """Initialize Firebase connection"""
        try:
            # Check if already initialized
            if not firebase_admin._apps:
                # Look for service account key file
                key_file = Path("firebase-key.json")
                if key_file.exists():
                    cred = credentials.Certificate(str(key_file))
                    firebase_admin.initialize_app(cred)
                else:
                    console.print("[yellow]Firebase key file not found. Using local storage instead.[/yellow]")
                    self.use_firebase = False
                    self._initialize_local_storage()
                    return
            
            self.db = firestore.client()
            console.print("[green]Connected to Firebase successfully![/green]")
        except Exception as e:
            console.print(f"[red]Error connecting to Firebase: {e}[/red]")
            console.print("[yellow]Falling back to local storage.[/yellow]")
            self.use_firebase = False
            self._initialize_local_storage()
    
    def _initialize_local_storage(self):
        """Initialize local storage"""
        # Create data directory if it doesn't exist
        self.local_data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different data types
        (self.local_data_dir / "players").mkdir(exist_ok=True)
        (self.local_data_dir / "guilds").mkdir(exist_ok=True)
        (self.local_data_dir / "questions").mkdir(exist_ok=True)
        
        console.print("[green]Local storage initialized.[/green]")
    
    # Player data methods
    def save_player(self, player_data):
        """Save player data
        
        Args:
            player_data (dict): Player data to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        player_id = player_data["name"]  # Using name as ID for simplicity
        
        try:
            if self.use_firebase:
                self.db.collection("players").document(player_id).set(player_data)
            else:
                file_path = self.local_data_dir / "players" / f"{player_id}.json"
                with open(file_path, "w") as f:
                    json.dump(player_data, f, indent=2)
            
            return True
        except Exception as e:
            console.print(f"[red]Error saving player data: {e}[/red]")
            return False
    
    def get_player(self, player_id):
        """Get player data
        
        Args:
            player_id (str): Player ID to get
            
        Returns:
            dict: Player data, or None if not found
        """
        try:
            if self.use_firebase:
                doc = self.db.collection("players").document(player_id).get()
                return doc.to_dict() if doc.exists else None
            else:
                file_path = self.local_data_dir / "players" / f"{player_id}.json"
                if file_path.exists():
                    with open(file_path, "r") as f:
                        return json.load(f)
                return None
        except Exception as e:
            console.print(f"[red]Error getting player data: {e}[/red]")
            return None
    
    def delete_player(self, player_id):
        """Delete player data
        
        Args:
            player_id (str): Player ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.use_firebase:
                self.db.collection("players").document(player_id).delete()
            else:
                file_path = self.local_data_dir / "players" / f"{player_id}.json"
                if file_path.exists():
                    file_path.unlink()
            
            return True
        except Exception as e:
            console.print(f"[red]Error deleting player data: {e}[/red]")
            return False
    
    def list_players(self):
        """List all players
        
        Returns:
            list: List of player IDs
        """
        try:
            if self.use_firebase:
                docs = self.db.collection("players").stream()
                return [doc.id for doc in docs]
            else:
                player_files = list((self.local_data_dir / "players").glob("*.json"))
                return [file.stem for file in player_files]
        except Exception as e:
            console.print(f"[red]Error listing players: {e}[/red]")
            return []
    
    # Guild data methods
    def save_guild(self, guild_data):
        """Save guild data
        
        Args:
            guild_data (dict): Guild data to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        guild_id = guild_data["id"]
        
        try:
            if self.use_firebase:
                self.db.collection("guilds").document(guild_id).set(guild_data)
            else:
                file_path = self.local_data_dir / "guilds" / f"{guild_id}.json"
                with open(file_path, "w") as f:
                    json.dump(guild_data, f, indent=2)
            
            return True
        except Exception as e:
            console.print(f"[red]Error saving guild data: {e}[/red]")
            return False
    
    def get_guild(self, guild_id):
        """Get guild data
        
        Args:
            guild_id (str): Guild ID to get
            
        Returns:
            dict: Guild data, or None if not found
        """
        try:
            if self.use_firebase:
                doc = self.db.collection("guilds").document(guild_id).get()
                return doc.to_dict() if doc.exists else None
            else:
                file_path = self.local_data_dir / "guilds" / f"{guild_id}.json"
                if file_path.exists():
                    with open(file_path, "r") as f:
                        return json.load(f)
                return None
        except Exception as e:
            console.print(f"[red]Error getting guild data: {e}[/red]")
            return None
    
    def delete_guild(self, guild_id):
        """Delete guild data
        
        Args:
            guild_id (str): Guild ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.use_firebase:
                self.db.collection("guilds").document(guild_id).delete()
            else:
                file_path = self.local_data_dir / "guilds" / f"{guild_id}.json"
                if file_path.exists():
                    file_path.unlink()
            
            return True
        except Exception as e:
            console.print(f"[red]Error deleting guild data: {e}[/red]")
            return False
    
    def list_guilds(self):
        """List all guilds
        
        Returns:
            list: List of guild IDs
        """
        try:
            if self.use_firebase:
                docs = self.db.collection("guilds").stream()
                return [doc.id for doc in docs]
            else:
                guild_files = list((self.local_data_dir / "guilds").glob("*.json"))
                return [file.stem for file in guild_files]
        except Exception as e:
            console.print(f"[red]Error listing guilds: {e}[/red]")
            return []
    
    # Question data methods
    def save_questions(self, subject, grade, questions):
        """Save questions for a subject and grade
        
        Args:
            subject (str): Subject (math, science, etc.)
            grade (str): Grade level (1-12 or college)
            questions (list): List of question dictionaries
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.use_firebase:
                self.db.collection("questions").document(f"{subject}_{grade}").set({
                    "subject": subject,
                    "grade": grade,
                    "questions": questions
                })
            else:
                file_path = self.local_data_dir / "questions" / f"{subject}_{grade}.json"
                with open(file_path, "w") as f:
                    json.dump({
                        "subject": subject,
                        "grade": grade,
                        "questions": questions
                    }, f, indent=2)
            
            return True
        except Exception as e:
            console.print(f"[red]Error saving questions: {e}[/red]")
            return False
    
    def get_questions(self, subject, grade):
        """Get questions for a subject and grade
        
        Args:
            subject (str): Subject (math, science, etc.)
            grade (str): Grade level (1-12 or college)
            
        Returns:
            list: List of question dictionaries, or empty list if not found
        """
        try:
            if self.use_firebase:
                doc = self.db.collection("questions").document(f"{subject}_{grade}").get()
                if doc.exists:
                    return doc.to_dict()["questions"]
                return []
            else:
                file_path = self.local_data_dir / "questions" / f"{subject}_{grade}.json"
                if file_path.exists():
                    with open(file_path, "r") as f:
                        return json.load(f)["questions"]
                return []
        except Exception as e:
            console.print(f"[red]Error getting questions: {e}[/red]")
            return []
    
    def get_all_questions(self):
        """Get all questions
        
        Returns:
            dict: Dictionary of questions by subject and grade
        """
        result = {}
        
        try:
            if self.use_firebase:
                docs = self.db.collection("questions").stream()
                for doc in docs:
                    data = doc.to_dict()
                    subject = data["subject"]
                    grade = data["grade"]
                    
                    if subject not in result:
                        result[subject] = {}
                    
                    result[subject][grade] = data["questions"]
            else:
                question_files = list((self.local_data_dir / "questions").glob("*.json"))
                for file in question_files:
                    with open(file, "r") as f:
                        data = json.load(f)
                        subject = data["subject"]
                        grade = data["grade"]
                        
                        if subject not in result:
                            result[subject] = {}
                        
                        result[subject][grade] = data["questions"]
        except Exception as e:
            console.print(f"[red]Error getting all questions: {e}[/red]")
        
        return result


# For testing
if __name__ == "__main__":
    # Initialize database
    db = Database(use_firebase=False)  # Use local storage for testing
    
    # Test saving and retrieving player data
    test_player = {
        "name": "TestPlayer",
        "grade": "10",
        "level": 1,
        "xp": 0,
        "traits": {"math": 0, "science": 0, "history": 0},
        "inventory": [],
        "skills": [],
        "guild_id": None
    }
    
    db.save_player(test_player)
    retrieved_player = db.get_player("TestPlayer")
    
    if retrieved_player:
        console.print("[green]Player data saved and retrieved successfully![/green]")
    else:
        console.print("[red]Error retrieving player data.[/red]")