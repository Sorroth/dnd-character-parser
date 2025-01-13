import json
from pathlib import Path
import pytest
from src.parser import CharacterParser

def test_character_info_output():
    """Test that character info is correctly parsed and saved to file."""
    # Initialize parser
    parser = CharacterParser('data/Miriam Hopps.json')
    
    # Get character info
    name = parser.get_name()
    username = parser.get_username()
    stats = parser.get_stats()
    race = parser.get_race()
    
    # Create output data
    output_data = {
        'player_username': username,
        'character_name': name,
        'stats': stats,
        'race': race
    }
    
    # Save to output file
    parser.save_output(output_data, 'character_info.json')
    
    # Verify the file exists
    assert Path('output/character_info.json').exists()
    
    # Read the output file and verify contents
    with open('output/character_info.json', 'r', encoding='utf-8') as file:
        saved_data = json.load(file)
        assert saved_data['player_username'] == 'whitneyowilkinson'
        assert saved_data['character_name'] == 'Miriam Hopps'
        assert saved_data['stats'] == {
            'strength': 18,
            'dexterity': 18,
            'constitution': 18,
            'intelligence': 9,
            'wisdom': 13,
            'charisma': 15
        }
        assert saved_data['race']['species'] == 'Variant Human'
        assert set(saved_data['race']['languages']) == {'Common', 'Draconic'}
        assert saved_data['race']['skills'] == ['Perception']
        assert saved_data['race']['ability_bonuses'] == {
            'strength': 1,
            'dexterity': 1
        }

def test_character_name_direct():
    """Test that character name is correctly parsed from JSON."""
    parser = CharacterParser('data/Miriam Hopps.json')
    assert parser.get_name() == 'Miriam Hopps'

def test_player_username():
    """Test that player username is correctly parsed from JSON."""
    parser = CharacterParser('data/Miriam Hopps.json')
    assert parser.get_username() == 'whitneyowilkinson'

def test_stats():
    """Test that stats are correctly parsed from JSON."""
    parser = CharacterParser('data/Miriam Hopps.json')
    stats = parser.get_stats()
    assert stats == {
        'strength': 18,
        'dexterity': 18,
        'constitution': 18,
        'intelligence': 9,
        'wisdom': 13,
        'charisma': 15
    }

def test_race():
    """Test that race is correctly parsed from JSON."""
    parser = CharacterParser('data/Miriam Hopps.json')
    race = parser.get_race()
    assert race['species'] == 'Variant Human'
    assert set(race['languages']) == {'Common', 'Draconic'}
    assert race['skills'] == ['Perception']
    assert race['ability_bonuses'] == {
        'strength': 1,
        'dexterity': 1
    } 