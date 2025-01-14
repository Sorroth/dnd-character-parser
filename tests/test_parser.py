import json
from pathlib import Path
import pytest
from src.parser import CharacterParser

@pytest.fixture
def parser():
    """Create a parser instance for testing."""
    return CharacterParser('data/Miriam Hopps.json')

def test_character_info_output():
    """Test that character info is correctly parsed and saved to file."""
    # Initialize parser
    parser = CharacterParser('data/Miriam Hopps.json')
    
    # Get character info
    name = parser.get_name()
    username = parser.get_username()
    stats = parser.get_stats()
    race = parser.get_race()
    classes = parser.get_classes()
    
    # Create output data
    output_data = {
        'player_username': username,
        'character_name': name,
        'stats': stats,
        'race': race,
        'classes': classes
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
        assert len(saved_data['classes']) == 1
        fighter = saved_data['classes'][0]
        assert fighter['base_class']['name'] == 'Fighter'
        assert fighter['base_class']['level'] == 4
        assert fighter['subclass']['name'] == 'Echo Knight'

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

def test_class_proficiencies():
    """Test that class proficiencies are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    proficiencies = parser.get_class_proficiencies()
    
    # Check that we get all expected proficiencies
    expected_proficiencies = [
        "Light Armor",
        "Medium Armor",
        "Heavy Armor",
        "Shields",
        "Simple Weapons",
        "Martial Weapons",
        "Strength Saving Throws",
        "Constitution Saving Throws",
        "Acrobatics",
        "Athletics"
    ]
    
    prof_names = [prof["name"] for prof in proficiencies]
    assert sorted(prof_names) == sorted(expected_proficiencies)
    
    # Check format of proficiencies
    for prof in proficiencies:
        assert "name" in prof
        assert "description" in prof
        assert len(prof["description"]) == 1
        assert prof["description"][0] == f"Proficiency in {prof['name']}"

def test_classes():
    """Test that classes are correctly parsed from JSON."""
    parser = CharacterParser('data/Miriam Hopps.json')
    classes = parser.get_classes()
    
    assert isinstance(classes, list)
    assert len(classes) == 1
    
    fighter = classes[0]
    assert fighter['base_class']['name'] == 'Fighter'
    assert fighter['base_class']['level'] == 4
    
    # Test class bonuses
    bonuses = fighter['base_class']['class_bonuses']
    
    # Should have at least 9 bonuses (1 fighting style + 8 proficiencies)
    assert len(bonuses) >= 9
    
    # Check fighting style
    fighting_style = next(bonus for bonus in bonuses if bonus['name'] == 'Thrown Weapon Fighting')
    assert fighting_style['description'] == [
        "Allows drawing thrown weapons as part of the attack",
        "Adds +2 to damage rolls with thrown weapons"
    ]
    
    # Check a proficiency
    armor_prof = next(bonus for bonus in bonuses if bonus['name'] == 'Light Armor')
    assert armor_prof['description'] == ["Proficiency in Light Armor"]
    
    assert fighter['subclass']['name'] == 'Echo Knight'

def test_parse_output_structure(parser):
    """Test the complete parsed output structure."""
    result = parser.parse()
    
    # Check top level keys
    assert set(result.keys()) == {
        'player_username', 
        'character_name', 
        'stats', 
        'racial_bonuses',
        'classes'
    }
    
    # Check classes structure
    assert isinstance(result['classes'], list)
    assert len(result['classes']) == 1
    
    fighter = result['classes'][0]
    assert fighter['base_class']['name'] == 'Fighter'
    assert fighter['base_class']['level'] == 4
    
    # Check class bonuses
    bonuses = fighter['base_class']['class_bonuses']
    assert len(bonuses) >= 9  # 1 fighting style + 8 proficiencies
    
    # Check fighting style is present
    fighting_style = next(bonus for bonus in bonuses if bonus['name'] == 'Thrown Weapon Fighting')
    assert fighting_style['description'] == [
        "Allows drawing thrown weapons as part of the attack",
        "Adds +2 to damage rolls with thrown weapons"
    ]
    
    # Check a proficiency is present
    armor_prof = next(bonus for bonus in bonuses if bonus['name'] == 'Light Armor')
    assert armor_prof['description'] == ["Proficiency in Light Armor"]
    
    assert fighter['subclass']['name'] == 'Echo Knight' 

def test_class_features():
    """Test that class features are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    classes = parser.get_classes()
    
    fighter = classes[0]
    bonuses = fighter['base_class']['class_bonuses']
    
    # Check for specific class features
    expected_features = [
        "Second Wind",
        "Action Surge"
    ]
    
    excluded_features = [
        "Fighting Style",
        "Martial Archetype",
        "Ability Score Improvement",
        "Hit Points",
        "Equipment",
        "Proficiencies"
    ]
    
    feature_names = [bonus["name"] for bonus in bonuses]
    
    # Check that expected features are present
    for feature in expected_features:
        assert feature in feature_names
    
    # Check that excluded features are not present
    for feature in excluded_features:
        assert feature not in feature_names
    
    # Check specific feature details
    second_wind = next(bonus for bonus in bonuses if bonus["name"] == "Second Wind")
    assert any("regain hit points equal to 1d10 + your fighter level" in line 
              for line in second_wind["description"])
    
    action_surge = next(bonus for bonus in bonuses if bonus["name"] == "Action Surge")
    assert any("take one additional action" in line 
              for line in action_surge["description"]) 