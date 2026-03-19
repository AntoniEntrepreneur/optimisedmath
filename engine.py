import pandas as pd
import random
import os

DATA_FILE = 'Courses_Data.csv'

# --- THE MATH FUNCTIONS (The "Chefs") ---
def add_fractions_simple(level):
    """Logic that separates difficulty strictly by level."""
    if level == 1:
        den = random.randint(3, 9)
    else:
        den = random.randint(10, 20) 
        
    num1 = random.randint(1, den - 1)
    num2 = random.randint(1, den - 1)
    
    return {
        "question": f"Oblicz: {num1}/{den} + {num2}/{den}",
        "correct": f"{num1+num2}/{den}",
        "trap": f"{num1+num2}/{den+den}",
        "wrong": f"{num1+num2+1}/{den}",
        "level_display": f"Poziom {level}" 
    }

def add_fractions_complex(level):
    """Logic for Level 3: Coprime denominators (Double Conversion)"""
    # 1. Pick coprime denominators (e.g., 3 and 4, or 2 and 5)
    pairs = [(2, 3), (2, 5), (3, 4), (3, 5), (4, 5)]
    d1, d2 = random.choice(pairs)
    
    # 2. Pick numerators
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    
    # 3. Calculate correct answer: (n1*d2 + n2*d1) / (d1*d2)
    common_den = d1 * d2
    correct_num = (n1 * d2) + (n2 * d1)
    
    # 4. Generate the "Level 1 Trap" (Adding numerators and denominators)
    # Based on your CSV rule: "Calculate by adding numerator to numerator and denominator to denominator directly."
    trap_num = n1 + n2
    trap_den = d1 + d2
    
    # 5. Generate a "Forgotten Scaling" Generic Error
    # Based on your CSV rule: "Calculate using correct common denominator, but fail to multiply numerators."
    wrong_num = n1 + n2
    
    return {
        "question": f"Oblicz: {n1}/{d1} + {n2}/{d2}",
        "correct": f"{correct_num}/{common_den}",
        "trap": f"{trap_num}/{trap_den}",
        "wrong": f"{wrong_num}/{common_den}",
        "level_display": f"Poziom {level}: Różne mianowniki"
    }

MATH_MAP = {
    "add_fractions_simple": add_fractions_simple,
    "add_fractions_complex": add_fractions_complex  # New link added
}

# --- THE LIBRARIAN ---
def get_problem_from_db(topic, level):
    if not os.path.exists(DATA_FILE):
        return {"error": "Missing CSV"}
    
    df = pd.read_csv(DATA_FILE, sep=';')
    
    row = df[(df['Micro_Topic'] == topic) & (df['Level'] == level)]
    
    if not row.empty:
        func_name = row.iloc[0]['Function_Name']
        current_level = int(row.iloc[0]['Level'])
        
        if func_name in MATH_MAP:
            return MATH_MAP[func_name](current_level)
    return None