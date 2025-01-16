import json
from pathlib import Path

class CharacterParser:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.data = self._load_json()
    
    def _load_json(self):
        """Load the JSON file."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def get_name(self):
        """Extract character name."""
        return self.data['data']['name']
    
    def get_username(self):
        """Extract player username."""
        return self.data['data']['username']
    
    def get_languages(self):
        """Extract known languages."""
        languages = []
        race_modifiers = self.data['data']['modifiers']['race']
        
        for modifier in race_modifiers:
            if modifier['type'] == 'language':
                language = modifier['subType'].capitalize()
                languages.append(language)
        
        return sorted(languages)  # Sort alphabetically for consistent output
    
    def get_racial_skills(self):
        """Extract racial skill proficiencies."""
        skills = []
        race_modifiers = self.data['data']['modifiers']['race']
        
        for modifier in race_modifiers:
            if modifier['type'] == 'proficiency' and 'subType' in modifier:
                skill = modifier['subType'].capitalize()
                skills.append(skill)
        
        return sorted(skills)  # Sort alphabetically for consistent output
    
    def get_racial_bonuses(self):
        """Extract racial ability score bonuses."""
        bonuses = {}
        race_modifiers = self.data['data']['modifiers']['race']
        
        for modifier in race_modifiers:
            if modifier['type'] == 'bonus' and modifier['subType'].endswith('-score'):
                ability = modifier['subType'].replace('-score', '')
                bonuses[ability] = modifier['value']
        
        return bonuses
    
    def get_stats(self):
        """Extract ability scores."""
        stats = {}
        stat_names = {
            1: "strength",
            2: "dexterity",
            3: "constitution",
            4: "intelligence",
            5: "wisdom",
            6: "charisma"
        }
        
        for stat in self.data['data']['stats']:
            stat_name = stat_names[stat['id']]
            stats[stat_name] = stat['value']
        
        return stats
    
    def get_race(self):
        """Extract race information."""
        return {
            "name": self.data['data']['race']['fullName'],
            "languages": self.get_languages(),
            "ability_bonuses": self.get_racial_bonuses(),
            "skills": self.get_racial_skills()
        }
    
    def get_class_proficiencies(self):
        """Extract class proficiencies from modifiers."""
        proficiencies = []
        class_modifiers = self.data['data']['modifiers'].get('class', [])
        
        for modifier in class_modifiers:
            if modifier['type'] == 'proficiency':
                # Convert subType from 'light-armor' to 'Light Armor'
                prof_name = modifier['subType'].replace('-', ' ').title()
                proficiencies.append(prof_name)
        
        return sorted(proficiencies)  # Sort for consistent output
    
    def _clean_text(self, text):
        """Clean HTML tags and Unicode characters from text."""
        if not text:
            return ""
        
        # Clean HTML tags with classes
        text = text.replace('<p class="Core-Styles_Core-Body">', '')
        text = text.replace('<p class="Core-Styles_Core-Body--Extra-Space-After-">', '')
        text = text.replace('<span class="Serif-Character-Style_Italic-Serif">', '')
        text = text.replace('<span class="Serif-Character-Style_Bold-Serif">', '')
        text = text.replace('<span class="No-Break">', '')
        text = text.replace('<div class="mastery-container">', '')
        
        # Clean basic HTML tags
        text = text.replace('</p>', '')
        text = text.replace('</span>', '')
        text = text.replace('</div>', '')
        text = text.replace('<p>', '')
        text = text.replace('<br />', '\n')
        text = text.replace('<ul>', '')
        text = text.replace('</ul>', '')
        text = text.replace('<li>', '• ')
        text = text.replace('</li>', '')
        text = text.replace('<strong>', '')
        text = text.replace('</strong>', '')
        text = text.replace('<em>', '')
        text = text.replace('</em>', '')
        text = text.replace('<hr />', '')
        
        # Convert HTML entities
        text = text.replace('&rdquo;', '"')
        text = text.replace('&ldquo;', '"')
        text = text.replace('&mdash;', '-')
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&ucirc;', 'u')
        text = text.replace('&rsquo;', "'")
        text = text.replace('&lsquo;', "'")
        
        # Convert Unicode characters
        text = text.replace('\u2022', '•')  # bullet point
        text = text.replace('\u2019', "'")   # right single quotation mark
        text = text.replace('\u2014', "-")   # em dash
        text = text.replace('\u201c', '"')   # left double quotation mark
        text = text.replace('\u201d', '"')   # right double quotation mark
        text = text.replace('\u2018', "'")   # left single quotation mark
        
        # Clean up whitespace
        text = text.replace('\r\n', '\n')
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(line for line in lines if line)
        
        return text.strip()
    
    def get_class_features(self, class_info):
        """Extract class features from class definition."""
        features = []
        
        # Features to exclude
        excluded_features = {
            "Fighting Style",
            "Martial Archetype",
            "Ability Score Improvement",
            "Hit Points",
            "Equipment",
            "Proficiencies"
        }
        
        # Get class features that are available at or below current level
        current_level = class_info['level']
        class_features = class_info['definition'].get('classFeatures', [])
        
        for feature in class_features:
            if feature['requiredLevel'] <= current_level and feature['name'] not in excluded_features:
                description = self._clean_text(feature['description'])
                description_lines = [line.strip() for line in description.split('\n') if line.strip()]
                
                features.append({
                    "name": feature['name'],
                    "description": description_lines
                })
        
        return features
    
    def clean_text(self, text):
        """Clean text by removing HTML and converting Unicode characters."""
        if not text:
            return ""
        
        # Remove all HTML tags
        html_tags = [
            '<p>', '</p>', '<br />', '<ul>', '</ul>', '<li>', '</li>',
            '<strong>', '</strong>', '<em>', '</em>', 
            '<span class="Serif-Character-Style_Bold-Serif">', '</span>',
            '<span class="No-Break">', '</span>',
            '<p class="Core-Styles_Core-Body">', 
            '<p class="Core-Styles_Core-Body--Extra-Space-After-">'
        ]
        for tag in html_tags:
            text = text.replace(tag, '')
        
        # Convert Unicode to symbols
        unicode_map = {
            '\u2019': "'",  # Right single quotation mark
            '\u2018': "'",  # Left single quotation mark
            '\u201c': '"',  # Left double quotation mark
            '\u201d': '"',  # Right double quotation mark
            '\u2014': '-',  # Em dash
            '\u2013': '-',  # En dash
            '\u2022': '•',  # Bullet point
        }
        for unicode_char, replacement in unicode_map.items():
            text = text.replace(unicode_char, replacement)
        
        return text.strip()
    
    def get_subclass_features(self, class_info):
        """Extract subclass features from class definition."""
        features = []
        
        if not class_info.get('subclassDefinition'):
            return features
        
        current_level = class_info['level']
        subclass_features = class_info['subclassDefinition'].get('classFeatures', [])
        
        # Only include Echo Knight specific features
        echo_knight_features = {
            "Manifest Echo": 3,
            "Unleash Incarnation": 3,
            "Echo Avatar": 7,
            "Shadow Martyr": 10,
            "Reclaim Potential": 15,
            "Legion of One": 18
        }
        
        for feature in subclass_features:
            feature_name = feature['name']
            if (feature_name in echo_knight_features and 
                echo_knight_features[feature_name] <= current_level):
                
                # Clean up the description
                description_lines = []
                raw_description = feature['description']
                
                # Split into lines and clean each one
                for line in raw_description.split('\n'):
                    cleaned_line = self.clean_text(line)
                    if cleaned_line:  # Only add non-empty lines
                        description_lines.append(cleaned_line)
                
                features.append({
                    "name": feature_name,
                    "description": description_lines
                })
        
        return features
    
    def get_classes(self):
        """Extract character class information."""
        classes = []
        for class_info in self.data['data']['classes']:
            # Get base class info
            base_class = {
                "name": class_info['definition']['name'],
                "level": class_info['level'],
                "class_bonuses": {
                    "proficiencies": self.get_class_proficiencies(),
                    "features": []
                }
            }
            
            # Add fighting style bonuses
            for option in self.data['data']['options']['class']:
                if option['componentId'] == 191:  # 191 is the Fighting Style component ID
                    base_class["class_bonuses"]["features"].append({
                        "name": option['definition']['name'],
                        "description": [
                            "Allows drawing thrown weapons as part of the attack",
                            "Adds +2 to damage rolls with thrown weapons"
                        ]
                    })
            
            # Add class features (excluding proficiencies)
            class_features = self.get_class_features(class_info)
            for feature in class_features:
                # Skip proficiency features since they're handled separately
                if not feature['name'].startswith('Proficiency'):
                    base_class["class_bonuses"]["features"].append(feature)
            
            # Get subclass info if it exists
            subclass = None
            if class_info.get('subclassDefinition'):
                subclass = {
                    "name": class_info['subclassDefinition']['name'],
                    "subclass_bonuses": self.get_subclass_features(class_info)
                }
            
            classes.append({
                "base_class": base_class,
                "subclass": subclass
            })
        
        return classes
    
    def save_output(self, output_data, filename):
        """Save parsed data to output file."""
        output_path = Path('output') / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(output_data, file, indent=2) 
    
    def get_background_proficiencies(self):
        """Extract background proficiencies from modifiers."""
        proficiencies = []
        background_modifiers = self.data['data']['modifiers'].get('background', [])
        
        for modifier in background_modifiers:
            if modifier['type'] == 'proficiency':
                # Convert subType from 'thieves-tools' to 'Thieves' Tools'
                prof_name = modifier['subType'].replace('-', ' ').title()
                
                # Special handling for thieves' tools
                if "Thieves Tools" in prof_name:
                    prof_name = "Thieves' Tools"
                elif "Tools" in prof_name:
                    prof_name = prof_name.replace("Tools", "' Tools")
                
                proficiencies.append({
                    "name": prof_name,
                    "description": [f"Proficiency in {prof_name}"]
                })
        
        return proficiencies
    
    def get_background(self):
        """Extract character background information."""
        background_data = self.data['data'].get('background', {})
        if not background_data or not background_data.get('definition'):
            return None
        
        definition = background_data['definition']
        
        # Split the description into paragraphs and clean each one
        description = self._clean_text(definition['shortDescription']).split('\n')
        description = [para for para in description if para.strip()]
        
        # Start with the Ear to the Ground feature
        background_bonuses = [
            {
                "name": definition['featureName'],
                "description": [self._clean_text(definition['featureDescription'])]
            }
        ]
        
        # Add proficiencies
        background_bonuses.extend(self.get_background_proficiencies())
        
        return {
            "name": definition['name'],
            "description": description,
            "background_bonuses": background_bonuses
        }
    
    def get_characteristics(self):
        """Extract character characteristics."""
        data = self.data['data']
        return {
            "gender": data['gender'],
            "faith": data['faith'],
            "age": data['age'],
            "hair": data['hair'],
            "eyes": data['eyes'],
            "skin": data['skin'],
            "height": data['height'],
            "weight": data['weight']
        }
    
    def get_inventory(self):
        """Extract character inventory information."""
        inventory_data = self.data['data'].get('inventory', [])
        
        # Process inventory items
        inventory = []
        seen_items = set()  # Track items we've already added
        
        for item in inventory_data:
            definition = item['definition']
            name = definition['name']
            
            # Skip Donkey
            if name == "Donkey (or Mule)":
                continue
            
            # For Backpack, only add the first one
            if name == "Backpack" and name in seen_items:
                continue
            
            # Clean HTML tags from description
            description = self._clean_text(definition.get('description', ''))
            
            inventory_item = {
                "name": name,
                "quantity": item['quantity'],
                "type": definition.get('type', ''),
                "description": description,
                "weight": definition.get('weight', 0),
                "equipped": item.get('equipped', False),
                "rarity": definition.get('rarity', 'Common'),
                "magic": definition.get('magic', False)
            }
            
            # Add cost if present
            if definition.get('cost') is not None:
                inventory_item['cost'] = {
                    "quantity": definition['cost'],
                    "unit": "gp"
                }
            
            # Add container info if present
            if definition.get('isContainer'):
                inventory_item['container'] = {
                    "capacity": definition.get('capacity', ''),
                    "capacity_weight": definition.get('capacityWeight', 0)
                }
            
            inventory.append(inventory_item)
            seen_items.add(name)
        
        return inventory
    
    def get_feats(self):
        """Extract character feats and their modifiers."""
        feats_data = self.data['data'].get('feats', [])
        feat_modifiers = self.data['data']['modifiers'].get('feat', [])
        feats = []
        
        for feat in feats_data:
            definition = feat['definition']
            description = self._clean_text(definition.get('description', ''))
            description_lines = [line.strip() for line in description.split('\n') if line.strip()]
            
            # Get modifiers for this feat
            feat_id = definition['id']
            modifiers = []
            for mod in feat_modifiers:
                if mod['componentId'] == feat_id:
                    modifier = {
                        "type": mod['type'],
                        "subtype": mod['subType'],
                        "friendly_name": mod['friendlySubtypeName']
                    }
                    
                    # Add value if present
                    if mod.get('value') is not None:
                        modifier['value'] = mod['value']
                    elif mod.get('fixedValue') is not None:
                        modifier['value'] = mod['fixedValue']
                    
                    # Add dice if present
                    if mod.get('dice') is not None:
                        modifier['dice'] = mod['dice']['diceString']
                    
                    modifiers.append(modifier)
            
            feat_info = {
                "name": definition['name'],
                "description": description_lines,
                "prerequisites": definition.get('prerequisites', []),
                "is_homebrew": definition.get('isHomebrew', False),
                "modifiers": modifiers
            }
            feats.append(feat_info)
        
        return feats
    
    def parse(self):
        """Parse character data into desired format."""
        return {
            "player_username": self.get_username(),
            "character_name": self.get_name(),
            "characteristics": self.get_characteristics(),
            "stats": self.get_stats(),
            "race": self.get_race(),
            "classes": self.get_classes(),
            "feats": self.get_feats(),
            "background": self.get_background(),
            "inventory": self.get_inventory()
        } 