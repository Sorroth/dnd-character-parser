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
    
    def save_output(self, output_data, filename):
        """Save parsed data to output file."""
        output_path = Path('output') / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(output_data, file, indent=2) 