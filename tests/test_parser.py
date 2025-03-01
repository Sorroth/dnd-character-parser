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
            'spells',
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
        'spells',
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

def test_clean_text():
    """Test that text cleaning works correctly."""
    parser = CharacterParser('data/Miriam Hopps.json')
    
    # Test HTML tag removal
    html_text = '<p>Test</p><br /><strong>Bold</strong><em>Italic</em>'
    assert parser.clean_text(html_text) == 'TestBoldItalic'
    
    # Test HTML entity conversion
    entity_text = 'Quote &ldquo;test&rdquo; with &mdash; and &nbsp;spaces'
    assert parser.clean_text(entity_text) == 'Quote "test" with - and spaces'
    
    # Test Unicode conversion
    unicode_text = 'Smart \u201cquotes\u201d and \u2019apostrophes\u2019 with \u2022 bullets'
    assert parser.clean_text(unicode_text) == 'Smart "quotes" and \'apostrophes\' with • bullets'
    
    # Test line break handling
    line_breaks = 'Line 1\nLine 2\r\nLine 3\rLine 4'
    assert parser.clean_text(line_breaks) == 'Line 1 Line 2 Line 3 Line 4'
    
    # Test complex HTML with No-Break spans
    complex_html = '''<div class="mastery-container"><hr />
    <span class="No-Break">Keep this together</span>
    <p class="Core-Styles_Core-Body">Normal text</p></div>'''
    assert parser.clean_text(complex_html) == 'Keep this together Normal text'

def test_background():
    """Test that background information is correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    background = parser.get_background()
    
    # Test basic structure
    assert background['name'] == 'Urban Bounty Hunter'
    
    # Test backstory
    assert 'backstory' in background
    assert isinstance(background['backstory'], list)
    assert len(background['backstory']) == 1
    assert "Miriam Hopps grew up in the quaint village of Greenest" in background['backstory'][0]
    
    # Test text cleaning in backstory
    backstory = background['backstory'][0]
    assert '<' not in backstory  # No HTML tags
    assert '&' not in backstory  # No HTML entities
    assert '\u2019' not in backstory  # No right single quotation mark
    assert '\u00a0' not in backstory  # No non-breaking space
    
    # Test that Unicode characters are properly cleaned
    description = background['description'][0]
    assert '\u2019' not in description  # No right single quotation mark
    assert '\u00a0' not in description  # No non-breaking space
    assert "you aren't" in description  # Verify apostrophe is standard
    assert "you're" in description or "you are" in description  # Verify either form is present
    
    # Test background bonuses
    bonuses = background['background_bonuses']
    assert len(bonuses) == 3
    
    # Test Ear to the Ground feature
    feature = bonuses[0]
    assert feature['name'] == 'Ear to the Ground'
    assert isinstance(feature['description'], list)
    assert len(feature['description']) == 1
    assert "You are in frequent contact with people" in feature['description'][0]
    
    # Test proficiencies
    proficiencies = bonuses[1]['proficiencies']
    expected_proficiencies = [
        "Deception",
        "Dragonchess Set",
        "Medicine",
        "Thieves' Tools"
    ]
    assert sorted(proficiencies) == expected_proficiencies
    
    # Test traits and additional traits
    traits_bonus = bonuses[2]
    assert 'traits' in traits_bonus
    assert 'additional_traits' in traits_bonus
    
    # Test traits content and Unicode cleaning
    traits = traits_bonus['traits']
    assert len(traits) == 5  # personality traits + ideal + bond + flaw
    for trait in traits:
        assert '\u2019' not in trait  # No right single quotation mark
        assert '\u00a0' not in trait  # No non-breaking space
    
    # Test additional traits content and Unicode cleaning
    additional_traits = traits_bonus['additional_traits']
    assert len(additional_traits) == 3
    expected_additional_traits = [
        "Heraldic Signs: A skull with a dagger through it, representing the doom you bring to your enemies",
        "Instructor: Street Fighter. Your trainer excels at urban combat, combining close-quarters work with silence and efficiency.",
        "Signature Style: Effortless. You rarely perspire or display anything other than a stoic expression in battle."
    ]
    
    # Clean the actual traits to replace non-breaking spaces with regular spaces
    cleaned_additional_traits = [
        trait.replace('\u00a0', ' ') for trait in additional_traits
    ]
    assert cleaned_additional_traits == expected_additional_traits
    
    # Test text cleaning
    for trait in additional_traits:
        assert '<' not in trait  # No HTML tags
        assert '&' not in trait  # No HTML entities
        assert '\u2019' not in trait  # No right single quotation mark

def test_inventory():
    """Test that inventory is correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    inventory = parser.get_inventory()
    
    assert isinstance(inventory, list)
    assert len(inventory) > 0
    
    for item in inventory:
        assert 'name' in item
        if 'description' in item:
            description = item['description']
            assert '<' not in description  # No HTML tags
            assert '&' not in description  # No HTML entities
            assert '\n' not in description  # No newlines
            assert '\r' not in description  # No carriage returns
            assert '  ' not in description  # No double spaces

