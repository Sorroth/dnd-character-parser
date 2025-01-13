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
            "skills": self.get_racial_skills()
        }
    
    def save_output(self, output_data, filename):
        """Save parsed data to output file."""
        output_path = Path('output') / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(output_data, file, indent=2) 