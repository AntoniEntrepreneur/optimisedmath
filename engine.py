import pandas as pd
import random
import os

DATA_FILE = 'Courses_Data.csv'

# --- HELPER FUNCTIONS ---
def format_fraction(num, den, whole=None):
    """Format a fraction (or mixed number) as LaTeX.
    
    Args:
        num: Numerator
        den: Denominator
        whole: Whole number part (optional). If provided, returns mixed number format.
    
    Returns:
        LaTeX-formatted string (wrapped in $ delimiters) for the fraction or mixed number.
    """
    if whole is not None:
        return rf"${whole}\frac{{{num}}}{{{den}}}$"
    else:
        return rf"$\frac{{{num}}}{{{den}}}$"

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
        "question": f"Oblicz: {format_fraction(num1, den)} + {format_fraction(num2, den)}",
        "correct": format_fraction(num1+num2, den) + "\n",
        "trap": format_fraction(num1+num2, den+den) + "\n",
        "wrong": format_fraction(num1+num2+1, den),
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
        "question": f"Oblicz: {format_fraction(n1, d1)} + {format_fraction(n2, d2)}",
        "correct": format_fraction(correct_num, common_den) + "\n",
        "trap": format_fraction(trap_num, trap_den) + "\n",
        "wrong": format_fraction(wrong_num, common_den),
        "level_display": f"Poziom {level}: Różne mianowniki"
    }

def add_mixed_numbers_simple(level):
    """Logic for Level 4: Mixed Numbers (Easy) - Identical Denominators, Fraction Sum < 1"""
    # 1. Pick identical denominator
    den = random.randint(3, 9)
    
    # 2. Pick whole numbers (typically 1-5 each)
    w1 = random.randint(1, 5)
    w2 = random.randint(1, 5)
    
    # 3. Pick numerators such that their sum < denominator (no carrying over)
    n1 = random.randint(1, den - 2)
    n2 = random.randint(1, den - n1 - 1)  # Ensures n1 + n2 < den
    
    # 4. Calculate correct answer
    correct_whole = w1 + w2
    correct_numerator = n1 + n2
    
    # 5. Generate the trap: Add whole numbers correctly, but add denominators for fractions
    trap_whole = w1 + w2
    trap_numerator = n1 + n2
    trap_denominator = den + den  # Level 1 trap: add denominators
    
    # 6. Generate wrong answer: Convert to improper fractions but make arithmetic error
    improper1_num = w1 * den + n1
    improper2_num = w2 * den + n2
    wrong_improper_sum = improper1_num + improper2_num + 1  # Arithmetic error: +1
    
    # LaTeX question
    question = f"Oblicz: {format_fraction(n1, den, w1)} + {format_fraction(n2, den, w2)}"
    
    return {
        "question": question,
        "correct": format_fraction(correct_numerator, den, correct_whole) + "\n",
        "trap": format_fraction(trap_numerator, trap_denominator, trap_whole) + "\n",
        "wrong": format_fraction(wrong_improper_sum, den),
        "level_display": f"Poziom {level}: Liczby mieszane (Łatwe)"
    }

def add_mixed_numbers_complex(level):
    """Logic for Level 5: Mixed Numbers (The Final Boss) - Coprime denominators, Fraction Sum > 1"""
    # 1. Pick coprime denominators
    pairs = [(2, 3), (2, 5), (3, 4), (3, 5), (4, 5)]
    d1, d2 = random.choice(pairs)
    
    # 2. Pick whole numbers (1 to 3)
    w1 = random.randint(1, 3)
    w2 = random.randint(1, 3)
    
    # 3. Pick numerators such that the sum of fractions exceeds 1
    # We need: (n1 * d2 + n2 * d1) / (d1 * d2) > 1
    # Which means: n1 * d2 + n2 * d1 > d1 * d2
    common_den = d1 * d2
    while True:
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        if (n1 * d2 + n2 * d1) > common_den:
            break
    
    # 4. Calculate correct answer
    # Convert to improper fractions, find sum, then convert back to mixed number
    frac_numerator_sum = (n1 * d2) + (n2 * d1)
    carry = frac_numerator_sum // common_den
    remainder = frac_numerator_sum % common_den
    correct_whole = w1 + w2 + carry
    correct_numerator = remainder
    
    # 5. Generate the trap: Add whole numbers correctly, but leave fractional part as improper
    # (fail to carry the 1 over from improper fraction)
    trap_whole = w1 + w2
    trap_numerator = frac_numerator_sum
    trap_denominator = common_den
    
    # 6. Generate wrong answer: Use common denominator but add original unscaled numerators
    # (forget to scale the numerators before adding)
    wrong_whole = w1 + w2
    wrong_numerator = n1 + n2
    wrong_denominator = common_den
    
    # LaTeX question
    question = f"Oblicz: {format_fraction(n1, d1, w1)} + {format_fraction(n2, d2, w2)}"
    
    return {
        "question": question,
        "correct": format_fraction(correct_numerator, common_den, correct_whole) + "\n",
        "trap": format_fraction(trap_numerator, trap_denominator, trap_whole) + "\n",
        "wrong": format_fraction(wrong_numerator, wrong_denominator, wrong_whole),
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