def test_get_feats():
    """Test that feats are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    feats = parser.get_feats()
    
    # Test basic structure
    assert isinstance(feats, list)
    assert len(feats) > 0
    
    # Test Sharpshooter feat
    sharpshooter = next((feat for feat in feats if feat['name'] == 'Sharpshooter'), None)
    assert sharpshooter is not None
    assert 'description' in sharpshooter
    assert isinstance(sharpshooter['description'], list)
    assert 'modifiers' in sharpshooter
    assert sharpshooter['modifiers'] == []
    
    # Test Tavern Brawler feat
    tavern_brawler = next((feat for feat in feats if feat['name'] == 'Tavern Brawler'), None)
    assert tavern_brawler is not None
    assert 'description' in tavern_brawler
    assert isinstance(tavern_brawler['description'], list)
    assert 'feat_bonuses' in tavern_brawler
    
    # Test Tavern Brawler bonuses
    bonuses = tavern_brawler['feat_bonuses']
    assert isinstance(bonuses, list)
    
    # Test ability bonuses
    ability_bonus = next((b for b in bonuses if 'ability_bonuses' in b), None)
    assert ability_bonus is not None
    assert 'strength' in ability_bonus['ability_bonuses']
    assert ability_bonus['ability_bonuses']['strength'] == 1
    
    # Test proficiencies
    proficiencies = next((b for b in bonuses if 'proficiencies' in b), None)
    assert proficiencies is not None
    assert 'Improvised Weapons' in proficiencies['proficiencies']
    
    # Test features
    features = next((b for b in bonuses if 'features' in b), None)
    assert features is not None
    assert any('improvised weapon strikes' in f.lower() for f in features['features'])
    assert any('grapple' in f.lower() for f in features['features'])
    
    # Test other bonuses
    other = next((b for b in bonuses if 'other' in b), None)
    assert other is not None
    assert any('unarmed-damage-die' in o for o in other['other'])
    assert any('1d4' in str(o.values()) for o in other['other']) 

def test_spells():
    """Test that spells are correctly parsed."""
    parser = CharacterParser('data/Miriam Hopps.json')
    spells = parser.get_spells()
    
    assert isinstance(spells, list)
    assert len(spells) == 1  # Only Gust of Wind from Wind Fan
    
    spell = spells[0]
    # Test basic spell info
    assert spell['name'] == 'Gust of Wind'
    assert spell['level'] == 2
    assert spell['school'] == 'Evocation'
    assert spell['casting_time'] == '1 action'
    assert spell['range'] == 'Self'
    assert spell['duration'] == 'Concentration, up to 1 minute'
    assert spell['concentration'] is True
    
    # Test components
    components = spell['components']
    assert components['verbal'] is True
    assert components['somatic'] is True
    assert components['material'] is True
    assert components['materials_needed'] == 'a legume seed'
    
    # Test source item
    assert 'source_item' in spell
    assert spell['source_item'] == 'Wind Fan'
    
    # Test description
    assert isinstance(spell['description'], list)
    assert len(spell['description']) == 1
    assert "A line of strong wind" in spell['description'][0]
    
    # Test text cleaning
    description = spell['description'][0]
    assert '<' not in description  # No HTML tags
    assert '&' not in description  # No HTML entities
    assert '\u2019' not in description  # No right single quotation mark
    assert '\u00a0' not in description  # No non-breaking space 