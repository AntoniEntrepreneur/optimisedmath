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

# --- THE MAPPER ---
MATH_MAP = {
    "add_fractions_simple": add_fractions_simple
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