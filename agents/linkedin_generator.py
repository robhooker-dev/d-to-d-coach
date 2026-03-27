import os
from datetime import datetime, date, timedelta
from typing import Dict, Any, List
import random

class LinkedInGenerator:
    """
    AI-powered LinkedIn content generator for Detective to Developer journey
    Creates personalized posts based on daily progress and learning activities
    """
    
    def __init__(self, ai_coach):
        self.ai_coach = ai_coach
        self.content_templates = self._load_content_templates()
        self.hashtag_strategy = self._build_hashtag_strategy()
        
        print("📱 LinkedIn Generator: Ready to create engaging content!")
    
    def generate_daily_post(self, progress_data: Dict[str, Any], 
                          linkedin_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete daily LinkedIn post with AI assistance"""
        
        # Determine post type based on rotation and recent activity
        post_type = self._determine_post_type(progress_data, linkedin_strategy)
        
        # Build context for post generation
        context = self._build_post_context(progress_data, post_type)
        
        # Generate post content
        if self.ai_coach.ai_enabled:
            post_content = self._ai_generate_post(context, post_type)
        else:
            post_content = self._template_generate_post(context, post_type)
        
        # Add engagement optimization
        optimized_post = self._optimize_for_engagement(post_content, post_type)
        
        # Update rotation index
        self._update_rotation_index(linkedin_strategy)
        
        return {
            "content": optimized_post,
            "post_type": post_type,
            "estimated_engagement": self._estimate_engagement(post_type, progress_data),
            "optimal_posting_time": self._get_optimal_posting_time(linkedin_strategy),
            "hashtags_used": self._extract_hashtags(optimized_post),
            "character_count": len(optimized_post),
            "generation_timestamp": datetime.now().isoformat()
        }
    
    def _determine_post_type(self, progress_data: Dict[str, Any], 
                           linkedin_strategy: Dict[str, Any]) -> str:
        """Intelligently determine what type of post to create today"""
        
        rotation = linkedin_strategy["posting_strategy"]["content_rotation"]
        current_index = linkedin_strategy["posting_strategy"].get("current_rotation_index", 0)
        
        # Get base post type from rotation
        base_type = rotation[current_index % len(rotation)]
        
        # Override based on recent significant events
        recent_activities = progress_data.get("completed_activities", {})
        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        
        # Check for major achievements in last 2 days
        for day in [today, yesterday]:
            if day in recent_activities:
                activities = recent_activities[day]["activities"]
                for activity in activities:
                    # Major project completion
                    if "completed" in activity.get("description", "").lower():
                        return "project_showcase"
                    # Long coding session (2+ hours)
                    if activity.get("duration_minutes", 0) >= 120:
                        return "progress_update"
        
        # Check for milestone achievements
        recent_achievements = progress_data.get("achievements", {})
        for category, achievements in recent_achievements.items():
            if achievements and achievements[-1]["date"] == today:
                return "progress_update"
        
        return base_type
    
    def _build_post_context(self, progress_data: Dict[str, Any], post_type: str) -> Dict[str, Any]:
        """Build comprehensive context for post generation"""
        
        # Current streaks
        coding_streak = progress_data["streaks"]["coding_streak"]["current"]
        learning_streak = progress_data["streaks"]["learning_streak"]["current"]
        
        # Recent activity summary
        recent_activity = self._get_recent_activity_summary(progress_data)
        
        # Current stage and progress
        current_stage = progress_data["user_info"]["current_stage"]
        current_focus = progress_data["current_focus"]
        
        # Recent achievements
        recent_achievements = self._get_recent_achievements(progress_data)
        
        return {
            "post_type": post_type,
            "coding_streak": coding_streak,
            "learning_streak": learning_streak,
            "current_stage": current_stage,
            "current_project": current_focus["primary_project"],
            "current_task": current_focus["current_task"],
            "recent_activity": recent_activity,
            "recent_achievements": recent_achievements,
            "days_since_start": (date.today() - date.fromisoformat(progress_data["user_info"]["start_date"])).days,
            "detective_angle": self._generate_detective_angle(post_type, recent_activity)
        }
    
    def _ai_generate_post(self, context: Dict[str, Any], post_type: str) -> str:
        """Use AI to generate personalized LinkedIn post"""
        
        prompts = {
            "progress_update": f"""
Create a LinkedIn post about Rob's coding progress.

Context:
- Detective Sergeant learning AI Engineering
- Current coding streak: {context['coding_streak']} days
- Recent work: {context['recent_activity']}
- Current project: {context['current_project']}

Style: Professional but authentic, show progress momentum
Include: Specific achievement, detective angle, community question
Length: 2-3 short paragraphs
End with engaging question

""",
            "learning_insight": f"""
Create a LinkedIn post about a fascinating parallel between detective work and AI development.

Context:
- Rob is {context['days_since_start']} days into his transition
- Recent learning: {context['recent_activity']}
- Detective angle: {context['detective_angle']}

Style: Thoughtful insight, professional
Structure: Parallel discovered → Detective context → AI application → Community question
Length: 2-3 paragraphs

""",
            "project_showcase": f"""
Create a LinkedIn post showcasing Rob's latest AI project.

Context:
- Project: {context['current_project']}
- Recent task: {context['current_task']}
- Background: Detective → AI Engineer transition
- Days into journey: {context['days_since_start']}

Style: Problem/solution format, technical but accessible
Include: What he built, why it matters, detective skills connection
End with question about similar experiences

""",
            "industry_reflection": f"""
Create a LinkedIn post about AI applications in law enforcement/security.

Context:
- Rob: Detective Sergeant learning AI
- Current learning: {context['recent_activity']}
- Unique perspective: Investigation + AI development

Style: Industry insight, future-focused
Structure: Current trend → Detective perspective → Future implications → Discussion prompt
Length: 2-3 paragraphs

""",
            "tip_sharing": f"""
Create a LinkedIn post sharing a practical tip from Rob's learning journey.

Context:
- Recent learning: {context['recent_activity']}
- Coding streak: {context['coding_streak']} days
- Background: Systematic detective mindset

Style: Helpful tip, actionable advice
Structure: Problem → Solution/Tip → Why it works → Call for others' tips
Include detective methodology angle

""",
            "community_question": f"""
Create a LinkedIn post asking the community for advice/input.

Context:
- Rob's current challenge: Learning {context['current_task']}
- His perspective: Detective background in AI development
- Days into transition: {context['days_since_start']}

Style: Genuine question, community-focused
Structure: Context → Specific question → Why their input matters
Encourage responses and discussion
"""
        }
        
        prompt = prompts.get(post_type, prompts["progress_update"])
        
        try:
            # Build AI context for personalization
            ai_context = {
                "user_profile": {"background": "Detective Sergeant transitioning to AI Engineer"},
                "current_stage": {"name": context["current_stage"]},
                "current_streaks": {
                    "coding_streak": {"current": context["coding_streak"]},
                    "learning_streak": {"current": context["learning_streak"]}
                },
                "current_focus": {
                    "primary_project": context["current_project"],
                    "current_task": context["current_task"]
                },
                "days_since_start": context["days_since_start"],
                "recent_activity": context["recent_activity"]
            }
            
            response = self.ai_coach.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}],
                system=f"""You are creating LinkedIn content for Rob, a Detective Sergeant transitioning to AI Engineer. 

Key guidelines:
- Always include #DetectiveToDeveloper hashtag
- Keep authentic, professional but not corporate tone
- Connect detective skills to AI development when relevant
- End with engaging questions
- Keep posts concise and mobile-friendly
- Show progress and learning, not just achievements"""
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"AI generation failed: {e}. Using template fallback.")
            return self._template_generate_post(context, post_type)
    
    def _template_generate_post(self, context: Dict[str, Any], post_type: str) -> str:
        """Generate post using templates when AI unavailable"""
        
        templates = {
            "progress_update": f"""Day {context['coding_streak']} of my coding streak! 🔥

Just made progress on {context['current_project']} - {context['current_task']}. The systematic approach I use in investigations translates perfectly to software development: break down complex problems, analyze each component, build evidence-based solutions.

{context['days_since_start']} days into my Detective → AI Engineer journey and loving the parallel thinking required.

What habits have been game-changers in your tech learning?

#DetectiveToDeveloper #AIEngineering #LearningInPublic""",

            "learning_insight": f"""Fascinating parallel I discovered today: 🧠

{context['detective_angle']}

Both investigation work and AI development require the same core skills: pattern recognition, systematic analysis, and building cases from evidence.

The transition feels more natural every day.

What unexpected connections have you found between your previous career and tech?

#CareerTransition #AIApplications #DetectiveToDeveloper""",

            "project_showcase": f"""From problem to solution! ⚡

Problem: {context['current_task']}
Solution: Built {context['current_project']}

Key insight: My investigation background proved invaluable for systematic problem-solving and requirement analysis.

{context['days_since_start']} days into my coding journey, and every project teaches me something new about the intersection of detective work and software development.

GitHub: [link coming soon]

What's the most valuable skill from your previous career that transfers to tech?

#BuildInPublic #DetectiveToDeveloper #ProblemSolving""",

            "industry_reflection": f"""The future of investigation is AI-augmented 🕵️

Currently learning {context['current_task']}, and I'm seeing huge potential for AI in law enforcement:

- Pattern recognition in large datasets
- Evidence analysis automation  
- Risk assessment optimization
- Case management intelligence

The key is AI enhancement, not replacement - human judgment remains crucial.

What's your view on AI's role in your industry?

#AIinLawEnforcement #FutureOfWork #DetectiveToDeveloper""",

            "tip_sharing": f"""Learning tip that's been game-changing: 📚

Apply investigation methodology to coding:
1. Define the problem clearly
2. Gather all relevant information  
3. Test hypotheses systematically
4. Document evidence and conclusions
5. Review and refine

This approach has accelerated my {context['current_task']} learning significantly.

Day {context['coding_streak']} of consistent coding, and the systematic mindset is paying off.

What methodologies from your background boost your learning?

#LearningTips #DetectiveToDeveloper #SystematicLearning""",

            "community_question": f"""Question for the AI engineering community: 🤔

{context['days_since_start']} days into my transition from Detective to AI Engineer, currently working on {context['current_task']}.

My investigation background gives me strong analytical skills, but I'm curious:

What advice would you give someone leveraging non-traditional experience in AI development?

Particularly interested in how to best position investigative thinking as a competitive advantage.

#AIEngineering #CareerTransition #DetectiveToDeveloper #CommunityWisdom"""
        }
        
        return templates.get(post_type, templates["progress_update"])
    
    def _optimize_for_engagement(self, post_content: str, post_type: str) -> str:
        """Optimize post for maximum LinkedIn engagement"""
        
        # Ensure proper hashtag inclusion
        post_content = self._ensure_core_hashtags(post_content)
        
        # Add emojis if missing
        post_content = self._add_strategic_emojis(post_content, post_type)
        
        # Ensure engaging question
        post_content = self._ensure_engagement_hook(post_content)
        
        # Format for mobile readability
        post_content = self._format_for_mobile(post_content)
        
        return post_content
    
    def _ensure_core_hashtags(self, content: str) -> str:
        """Ensure essential hashtags are included"""
        core_hashtags = ["#DetectiveToDeveloper"]
        
        for hashtag in core_hashtags:
            if hashtag not in content:
                content += f" {hashtag}"
        
        return content
    
    def _add_strategic_emojis(self, content: str, post_type: str) -> str:
        """Add relevant emojis based on post type"""
        emoji_map = {
            "progress_update": ["🔥", "🚀", "💪", "📈"],
            "learning_insight": ["🧠", "💡", "🔍", "🎯"],
            "project_showcase": ["⚡", "🛠️", "✨", "🎉"],
            "industry_reflection": ["🕵️", "🔮", "🌟", "📊"],
            "tip_sharing": ["📚", "💎", "🎯", "⭐"],
            "community_question": ["🤔", "💬", "🌟", "🙋‍♂️"]
        }
        
        # Add emoji if first line doesn't have one
        lines = content.split('\n')
        if lines and not any(emoji in lines[0] for emoji in "🚀🔥💪📈🧠💡🔍🎯⚡🛠️✨🎉🕵️🔮🌟📊📚💎⭐🤔💬🙋‍♂️"):
            emoji = random.choice(emoji_map.get(post_type, ["🚀"]))
            lines[0] = f"{lines[0]} {emoji}"
            content = '\n'.join(lines)
        
        return content
    
    def _ensure_engagement_hook(self, content: str) -> str:
        """Ensure post ends with engaging question"""
        if not content.strip().endswith('?'):
            engagement_questions = [
                "\nWhat's been your experience with career transitions?",
                "\nWhat advice would you give someone on a similar journey?",
                "\nHow has your background influenced your tech learning?",
                "\nWhat unexpected skills have transferred to your current role?"
            ]
            content += random.choice(engagement_questions)
        
        return content
    
    def _format_for_mobile(self, content: str) -> str:
        """Format content for mobile readability"""
        # Ensure paragraph breaks for long content
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            if len(line) > 100 and '.' in line:
                # Break long sentences
                sentences = line.split('. ')
                formatted_lines.extend([s + '.' if not s.endswith('.') else s for s in sentences[:-1]])
                formatted_lines.append(sentences[-1])
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def _get_recent_activity_summary(self, progress_data: Dict[str, Any]) -> str:
        """Get summary of recent meaningful activity"""
        recent_days = list(progress_data["completed_activities"].keys())[-3:]  # Last 3 days
        
        activities = []
        for day in recent_days:
            if day in progress_data["completed_activities"]:
                day_activities = progress_data["completed_activities"][day]["activities"]
                for activity in day_activities:
                    if activity["duration_minutes"] >= 30:  # Only significant activities
                        activities.append(activity["description"])
        
        if activities:
            return activities[-1]  # Most recent significant activity
        else:
            return progress_data["current_focus"]["current_task"]
    
    def _get_recent_achievements(self, progress_data: Dict[str, Any]) -> List[str]:
        """Get recent achievements for context"""
        all_achievements = []
        for category, achievements in progress_data["achievements"].items():
            for achievement in achievements:
                all_achievements.append(achievement)
        
        # Sort by date and return most recent
        all_achievements.sort(key=lambda x: x.get("date", ""), reverse=True)
        return [a["achievement"] for a in all_achievements[:3]]
    
    def _generate_detective_angle(self, post_type: str, recent_activity: str) -> str:
        """Generate detective perspective angle for different post types"""
        angles = {
            "progress_update": "Systematic evidence-based approach to learning",
            "learning_insight": "Pattern recognition skills transferring to code analysis",
            "project_showcase": "Investigation methodology applied to software development",
            "industry_reflection": "Understanding adversarial thinking and security implications",
            "tip_sharing": "Detective methodology for systematic problem-solving",
            "community_question": "Leveraging analytical and investigative expertise"
        }
        
        return angles.get(post_type, "Investigation skills enhancing AI development")
    
    def _estimate_engagement(self, post_type: str, progress_data: Dict[str, Any]) -> Dict[str, int]:
        """Estimate likely engagement based on post type and current following"""
        
        base_engagement = {
            "progress_update": {"likes": 25, "comments": 3, "shares": 1},
            "learning_insight": {"likes": 35, "comments": 5, "shares": 2},
            "project_showcase": {"likes": 45, "comments": 7, "shares": 3},
            "industry_reflection": {"likes": 30, "comments": 6, "shares": 2},
            "tip_sharing": {"likes": 40, "comments": 8, "shares": 4},
            "community_question": {"likes": 20, "comments": 12, "shares": 1}
        }
        
        # Adjust based on current streak (higher streaks = more engagement)
        coding_streak = progress_data["streaks"]["coding_streak"]["current"]
        multiplier = 1 + (coding_streak * 0.05)  # 5% increase per streak day
        
        estimated = base_engagement.get(post_type, base_engagement["progress_update"])
        return {k: int(v * multiplier) for k, v in estimated.items()}
    
    def _get_optimal_posting_time(self, linkedin_strategy: Dict[str, Any]) -> str:
        """Get optimal posting time based on strategy"""
        times = linkedin_strategy["posting_strategy"]["best_posting_times"]
        return random.choice(times)
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from post content"""
        words = content.split()
        hashtags = [word for word in words if word.startswith('#')]
        return hashtags
    
    def _update_rotation_index(self, linkedin_strategy: Dict[str, Any]):
        """Update rotation index for next post"""
        rotation_length = len(linkedin_strategy["posting_strategy"]["content_rotation"])
        current_index = linkedin_strategy["posting_strategy"].get("current_rotation_index", 0)
        linkedin_strategy["posting_strategy"]["current_rotation_index"] = (current_index + 1) % rotation_length
    
    def _load_content_templates(self) -> Dict[str, Any]:
        """Load content templates for different post types"""
        return {
            "hooks": {
                "progress_update": [
                    "Day {streak} of my coding journey! 🚀",
                    "Week {week} milestone achieved! ✅",
                    "From zero to {achievement} in {timeframe}! 💪"
                ],
                "learning_insight": [
                    "Fascinating parallel I discovered today: 🧠",
                    "Mind-blown moment in my AI learning: 💡",
                    "The intersection of investigation and AI: 🔍"
                ]
            },
            "detective_connections": [
                "Pattern recognition skills transfer perfectly",
                "Evidence-based systematic approach",
                "Analytical thinking and attention to detail",
                "Understanding adversarial mindset",
                "Risk assessment and threat analysis"
            ]
        }
    
    def _build_hashtag_strategy(self) -> Dict[str, List[str]]:
        """Build comprehensive hashtag strategy"""
        return {
            "core": ["#DetectiveToDeveloper"],  # Always include
            "ai_engineering": ["#AIEngineering", "#ArtificialIntelligence", "#MachineLearning", "#AI"],
            "career_transition": ["#CareerTransition", "#LearningInPublic", "#TechTransition", "#CareerChange"],
            "learning": ["#LearningInPublic", "#TechSkills", "#Programming", "#Python"],
            "industry": ["#LawEnforcement", "#AIinSecurity", "#TechInnovation"],
            "engagement": ["#TechCommunity", "#AIApplications", "#ProfessionalDevelopment"]
        }
    
    # ========== CONTENT PERFORMANCE TRACKING ==========
    
    def track_post_performance(self, post_data: Dict[str, Any], 
                             engagement_data: Dict[str, int], 
                             linkedin_strategy: Dict[str, Any]):
        """Track post performance for future optimization"""
        
        performance_record = {
            "date": date.today().isoformat(),
            "post_type": post_data["post_type"],
            "character_count": post_data["character_count"],
            "hashtags": post_data["hashtags_used"],
            "engagement": engagement_data,
            "posting_time": post_data["optimal_posting_time"]
        }
        
        if "post_performance" not in linkedin_strategy["engagement_tracking"]:
            linkedin_strategy["engagement_tracking"]["post_performance"] = []
        
        linkedin_strategy["engagement_tracking"]["post_performance"].append(performance_record)
        
        # Keep only last 30 posts to prevent data bloat
        linkedin_strategy["engagement_tracking"]["post_performance"] = \
            linkedin_strategy["engagement_tracking"]["post_performance"][-30:]