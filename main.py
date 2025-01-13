from src.parser import CharacterParser
from src.utils import validate_json_file
import sys

def main():
    """Main function to run the character parser."""
    parser = CharacterParser('data/Miriam Hopps.json')
    
    # Get parsed data
    output_data = parser.parse()
    
    # Save to output file
    parser.save_output(output_data, 'character_info.json')

if __name__ == '__main__':
    main() 