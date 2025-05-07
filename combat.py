#!/usr/bin/env python3
"""
EduRPG - Text-Based Educational RPG
Combat module for educational battles
"""

import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress

console = Console()

class Enemy:
    """Enemy class for combat encounters"""
    
    def __init__(self, name, sprite, subject, hp, questions, grade_level=None):
        """Initialize a new enemy
        
        Args:
            name (str): Enemy name
            sprite (str): ASCII art representation
            subject (str): Primary subject (math, science, etc.)
            hp (int): Hit points
            questions (list): List of question dictionaries
            grade_level (str, optional): Target grade level. Defaults to None.
        """
        self.name = name
        self.sprite = sprite
        self.subject = subject
        self.max_hp = hp
        self.hp = hp
        self.questions = questions
        self.grade_level = grade_level
    
    def is_defeated(self):
        """Check if enemy is defeated
        
        Returns:
            bool: True if HP is 0 or less
        """
        return self.hp <= 0
    
    def take_damage(self, amount):
        """Reduce enemy HP by damage amount
        
        Args:
            amount (int): Damage amount
            
        Returns:
            int: Actual damage dealt (may be capped)
        """
        actual_damage = min(self.hp, amount)
        self.hp -= actual_damage
        return actual_damage
    
    def get_random_question(self):
        """Get a random question from the enemy's question pool
        
        Returns:
            dict: Question dictionary
        """
        return random.choice(self.questions)
    
    def get_hp_percentage(self):
        """Get the enemy's HP as a percentage
        
        Returns:
            float: HP percentage (0-100)
        """
        return (self.hp / self.max_hp) * 100


