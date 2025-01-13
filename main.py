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
        
        # Get character info
        name = parser.get_name()
        username = parser.get_username()
        languages = parser.get_languages()
        
        # Create output data
        output_data = {
            'player_username': username,
            'character_name': name,
            'languages': languages
        }
        
        # Save to output file
        parser.save_output(output_data, 'character_info.json')
        print(f"Successfully parsed character info:")
        print(f"Player Username: {username}")
        print(f"Character Name: {name}")
        print(f"Languages: {', '.join(languages)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 