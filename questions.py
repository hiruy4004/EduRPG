#!/usr/bin/env python3
"""
EduRPG - Text-Based Educational RPG
Questions database for educational content
"""

# Sample questions database organized by subject and grade level
# Each question has text, options (for multiple choice), answer, and explanation

QUESTIONS_DB = {
    "math": {
        "1": [
            {
                "text": "What is 5 + 3?",
                "options": ["7", "8", "9", "10"],
                "answer": "8",
                "explanation": "5 + 3 = 8"
            },
            {
                "text": "Count the apples: 🍎🍎🍎. How many are there?",
                "options": ["2", "3", "4", "5"],
                "answer": "3",
                "explanation": "There are 3 apple emojis."
            },
            {
                "text": "What number comes after 6?",
                "options": ["5", "6", "7", "8"],
                "answer": "7",
                "explanation": "The numbers in order are: 5, 6, 7, 8..."
            }
        ],
        "5": [
            {
                "text": "What is 12 × 8?",
                "options": ["86", "96", "106", "96"],
                "answer": "96",
                "explanation": "12 × 8 = 96"
            },
            {
                "text": "What is the perimeter of a square with sides of 7 cm?",
                "options": ["14 cm", "21 cm", "28 cm", "49 cm"],
                "answer": "28 cm",
                "explanation": "The perimeter of a square is 4 × side length. So 4 × 7 cm = 28 cm."
            },
            {
                "text": "What fraction of 20 is 5?",
                "options": ["1/4", "1/5", "1/2", "1/3"],
                "answer": "1/4",
                "explanation": "5 is 1/4 of 20 because 5 × 4 = 20."
            }
        ],
        "10": [
            {
                "text": "Solve for x: 3x - 7 = 14",
                "options": ["5", "7", "9", "21"],
                "answer": "7",
                "explanation": "3x - 7 = 14\n3x = 21\nx = 7"
            },
            {
                "text": "What is the slope of the line passing through points (2, 3) and (6, 11)?",
                "options": ["1", "2", "3", "4"],
                "answer": "2",
                "explanation": "Slope = (y₂ - y₁)/(x₂ - x₁) = (11 - 3)/(6 - 2) = 8/4 = 2"
            },
            {
                "text": "If f(x) = x² - 3x + 2, what is f(4)?",
                "options": ["6", "10", "14", "18"],
                "answer": "6",
                "explanation": "f(4) = 4² - 3(4) + 2 = 16 - 12 + 2 = 6"
            }
        ],
        "College": [
            {
                "text": "Find the derivative of f(x) = 3x⁴ - 2x² + 5x - 7",
                "options": ["f'(x) = 12x³ - 4x + 5", "f'(x) = 12x³ - 4x - 5", "f'(x) = 12x³ - 4x + 5 - 7", "f'(x) = 12x³ - 4x"],
                "answer": "f'(x) = 12x³ - 4x + 5",
                "explanation": "The derivative of x^n is n*x^(n-1). So f'(x) = 3(4)x³ - 2(2)x¹ + 5(1)x⁰ - 0 = 12x³ - 4x + 5"
            },
            {
                "text": "Evaluate the integral ∫(2x + 3)dx from x=1 to x=4",
                "options": ["15.5", "21", "24.5", "27"],
                "answer": "24.5",
                "explanation": "∫(2x + 3)dx = x² + 3x + C\nFrom x=1 to x=4: (4² + 3(4)) - (1² + 3(1)) = (16 + 12) - (1 + 3) = 28 - 4 = 24"
            },
            {
                "text": "What is the solution to the differential equation dy/dx = 2xy with initial condition y(0) = 3?",
                "options": ["y = 3e^(x²)", "y = 3e^x", "y = 3 + x²", "y = 3x²"],
                "answer": "y = 3e^(x²)",
                "explanation": "This is a separable differential equation. Separating variables: dy/y = 2x dx\nIntegrating both sides: ln|y| = x² + C\ny = e^(x² + C) = e^C * e^(x²)\nUsing initial condition y(0) = 3: 3 = e^C * e^0 = e^C\nTherefore, y = 3e^(x²)"
            }
        ]
    },
    "science": {
        "1": [
            {
                "text": "Which animal lays eggs?",
                "options": ["Dog", "Cat", "Bird", "Cow"],
                "answer": "Bird",
                "explanation": "Birds lay eggs to reproduce, while dogs, cats, and cows give birth to live young."
            },
            {
                "text": "What do plants need to grow?",
                "options": ["Only water", "Only sunlight", "Water and sunlight", "Nothing"],
                "answer": "Water and sunlight",
                "explanation": "Plants need both water and sunlight to grow through the process of photosynthesis."
            },
            {
                "text": "Which is a living thing?",
                "options": ["Rock", "Water", "Tree", "Air"],
                "answer": "Tree",
                "explanation": "Trees are living organisms that grow, reproduce, and respond to their environment."
            }
        ],
        "5": [
            {
                "text": "What is the largest planet in our solar system?",
                "options": ["Earth", "Mars", "Jupiter", "Venus"],
                "answer": "Jupiter",
                "explanation": "Jupiter is the largest planet in our solar system, with a diameter about 11 times that of Earth."
            },
            {
                "text": "What is the process by which plants make their own food?",
                "options": ["Respiration", "Photosynthesis", "Digestion", "Circulation"],
                "answer": "Photosynthesis",
                "explanation": "Photosynthesis is the process where plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar."
            },
            {
                "text": "What are the three states of matter?",
                "options": ["Solid, gas, plasma", "Liquid, gas, plasma", "Solid, liquid, plasma", "Solid, liquid, gas"],
                "answer": "Solid, liquid, gas",
                "explanation": "The three common states of matter are solid, liquid, and gas. Plasma is often considered the fourth state."
            }
        ],
        "10": [
            {
                "text": "What is the chemical formula for water?",
                "options": ["H2O", "CO2", "O2", "H2O2"],
                "answer": "H2O",
                "explanation": "Water consists of two hydrogen atoms bonded to one oxygen atom, giving it the formula H2O."
            },
            {
                "text": "Which of these is NOT a type of chemical bond?",
                "options": ["Ionic bond", "Covalent bond", "Hydrogen bond", "Quantum bond"],
                "answer": "Quantum bond",
                "explanation": "Ionic, covalent, and hydrogen bonds are real types of chemical bonds. 'Quantum bond' is not a recognized type of chemical bond."
            },
            {
                "text": "What is the acceleration due to gravity on Earth (approximate value)?",
                "options": ["5 m/s²", "9.8 m/s²", "15 m/s²", "20 m/s²"],
                "answer": "9.8 m/s²",
                "explanation": "The acceleration due to gravity on Earth is approximately 9.8 meters per second squared."
            }
        ],
        "College": [
            {
                "text": "Which of the following is NOT a fundamental force in physics?",
                "options": ["Gravitational force", "Electromagnetic force", "Strong nuclear force", "Centrifugal force"],
                "answer": "Centrifugal force",
                "explanation": "The four fundamental forces are gravitational, electromagnetic, strong nuclear, and weak nuclear forces. Centrifugal force is a fictitious force in a rotating reference frame."
            },
            {
                "text": "What is the primary function of RNA polymerase in cells?",
                "options": ["DNA replication", "Protein synthesis", "Transcription", "Translation"],
                "answer": "Transcription",
                "explanation": "RNA polymerase is responsible for transcription, the process of creating an RNA copy of a DNA sequence."
            },
            {
                "text": "Which law of thermodynamics states that energy cannot be created or destroyed, only transformed?",
                "options": ["Zeroth law", "First law", "Second law", "Third law"],
                "answer": "First law",
                "explanation": "The first law of thermodynamics, also known as the law of energy conservation, states that energy cannot be created or destroyed, only transformed from one form to another."
            }
        ]
    },
    "history": {
        "1": [
            {
                "text": "Who was the first president of the United States?",
                "options": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "John Adams"],
                "answer": "George Washington",
                "explanation": "George Washington was the first president of the United States, serving from 1789 to 1797."
            },
            {
                "text": "What holiday celebrates freedom and independence in the United States?",
                "options": ["Christmas", "Thanksgiving", "Veterans Day", "Independence Day"],
                "answer": "Independence Day",
                "explanation": "Independence Day (July 4th) celebrates the adoption of the Declaration of Independence in 1776."
            },
            {
                "text": "Which of these is a famous American symbol?",
                "options": ["Eiffel Tower", "Liberty Bell", "Big Ben", "Great Wall"],
                "answer": "Liberty Bell",
                "explanation": "The Liberty Bell is an American symbol of independence, located in Philadelphia, Pennsylvania."
            }
        ],
        "5": [
            {
                "text": "What ancient civilization built the pyramids at Giza?",
                "options": ["Romans", "Greeks", "Egyptians", "Mayans"],
                "answer": "Egyptians",
                "explanation": "The ancient Egyptians built the pyramids at Giza as tombs for their pharaohs."
            },
            {
                "text": "Who wrote the Declaration of Independence?",
                "options": ["George Washington", "Thomas Jefferson", "Benjamin Franklin", "John Adams"],
                "answer": "Thomas Jefferson",
                "explanation": "Thomas Jefferson was the principal author of the Declaration of Independence, with input from others including Benjamin Franklin and John Adams."
            },
            {
                "text": "What was the name of the ship that brought the Pilgrims to America in 1620?",
                "options": ["Santa Maria", "Mayflower", "Nina", "Titanic"],
                "answer": "Mayflower",
                "explanation": "The Mayflower brought the Pilgrims from England to Plymouth, Massachusetts in 1620."
            }
        ],
        "10": [
            {
                "text": "What event marked the beginning of World War I?",
                "options": ["The bombing of Pearl Harbor", "The assassination of Archduke Franz Ferdinand", "The invasion of Poland", "The signing of the Treaty of Versailles"],
                "answer": "The assassination of Archduke Franz Ferdinand",
                "explanation": "World War I began after the assassination of Archduke Franz Ferdinand of Austria in June 1914."
            },
            {
                "text": "Which of these was NOT one of the original 13 American colonies?",
                "options": ["Virginia", "Massachusetts", "Ohio", "Georgia"],
                "answer": "Ohio",
                "explanation": "Ohio was not one of the original 13 colonies. It became the 17th state in 1803."
            },
            {
                "text": "What was the main goal of the Civil Rights Movement in the United States?",
                "options": ["Women's suffrage", "End to prohibition", "Equality for African Americans", "Environmental protection"],
                "answer": "Equality for African Americans",
                "explanation": "The Civil Rights Movement aimed to end racial segregation and discrimination against African Americans and secure legal recognition and federal protection of citizenship rights."
            }
        ],
        "College": [
            {
                "text": "Which treaty ended the Thirty Years' War?",
                "options": ["Treaty of Versailles", "Treaty of Paris", "Treaty of Westphalia", "Treaty of Tordesillas"],
                "answer": "Treaty of Westphalia",
                "explanation": "The Peace of Westphalia (1648) was a series of peace treaties that ended the Thirty Years' War and established the principle of state sovereignty."
            },
            {
                "text": "What economic system was criticized by Karl Marx in 'Das Kapital'?",
                "options": ["Socialism", "Communism", "Capitalism", "Feudalism"],
                "answer": "Capitalism",
                "explanation": "In 'Das Kapital,' Karl Marx provided a critical analysis of capitalism and its exploitative nature according to his theory."
            },
            {
                "text": "Which of these was NOT a cause of the French Revolution?",
                "options": ["Financial crisis", "Social inequality", "Enlightenment ideas", "The Cold War"],
                "answer": "The Cold War",
                "explanation": "The Cold War occurred in the 20th century, long after the French Revolution (1789-1799). The main causes of the French Revolution were financial crisis, social inequality, and Enlightenment ideas."
            }
        ]
    },
    "language": {
        "1": [
            {
                "text": "Which of these is a vowel?",
                "options": ["B", "C", "D", "E"],
                "answer": "E",
                "explanation": "E is a vowel. The vowels in English are A, E, I, O, U, and sometimes Y."
            },
            {
                "text": "What is the past tense of 'run'?",
                "options": ["Runned", "Ran", "Running", "Runs"],
                "answer": "Ran",
                "explanation": "The past tense of 'run' is 'ran'. 'Running' is the present participle, and 'runs' is the third-person singular present tense."
            },
            {
                "text": "Which word means the opposite of 'hot'?",
                "options": ["Warm", "Burning", "Cold", "Boiling"],
                "answer": "Cold",
                "explanation": "'Cold' is the antonym (opposite) of 'hot'."
            }
        ],
        "5": [
            {
                "text": "What is a noun?",
                "options": ["A word that describes an action", "A word that names a person, place, or thing", "A word that describes a noun", "A word that replaces a noun"],
                "answer": "A word that names a person, place, or thing",
                "explanation": "A noun is a word that names a person, place, thing, or idea."
            },
            {
                "text": "Which of these sentences uses correct punctuation?",
                "options": ["Where are you going.", "Where are you going?", "Where are you going,", "Where are you going!"],
                "answer": "Where are you going?",
                "explanation": "Questions should end with a question mark (?). The sentence 'Where are you going?' is correctly punctuated."
            },
            {
                "text": "What is a synonym for 'happy'?",
                "options": ["Sad", "Angry", "Joyful", "Tired"],
                "answer": "Joyful",
                "explanation": "'Joyful' is a synonym (word with similar meaning) for 'happy'."
            }
        ],
        "10": [
            {
                "text": "What literary device is used when giving human qualities to non-human things?",
                "options": ["Simile", "Metaphor", "Personification", "Alliteration"],
                "answer": "Personification",
                "explanation": "Personification is giving human qualities, characteristics, or behaviors to non-human objects or concepts."
            },
            {
                "text": "Which of these is an example of a compound sentence?",
                "options": ["The dog barked loudly.", "The dog barked loudly, and the cat ran away.", "The dog, which was large, barked loudly.", "Barking loudly, the dog scared the cat."],
                "answer": "The dog barked loudly, and the cat ran away.",
                "explanation": "A compound sentence contains two independent clauses joined by a coordinating conjunction (like 'and', 'but', 'or'). 'The dog barked loudly' and 'the cat ran away' are both independent clauses."
            },
            {
                "text": "What is the meaning of the prefix 'anti-'?",
                "options": ["Before", "After", "Against", "With"],
                "answer": "Against",
                "explanation": "The prefix 'anti-' means 'against' or 'opposed to', as in 'antiwar' (against war) or 'antisocial' (opposed to social interaction)."
            }
        ],
        "College": [
            {
                "text": "Which of these is an example of a gerund?",
                "options": ["To swim", "Swimming", "Swam", "Swims"],
                "answer": "Swimming",
                "explanation": "A gerund is a verb form that functions as a noun and ends in '-ing'. In this case, 'swimming' is a gerund when used in sentences like 'Swimming is good exercise.'"
            },
            {
                "text": "What rhetorical device involves asking a question that doesn't expect an answer?",
                "options": ["Hyperbole", "Rhetorical question", "Oxymoron", "Euphemism"],
                "answer": "Rhetorical question",
                "explanation": "A rhetorical question is asked for effect, to emphasize a point, or to provoke thought rather than to elicit an answer."
            },
            {
                "text": "In linguistics, what is code-switching?",
                "options": ["Creating a secret language", "Alternating between two or more languages in a single conversation", "Developing a new writing system", "Translating text from one language to another"],
                "answer": "Alternating between two or more languages in a single conversation",
                "explanation": "Code-switching is the practice of alternating between two or more languages or language varieties within a conversation or even a single sentence."
            }
        ]
    }
}


def get_questions_by_subject_and_grade(subject, grade, count=3):
    """Get a list of questions for a specific subject and grade
    
    Args:
        subject (str): Subject (math, science, history, language)
        grade (str): Grade level (1-12 or college)
        count (int, optional): Number of questions to return. Defaults to 3.
        
    Returns:
        list: List of question dictionaries
    """
    # Convert grade to string if it's a number
    grade = str(grade)
    
    # Check if subject and grade exist in the database
    if subject not in QUESTIONS_DB or grade not in QUESTIONS_DB[subject]:
        return []
    
    # Get questions for the subject and grade
    questions = QUESTIONS_DB[subject][grade]
    
    # Return requested number of questions (or all if fewer are available)
    import random
    if len(questions) <= count:
        return questions
    else:
        return random.sample(questions, count)


# For testing
if __name__ == "__main__":
    import json
    
    # Test getting questions
    math_questions = get_questions_by_subject_and_grade("math", 5, 2)
    print(json.dumps(math_questions, indent=2))
    
    # Test getting questions for a non-existent grade
    invalid_questions = get_questions_by_subject_and_grade("science", 100)
    print(f"Invalid grade questions: {len(invalid_questions)}")