# EduRPG - Text-Based Educational RPG

EduRPG is a cross-platform educational game where students answer curriculum-aligned questions to level up avatars, join guilds, and battle enemies with ASCII sprites.

## Project Structure

### Core Components

1. **Terminal Version (Python)**
   - `main.py`: Entry point for the terminal application
   - `player.py`: Player class and progression system
   - `combat.py`: Battle system with educational questions
   - `guild.py`: Guild system with collaborative quests
   - `database.py`: Firebase integration for data persistence
   - `ui.py`: Terminal UI using Rich/Textual libraries

2. **Web Version (React)**
   - `web/`: Contains React application code
   - `web/src/components/`: UI components
   - `web/src/services/`: Firebase integration

3. **Mobile Version (Flutter)**
   - `mobile/`: Contains Flutter application code
   - `mobile/lib/`: Main application code

### Getting Started

#### Terminal Version
1. Install dependencies: `pip install -r requirements.txt`
2. Run the game: `python main.py`

#### Web Version
1. Navigate to the web directory: `cd web`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

#### Mobile Version
1. Navigate to the mobile directory: `cd mobile`
2. Install dependencies: `flutter pub get`
3. Run the app: `flutter run`

## Features

- **User Profile System**: Create and customize your character with traits and skills
- **Combat System**: Battle enemies by answering educational questions
- **Guild System**: Join or create guilds, participate in collaborative quests
- **Cross-Platform**: Play on terminal, web, or mobile devices
- **Educational Content**: Curriculum-aligned questions for grades 1-12 and college# EduRPG
