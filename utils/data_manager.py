import json
import os
from datetime import datetime, date
from typing import Dict, Any, List

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Creating empty structure.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {filename}")
            return {}
    
    def save_json(self, filename: str, data: Dict[str, Any]):
        """Save data to JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving {filename}: {str(e)}")
    
    def load_master_plan(self) -> Dict[str, Any]:
        """Load the complete learning roadmap"""
        return self.load_json("master_plan.json")
    
    def load_user_progress(self) -> Dict[str, Any]:
        """Load current user progress data"""
        return self.load_json("user_progress.json")
    
    def load_ai_memory(self) -> Dict[str, Any]:
        """Load AI conversation context"""
        return self.load_json("ai_memory.json")
    
    def load_linkedin_strategy(self) -> Dict[str, Any]:
        """Load LinkedIn strategy and performance data"""
        return self.load_json("linkedin_strategy.json")
    
    def save_user_progress(self, data: Dict[str, Any]):
        """Save updated progress data"""
        self.save_json("user_progress.json", data)
    
    def save_ai_memory(self, data: Dict[str, Any]):
        """Save AI memory context"""
        self.save_json("ai_memory.json", data)
    
    def save_linkedin_strategy(self, data: Dict[str, Any]):
        """Save LinkedIn strategy data"""
        self.save_json("linkedin_strategy.json", data)