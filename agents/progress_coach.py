import os
import sys
from datetime import datetime, date
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_manager import DataManager
from agents.ai_coach import AICoach
from agents.linkedin_generator import LinkedInGenerator
from utils.streak_calculator import StreakCalculator
from utils.analytics import ProgressAnalytics

class DetectiveToDeveloperCoach:
    """
    Master AI Progress Coach for Detective to Developer transition
    Coordinates all subsystems: progress tracking, AI coaching, LinkedIn content, analytics
    """
    
    def __init__(self):
        self.data_manager = DataManager()
        self.load_all_data()
        
        # Initialize subsystems
        self.ai_coach = AICoach(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.linkedin_generator = LinkedInGenerator(self.ai_coach)
        self.streak_calculator = StreakCalculator()
        self.analytics = ProgressAnalytics()
        
        print("🤖 Detective to Developer Coach initialized successfully!")
    
    def load_all_data(self):
        """Load all data from JSON files"""
        self.master_plan = self.data_manager.load_master_plan()
        self.progress_data = self.data_manager.load_user_progress()
        self.ai_memory = self.data_manager.load_ai_memory()
        self.linkedin_strategy = self.data_manager.load_linkedin_strategy()
    
    def save_all_data(self):
        """Save all modified data back to files"""
        self.data_manager.save_user_progress(self.progress_data)
        self.data_manager.save_ai_memory(self.ai_memory)
        self.data_manager.save_linkedin_strategy(self.linkedin_strategy)
    
    # ========== DAILY INTERACTION METHODS ==========
    
    def daily_checkin(self) -> Dict[str, Any]:
        """Complete daily check-in flow - main entry point"""
        today = date.today().isoformat()
        
        # Update streaks
        current_streaks = self.streak_calculator.calculate_all_streaks(self.progress_data)
        
        # Get today's focus
        focus = self.get_today_focus()
        
        # Generate LinkedIn post
        suggested_post = self.linkedin_generator.generate_daily_post(
            self.progress_data, self.linkedin_strategy
        )
        
        # Get AI motivation message
        motivation = self.ai_coach.get_daily_motivation(self.build_ai_context())
        
        return {
            "date": today,
            "streaks": current_streaks,
            "focus": focus,
            "suggested_linkedin_post": suggested_post,
            "motivation": motivation,
            "progress_summary": self.get_progress_summary()
        }
    
    def get_today_focus(self) -> Dict[str, Any]:
        """Determine what to focus on today based on current progress"""
        current_stage = self.progress_data["current_focus"]
        
        # AI determines optimal focus based on progress and time constraints
        context = self.build_ai_context()
        focus_suggestion = self.ai_coach.suggest_daily_focus(context)
        
        return {
            "primary_project": current_stage["primary_project"],
            "current_task": current_stage["current_task"],
            "estimated_time": "60 minutes",
            "ai_suggestion": focus_suggestion,
            "next_milestone": current_stage["next_milestone"]
        }
    
    # ========== ACTIVITY LOGGING ==========
    
    def log_activity(self, activity_type: str, duration_minutes: int, 
                    description: str = "", difficulty: str = "medium", 
                    notes: str = "") -> Dict[str, Any]:
        """Log any learning/coding activity and update all systems"""
        
        today = date.today().isoformat()
        timestamp = datetime.now().isoformat()
        
        # Create activity record
        activity = {
            "type": activity_type,
            "description": description,
            "duration_minutes": duration_minutes,
            "difficulty": difficulty,
            "notes": notes,
            "timestamp": timestamp
        }
        
        # Add to daily log
        if today not in self.progress_data["completed_activities"]:
            self.progress_data["completed_activities"][today] = {
                "coding_minutes": 0,
                "learning_minutes": 0,
                "activities": [],
                "mood": "neutral",
                "energy_level": "medium"
            }
        
        # Update totals
        if activity_type.lower() in ["coding", "programming", "project"]:
            self.progress_data["completed_activities"][today]["coding_minutes"] += duration_minutes
        else:
            self.progress_data["completed_activities"][today]["learning_minutes"] += duration_minutes
        
        # Add activity to list
        self.progress_data["completed_activities"][today]["activities"].append(activity)
        
        # Recalculate streaks
        new_streaks = self.streak_calculator.calculate_all_streaks(self.progress_data)
        self.progress_data["streaks"] = new_streaks
        
        # Update AI memory with recent activity
        self.update_ai_memory_with_activity(activity)
        
        # Save all changes
        self.save_all_data()
        
        return {
            "activity_logged": activity,
            "updated_streaks": new_streaks,
            "daily_totals": self.progress_data["completed_activities"][today],
            "success_message": f"✅ Logged {duration_minutes} minutes of {activity_type}"
        }
    
    def mark_task_complete(self, task_name: str, project: str = "", notes: str = "") -> Dict[str, Any]:
        """Mark a specific task as completed"""
        today = date.today().isoformat()
        
        achievement = {
            "date": today,
            "achievement": f"Completed: {task_name}",
            "description": f"{project} - {notes}" if project else notes,
            "project": project
        }
        
        # Add to achievements
        if "task_completions" not in self.progress_data["achievements"]:
            self.progress_data["achievements"]["task_completions"] = []
        
        self.progress_data["achievements"]["task_completions"].append(achievement)
        
        # Update current focus if this was the current task
        next_task = None
        if task_name == self.progress_data["current_focus"]["current_task"]:
            next_task = self.ai_coach.suggest_next_task(self.build_ai_context())
            self.progress_data["current_focus"]["current_task"] = next_task

        self.save_all_data()
        return {"achievement": achievement, "next_task": next_task}
    
    # ========== AI INTERACTION ==========
    
    def chat_with_coach(self, user_message: str) -> str:
        """Have a conversation with the AI coach"""
        context = self.build_ai_context()
        response = self.ai_coach.chat(user_message, context)
        
        # Log conversation
        conversation_record = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "coach_response": response
        }
        
        if "recent_conversations" not in self.ai_memory:
            self.ai_memory["recent_conversations"] = []
        
        self.ai_memory["recent_conversations"].append(conversation_record)
        
        # Keep only last 20 conversations to prevent memory bloat
        self.ai_memory["recent_conversations"] = self.ai_memory["recent_conversations"][-20:]
        
        self.save_all_data()
        return response
    
    def build_ai_context(self) -> Dict[str, Any]:
        """Build complete context for AI conversations"""
        current_streaks = self.streak_calculator.calculate_all_streaks(self.progress_data)
        recent_activity = self.get_recent_activity_summary()
        current_stage_info = self.get_current_stage_info()
        
        return {
            "user_profile": self.ai_memory["personality_profile"],
            "current_streaks": current_streaks,
            "recent_activity": recent_activity,
            "current_stage": current_stage_info,
            "current_focus": self.progress_data["current_focus"],
            "recent_challenges": self.ai_memory["conversation_context"]["current_challenges"],
            "recent_wins": self.ai_memory["conversation_context"]["recent_wins"],
            "days_since_start": (date.today() - date.fromisoformat(self.progress_data["user_info"]["start_date"])).days
        }
    
    # ========== PROGRESS ANALYSIS ==========
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get comprehensive progress summary"""
        current_stage = self.progress_data["user_info"]["current_stage"]
        stage_info = self.master_plan["stages"][current_stage]
        
        return {
            "current_stage": {
                "name": stage_info["name"],
                "progress": stage_info["completion_percentage"],
                "status": stage_info["status"]
            },
            "overall_progress": self.calculate_overall_progress(),
            "streaks": self.streak_calculator.calculate_all_streaks(self.progress_data),
            "recent_achievements": self.get_recent_achievements(),
            "performance_metrics": self.analytics.calculate_performance_metrics(self.progress_data)
        }
    
    def calculate_overall_progress(self) -> float:
        """Calculate overall program completion percentage"""
        total_stages = len(self.master_plan["stages"])
        completed_stages = sum(1 for stage in self.master_plan["stages"].values() 
                             if stage["status"] == "completed")
        
        # Add partial progress from current stage
        current_stage = self.progress_data["user_info"]["current_stage"]
        current_progress = self.master_plan["stages"][current_stage]["completion_percentage"] / 100
        
        overall = (completed_stages + current_progress) / total_stages * 100
        return round(overall, 1)
    
    # ========== HELPER METHODS ==========
    
    def get_recent_activity_summary(self) -> Dict[str, Any]:
        """Get summary of recent activity for AI context"""
        recent_days = list(self.progress_data["completed_activities"].keys())[-7:]  # Last 7 days
        
        total_coding = sum(
            self.progress_data["completed_activities"][day]["coding_minutes"] 
            for day in recent_days if day in self.progress_data["completed_activities"]
        )
        
        total_learning = sum(
            self.progress_data["completed_activities"][day]["learning_minutes"] 
            for day in recent_days if day in self.progress_data["completed_activities"]
        )
        
        return {
            "days_analyzed": len(recent_days),
            "total_coding_minutes": total_coding,
            "total_learning_minutes": total_learning,
            "average_daily_coding": round(total_coding / max(len(recent_days), 1)),
            "average_daily_learning": round(total_learning / max(len(recent_days), 1)),
            "most_recent_activities": self.get_most_recent_activities(3)
        }
    
    def get_most_recent_activities(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent activities across all days"""
        all_activities = []
        
        for day, data in self.progress_data["completed_activities"].items():
            for activity in data["activities"]:
                activity["date"] = day
                all_activities.append(activity)
        
        # Sort by timestamp and return most recent
        all_activities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return all_activities[:count]
    
    def get_current_stage_info(self) -> Dict[str, Any]:
        """Get detailed info about current stage"""
        current_stage = self.progress_data["user_info"]["current_stage"]
        return self.master_plan["stages"][current_stage]
    
    def get_recent_achievements(self) -> List[Dict[str, Any]]:
        """Get recent achievements across all categories"""
        all_achievements = []
        
        for category, achievements in self.progress_data["achievements"].items():
            for achievement in achievements:
                achievement["category"] = category
                all_achievements.append(achievement)
        
        # Sort by date and return most recent
        all_achievements.sort(key=lambda x: x.get("date", ""), reverse=True)
        return all_achievements[:5]
    
    def update_ai_memory_with_activity(self, activity: Dict[str, Any]):
        """Update AI memory with new activity for better context"""
        # Update recent wins if significant achievement
        if activity["duration_minutes"] >= 60:
            win = f"Completed {activity['duration_minutes']} minutes of {activity['type']}"
            if win not in self.ai_memory["conversation_context"]["recent_wins"]:
                self.ai_memory["conversation_context"]["recent_wins"].append(win)
                # Keep only last 5 wins
                self.ai_memory["conversation_context"]["recent_wins"] = \
                    self.ai_memory["conversation_context"]["recent_wins"][-5:]