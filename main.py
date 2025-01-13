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
        
        # Get character name
        name = parser.get_name()
        
        # Create output data
        output_data = {
            'character_name': name
        }
        
        # Save to output file
        parser.save_output(output_data, 'character_name.json')
        print(f"Successfully parsed character name: {name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 