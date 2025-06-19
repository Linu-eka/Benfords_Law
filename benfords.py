from collections import Counter
import math

def calculate_benfords(amounts):
    """
    Calculate the first digit distribution of the given amounts and compare it to Benford's Law.
    
    Args:
        amounts (list): List of amounts to analyze.
    
    Returns:
        tuple: A tuple containing:
            total_count (int): Total number of amounts analyzed.
            comparison (dict): Dictionary containing the expected and real frequency of first digits.
    """
    
    #Extract first digits from amounts
    first_digits = [str(int(str(amount)[0])) for amount in amounts if amount > 0]
    total_count = len(first_digits)
    digit_count = Counter(first_digits)
    
    # Calculate the expected frequency according to Benford's Law
    expected_frequency = {str(digit): (math.log10(1 + 1/digit)) for digit in range(1, 10)}

    expected_count = {str(digit): expected_frequency[str(digit)] * total_count for digit in range(1, 10)}

    real_frequency = {str(digit): digit_count.get(str(digit), 0) / total_count for digit in range(1, 10)}

    #Compare the real frequency with the expected frequency
    comparison = {}
    for digit in range(1, 10):
        expected = expected_frequency[str(digit)]
        real = real_frequency[str(digit)]
        comparison[str(digit)] = {
            'expected': round(expected*100,4),
            'real': round(real*100,4),
            'difference': round(abs(expected - real)*100,4)
        }
    return total_count,digit_count, expected_count, comparison

    
