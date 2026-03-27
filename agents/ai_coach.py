import os
from datetime import datetime, date
from typing import Dict, Any, List
import anthropic

class AICoach:
    """
    AI-powered coach that provides personalized guidance, motivation, and suggestions
    Uses Anthropic's Claude with full context of Rob's learning journey
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        
        if self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.ai_enabled = True
            print("🤖 AI Coach: Connected to Claude API")
        else:
            self.ai_enabled = False
            print("⚠️ AI Coach: No API key found. Running in offline mode.")
        
        self.system_prompt_template = self._build_system_prompt_template()
    
    def _build_system_prompt_template(self) -> str:
        """Build the core system prompt template for Claude"""
        return """You are Rob's personal AI career transition coach. You are encouraging, direct, and understand the investigative mindset.

BACKGROUND:
- Detective Sergeant Rob with 15+ years in counter-corruption
- Transitioning to AI Engineer role in 18 months
- Target: £100k+ role at Palantir, Quantexa, BAE Systems, or NCA
- Unique advantage: Investigation skills transfer to AI development

CURRENT STATUS:
- Stage: {current_stage}
- Progress: {stage_progress}% through current stage
- Coding streak: {coding_streak} days
- Learning streak: {learning_streak} days
- Days since start: {days_since_start}

RECENT ACTIVITY:
{recent_activity_summary}

CURRENT FOCUS:
- Primary project: {primary_project}
- Current task: {current_task}
- Next milestone: {next_milestone}

PERSONALITY TRAITS TO REMEMBER:
- Values systematic, evidence-based approaches
- Appreciates direct communication (no fluff)
- Motivated by clear progress tracking and next steps
- Enjoys connecting investigation skills to AI development
- Prefers practical applications over theory

RESPONSE GUIDELINES:
1. Always reference his specific progress and current position
2. Connect advice to his detective background when relevant
3. Give specific, actionable next steps
4. Keep responses focused and practical
5. Use encouraging but professional tone
6. Reference his streaks and achievements for motivation

Current challenges: {current_challenges}
Recent wins: {recent_wins}
"""
    
    def chat(self, user_message: str, context: Dict[str, Any]) -> str:
        """Main chat interface with full context"""
        
        if not self.ai_enabled:
            return self._offline_response(user_message, context)
        
        try:
            # Build system prompt with current context
            system_prompt = self._build_system_prompt(context)
            
            # Make API call
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                messages=[
                    {"role": "user", "content": f"{user_message}"}
                ],
                system=system_prompt
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"🔧 AI temporarily unavailable: {str(e)}\n\nOffline suggestion: {self._offline_response(user_message, context)}"
    
    def get_daily_motivation(self, context: Dict[str, Any]) -> str:
        """Generate personalized daily motivation message"""
        
        if not self.ai_enabled:
            return self._offline_motivation(context)
        
        motivation_prompt = f"""Based on Rob's current progress, generate a brief motivational message for today.

Consider:
- His current {context['current_streaks']['coding_streak']['current']}-day coding streak
- Recent achievement: {context['recent_activity']['most_recent_activities'][0]['description'] if context['recent_activity']['most_recent_activities'] else 'continuing progress'}
- Current focus: {context['current_focus']['current_task']}

Keep it:
- Encouraging but not cheesy
- Reference his detective background
- Mention specific progress
- 2-3 sentences max
- Include today's recommended action
"""
        
        try:
            system_prompt = self._build_system_prompt(context)
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[{"role": "user", "content": motivation_prompt}],
                system=system_prompt
            )
            
            return response.content[0].text
            
        except Exception as e:
            return self._offline_motivation(context)
    
    def suggest_daily_focus(self, context: Dict[str, Any]) -> str:
        """AI suggests what to focus on today based on progress and context"""
        
        if not self.ai_enabled:
            return self._offline_focus_suggestion(context)
        
        focus_prompt = f"""Based on Rob's current progress and typical 60-minute evening coding session, suggest what he should focus on today.

Current status:
- Working on: {context['current_focus']['primary_project']}
- Current task: {context['current_focus']['current_task']}
- Recent coding: {context['recent_activity']['total_coding_minutes']} minutes in last 7 days
- Stage progress: {context['current_stage']['completion_percentage']}%

Suggest:
1. Specific task for tonight (60 min session)
2. Why this is the priority right now
3. What this achieves toward the next milestone

Keep practical and specific."""
        
        try:
            system_prompt = self._build_system_prompt(context)
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": focus_prompt}],
                system=system_prompt
            )
            
            return response.content[0].text
            
        except Exception as e:
            return self._offline_focus_suggestion(context)
    
    def suggest_next_task(self, context: Dict[str, Any]) -> str:
        """Suggest what task comes next after completing current one"""
        
        if not self.ai_enabled:
            return "Continue with next step in current project"
        
        next_task_prompt = f"""Rob just completed a task. Based on his current project ({context['current_focus']['primary_project']}) and stage progress, what should be his next specific task?

Current milestone goal: {context['current_focus']['next_milestone']}

Give just the next task name (concise, actionable)."""
        
        try:
            system_prompt = self._build_system_prompt(context)
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[{"role": "user", "content": next_task_prompt}],
                system=system_prompt
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            return "Continue building current project features"
    
    def analyze_progress_velocity(self, context: Dict[str, Any]) -> str:
        """Analyze if Rob is on track with his timeline"""
        
        progress_prompt = f"""Analyze Rob's progress velocity and timeline adherence.

