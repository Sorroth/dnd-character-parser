from src.parser import CharacterParser
from src.utils import validate_json_file
import sys

def main():
    # Input file path
    input_file = 'data/Miriam Hopps.json'
    
    # Validate input file
    if not validate_json_file(input_file):
        print("Error: Invalid input file")
        sys.exit(1)
    
    try:
        # Initialize parser
        parser = CharacterParser(input_file)
        
        # Get character name and username
        name = parser.get_name()
        username = parser.get_username()
        
        # Create output data with username first
        output_data = {
            'player_username': username,
            'character_name': name
        }
        
        # Save to output file
        parser.save_output(output_data, 'character_info.json')
        print(f"Successfully parsed character info:")
        print(f"Player Username: {username}")
        print(f"Character Name: {name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 