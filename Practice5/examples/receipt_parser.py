import re

#Example 1

def exercise_1():
    print("\n" + "=" * 60)
    print("EXERCISE 1: Match 'a' followed by zero or more 'b'")
    print("=" * 60)
    
    # Pattern: 'a' followed by zero or more 'b'
    pattern = r'ab*'
    
    # Test strings
    test_strings = ['a', 'ab', 'abb', 'abbb', 'b', 'abc', 'abbbbb']
    
    for s in test_strings:
        if re.fullmatch(pattern, s):
            print(f"✓ '{s}' matches pattern (a + zero or more b)")
        else:
            print(f"✗ '{s}' does NOT match pattern")
    
    # Find all matches in a text
    text = "Find a, ab, abb, abbb in this text"
    matches = re.findall(pattern, text)
    print(f"\nAll matches found: {matches}")


#Example 2

def exercise_2():
    print("\n" + "=" * 60)
    print("EXERCISE 2: Match 'a' followed by two to three 'b'")
    print("=" * 60)
    
    # Pattern: 'a' followed by exactly 2 or 3 'b'
    pattern = r'ab{2,3}'
    
    # Test strings
    test_strings = ['ab', 'abb', 'abbb', 'abbbb', 'a', 'abc']
    
    for s in test_strings:
        if re.fullmatch(pattern, s):
            print(f"✓ '{s}' matches pattern (a + 2-3 b)")
        else:
            print(f"✗ '{s}' does NOT match pattern")
    
    # Extract from text
    text = "Strings: ab, abb, abbb, abbbb"
    matches = re.findall(pattern, text)
    print(f"\nMatches found in text: {matches}")


#Example 3

def exercise_3():
    print("\n" + "=" * 60)
    print("Example 3: Find lowercase sequences joined with underscore")
    print("=" * 60)
    
    # Pattern for snake case: words in lowercase separated by underscore
    pattern = r'\b[a-z]+(_[a-z]+)*\b'
    
    # Test text with various formats
    text = "Variables: user_name, first_name, age, user_123, UserName, user-name"
    
    matches = re.findall(pattern, text)
    print(f"Original text: {text}")
    print(f"\nSnake case variables found: {matches}")
    
    # Test individual strings
    test_strings = ['hello', 'hello_world', 'hello_world_python', 'Hello_World', 'hello-world']
    
    print("\nTesting individual strings:")
    for s in test_strings:
        if re.fullmatch(pattern, s):
            print(f"✓ '{s}' is valid snake case")
        else:
            print(f"✗ '{s}' is NOT valid snake case")


#Example 4

def exercise_4():
    print("\n" + "=" * 60)
    print("Example 4: Replace space, comma, or dot with colon")
    print("=" * 60)
    
    # Test strings with different separators
    test_strings = [
        'Hello, world.',
        'First, second. third',
        'One. Two, Three',
        'Space comma, dot.'
    ]
    
    for i, s in enumerate(test_strings, 1):
        # Replace space, comma, or dot with colon
        replaced = re.sub(r'[ ,.]', ':', s)
        print(f"\nOriginal {i}: '{s}'")
        print(f"Replaced {i}: '{replaced}'")
    
    # Version that handles multiple consecutive separators
    text = "Many,, spaces... and, commas."
    result = re.sub(r'[ ,.]+', ':', text)
    print(f"\nMultiple separators: '{text}'")
    print(f"After replacement:   '{result}'")


#Example 5

def exercise_5():
    print("\n" + "=" * 60)
    print("Example 5: Split string at uppercase letters")
    print("=" * 60)
    
    # Test strings with camelCase or PascalCase
    test_strings = [
        'HelloWorldPython',
        'camelCaseExample',
        'XMLHttpRequest',
        'UpperCaseLetters'
    ]
    
    for s in test_strings:
        # Split at uppercase letters (keep the uppercase letter)
        parts = re.findall(r'[A-Z][a-z]*|[a-z]+', s)
        print(f"\nOriginal: '{s}'")
        print(f"Split:    {parts}")
        print(f"Joined:   '{" ".join(parts)}'")
    
    # Alternative using re.split with positive lookahead
    print("\nUsing re.split with lookahead:")
    text = "SplitThisString"
    result = re.split(r'(?=[A-Z])', text)
    print(f"'{text}' -> {result[1:]}")


#Main function to run all examples
if __name__ == "__main__":
    """
    Main function to demonstrate all regex exercises
    """
    print("=" * 60)
    print("REGEX EXERCISES - RECEIPT PARSER")
    print("=" * 60)
    
    # Run all exercises
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    
    print("\n" + "=" * 60)
    print("ALL EXERCISES COMPLETED")
    print("=" * 60)