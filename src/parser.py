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
            "species": self.data['data']['race']['fullName'],
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
                proficiencies.append({
                    "name": prof_name,
                    "description": [f"Proficiency in {prof_name}"]
                })
        
        return proficiencies
    
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
                # Clean up the description by removing HTML tags
                description = feature['description']
                description = description.replace('<p>', '').replace('</p>', '')
                description = description.replace('<br />', '\n')
                description = description.replace('<ul>', '').replace('</ul>', '')
                description = description.replace('<li>', '• ').replace('</li>', '')
                description = description.replace('<strong>', '').replace('</strong>', '')
                description = description.replace('<span class="Serif-Character-Style_Bold-Serif">', '').replace('</span>', '')
                
                # Split description into lines and remove empty ones
                description_lines = [line.strip() for line in description.split('\n') if line.strip()]
                
                features.append({
                    "name": feature['name'],
                    "description": description_lines
                })
        
        return features
    
    def get_subclass_features(self, class_info):
        """Extract subclass features from class definition."""
        features = []
        
        # Features to exclude
        excluded_features = {
            "Martial Archetype",
            "Fighting Style",
            "Second Wind",
            "Action Surge",
            "Ability Score Improvement",
            "Proficiencies",
            "Hit Points",
            "Equipment"
        }
        
        if not class_info.get('subclassDefinition'):
            return features
        
        current_level = class_info['level']
        subclass_features = class_info['subclassDefinition'].get('classFeatures', [])
        
        for feature in subclass_features:
            if feature['requiredLevel'] <= current_level and feature['name'] not in excluded_features:
                # Clean up the description by removing HTML tags
                description = feature['description']
                description = description.replace('<p>', '').replace('</p>', '')
                description = description.replace('<br />', '\n')
                description = description.replace('<ul>', '').replace('</ul>', '')
                description = description.replace('<li>', '• ').replace('</li>', '')
                description = description.replace('<strong>', '').replace('</strong>', '')
                description = description.replace('<span class="Serif-Character-Style_Bold-Serif">', '').replace('</span>', '')
                
                # Split description into lines and remove empty ones
                description_lines = [line.strip() for line in description.split('\n') if line.strip()]
                
                features.append({
                    "name": feature['name'],
                    "description": description_lines
                })
        
        return features
    
    def get_classes(self):
        """Extract character class information."""
        classes = []
        for class_info in self.data['data']['classes']:
            # Get fighting style from options
            class_bonuses = []
            
            # Add fighting style bonuses
            for option in self.data['data']['options']['class']:
                if option['componentId'] == 191:  # 191 is the Fighting Style component ID
                    class_bonuses.append({
                        "name": option['definition']['name'],
                        "description": [
                            "Allows drawing thrown weapons as part of the attack",
                            "Adds +2 to damage rolls with thrown weapons"
                        ]
                    })
            
            # Add proficiency bonuses
            class_bonuses.extend(self.get_class_proficiencies())
            
            # Add class features
            class_bonuses.extend(self.get_class_features(class_info))

            # Get subclass features
            subclass_bonuses = self.get_subclass_features(class_info)

            class_data = {
                "base_class": {
                    "name": class_info['definition']['name'],
                    "level": class_info['level'],
                    "class_bonuses": class_bonuses
                },
                "subclass": {
                    "name": class_info['subclassDefinition']['name'],
                    "subclass_bonuses": subclass_bonuses
                } if class_info.get('subclassDefinition') else None
            }
            classes.append(class_data)
        return classes
    
    def save_output(self, output_data, filename):
        """Save parsed data to output file."""
        output_path = Path('output') / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(output_data, file, indent=2) 
    
    def parse(self):
        """Parse character data into desired format."""
        return {
            "player_username": self.get_username(),
            "character_name": self.get_name(),
            "stats": self.get_stats(),
            "racial_bonuses": self.get_race(),
            "classes": self.get_classes()
        } 