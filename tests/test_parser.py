import json
from pathlib import Path
import pytest
from src.parser import CharacterParser

def test_character_name_output():
    """Test that character name is correctly parsed and saved to file."""
    # Initialize parser
    parser = CharacterParser('data/Miriam Hopps.json')
    
    # Get name and create output data
    name = parser.get_name()
    output_data = {'character_name': name}
    
    # Save to test output file
    test_output_file = 'output/test_character_name.json'
    parser.save_output(output_data, 'test_character_name.json')
    
    # Verify the file exists
    assert Path(test_output_file).exists()
    
    # Read the output file and verify contents
    with open(test_output_file, 'r', encoding='utf-8') as file:
        saved_data = json.load(file)
        assert saved_data['character_name'] == 'Miriam Hopps'

def test_character_name_direct():
    """Test that character name is correctly parsed from JSON."""
    parser = CharacterParser('data/Miriam Hopps.json')
    assert parser.get_name() == 'Miriam Hopps' 

def test_player_username():
    """Test that player username is correctly parsed from JSON."""
    parser = CharacterParser('data/Miriam Hopps.json')
    assert parser.get_username() == 'whitneyowilkinson' 