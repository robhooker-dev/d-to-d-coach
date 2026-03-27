from datetime import datetime, date, timedelta
from typing import Dict, Any, List

class StreakCalculator:
    """
    Calculates and manages all types of streaks for the Detective to Developer journey
    Handles coding streaks, learning streaks, LinkedIn posting streaks, and more
    """
    
    def __init__(self):
        print("🔥 Streak Calculator: Ready to track momentum!")
    
    def calculate_all_streaks(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate all streak types from progress data"""
        
        activities = progress_data.get("completed_activities", {})
        
        return {
            "coding_streak": self.calculate_coding_streak(activities),
            "learning_streak": self.calculate_learning_streak(activities),
            "linkedin_streak": self.calculate_linkedin_streak(progress_data),
            "consistency_streak": self.calculate_consistency_streak(activities),
            "daily_goal_streak": self.calculate_daily_goal_streak(activities)
        }
    
    def calculate_coding_streak(self, activities: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate current and longest coding streaks"""
        
        # Define minimum coding minutes for a "coding day"
        MIN_CODING_MINUTES = 30
        
        # Get all dates with coding activity
        coding_dates = []
        for date_str, day_data in activities.items():
            if day_data.get("coding_minutes", 0) >= MIN_CODING_MINUTES:
                try:
                    coding_dates.append(date.fromisoformat(date_str))
                except ValueError:
                    continue  # Skip invalid dates
        
        # Sort dates
        coding_dates.sort(reverse=True)  # Most recent first
        
        if not coding_dates:
            return {
                "current": 0,
                "longest_ever": 0,
                "last_activity_date": None,
                "days_since_last": 0,
                "is_active": False
            }
        
        # Calculate current streak
        current_streak = 0
        today = date.today()
        check_date = today
        
        # Check if we need to start from yesterday (if today isn't complete yet)
        today_str = today.isoformat()
        if today_str not in activities or activities[today_str].get("coding_minutes", 0) < MIN_CODING_MINUTES:
            check_date = today - timedelta(days=1)
        
        # Count consecutive days backwards
        while check_date in coding_dates:
            current_streak += 1
            check_date -= timedelta(days=1)
        
        # Calculate longest streak ever
        longest_streak = self._calculate_longest_streak(coding_dates)
        
        # Days since last coding
        days_since_last = (today - coding_dates[0]).days if coding_dates else 0
        
        return {
            "current": current_streak,
            "longest_ever": max(longest_streak, current_streak),
            "last_activity_date": coding_dates[0].isoformat() if coding_dates else None,
            "days_since_last": days_since_last,
            "is_active": days_since_last <= 1,
            "total_coding_days": len(coding_dates),
            "average_minutes_per_day": self._calculate_average_coding_minutes(activities, coding_dates)
        }
    
    def calculate_learning_streak(self, activities: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate learning streak (any learning activity)"""
        
        # Any learning activity counts (coding, reading, podcasts, courses)
        MIN_LEARNING_MINUTES = 15
        
        learning_dates = []
        for date_str, day_data in activities.items():
            total_learning = day_data.get("coding_minutes", 0) + day_data.get("learning_minutes", 0)
            if total_learning >= MIN_LEARNING_MINUTES:
                try:
                    learning_dates.append(date.fromisoformat(date_str))
                except ValueError:
                    continue
        
        learning_dates.sort(reverse=True)
        
        if not learning_dates:
            return {
                "current": 0,
                "longest_ever": 0,
                "last_activity_date": None,
                "days_since_last": 0,
                "is_active": False
            }
        
        # Calculate current streak
        current_streak = 0
        today = date.today()
        check_date = today
        
        # Check if we need to start from yesterday
        today_str = today.isoformat()
        if today_str not in activities:
            check_date = today - timedelta(days=1)
        
        while check_date in learning_dates:
            current_streak += 1
            check_date -= timedelta(days=1)
        
        longest_streak = self._calculate_longest_streak(learning_dates)
        days_since_last = (today - learning_dates[0]).days if learning_dates else 0
        
        return {
            "current": current_streak,
            "longest_ever": max(longest_streak, current_streak),
            "last_activity_date": learning_dates[0].isoformat() if learning_dates else None,
            "days_since_last": days_since_last,
            "is_active": days_since_last <= 1,
            "total_learning_days": len(learning_dates)
        }
    
    def calculate_linkedin_streak(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate LinkedIn posting streak"""
        
        # Basic implementation - will be enhanced when we track actual LinkedIn posts
        return {
            "current": 0,
            "longest_ever": 0,
            "last_post_date": None,
            "days_since_last_post": 0,
            "posts_this_week": 0,
            "posts_this_month": 0
        }
    
    def calculate_consistency_streak(self, activities: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate consistency streak (meeting daily goals regularly)"""
        
        # Define daily goal: 45+ minutes of any learning activity
        DAILY_GOAL_MINUTES = 45
        
        goal_met_dates = []
        for date_str, day_data in activities.items():
            total_minutes = day_data.get("coding_minutes", 0) + day_data.get("learning_minutes", 0)
            if total_minutes >= DAILY_GOAL_MINUTES:
                try:
                    goal_met_dates.append(date.fromisoformat(date_str))
                except ValueError:
                    continue
        
        goal_met_dates.sort(reverse=True)
        
        if not goal_met_dates:
            return {
                "current": 0,
                "longest_ever": 0,
                "goal_completion_rate": 0,
                "weekly_consistency": 0
            }
        
        current_streak = self._calculate_current_streak_flexible(goal_met_dates, max_gap_days=1)
        longest_streak = self._calculate_longest_streak(goal_met_dates)
        
        # Calculate weekly consistency (last 7 days)
        week_ago = date.today() - timedelta(days=7)
        recent_goal_days = [d for d in goal_met_dates if d >= week_ago]
        weekly_consistency = len(recent_goal_days) / 7 * 100
        
        return {
            "current": current_streak,
            "longest_ever": max(longest_streak, current_streak),
            "goal_completion_rate": len(goal_met_dates) / max(len(activities), 1) * 100,
            "weekly_consistency": round(weekly_consistency, 1),
            "total_goal_days": len(goal_met_dates)
        }
    
    def calculate_daily_goal_streak(self, activities: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate streak of meeting specific daily goals"""
        
        goals_met_dates = []
        
        for date_str, day_data in activities.items():
            daily_goals_met = 0
            total_goals = 3  # Coding, Learning, Reflection
            
            # Goal 1: 30+ minutes coding
            if day_data.get("coding_minutes", 0) >= 30:
                daily_goals_met += 1
            
            # Goal 2: 15+ minutes learning
            if day_data.get("learning_minutes", 0) >= 15:
                daily_goals_met += 1
            
            # Goal 3: Daily reflection/notes
            if day_data.get("daily_reflection", "").strip():
                daily_goals_met += 1
            
            # Count as goal day if met 2+ of 3 goals
            if daily_goals_met >= 2:
                try:
                    goals_met_dates.append(date.fromisoformat(date_str))
                except ValueError:
                    continue
        
        goals_met_dates.sort(reverse=True)
        
        current_streak = self._calculate_current_streak_strict(goals_met_dates) if goals_met_dates else 0
        longest_streak = self._calculate_longest_streak(goals_met_dates)
        
        return {
            "current": current_streak,
            "longest_ever": max(longest_streak, current_streak),
            "success_rate": len(goals_met_dates) / max(len(activities), 1) * 100,
            "total_successful_days": len(goals_met_dates)
        }
    
    # ========== HELPER METHODS ==========
    
    def _calculate_longest_streak(self, dates: List[date]) -> int:
        """Calculate the longest consecutive streak from a list of dates"""
        if not dates:
            return 0
        
        dates = sorted(set(dates))  # Remove duplicates and sort
        
        longest = 1
        current = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        return longest
    
    def _calculate_current_streak_strict(self, dates: List[date]) -> int:
        """Calculate current streak with no gaps allowed"""
        if not dates:
            return 0
        
        dates = sorted(set(dates), reverse=True)
        today = date.today()
        
        # Check if today or yesterday has activity
        if dates[0] not in [today, today - timedelta(days=1)]:
            return 0
        
        streak = 0
        check_date = dates[0]
        
        for activity_date in dates:
            if activity_date == check_date:
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def _calculate_current_streak_flexible(self, dates: List[date], max_gap_days: int = 1) -> int:
        """Calculate current streak allowing small gaps"""
        if not dates:
            return 0
        
        dates = sorted(set(dates), reverse=True)
        today = date.today()
        
        # Start from most recent activity
        if (today - dates[0]).days > max_gap_days:
            return 0
        
        streak = 1
        last_date = dates[0]
        
        for activity_date in dates[1:]:
            gap = (last_date - activity_date).days
            if gap <= max_gap_days + 1:  # Allow small gaps
                streak += 1
                last_date = activity_date
            else:
                break
        
        return streak
    
    def _calculate_average_coding_minutes(self, activities: Dict[str, Any], coding_dates: List[date]) -> float:
        """Calculate average coding minutes per coding day"""
        if not coding_dates:
            return 0
        
        total_minutes = 0
        for coding_date in coding_dates:
            date_str = coding_date.isoformat()
            if date_str in activities:
                total_minutes += activities[date_str].get("coding_minutes", 0)
        
        return round(total_minutes / len(coding_dates), 1)
    
    # ========== STREAK ANALYSIS METHODS ==========
    
    def analyze_streak_patterns(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in streak performance"""
        
        activities = progress_data.get("completed_activities", {})
        all_streaks = self.calculate_all_streaks(progress_data)
        
        return {
            "current_momentum": self._assess_current_momentum(all_streaks),
            "sustainability_score": self._analyze_sustainability(activities),
            "areas_for_improvement": self._identify_improvement_areas(all_streaks, activities),
            "streak_recommendations": self._generate_streak_recommendations(all_streaks, activities)
        }
    
    def _assess_current_momentum(self, streaks: Dict[str, Any]) -> str:
        """Assess overall momentum based on all streaks"""
        
        active_streaks = sum(1 for streak in streaks.values() 
                           if isinstance(streak, dict) and streak.get("current", 0) > 0)
        
        total_streak_strength = sum(
            streak.get("current", 0) for streak in streaks.values() 
            if isinstance(streak, dict)
        )
        
        if active_streaks >= 3 and total_streak_strength > 15:
            return "🚀 Excellent momentum! Multiple strong streaks active."
        elif active_streaks >= 2 and total_streak_strength > 8:
            return "📈 Good momentum building. Keep pushing!"
        elif active_streaks >= 1:
            return "⚡ Some momentum. Focus on consistency."
        else:
            return "🔄 Rebuild phase. Start with small daily wins."
    
    def _analyze_sustainability(self, activities: Dict[str, Any]) -> float:
        """Analyze how sustainable the current learning pace is"""
        
        recent_days = list(activities.keys())[-14:]  # Last 2 weeks
        daily_totals = []
        
        for day in recent_days:
            if day in activities:
                total = activities[day].get("coding_minutes", 0) + activities[day].get("learning_minutes", 0)
                daily_totals.append(total)
        
        if not daily_totals:
            return 0.0
        
        # Calculate sustainability metrics
        average_daily = sum(daily_totals) / len(daily_totals)
        consistency = len([d for d in daily_totals if d > 0]) / len(daily_totals)
        burnout_risk = len([d for d in daily_totals if d > 180]) / len(daily_totals)  # 3+ hours might be unsustainable
        
        # Sustainability score (0-100)
        sustainability = (consistency * 60) + (min(average_daily/60, 1) * 30) - (burnout_risk * 20)
        
        return max(0, min(100, sustainability))
    
    def _identify_improvement_areas(self, streaks: Dict[str, Any], activities: Dict[str, Any]) -> List[str]:
        """Identify specific areas for improvement"""
        
        improvements = []
        
        if streaks["coding_streak"]["current"] < 3:
            improvements.append("Build consistent daily coding habit")
        
        if streaks["consistency_streak"]["weekly_consistency"] < 70:
            improvements.append("Improve weekly consistency to 5+ days")
        
        return improvements
    
    def _generate_streak_recommendations(self, streaks: Dict[str, Any], activities: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations to improve streaks"""
        
        recommendations = []
        
        coding_streak = streaks["coding_streak"]["current"]
        if coding_streak == 0:
            recommendations.append("🎯 Start with 30-minute coding session tonight")
        elif coding_streak < 7:
            recommendations.append(f"🔥 You're at {coding_streak} days! Push for a full week")
        elif coding_streak < 30:
            recommendations.append(f"💪 {coding_streak} days strong! Aim for the 30-day milestone")
        
        return recommendations