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
    
    # Get character info directly using parse()
    output_data = parser.parse()
    
    # Save to output file
    parser.save_output(output_data, 'character_info.json')
    
    # Verify the file exists
    assert Path('output/character_info.json').exists()
    
    # Read the output file and verify contents
    with open('output/character_info.json', 'r', encoding='utf-8') as file:
        saved_data = json.load(file)
        
        # Verify all top-level keys are present
        assert set(saved_data.keys()) == {
            'player_username',
            'character_name',
            'characteristics',
            'stats',
            'race',
            'classes',
            'feats',
            'background',
            'inventory'
        }
        
        # Verify basic content
        assert saved_data['player_username'] == 'whitneyowilkinson'
        assert saved_data['character_name'] == 'Miriam Hopps'
        
        # Verify stats
        assert saved_data['stats'] == {
            'strength': 18,
            'dexterity': 18,
            'constitution': 18,
            'intelligence': 9,
            'wisdom': 13,
            'charisma': 15
        }
        
        # Verify race
        assert saved_data['race']['name'] == 'Variant Human'
        assert set(saved_data['race']['languages']) == {'Common', 'Draconic'}
        assert saved_data['race']['skills'] == ['Perception']
        assert saved_data['race']['ability_bonuses'] == {
            'strength': 1,
            'dexterity': 1
        }
        
        # Verify classes
        assert len(saved_data['classes']) == 1
        fighter = saved_data['classes'][0]
        assert fighter['base_class']['name'] == 'Fighter'
        assert fighter['base_class']['level'] == 4
        assert fighter['subclass']['name'] == 'Echo Knight'
        
        # Verify feats
        assert len(saved_data['feats']) == 2
        assert any(feat['name'] == 'Sharpshooter' for feat in saved_data['feats'])
        assert any(feat['name'] == 'Tavern Brawler' for feat in saved_data['feats'])
        
        # Verify inventory exists and has items
        assert 'inventory' in saved_data
        assert isinstance(saved_data['inventory'], list)
        assert len(saved_data['inventory']) > 0

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
    assert race['name'] == 'Variant Human'
    assert set(race['languages']) == {'Common', 'Draconic'}
    assert race['skills'] == ['Perception']
    assert race['ability_bonuses'] == {
        'strength': 1,
        'dexterity': 1
    }

def test_class_proficiencies():
    """Test that class proficiencies are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    classes = parser.get_classes()
    
    # Get fighter proficiencies
    fighter = classes[0]['base_class']
    proficiencies = fighter['class_bonuses']['proficiencies']
    
    # Check that we get all expected proficiencies
    expected_proficiencies = [
        "Acrobatics",
        "Athletics",
        "Constitution Saving Throws",
        "Heavy Armor",
        "Light Armor",
        "Martial Weapons",
        "Medium Armor",
        "Shields",
        "Simple Weapons",
        "Strength Saving Throws"
    ]
    
    assert sorted(proficiencies) == expected_proficiencies
    
    # Check that proficiencies are not in features
    feature_names = [feature['name'] for feature in fighter['class_bonuses']['features']]
    assert not any('Proficiency' in name for name in feature_names)

def test_classes():
    """Test that classes are correctly parsed from JSON."""
    parser = CharacterParser('data/Miriam Hopps.json')
    classes = parser.get_classes()
    
    assert isinstance(classes, list)
    assert len(classes) == 1
    
    fighter = classes[0]
    assert fighter['base_class']['name'] == 'Fighter'
    assert fighter['base_class']['level'] == 4
    
    # Test class features
    features = fighter['base_class']['class_bonuses']['features']
    assert len(features) == 3  # fighting style + second wind + action surge
    
    # Check proficiencies are in class_bonuses
    proficiencies = fighter['base_class']['class_bonuses']['proficiencies']
    assert len(proficiencies) == 10  # Should have 10 proficiencies

def test_parse_output_structure(parser):
    """Test the complete parsed output structure."""
    result = parser.parse()
    
    # Check top level keys
    assert set(result.keys()) == {
        'player_username',
        'character_name',
        'characteristics',
        'stats',
        'race',
        'classes',
        'feats',
        'background',
        'inventory'
    }
    
    # Verify characteristics structure
    assert result['characteristics'] == {
        "gender": "Female",
        "faith": "Chauntea",
        "age": 20,
        "hair": "Brown",
        "eyes": "Brown",
        "skin": "White",
        "height": "6'0\"",
        "weight": 200
    }
    
    # Remove characteristics verification
    
    # Check classes structure
    assert isinstance(result['classes'], list)
    assert len(result['classes']) == 1
    
    fighter = result['classes'][0]
    assert fighter['base_class']['name'] == 'Fighter'
    assert fighter['base_class']['level'] == 4
    
    # Check class features
    features = fighter['base_class']['class_bonuses']['features']
    assert len(features) == 3  # fighting style + second wind + action surge
    
    # Check fighting style is present
    fighting_style = next(feature for feature in features if feature['name'] == 'Thrown Weapon Fighting')
    assert fighting_style['description'] == [
        "Allows drawing thrown weapons as part of the attack",
        "Adds +2 to damage rolls with thrown weapons"
    ]
    
    assert fighter['subclass']['name'] == 'Echo Knight'

def test_class_features():
    """Test that class features are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    classes = parser.get_classes()
    
    fighter = classes[0]
    features = fighter['base_class']['class_bonuses']['features']
    
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
    
    feature_names = [feature["name"] for feature in features]
    
    # Check that expected features are present
    for feature in expected_features:
        assert feature in feature_names
    
    # Check that excluded features are not present
    for feature in excluded_features:
        assert feature not in feature_names
    
    # Check specific feature details
    second_wind = next(feature for feature in features if feature["name"] == "Second Wind")
    assert any("regain hit points equal to 1d10 + your fighter level" in line 
              for line in second_wind["description"])
    
    action_surge = next(feature for feature in features if feature["name"] == "Action Surge")
    assert any("take one additional action" in line 
              for line in action_surge["description"])