class CombatSystem:
    """Combat system for educational battles"""
    
    def __init__(self, player):
        """Initialize the combat system
        
        Args:
            player: Player object
        """
        self.player = player
        self.enemy = None
        self.question_bank = self._load_question_bank()
        self.difficulty_multiplier = 1.0
    
    def _load_question_bank(self):
        """Load questions from database or local storage
        
        Returns:
            dict: Dictionary of questions by subject and grade
        """
        # This would normally load from a database or file
        # For now, we'll use a small sample question bank
        return {
            "math": {
                "1": [
                    {"question": "What is 5 + 3?", "answer": "8", "difficulty": 1},
                    {"question": "What is 10 - 4?", "answer": "6", "difficulty": 1},
                ],
                "5": [
                    {"question": "What is the area of a square with side length 7?", "answer": "49", "difficulty": 2},
                    {"question": "What is 3 × 12?", "answer": "36", "difficulty": 2},
                ],
                "10": [
                    {"question": "Factor x² + 5x + 6", "answer": "(x+2)(x+3)", "difficulty": 3},
                    {"question": "Solve 2x - 4 = 10", "answer": "7", "difficulty": 3},
                ],
                "college": [
                    {"question": "Find the derivative of f(x) = x³ + 2x² - 5x + 3", "answer": "3x² + 4x - 5", "difficulty": 4},
                    {"question": "Evaluate ∫(2x + 3)dx from x=0 to x=4", "answer": "28", "difficulty": 4},
                ],
            },
            "science": {
                "1": [
                    {"question": "What is the closest planet to the Sun?", "answer": "Mercury", "difficulty": 1},
                    {"question": "What do plants need to grow?", "answer": "Sunlight, water, air", "difficulty": 1},
                ],
                "5": [
                    {"question": "What are the three states of matter?", "answer": "Solid, liquid, gas", "difficulty": 2},
                    {"question": "What is photosynthesis?", "answer": "The process by which plants make food using sunlight", "difficulty": 2},
                ],
                "10": [
                    {"question": "What is the chemical formula for water?", "answer": "H2O", "difficulty": 3},
                    {"question": "What is Newton's Second Law of Motion?", "answer": "F = ma", "difficulty": 3},
                ],
                "college": [
                    {"question": "What is the Heisenberg Uncertainty Principle?", "answer": "It is impossible to simultaneously know the exact position and momentum of a particle", "difficulty": 4},
                    {"question": "What are the four fundamental forces in physics?", "answer": "Gravity, electromagnetic, strong nuclear, weak nuclear", "difficulty": 4},
                ],
            },
            "history": {
                "1": [
                    {"question": "Who was the first President of the United States?", "answer": "George Washington", "difficulty": 1},
                    {"question": "What holiday celebrates independence in the United States?", "answer": "Independence Day", "difficulty": 1},
                ],
                "5": [
                    {"question": "What ancient civilization built the pyramids?", "answer": "Egyptians", "difficulty": 2},
                    {"question": "Who wrote the Declaration of Independence?", "answer": "Thomas Jefferson", "difficulty": 2},
                ],
                "10": [
                    {"question": "When did World War II end?", "answer": "1945", "difficulty": 3},
                    {"question": "What was the name of the conflict between the North and South in the United States?", "answer": "Civil War", "difficulty": 3},
                ],
                "college": [
                    {"question": "What was the significance of the Treaty of Westphalia?", "answer": "It ended the Thirty Years' War and established the principle of state sovereignty", "difficulty": 4},
                    {"question": "What economic system did Karl Marx criticize in 'Das Kapital'?", "answer": "Capitalism", "difficulty": 4},
                ],
            },
        }
    
    def generate_enemy(self, subject=None):
        """Generate an enemy appropriate for the player's level and grade
        
        Args:
            subject (str, optional): Subject focus for the enemy. Defaults to random.
            
        Returns:
            Enemy: Generated enemy
        """
        if not subject:
            subject = random.choice(["math", "science", "history"])
        
        # Determine grade level for questions
        grade = self.player.grade
        
        # Get questions for this subject and grade
        available_questions = []
        if grade in self.question_bank[subject]:
            available_questions.extend(self.question_bank[subject][grade])
        
        # If not enough questions, add some from adjacent grades
        if len(available_questions) < 5:
            for g in self.question_bank[subject].keys():
                if g != grade:
                    available_questions.extend(self.question_bank[subject][g])
        
        # Take a random sample of questions
        if len(available_questions) > 5:
            battle_questions = random.sample(available_questions, 5)
        else:
            battle_questions = available_questions
        
        # Generate enemy based on subject
        enemy_templates = {
            "math": [
                {
                    "name": "Polynomial Golem",
                    "sprite": "🔥📐\n/()\\\n /\\",
                    "hp": 100 + (self.player.level * 10)
                },
                {
                    "name": "Fraction Phantom",
                    "sprite": "  👻\n /|\\\n/ | \\",
                    "hp": 80 + (self.player.level * 8)
                },
            ],
            "science": [
                {
                    "name": "Chemical Construct",
                    "sprite": "⚗️ 🧪\n/|\\\n/ \\",
                    "hp": 90 + (self.player.level * 9)
                },
                {
                    "name": "Physics Phantom",
                    "sprite": "  ⚛️\n /|\\\n/ | \\",
                    "hp": 85 + (self.player.level * 8.5)
                },
            ],
            "history": [
                {
                    "name": "Chronos Guardian",
                    "sprite": "⏳ 📜\n/|\\\n/ \\",
                    "hp": 95 + (self.player.level * 9.5)
                },
                {
                    "name": "Ancient Archivist",
                    "sprite": "  📚\n /|\\\n/ | \\",
                    "hp": 85 + (self.player.level * 8.5)
                },
            ],
        }
        
        # Select a random enemy template for the subject
        template = random.choice(enemy_templates[subject])
        
        return Enemy(
            name=template["name"],
            sprite=template["sprite"],
            subject=subject,
            hp=template["hp"],
            questions=battle_questions,
            grade_level=grade
        )
    
    def start_battle(self, enemy=None):
        """Start a battle with an enemy
        
        Args:
            enemy (Enemy, optional): Enemy to battle. If None, generates one.
            
        Returns:
            bool: True if player won, False if player fled
        """
        if not enemy:
            enemy = self.generate_enemy()
        
        self.enemy = enemy
        
        console.print(f"\n[bold red]A wild {enemy.name} appears![/bold red]")
        console.print(Panel(enemy.sprite, title=enemy.name))
        console.print(f"Subject: [cyan]{enemy.subject.capitalize()}[/cyan]")
        
        # Battle loop
        battle_round = 1
        while not enemy.is_defeated():
            console.print(f"\n[bold]===== Round {battle_round} =====[/bold]")
            
            # Show enemy health
            hp_percent = enemy.get_hp_percentage()
            hp_bar = "[" + "#" * int(hp_percent / 5) + "-" * (20 - int(hp_percent / 5)) + "]" 
            console.print(f"Enemy HP: {hp_bar} {enemy.hp}/{enemy.max_hp}")
            
            # Player options
            console.print("\n[bold cyan]What will you do?[/bold cyan]")
            console.print("1. Answer a question (attack)")
            console.print("2. Use an item")
            console.print("3. Flee")
            
            choice = Prompt.ask("Choose an action", choices=["1", "2", "3"])
            
            if choice == "1":
                # Get a question and ask player
                result = self._handle_question()
                if result:
                    # Correct answer - deal damage
                    damage = self._calculate_damage(result)
                    actual_damage = enemy.take_damage(damage)
                    console.print(f"[bold green]You dealt {actual_damage} damage to {enemy.name}![/bold green]")
                else:
                    # Incorrect answer - no damage
                    console.print(f"[bold red]Your attack missed![/bold red]")
            
            elif choice == "2":
                # Use an item (placeholder)
                if not self.player.inventory:
                    console.print("[yellow]You don't have any items![/yellow]")
                else:
                    console.print("[yellow]Item use not implemented yet![/yellow]")
            
            elif choice == "3":
                # Flee from battle
                if Confirm.ask("Are you sure you want to flee?"):
                    console.print("[yellow]You fled from battle![/yellow]")
                    return False
            
            # Check if enemy is defeated
            if enemy.is_defeated():
                self._handle_victory()
                return True
            
            # Increment round counter
            battle_round += 1
            time.sleep(1)
    
    def _handle_question(self):
        """Present a question to the player and check the answer
        
        Returns:
            int: Score based on answer correctness and speed, or 0 if incorrect
        """
        question_data = self.enemy.get_random_question()
        question_text = question_data["question"]
        correct_answer = question_data["difficulty"]
        
        console.print(f"\n[bold cyan]Question:[/bold cyan] {question_text}")
        
        # Timer for answering (more points for faster answers)
        start_time = time.time()
        
        # Get player's answer
        answer = Prompt.ask("Your answer")
        
        # Calculate time taken (capped at 30 seconds)
        time_taken = min(time.time() - start_time, 30)
        
        # Check if answer is correct
        # In a real implementation, this would use more sophisticated answer checking
        # For now, we'll do a simple string comparison
        if answer.lower().strip() == question_data["answer"].lower().strip():
            # Calculate score based on time taken and difficulty
            time_factor = max(0, 1 - (time_taken / 30))  # 1.0 for instant, 0 for 30+ seconds
            difficulty_bonus = question_data["difficulty"] * 5
            score = int(10 + (difficulty_bonus * time_factor))
            
            console.print(f"[bold green]Correct! +{score} points[/bold green]")
            
            # Add XP to player
            xp_gained = score * 2
            self.player.gain_xp(xp_gained, self.enemy.subject)
            console.print(f"[green]You gained {xp_gained} XP in {self.enemy.subject}![/green]")
            
            return score
        else:
            console.print(f"[bold red]Incorrect! The answer was: {question_data['answer']}[/bold red]")
            return 0
    
    def _calculate_damage(self, score):
        """Calculate damage based on score and player traits
        
        Args:
            score (int): Score from answering the question
            
        Returns:
            int: Damage amount
        """
        # Base damage from score
        damage = score
        
        # Apply trait bonus
        trait_value = self.player.traits.get(self.enemy.subject, 0)
        trait_multiplier = 1 + (trait_value / 200)  # +50% damage at 100 trait points
        damage = int(damage * trait_multiplier)
        
        # Apply level scaling
        level_bonus = 1 + (self.player.level / 20)  # +50% damage at level 10
        damage = int(damage * level_bonus)
        
        return max(1, damage)  # Minimum 1 damage
    
    def _handle_victory(self):
        """Handle enemy defeat and rewards"""
        console.print(f"\n[bold green]Victory! You defeated the {self.enemy.name}![/bold green]")
        
        # Calculate rewards
        xp_reward = int(self.enemy.max_hp / 5)
        console.print(f"[green]You gained {xp_reward} XP![/green]")
        self.player.gain_xp(xp_reward, self.enemy.subject)
        
        # Random chance for item drop
        if random.random() < 0.3:  # 30% chance
            item = self._generate_random_item()
            self.player.add_to_inventory(item)
    
    def _generate_random_item(self):
        """Generate a random item as loot
        
        Returns:
            dict: Item data
        """
        item_templates = [
            {
                "name": "Math Textbook",
                "type": "book",
                "subject": "math",
                "effect": {"trait_bonus": {"math": 5}},
                "description": "A comprehensive math textbook. Grants +5 to Math trait."
            },
            {
                "name": "Science Journal",
                "type": "book",
                "subject": "science",
                "effect": {"trait_bonus": {"science": 5}},
                "description": "A scientific journal with the latest discoveries. Grants +5 to Science trait."
            },
            {
                "name": "History Scroll",
                "type": "book",
                "subject": "history",
                "effect": {"trait_bonus": {"history": 5}},
                "description": "An ancient scroll containing historical knowledge. Grants +5 to History trait."
            },
            {
                "name": "Precision Compass",
                "type": "tool",
                "subject": "math",
                "effect": {"damage_bonus": 2},
                "description": "A precision drawing compass. Increases Math damage by 2."
            },
            {
                "name": "Microscope",
                "type": "tool",
                "subject": "science",
                "effect": {"damage_bonus": 2},
                "description": "A powerful microscope. Increases Science damage by 2."
            },
            {
                "name": "Antique Map",
                "type": "tool",
                "subject": "history",
                "effect": {"damage_bonus": 2},
                "description": "An antique map with historical routes. Increases History damage by 2."
            },
        ]
        
        # Choose a random item, with preference for the enemy's subject
        subject_items = [item for item in item_templates if item["subject"] == self.enemy.subject]
        if subject_items and random.random() < 0.7:  # 70% chance for subject-specific item
            return random.choice(subject_items)
        else:
            return random.choice(item_templates)


# For testing
if __name__ == "__main__":
    from player import Player
    
    # Create a test player
    player = Player("Test Player", "10")
    
    # Create combat system
    combat = CombatSystem(player)
    
    # Start a battle
    combat.start_battle()