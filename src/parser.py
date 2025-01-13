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
    
    def save_output(self, output_data, filename):
        """Save parsed data to output file."""
        output_path = Path('output') / filename
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(output_data, file, indent=2) 