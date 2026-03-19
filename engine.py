import pandas as pd
import random
import os
import math

DATA_FILE = 'Courses_Data.csv'

# --- HELPER FUNCTIONS ---
def format_fraction(num, den, whole=None):
    """Format a fraction (or mixed number) as raw LaTeX."""
    # We removed the $ signs from here so the equation stays connected
    if whole is not None:
        return rf"{whole}\frac{{{num}}}{{{den}}}"
    else:
        return rf"\frac{{{num}}}{{{den}}}"

# --- THE MATH FUNCTIONS (The "Chefs") ---
def add_fractions_simple(level):
    """Level 1: Identical denominators, sum < 1, NOT simplifiable."""
    while True:
        if level == 1:
            den = random.randint(3, 9)
        else:
            den = random.randint(10, 20) 
            
        # Ensure num1 + num2 is strictly less than den
        num1 = random.randint(1, den - 2)
        num2 = random.randint(1, den - num1 - 1)
        
        # Science-based check: The Greatest Common Divisor must be 1 (meaning it cannot be simplified)
        if math.gcd(num1 + num2, den) == 1:
            break # The math is perfect, break out of the loop and serve the problem
            
    return {
        "question": f"Oblicz: {format_fraction(num1, den)} + {format_fraction(num2, den)}",
        "correct": f"$\\displaystyle {format_fraction(num1+num2, den)}$",
        "trap": f"$\\displaystyle {format_fraction(num1+num2, den+den)}$",
        "wrong": f"$\\displaystyle {format_fraction(num1+num2+1, den)}$",
        "level_display": f"Poziom {level}" 
    }

def add_fractions_complex(level):
    pairs = [(2, 3), (2, 5), (3, 4), (3, 5), (4, 5)]
    d1, d2 = random.choice(pairs)
    
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    
    common_den = d1 * d2
    correct_num = (n1 * d2) + (n2 * d1)
    
    trap_num = n1 + n2
    trap_den = d1 + d2
    
    wrong_num = n1 + n2
    
    return {
        "question": f"Oblicz: {format_fraction(n1, d1)} + {format_fraction(n2, d2)}",
        "correct": f"$\\displaystyle {format_fraction(correct_num, common_den)}$",
        "trap": f"$\\displaystyle {format_fraction(trap_num, trap_den)}$",
        "wrong": f"$\\displaystyle {format_fraction(wrong_num, common_den)}$",
        "level_display": f"Poziom {level}: Różne mianowniki"
    }

def add_mixed_numbers_simple(level):
    den = random.randint(3, 9)
    
    w1 = random.randint(1, 5)
    w2 = random.randint(1, 5)
    
    n1 = random.randint(1, den - 2)
    n2 = random.randint(1, den - n1 - 1) 
    
    correct_whole = w1 + w2
    correct_numerator = n1 + n2
    
    trap_whole = w1 + w2
    trap_numerator = n1 + n2
    trap_denominator = den + den 
    
    improper1_num = w1 * den + n1
    improper2_num = w2 * den + n2
    wrong_improper_sum = improper1_num + improper2_num + 1 
    
    return {
        "question": f"Oblicz: {format_fraction(n1, den, w1)} + {format_fraction(n2, den, w2)}",
        "correct": f"$\\displaystyle {format_fraction(correct_numerator, den, correct_whole)}$",
        "trap": f"$\\displaystyle {format_fraction(trap_numerator, trap_denominator, trap_whole)}$",
        "wrong": f"$\\displaystyle {format_fraction(wrong_improper_sum, den)}$",
        "level_display": f"Poziom {level}: Liczby mieszane (Łatwe)"
    }

def add_mixed_numbers_complex(level):
    pairs = [(2, 3), (2, 5), (3, 4), (3, 5), (4, 5)]
    d1, d2 = random.choice(pairs)
    
    w1 = random.randint(1, 3)
    w2 = random.randint(1, 3)
    
    common_den = d1 * d2
    while True:
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        if (n1 * d2 + n2 * d1) > common_den:
            break
    
    frac_numerator_sum = (n1 * d2) + (n2 * d1)
    carry = frac_numerator_sum // common_den
    remainder = frac_numerator_sum % common_den
    correct_whole = w1 + w2 + carry
    correct_numerator = remainder
    
    trap_whole = w1 + w2
    trap_numerator = frac_numerator_sum
    trap_denominator = common_den
    
    wrong_whole = w1 + w2
    wrong_numerator = n1 + n2
    wrong_denominator = common_den
    
    return {
        "question": f"Oblicz: {format_fraction(n1, d1, w1)} + {format_fraction(n2, d2, w2)}",
        "correct": f"$\\displaystyle {format_fraction(correct_numerator, common_den, correct_whole)}$",
        "trap": f"$\\displaystyle {format_fraction(trap_numerator, trap_denominator, trap_whole)}$",
        "wrong": f"$\\displaystyle {format_fraction(wrong_numerator, wrong_denominator, wrong_whole)}$",
        "level_display": f"Poziom {level}: Liczby mieszane (Ostateczny boss)"
    }

MATH_MAP = {
    "add_fractions_simple": add_fractions_simple,
    "add_fractions_complex": add_fractions_complex,
    "add_mixed_numbers_simple": add_mixed_numbers_simple,
    "add_mixed_numbers_complex": add_mixed_numbers_complex
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