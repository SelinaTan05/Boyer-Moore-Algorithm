# Implementation of the Full Boyer-Moore String Search Algorithm
# Incorporating both Bad Character and Good Suffix Heuristics

def preprocess_bad_character(pattern, m):
    """
    Build the Bad Character table.
    Stores the rightmost index of every character present in the pattern.
    """
    bad_char = {}
    
    # Record the last occurrence of each character in the pattern
    for i in range(m):
        bad_char[pattern[i]] = i
        
    return bad_char

def preprocess_strong_suffix(shift, bpos, pattern, m):
    """
    Build shift values for the Strong Good Suffix rule.
    """
    i = m
    j = m + 1
    bpos[i] = j

    while i > 0:
        # Find the next matching border
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = bpos[j]
            
        i -= 1
        j -= 1
        bpos[i] = j

def preprocess_case_2(shift, bpos, pattern, m):
    """
    Handle suffixes that also match a pattern prefix.
    """
    j = bpos[0]
    
    for i in range(m + 1):
        # Fill remaining shift values
        if shift[i] == 0:
            shift[i] = j
            
        # Move to the next border
        if i == j:
            j = bpos[j]

def boyer_moore_search(text, pattern):
    """
    Search for all occurrences of a pattern using Boyer-Moore.
    """
    m = len(pattern)
    n = len(text)

    # Edge case: Empty pattern
    if m == 0:
        return []

    # Good Suffix tables
    bpos = [0] * (m + 1)
    shift = [0] * (m + 1)

    # Build Bad Character table
    bad_char = preprocess_bad_character(pattern, m)

    # Build Good Suffix table
    preprocess_strong_suffix(shift, bpos, pattern, m)
    
    # Preprocess the pattern for good suffix rule 
    preprocess_case_2(shift, bpos, pattern, m)

    s = 0 
    occurrences = [] 
    found = False 

    # Perform the search
    while s <= (n - m):
        j = m - 1

        # Compare from right to left
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        # Match found
        if j < 0:
            occurrences.append(s)
            print(f"Pattern occurs at shift = {s}")
            found = True

            # Shift according to Good Suffix rule
            s += shift[0]
        else:
            # Bad Character shift
            bad_char_shift = j - bad_char.get(text[s + j], -1)

            # Good Suffix shift
            good_suffix_shift = shift[j + 1]

            # Apply the larger shift
            s += max(good_suffix_shift, bad_char_shift)

    if not found:
        print("Pattern not found")
        
    return occurrences

# Driver code
if __name__ == "__main__":
    print("--- Boyer-Moore Algorithm Execution ---")

    text_input = input("Key in the Text: ")
    pattern_input = input("Key in the Pattern: ")
    
    boyer_moore_search(text_input, pattern_input)