def test_subclass_features():
    """Test that subclass features are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    classes = parser.get_classes()
    
    fighter = classes[0]
    assert fighter['subclass']['name'] == 'Echo Knight'
    assert fighter['base_class']['level'] == 4  # Verify character level
    
    # Check subclass bonuses exist
    assert 'subclass_bonuses' in fighter['subclass']
    subclass_bonuses = fighter['subclass']['subclass_bonuses']
    
    # Get all feature names
    feature_names = [bonus["name"] for bonus in subclass_bonuses]
    
    # Check that only features available at level 4 are included
    assert "Manifest Echo" in feature_names  # Level 3 feature
    assert "Unleash Incarnation" in feature_names  # Level 3 feature
    assert "Echo Avatar" not in feature_names  # Level 7 feature
    assert "Shadow Martyr" not in feature_names  # Level 10 feature
    assert "Reclaim Potential" not in feature_names  # Level 15 feature
    assert "Legion of One" not in feature_names  # Level 18 feature
    
    # Check format of features
    for bonus in subclass_bonuses:
        assert "name" in bonus
        assert "description" in bonus
        assert isinstance(bonus["description"], list)
        assert len(bonus["description"]) > 0
        
        # Check that descriptions don't contain HTML or Unicode characters
        # (except for bullet points)
        for line in bonus["description"]:
            assert '<' not in line  # No HTML tags
            assert '&' not in line  # No HTML entities
            # Allow bullet points but no other Unicode
            cleaned_line = line.replace('\u2022', '')  # Remove bullet points
            # Debug: Print any non-ASCII characters
            non_ascii = [c for c in cleaned_line if ord(c) >= 128]
            if non_ascii:
                print(f"Non-ASCII characters found: {non_ascii}")
                print(f"In line: {cleaned_line}")
            assert all(ord(c) < 128 for c in cleaned_line)  # Check remaining chars are ASCII

def test_background():
    """Test that background information is correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    background = parser.get_background()
    
    assert background['name'] == 'Urban Bounty Hunter'
    
    # Check description
    assert 'description' in background
    assert isinstance(background['description'], list)
    assert len(background['description']) == 3  # Three paragraphs
    assert "Before you became an adventurer" in background['description'][0]
    assert "You might be a cunning thief-catcher" in background['description'][1]
    assert "As a member of an adventuring party" in background['description'][2]
    
    # Check background bonuses
    assert 'background_bonuses' in background
    assert isinstance(background['background_bonuses'], list)
    
    # Get all bonus names
    bonus_names = [bonus['name'] for bonus in background['background_bonuses']]
    
    # Check Ear to the Ground feature
    assert 'Ear to the Ground' in bonus_names
    ear_to_ground = next(b for b in background['background_bonuses'] if b['name'] == 'Ear to the Ground')
    assert "segment of society" in ear_to_ground['description'][0]
    
    # Check proficiencies
    expected_proficiencies = [
        'Deception',
        'Medicine',
        "Thieves' Tools",
        'Dragonchess Set'
    ]
    
    # Convert both sides to sets for comparison to avoid order issues
    assert set(expected_proficiencies).issubset(set(bonus_names)) 

