"""
Simple Custom Password Hashing 
Uses string indexing and slicing - simple approach
"""

def simple_hash(password):
    """
    Simple custom hash using string manipulation
    Uses indexing, slicing, and character code transformations
    """
    if not password:
        return ""
    
    # Convert to string and add length marker
    pwd = str(password)
    length = len(pwd)
    
    # Step 1: Reverse the string
    result = pwd[::-1]
    
    # Step 2: Add character positions as numbers
    temp = ""
    for i, char in enumerate(result):
        temp += char + str(i % 10)
    result = temp
    
    # Step 3: Convert characters to their ASCII codes and mix
    coded = ""
    for i, char in enumerate(result):
        code = ord(char) + length + i
        coded += str(code) + "-"
    
    # Step 4: Reverse again and add prefix/suffix
    final = "PW" + coded[::-1] + "END"
    
    # Step 5: Insert the original length at position 5
    final = final[:5] + str(length) + final[5:]
    
    return final


def verify_simple_hash(password, hashed):
    """
    Verify password against simple hash
    """
    if not password or not hashed:
        return False
    
    return simple_hash(password) == hashed


# Example usage:
if __name__ == "__main__":
    password = "test123"
    hashed = simple_hash(password)
    print(f"Password: {password}")
    print(f"Hashed: {hashed}")
    print(f"Verify correct: {verify_simple_hash(password, hashed)}")
    print(f"Verify wrong: {verify_simple_hash('wrong', hashed)}")