Data:
- Days since start: {context['days_since_start']}
- Overall progress: Multiple stages, currently in {context['current_stage']['name']}
- Recent activity: {context['recent_activity']['total_coding_minutes']} coding minutes in 7 days
- Coding streak: {context['current_streaks']['coding_streak']['current']} days

Assessment needed:
1. Is he on track for 18-month goal?
2. What's going well?
3. Any areas of concern?
4. Specific recommendations

Be honest but encouraging."""
        
        try:
            system_prompt = self._build_system_prompt(context)
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                messages=[{"role": "user", "content": progress_prompt}],
                system=system_prompt
            )
            
            return response.content[0].text
            
        except Exception as e:
            return "Progress analysis temporarily unavailable. Continue with consistent daily coding sessions."
    
    def get_learning_suggestion(self, available_time_minutes: int, context: Dict[str, Any]) -> str:
        """Suggest learning activity based on available time"""
        
        time_prompt = f"""Rob has {available_time_minutes} minutes available for learning. Based on his current stage and progress, what's the most valuable use of this time?

Current focus: {context['current_focus']['current_task']}
Current stage: {context['current_stage']['name']}

Suggest specific activity that fits the time available."""
        
        try:
            system_prompt = self._build_system_prompt(context)
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[{"role": "user", "content": time_prompt}],
                system=system_prompt
            )
            
            return response.content[0].text
            
        except Exception as e:
            return self._offline_time_suggestion(available_time_minutes, context)
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build complete system prompt with current context"""
        return self.system_prompt_template.format(
            current_stage=context['current_stage']['name'],
            stage_progress=context['current_stage'].get('completion_percentage', 0),
            coding_streak=context['current_streaks']['coding_streak']['current'],
            learning_streak=context['current_streaks']['learning_streak']['current'],
            days_since_start=context['days_since_start'],
            recent_activity_summary=self._format_recent_activity(context['recent_activity']),
            primary_project=context['current_focus']['primary_project'],
            current_task=context['current_focus']['current_task'],
            next_milestone=context['current_focus']['next_milestone'],
            current_challenges=", ".join(context.get('recent_challenges', [])),
            recent_wins=", ".join(context.get('recent_wins', []))
        )
    
    def _format_recent_activity(self, recent_activity: Dict[str, Any]) -> str:
        """Format recent activity for system prompt"""
        activities = recent_activity.get('most_recent_activities', [])
        if not activities:
            return "No recent activities logged"
        
        formatted = []
        for activity in activities[:3]:  # Last 3 activities
            formatted.append(f"- {activity['type']}: {activity['description']} ({activity['duration_minutes']} mins)")
        
        return "\n".join(formatted)
    
    # ========== OFFLINE FALLBACK METHODS ==========
    
    def _offline_response(self, user_message: str, context: Dict[str, Any]) -> str:
        """Provide helpful response when AI is unavailable"""
        message_lower = user_message.lower()
        
        if "progress" in message_lower or "status" in message_lower:
            return self._format_progress_summary(context)
        elif "next" in message_lower or "focus" in message_lower:
            return self._offline_focus_suggestion(context)
        elif "motivation" in message_lower or "encourage" in message_lower:
            return self._offline_motivation(context)
        else:
            return f"""🤖 AI Coach (Offline Mode):
            
Current focus: {context['current_focus']['current_task']}
Coding streak: {context['current_streaks']['coding_streak']['current']} days - Keep it going!

For full AI conversations, add your Anthropic API key to the .env file.

What specific aspect of your progress would you like to discuss?"""
    
    def _offline_motivation(self, context: Dict[str, Any]) -> str:
        """Provide motivation when AI unavailable"""
        streak = context['current_streaks']['coding_streak']['current']
        task = context['current_focus']['current_task']
        
        return f"""🔥 {streak}-day coding streak - you're building serious momentum!

Today's focus: {task}

Your investigative background gives you a unique edge in AI development. Keep building systematically, just like you approach complex cases.

Every hour of coding gets you closer to that £100k AI Engineer role!"""
    
    def _offline_focus_suggestion(self, context: Dict[str, Any]) -> str:
        """Suggest focus when AI unavailable"""
        current_task = context['current_focus']['current_task']
        return f"""📋 Suggested focus for tonight's 60-minute session:

Continue with: {current_task}

Break it down systematically (detective approach):
1. Define the specific problem to solve
2. Research the solution approach  
3. Implement step by step
4. Test and validate
5. Document what you learned

This systematic approach leverages your investigation skills for coding success."""
    
    def _offline_time_suggestion(self, minutes: int, context: Dict[str, Any]) -> str:
        """Time-based suggestions when AI unavailable"""
        if minutes >= 60:
            return f"Perfect for a focused coding session on: {context['current_focus']['current_task']}"
        elif minutes >= 30:
            return "Great time for reading documentation or watching a tutorial"
        elif minutes >= 15:
            return "Quick review of today's learning goals or plan tomorrow's session"
        else:
            return "Check your progress stats or review your roadmap"
    
    def _format_progress_summary(self, context: Dict[str, Any]) -> str:
        """Format progress summary for offline mode"""
        return f"""📊 Current Progress Summary:

🎯 Stage: {context['current_stage']['name']}
📈 Progress: {context['current_stage'].get('completion_percentage', 0)}%
🔥 Coding Streak: {context['current_streaks']['coding_streak']['current']} days
📚 Learning Streak: {context['current_streaks']['learning_streak']['current']} days
⏱️ Days Since Start: {context['days_since_start']}

🎯 Current Focus: {context['current_focus']['current_task']}
🏆 Next Milestone: {context['current_focus']['next_milestone']}

Keep up the excellent work! Your systematic approach is paying off."""