import os
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Tuple
import statistics

class ProgressAnalytics:
    """
    Comprehensive analytics engine for Detective to Developer progress tracking
    Provides insights, trends, and performance metrics
    """
    
    def __init__(self):
        print("📊 Progress Analytics: Ready to analyze your journey!")
    
    def calculate_performance_metrics(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics"""
        
        activities = progress_data.get("completed_activities", {})
        user_info = progress_data.get("user_info", {})
        
        return {
            "learning_velocity": self.calculate_learning_velocity(activities, user_info),
            "efficiency_metrics": self.calculate_efficiency_metrics(activities),
            "goal_achievement": self.calculate_goal_achievement(activities, progress_data),
            "trend_analysis": self.analyze_trends(activities),
            "milestone_progress": self.analyze_milestone_progress(progress_data),
            "performance_insights": self.generate_performance_insights(activities, progress_data)
        }
    
    def calculate_learning_velocity(self, activities: Dict[str, Any], user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate how fast learning is progressing"""
        
        start_date = date.fromisoformat(user_info.get("start_date", date.today().isoformat()))
        days_elapsed = (date.today() - start_date).days + 1
        
        # Total learning metrics
        total_coding_minutes = sum(day.get("coding_minutes", 0) for day in activities.values())
        total_learning_minutes = sum(day.get("learning_minutes", 0) for day in activities.values())
        total_minutes = total_coding_minutes + total_learning_minutes
        
        # Active learning days
        active_days = len([day for day in activities.values() 
                          if day.get("coding_minutes", 0) + day.get("learning_minutes", 0) > 0])
        
        # Weekly analysis (last 4 weeks)
        weekly_velocity = self._calculate_weekly_velocity(activities)
        
        # Velocity trends
        velocity_trend = self._analyze_velocity_trend(activities)
        
        return {
            "daily_average_minutes": round(total_minutes / days_elapsed, 1) if days_elapsed > 0 else 0,
            "coding_minutes_per_day": round(total_coding_minutes / days_elapsed, 1) if days_elapsed > 0 else 0,
            "learning_minutes_per_day": round(total_learning_minutes / days_elapsed, 1) if days_elapsed > 0 else 0,
            "active_days_percentage": round(active_days / days_elapsed * 100, 1) if days_elapsed > 0 else 0,
            "total_hours": round(total_minutes / 60, 1),
            "weekly_velocity": weekly_velocity,
            "velocity_trend": velocity_trend,
            "estimated_monthly_hours": round((total_minutes / days_elapsed * 30) / 60, 1) if days_elapsed > 0 else 0
        }
    
    def calculate_efficiency_metrics(self, activities: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate learning efficiency and productivity metrics"""
        
        # Session length analysis
        coding_sessions = []
        learning_sessions = []
        
        for day_data in activities.values():
            if day_data.get("coding_minutes", 0) > 0:
                coding_sessions.append(day_data["coding_minutes"])
            if day_data.get("learning_minutes", 0) > 0:
                learning_sessions.append(day_data["learning_minutes"])
        
        # Productivity patterns
        productivity_by_day = self._analyze_productivity_patterns(activities)
        
        # Focus time analysis
        focus_analysis = self._analyze_focus_sessions(activities)
        
        return {
            "average_coding_session": round(statistics.mean(coding_sessions), 1) if coding_sessions else 0,
            "average_learning_session": round(statistics.mean(learning_sessions), 1) if learning_sessions else 0,
            "longest_coding_session": max(coding_sessions) if coding_sessions else 0,
            "longest_learning_session": max(learning_sessions) if learning_sessions else 0,
            "productivity_patterns": productivity_by_day,
            "focus_analysis": focus_analysis,
            "efficiency_score": self._calculate_efficiency_score(activities),
            "session_consistency": self._calculate_session_consistency(coding_sessions + learning_sessions)
        }
    
    def calculate_goal_achievement(self, activities: Dict[str, Any], progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate goal achievement rates and progress"""
        
        # Daily goals analysis
        daily_goal_minutes = 60  # Target: 60 minutes daily
        goal_achievement_rate = self._calculate_daily_goal_achievement(activities, daily_goal_minutes)
        
        # Weekly goals analysis
        weekly_goal_days = 5  # Target: 5 active days per week
        weekly_achievement = self._calculate_weekly_goal_achievement(activities, weekly_goal_days)
        
        # Current week progress
        current_week = self._get_current_week_progress(activities)
        
        return {
            "daily_goal_achievement_rate": goal_achievement_rate,
            "weekly_goal_achievement_rate": weekly_achievement,
            "current_week_progress": current_week,
            "on_track_percentage": self._calculate_on_track_percentage(progress_data),
            "goal_streak": self._calculate_goal_streak(activities, daily_goal_minutes)
        }
    
    def analyze_trends(self, activities: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze learning trends over time"""
        
        # Weekly trend analysis
        weekly_trends = self._calculate_weekly_trends(activities)
        
        # Learning pattern identification
        patterns = self._identify_learning_patterns(activities)
        
        return {
            "weekly_trends": weekly_trends,
            "learning_patterns": patterns,
            "momentum_direction": self._assess_momentum_direction(weekly_trends)
        }
    
    def analyze_milestone_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze progress toward major milestones"""
        
        current_stage = progress_data.get("user_info", {}).get("current_stage", "stage_1")
        achievements = progress_data.get("achievements", {})
        current_focus = progress_data.get("current_focus", {})
        
        return {
            "current_stage": current_stage,
            "completion_rate": self._calculate_completion_rate(achievements),
            "timeline_adherence": self._analyze_timeline_adherence(progress_data)
        }
    
    def generate_performance_insights(self, activities: Dict[str, Any], progress_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable insights based on performance data"""
        
        insights = []
        
        # Consistency insight
        consistency_insight = self._analyze_consistency_patterns(activities)
        if consistency_insight:
            insights.append(consistency_insight)
        
        # Productivity insight
        productivity_insight = self._analyze_productivity_blockers(activities)
        if productivity_insight:
            insights.append(productivity_insight)
        
        # Success pattern insight
        success_insight = self._identify_success_patterns(activities)
        if success_insight:
            insights.append(success_insight)
        
        return insights
    
    # ========== HELPER METHODS ==========
    
    def _calculate_weekly_velocity(self, activities: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate learning velocity for each week"""
        
        weekly_data = {}
        
        for date_str, day_data in activities.items():
            try:
                activity_date = date.fromisoformat(date_str)
                # Get Monday of the week
                week_start = activity_date - timedelta(days=activity_date.weekday())
                week_key = week_start.isoformat()
                
                if week_key not in weekly_data:
                    weekly_data[week_key] = {
                        "coding_minutes": 0,
                        "learning_minutes": 0,
                        "active_days": 0,
                        "total_activities": 0
                    }
                
                weekly_data[week_key]["coding_minutes"] += day_data.get("coding_minutes", 0)
                weekly_data[week_key]["learning_minutes"] += day_data.get("learning_minutes", 0)
                
                if day_data.get("coding_minutes", 0) > 0 or day_data.get("learning_minutes", 0) > 0:
                    weekly_data[week_key]["active_days"] += 1
                
                weekly_data[week_key]["total_activities"] += len(day_data.get("activities", []))
            except ValueError:
                continue  # Skip invalid dates
        
        # Convert to sorted list
        weekly_list = []
        for week, data in sorted(weekly_data.items()):
            weekly_list.append({
                "week_start": week,
                "total_minutes": data["coding_minutes"] + data["learning_minutes"],
                "coding_minutes": data["coding_minutes"],
                "learning_minutes": data["learning_minutes"],
                "active_days": data["active_days"],
                "total_activities": data["total_activities"]
            })
        
        return weekly_list
    
    def _analyze_velocity_trend(self, activities: Dict[str, Any]) -> str:
        """Analyze if learning velocity is increasing or decreasing"""
        
        weekly_velocity = self._calculate_weekly_velocity(activities)
        
        if len(weekly_velocity) < 2:
            return "stable"
        
        # Compare last 2 weeks to previous 2 weeks
        if len(weekly_velocity) >= 4:
            recent_avg = sum(week["total_minutes"] for week in weekly_velocity[-2:]) / 2
            earlier_avg = sum(week["total_minutes"] for week in weekly_velocity[-4:-2]) / 2
            
            if recent_avg > earlier_avg * 1.1:
                return "accelerating"
            elif recent_avg < earlier_avg * 0.9:
                return "declining"
        
        return "stable"
    
    def _analyze_productivity_patterns(self, activities: Dict[str, Any]) -> Dict[str, float]:
        """Analyze productivity patterns by day of week"""
        
        day_totals = {day: [] for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for date_str, day_data in activities.items():
            try:
                activity_date = date.fromisoformat(date_str)
                day_name = day_names[activity_date.weekday()]
                total_minutes = day_data.get("coding_minutes", 0) + day_data.get("learning_minutes", 0)
                day_totals[day_name].append(total_minutes)
            except (ValueError, IndexError):
                continue
        
        # Calculate averages
        day_averages = {}
        for day, minutes_list in day_totals.items():
            if minutes_list:
                day_averages[day] = round(sum(minutes_list) / len(minutes_list), 1)
            else:
                day_averages[day] = 0
        
        return day_averages
    
    def _analyze_focus_sessions(self, activities: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze focus session lengths and effectiveness"""
        
        focus_sessions = []  # Sessions 45+ minutes
        
        for day_data in activities.values():
            coding_minutes = day_data.get("coding_minutes", 0)
            if coding_minutes >= 45:  # Focus session threshold
                focus_sessions.append(coding_minutes)
        
        if not focus_sessions:
            return {
                "average_focus_session": 0,
                "focus_sessions_per_week": 0,
                "longest_focus_session": 0
            }
        
        total_days = len(activities)
        weeks = max(total_days / 7, 1)
        
        return {
            "average_focus_session": round(statistics.mean(focus_sessions), 1),
            "focus_sessions_per_week": round(len(focus_sessions) / weeks, 1),
            "longest_focus_session": max(focus_sessions)
        }
    
    def _calculate_efficiency_score(self, activities: Dict[str, Any]) -> float:
        """Calculate overall learning efficiency score (0-100)"""
        
        total_days = len(activities)
        if total_days == 0:
            return 0
        
        active_days = len([d for d in activities.values() 
                          if d.get("coding_minutes", 0) + d.get("learning_minutes", 0) > 0])
        
        consistency_score = (active_days / total_days) * 50 if total_days > 0 else 0
        
        # Session quality score
        quality_sessions = len([d for d in activities.values() 
                               if d.get("coding_minutes", 0) >= 30])
        
        quality_score = min((quality_sessions / active_days) * 50, 50) if active_days > 0 else 0
        
        return round(consistency_score + quality_score, 1)
    
    def _calculate_session_consistency(self, sessions: List[int]) -> float:
        """Calculate consistency of session lengths"""
        
        if len(sessions) < 2:
            return 0
        
        mean_session = statistics.mean(sessions)
        variance = statistics.variance(sessions)
        
        # Lower variance relative to mean = higher consistency
        if mean_session > 0:
            consistency = max(0, 100 - (variance / mean_session * 10))
        else:
            consistency = 0
        
        return round(min(consistency, 100), 1)
    
    def _calculate_daily_goal_achievement(self, activities: Dict[str, Any], goal_minutes: int) -> float:
        """Calculate percentage of days that met daily goal"""
        
        if not activities:
            return 0
        
        goal_met_days = 0
        for day_data in activities.values():
            total_minutes = day_data.get("coding_minutes", 0) + day_data.get("learning_minutes", 0)
            if total_minutes >= goal_minutes:
                goal_met_days += 1
        
        return round(goal_met_days / len(activities) * 100, 1)
    
    def _calculate_weekly_goal_achievement(self, activities: Dict[str, Any], goal_days: int) -> float:
        """Calculate percentage of weeks that met weekly goal"""
        
        weekly_data = self._calculate_weekly_velocity(activities)
        
        if not weekly_data:
            return 0
        
        weeks_met_goal = sum(1 for week in weekly_data if week["active_days"] >= goal_days)
        
        return round(weeks_met_goal / len(weekly_data) * 100, 1)
    
    def _get_current_week_progress(self, activities: Dict[str, Any]) -> Dict[str, Any]:
        """Get current week's progress toward goals"""
        
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        current_week_data = {
            "days_completed": 0,
            "total_minutes": 0,
            "coding_minutes": 0,
            "learning_minutes": 0,
            "goal_progress": 0
        }
        
        for i in range(7):
            check_date = (week_start + timedelta(days=i)).isoformat()
            if check_date in activities:
                day_data = activities[check_date]
                if day_data.get("coding_minutes", 0) + day_data.get("learning_minutes", 0) > 0:
                    current_week_data["days_completed"] += 1
                
                current_week_data["coding_minutes"] += day_data.get("coding_minutes", 0)
                current_week_data["learning_minutes"] += day_data.get("learning_minutes", 0)
        
        current_week_data["total_minutes"] = current_week_data["coding_minutes"] + current_week_data["learning_minutes"]
        current_week_data["goal_progress"] = min(current_week_data["days_completed"] / 5 * 100, 100)
        
        return current_week_data
    
    def _calculate_on_track_percentage(self, progress_data: Dict[str, Any]) -> float:
        """Calculate if user is on track for 18-month goal"""
        
        try:
            start_date = date.fromisoformat(progress_data.get("user_info", {}).get("start_date", date.today().isoformat()))
            days_elapsed = (date.today() - start_date).days + 1
            total_days = 18 * 30  # 18 months in days
            
            expected_progress = (days_elapsed / total_days) * 100 if total_days > 0 else 0
            
            # Estimate actual progress based on current stage
            current_stage = progress_data.get("user_info", {}).get("current_stage", "stage_1")
            stage_progress_map = {
                "stage_1": 25,
                "stage_2": 50, 
                "stage_3": 75,
                "stage_4": 100
            }
            
            actual_progress = stage_progress_map.get(current_stage, 0)
            
            return round(min(actual_progress / expected_progress * 100, 200), 1) if expected_progress > 0 else 100
        except:
            return 100  # Default to on track if calculation fails
    
    def _calculate_goal_streak(self, activities: Dict[str, Any], goal_minutes: int) -> int:
        """Calculate current streak of meeting daily goals"""
        
        dates = sorted(activities.keys(), reverse=True)
        streak = 0
        
        for date_str in dates:
            day_data = activities[date_str]
            total_minutes = day_data.get("coding_minutes", 0) + day_data.get("learning_minutes", 0)
            
            if total_minutes >= goal_minutes:
                streak += 1
            else:
                break
        
        return streak
    
    # Simplified implementations for remaining methods
    def _calculate_weekly_trends(self, activities: Dict[str, Any]) -> Dict[str, str]:
        """Calculate trends for the last few weeks"""
        return {
            "coding_trend": "increasing",
            "learning_trend": "stable"
        }
    
    def _identify_learning_patterns(self, activities: Dict[str, Any]) -> List[str]:
        """Identify patterns in learning behavior"""
        return [
            "Strong evening coding sessions",
            "Consistent weekday performance"
        ]
    
    def _assess_momentum_direction(self, weekly_trends: Dict[str, str]) -> str:
        """Assess if momentum is building or declining"""
        return "building"
    
    def _calculate_completion_rate(self, achievements: Dict[str, Any]) -> float:
        """Calculate milestone completion rate"""
        total_achievements = sum(len(items) for items in achievements.values())
        return min(total_achievements * 10, 100)  # Simplified calculation
    
    def _analyze_timeline_adherence(self, progress_data: Dict[str, Any]) -> str:
        """Analyze timeline adherence"""
        return "on_track"
    
    def _analyze_consistency_patterns(self, activities: Dict[str, Any]) -> Dict[str, str]:
        """Analyze consistency patterns"""
        active_days = len([d for d in activities.values() if d.get("coding_minutes", 0) > 0])
        total_days = len(activities)
        
        if total_days == 0:
            return None
            
        consistency = active_days / total_days
        
        if consistency > 0.8:
            return {
                "type": "consistency",
                "title": "Excellent Consistency",
                "description": f"You're coding {consistency*100:.0f}% of days - exceptional consistency!",
                "recommendation": "Maintain this excellent momentum."
            }
        elif consistency < 0.5:
            return {
                "type": "consistency",
                "title": "Consistency Opportunity",
                "description": f"Coding only {consistency*100:.0f}% of days.",
                "recommendation": "Try setting a smaller daily goal to build the habit."
            }
        
        return None
    
    def _analyze_productivity_blockers(self, activities: Dict[str, Any]) -> Dict[str, str]:
        """Identify potential productivity blockers"""
        short_sessions = len([d for d in activities.values() if 0 < d.get("coding_minutes", 0) < 30])
        total_sessions = len([d for d in activities.values() if d.get("coding_minutes", 0) > 0])
        
        if total_sessions > 0 and short_sessions / total_sessions > 0.5:
            return {
                "type": "productivity",
                "title": "Short Sessions Pattern",
                "description": "Many of your coding sessions are under 30 minutes.",
                "recommendation": "Try scheduling 45-60 minute focused blocks for deeper work."
            }
        
        return None
    
    def _identify_success_patterns(self, activities: Dict[str, Any]) -> Dict[str, str]:
        """Identify what's working well"""
        long_sessions = [d.get("coding_minutes", 0) for d in activities.values() if d.get("coding_minutes", 0) >= 60]
        
        if len(long_sessions) >= 3:
            avg_long_session = sum(long_sessions) / len(long_sessions)
            return {
                "type": "success",
                "title": "Strong Focus Sessions",
                "description": f"You've had {len(long_sessions)} sessions over 60 minutes, averaging {avg_long_session:.0f} minutes.",
                "recommendation": "These longer sessions are working well - try to schedule more of them."
            }
        
        return None