def test_characteristics():
    """Test that characteristics are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    characteristics = parser.get_characteristics()
    
    assert characteristics == {
        "gender": "Female",
        "faith": "Chauntea",
        "age": 20,
        "hair": "Brown",
        "eyes": "Brown",
        "skin": "White",
        "height": "6'0\"",
        "weight": 200
    } 

def test_inventory():
    """Test that inventory is correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    inventory = parser.get_inventory()
    
    assert isinstance(inventory, list)
    
    # Check for specific items if they exist
    if inventory:
        # Verify basic structure of each item
        for item in inventory:
            assert 'name' in item
            assert 'quantity' in item
            assert 'description' in item
            assert 'weight' in item
            assert 'cost' in item or item.get('magic', False)  # Magical items might not have cost
            assert isinstance(item.get('cost', {}), dict)
            if 'cost' in item:
                assert 'quantity' in item['cost']
                assert 'unit' in item['cost']
        
        # Verify Donkey is not in inventory
        assert not any(item['name'] == "Donkey (or Mule)" for item in inventory)
        
        # Verify only one Backpack
        backpacks = [item for item in inventory if item['name'] == "Backpack"]
        assert len(backpacks) == 1
        
        # Verify Backpack has container info
        backpack = backpacks[0]
        assert 'container' in backpack
        assert backpack['container']['capacity_weight'] == 30 

def test_feats():
    """Test that feats are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    feats = parser.get_feats()
    
    assert isinstance(feats, list)
    assert len(feats) == 2  # Sharpshooter and Tavern Brawler
    
    # Check Sharpshooter feat
    sharpshooter = next(feat for feat in feats if feat['name'] == 'Sharpshooter')
    assert not sharpshooter['is_homebrew']
    assert len(sharpshooter['description']) > 0
    assert any('long range' in line for line in sharpshooter['description'])
    assert 'modifiers' in sharpshooter
    
    # Check Tavern Brawler feat
    tavern_brawler = next(feat for feat in feats if feat['name'] == 'Tavern Brawler')
    assert tavern_brawler['is_homebrew']
    assert len(tavern_brawler['description']) > 0
    assert any('unarmed strike' in line for line in tavern_brawler['description'])
    
    # Check Tavern Brawler modifiers
    assert 'modifiers' in tavern_brawler
    modifiers = tavern_brawler['modifiers']
    assert len(modifiers) == 3
    
    # Check strength bonus modifier
    strength_mod = next(m for m in modifiers if m['subtype'] == 'strength-score')
    assert strength_mod['type'] == 'bonus'
    assert strength_mod['value'] == 1
    
    # Check improvised weapons proficiency
    weapon_mod = next(m for m in modifiers if m['subtype'] == 'improvised-weapons')
    assert weapon_mod['type'] == 'proficiency'
    
    # Check unarmed strike damage
    unarmed_mod = next(m for m in modifiers if m['subtype'] == 'unarmed-damage-die')
    assert unarmed_mod['type'] == 'set'
    assert unarmed_mod['dice'] == '1d4' 

def test_text_cleaning():
    """Test that HTML and Unicode characters are properly cleaned."""
    parser = CharacterParser('data/Miriam Hopps.json')
    
    # Test HTML cleaning
    html_text = '<p class="Core-Styles_Core-Body">Test <em>text</em> with <strong>tags</strong></p>'
    assert parser._clean_text(html_text) == 'Test text with tags'
    
    # Test Unicode character cleaning
    unicode_text = 'Text with \u2022 bullet and \u2019 quote'
    assert parser._clean_text(unicode_text) == 'Text with • bullet and \' quote'
    
    # Test HTML entities
    entity_text = 'Text with &rdquo;quotes&ldquo; and &mdash; dash'
    assert parser._clean_text(entity_text) == 'Text with "quotes" and - dash'
    
    # Test combined cleaning
    complex_text = '<p>Text with \u2022 bullet and <em>emphasis</em> &rdquo;quotes&ldquo;</p>'
    assert parser._clean_text(complex_text) == 'Text with • bullet and emphasis "quotes"' 