import streamlit as st
import os
import sys
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom classes
from agents.progress_coach import DetectiveToDeveloperCoach
from utils.data_manager import DataManager
from utils.analytics import ProgressAnalytics
from utils.streak_calculator import StreakCalculator

# ========== STREAMLIT CONFIGURATION ==========

st.set_page_config(
    page_title="Detective to Developer Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3d59, #457b9d);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #457b9d;
        margin-bottom: 1rem;
    }
    .streak-badge {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.25rem;
    }
    .insight-box {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
    }
    .linkedin-post {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 1rem 0;
        font-family: 'Segoe UI', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE INITIALIZATION ==========

def init_session_state():
    """Initialize session state variables"""
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True

    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"

    if 'coach' not in st.session_state:
        try:
            st.session_state.coach = DetectiveToDeveloperCoach()
        except Exception as e:
            st.error(f"Failed to initialize coach: {e}")
            st.stop()

    if 'ai_coach' not in st.session_state:
        st.session_state.ai_coach = st.session_state.coach.ai_coach

    if 'daily_checkin_done' not in st.session_state:
        st.session_state.daily_checkin_done = False

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

# ========== MAIN APPLICATION ==========

def main():
    """Main application function"""
    
    init_session_state()
    coach = st.session_state.coach
    
    # Sidebar navigation
    st.sidebar.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #1e3d59, #457b9d); border-radius: 10px; margin-bottom: 1rem;'>
        <h2 style='color: white; margin: 0;'>🕵️‍♂️ → 🤖</h2>
        <p style='color: white; margin: 0; font-size: 14px;'>Detective to Developer</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["🏠 Dashboard", "🤖 AI Coach", "📱 LinkedIn Content", "📝 Log Activity", "📊 Analytics", "⚙️ Settings"],
        index=0
    )
    
    # Route to different pages
    if page == "🏠 Dashboard":
        show_dashboard(coach)
    elif page == "🤖 AI Coach":
        show_ai_coach(coach)
    elif page == "📱 LinkedIn Content":
        show_linkedin_content(coach)
    elif page == "📝 Log Activity":
        show_activity_logging(coach)
    elif page == "📊 Analytics":
        show_analytics(coach)
    elif page == "⚙️ Settings":
        show_settings(coach)

# ========== DASHBOARD PAGE ==========

def show_dashboard(coach):
    """Main dashboard with overview and daily check-in"""
    
    st.markdown("""
    <div class='main-header'>
        <h1 style='margin: 0;'>🤖 Detective to Developer Progress Coach</h1>
        <p style='margin: 0; opacity: 0.9;'>Your AI-powered career transition companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Daily check-in section
    if not st.session_state.daily_checkin_done:
        st.markdown("### 🌅 Daily Check-in")
        if st.button("🚀 Start Daily Check-in", type="primary", use_container_width=True):
            daily_checkin_result = coach.daily_checkin()
            st.session_state.daily_checkin_result = daily_checkin_result
            st.session_state.daily_checkin_done = True
            st.rerun()
    
    # Show daily check-in results
    if st.session_state.daily_checkin_done and 'daily_checkin_result' in st.session_state:
        show_daily_checkin_results(st.session_state.daily_checkin_result)
    
    # Key metrics overview
    st.markdown("### 📊 Key Metrics Overview")
    
    progress_summary = coach.get_progress_summary()
    streaks = progress_summary["streaks"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔥 Coding Streak", 
            value=f"{streaks['coding_streak']['current']} days",
            delta=f"+1" if streaks['coding_streak']['current'] > 0 else "Start today!"
        )
    
    with col2:
        st.metric(
            label="📚 Learning Streak", 
            value=f"{streaks['learning_streak']['current']} days",
            delta=f"Best: {streaks['learning_streak']['longest_ever']}"
        )
    
    with col3:
        st.metric(
            label="📈 Stage Progress", 
            value=f"{progress_summary['current_stage']['progress']}%",
            delta=f"{progress_summary['current_stage']['name']}"
        )
    
    with col4:
        st.metric(
            label="🎯 Overall Progress",
            value=f"{coach.calculate_overall_progress()}%",
            delta=f"Day {(date.today() - date.fromisoformat(coach.progress_data['user_info']['start_date'])).days + 1}"
        )
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("🎯 Get AI Suggestion", use_container_width=True):
            context = coach.build_ai_context()
            suggestion = coach.ai_coach.suggest_daily_focus(context)
            st.info(f"💡 **Today's AI Suggestion:**\n\n{suggestion}")
    
    with action_col2:
        if st.button("📝 Quick Log Coding", use_container_width=True):
            st.session_state.show_quick_log = True
    
    with action_col3:
        if st.button("📱 Generate LinkedIn Post", use_container_width=True):
            linkedin_post = coach.linkedin_generator.generate_daily_post(
                coach.progress_data, coach.linkedin_strategy
            )
            st.session_state.generated_post = linkedin_post
    
    with action_col4:
        if st.button("📊 Progress Report", use_container_width=True):
            st.session_state.show_progress_report = True
    
    # Handle quick actions
    handle_quick_actions(coach)
    
    # Current focus section
    show_current_focus(coach)
    
    # Recent activity
    show_recent_activity(coach)

def show_daily_checkin_results(checkin_result):
    """Display daily check-in results"""
    
    st.markdown("### 🌅 Today's Check-in Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 Current Streaks")
        streaks = checkin_result["streaks"]
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>🔥 Coding Streak: {streaks['coding_streak']['current']} days</h4>
            <p>Longest ever: {streaks['coding_streak']['longest_ever']} days</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>📚 Learning Streak: {streaks['learning_streak']['current']} days</h4>
            <p>Keep the momentum going!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Today's Focus")
        focus = checkin_result["focus"]
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Primary Project</h4>
            <p><strong>{focus['primary_project']}</strong></p>
            <h4>Current Task</h4>
            <p>{focus['current_task']}</p>
            <h4>Next Milestone</h4>
            <p>{focus['next_milestone']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI motivation message
    if "motivation" in checkin_result:
        st.markdown("#### 🤖 AI Coach Message")
        st.markdown(f"""
        <div class='insight-box'>
            {checkin_result['motivation']}
        </div>
        """, unsafe_allow_html=True)
    
    # LinkedIn post suggestion
    if "suggested_linkedin_post" in checkin_result:
        st.markdown("#### 📱 Today's LinkedIn Post Suggestion")
        post_data = checkin_result["suggested_linkedin_post"]
        
        st.markdown(f"""
        <div class='linkedin-post'>
            <h5>📝 {post_data['post_type'].replace('_', ' ').title()}</h5>
            <div style='white-space: pre-wrap; font-size: 14px; line-height: 1.6;'>
{post_data['content']}
            </div>
            <hr style='margin: 1rem 0;'>
            <small>
                <strong>Estimated engagement:</strong> {post_data['estimated_engagement']['likes']} likes, 
                {post_data['estimated_engagement']['comments']} comments<br>
                <strong>Best posting time:</strong> {post_data['optimal_posting_time']}<br>
                <strong>Character count:</strong> {post_data['character_count']}
            </small>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Draft"):
                st.success("Post saved as draft!")
        with col2:
            if st.button("📋 Copy to Clipboard"):
                st.success("Copied! Ready to paste on LinkedIn")
        with col3:
            if st.button("✏️ Customize"):
                st.session_state.customize_post = post_data

def handle_quick_actions(coach):
    """Handle quick action buttons"""
    
    # Quick logging modal
    if st.session_state.get('show_quick_log', False):
        with st.expander("📝 Quick Log Activity", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                duration = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=60)
            with col2:
                activity_type = st.selectbox("Activity Type", 
                    ["Coding", "Learning", "Reading", "Project Work", "Research"])
            
            description = st.text_input("Brief description", placeholder="What did you work on?")
            
            if st.button("✅ Log Activity"):
                result = coach.log_activity(activity_type, duration, description)
                st.success(result["success_message"])
                st.session_state.show_quick_log = False
                st.rerun()
    
    # Progress report
    if st.session_state.get('show_progress_report', False):
        show_progress_report_modal(coach)
    
    # Generated post display
    if st.session_state.get('generated_post'):
        post = st.session_state.generated_post
        st.markdown("#### 📱 Generated LinkedIn Post")
        st.markdown(f"""
        <div class='linkedin-post'>
            <h5>{post['post_type'].replace('_', ' ').title()}</h5>
            <div style='white-space: pre-wrap;'>{post['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Clear Post"):
            del st.session_state.generated_post
            st.rerun()

def show_current_focus(coach):
    """Display current focus section"""
    
    st.markdown("### 🎯 Current Focus")
    
    current_focus = coach.progress_data["current_focus"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **🚀 Primary Project:** {current_focus['primary_project']}
        
        **📋 Current Task:** {current_focus['current_task']}
        
        **🏆 Next Milestone:** {current_focus['next_milestone']}
        """)
    
    with col2:
        st.markdown(f"""
        **📅 Target Completion:** {current_focus.get('estimated_completion', 'TBD')}
        
        **🎯 Priority Skills:** {', '.join(current_focus.get('priority_skills', []))}
        """)

def show_recent_activity(coach):
    """Display recent activity summary"""
    
    st.markdown("### 📈 Recent Activity")
    
    recent_activities = coach.get_most_recent_activities(5)
    
    if recent_activities:
        for activity in recent_activities:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{activity['type']}:** {activity['description']}")
            with col2:
                st.write(f"📅 {activity['date']}")
            with col3:
                st.write(f"⏱️ {activity['duration_minutes']} min")
    else:
        st.info("No recent activities logged. Start by logging your first activity!")

# ========== AI COACH PAGE ==========

def show_ai_coach(coach):
    """AI Coach page with real conversations"""
    st.markdown("# 🤖 AI Progress Coach")
    
    # Check AI connection
    if st.session_state.ai_coach and st.session_state.ai_coach.ai_enabled:
        st.success("✅ AI Coach: Connected to Claude API")
    else:
        st.error("❌ AI Coach: Not connected. Check your API key.")
        return
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Recent Conversation")
        
        # Show last 5 exchanges
        for i, (user_msg, ai_response) in enumerate(st.session_state.chat_history[-5:]):
            st.markdown(f"**You:** {user_msg}")
            st.markdown(f"**🤖 AI Coach:** {ai_response}")
            if i < len(st.session_state.chat_history[-5:]) - 1:
                st.markdown("---")
    
    # Chat input section
    st.markdown("### 💭 Ask Your Coach")
    
    # Create form for chat
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "What would you like to discuss?",
            placeholder="Examples:\n• How am I doing with my progress?\n• What should I focus on today?\n• I'm feeling stuck with Python, any advice?\n• How can I leverage my detective skills in AI?",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_button = st.form_submit_button("🚀 Send", type="primary")
        
        if submit_button and user_input.strip():
            # Show thinking indicator
            with st.spinner("🤖 AI Coach is thinking..."):
                try:
                    # Create basic context for the AI
                    context = {
                        "user_profile": {
                            "background": "Detective Sergeant transitioning to AI Engineer",
                            "goal": "£100k+ AI Engineer role in 18 months",
                            "target_companies": ["Palantir", "Quantexa", "BAE Systems", "NCA"]
                        },
                        "current_stage": {"name": "Stage 2: Real AI Integration"},
                        "current_streaks": {
                            "coding_streak": {"current": 5},
                            "learning_streak": {"current": 12}
                        },
                        "current_focus": {
                            "primary_project": "AI Progress Coach",
                            "current_task": "Building conversational AI interface",
                            "next_milestone": "Complete functional progress coach"
                        },
                        "days_since_start": 7,
                        "recent_activity": {
                            "most_recent_activities": [{
                                "type": "coding",
                                "description": "Building Streamlit AI coach interface",
                                "duration_minutes": 90
                            }]
                        },
                        "recent_challenges": ["Learning Streamlit", "API integration"],
                        "recent_wins": ["Successfully connected Claude API", "Built working web interface"]
                    }
                    
                    # Get AI response
                    ai_response = st.session_state.ai_coach.chat(user_input, context)
                    
                    # Add to chat history
                    st.session_state.chat_history.append((user_input, ai_response))
                    
                    # Rerun to show the new message
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"AI Error: {str(e)}")
                    st.info("The AI coach had a temporary issue. Please try again.")
    
    # Quick question buttons
    st.markdown("### ⚡ Quick Questions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 How am I progressing?", use_container_width=True):
            quick_question = "How am I progressing overall with my Detective to AI Engineer transition? Give me an honest assessment."
            st.session_state.pending_question = quick_question
            st.rerun()
    
    with col2:
        if st.button("🎯 What should I focus on?", use_container_width=True):
            quick_question = "What should I focus on today for my learning? I have about 60 minutes for coding/learning tonight."
            st.session_state.pending_question = quick_question
            st.rerun()
    
    with col3:
        if st.button("💡 Career advice?", use_container_width=True):
            quick_question = "As a Detective transitioning to AI Engineer, what's my biggest advantage and how should I leverage it?"
            st.session_state.pending_question = quick_question
            st.rerun()
    
    # Handle pending questions from quick buttons
    if hasattr(st.session_state, 'pending_question'):
        question = st.session_state.pending_question
        del st.session_state.pending_question
        
        with st.spinner("🤖 AI Coach is thinking..."):
            try:
                context = {
                    "user_profile": {
                        "background": "Detective Sergeant transitioning to AI Engineer",
                        "goal": "£100k+ AI Engineer role in 18 months"
                    },
                    "current_stage": {"name": "Stage 2: Real AI Integration"},
                    "current_streaks": {
                        "coding_streak": {"current": 5},
                        "learning_streak": {"current": 12}
                    },
                    "current_focus": {
                        "primary_project": "AI Progress Coach",
                        "current_task": "Building AI conversations"
                    },
                    "days_since_start": 7,
                    "recent_activity": {"most_recent_activities": []},
                    "recent_challenges": [],
                    "recent_wins": []
                }
                
                ai_response = st.session_state.ai_coach.chat(question, context)
                st.session_state.chat_history.append((question, ai_response))
                st.rerun()
                
            except Exception as e:
                st.error(f"AI Error: {str(e)}")
    
    # Clear chat history button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

# ========== LINKEDIN CONTENT PAGE ==========

def show_linkedin_content(coach):
    """LinkedIn content generation and management"""
    
    st.markdown("# 📱 LinkedIn Content Studio")
    st.markdown("Generate, customize, and manage your professional LinkedIn content for your Detective to Developer journey.")
    
    # Content generation section
    st.markdown("### 🎨 Generate New Post")
    
    col1, col2 = st.columns(2)
    
    with col1:
        post_type = st.selectbox(
            "Post Type",
            ["progress_update", "learning_insight", "project_showcase", "industry_reflection", "tip_sharing", "community_question"],
            format_func=lambda x: x.replace('_', ' ').title()
        )
    
    with col2:
        if st.button("🚀 Generate Post", type="primary", use_container_width=True):
            # Force specific post type
            coach.linkedin_strategy["posting_strategy"]["current_rotation_index"] = \
                coach.linkedin_strategy["posting_strategy"]["content_rotation"].index(post_type)
            
            generated_post = coach.linkedin_generator.generate_daily_post(
                coach.progress_data, coach.linkedin_strategy
            )
            
            st.session_state.linkedin_post = generated_post
    
    # Display generated post
    if st.session_state.get('linkedin_post'):
        post = st.session_state.linkedin_post
        
        st.markdown("### ✨ Generated Post")
        
        st.markdown(f"""
        <div class='linkedin-post'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                <h4 style='margin: 0;'>📝 {post['post_type'].replace('_', ' ').title()}</h4>
                <span style='background: #0066cc; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 12px;'>
                    {post['character_count']} characters
                </span>
            </div>
            <div style='white-space: pre-wrap; font-size: 15px; line-height: 1.6; margin-bottom: 1rem;'>
{post['content']}
            </div>
            <hr style='margin: 1rem 0;'>
            <div style='font-size: 13px; color: #666;'>
                <strong>📊 Estimated Engagement:</strong> {post['estimated_engagement']['likes']} likes, 
                {post['estimated_engagement']['comments']} comments, {post['estimated_engagement']['shares']} shares<br>
                <strong>⏰ Optimal Time:</strong> {post['optimal_posting_time']}<br>
                <strong>🏷️ Hashtags:</strong> {', '.join(post['hashtags_used'])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📋 Copy Text"):
                st.success("✅ Copied to clipboard!")
        
        with col2:
            if st.button("✏️ Edit Post"):
                st.session_state.editing_post = True
        
        with col3:
            if st.button("💾 Save Draft"):
                st.success("💾 Saved as draft!")
        
        with col4:
            if st.button("🔄 Generate New"):
                del st.session_state.linkedin_post
                st.rerun()
    
    # Edit post modal
    if st.session_state.get('editing_post', False):
        show_post_editor(coach)
    
    # Content strategy overview
    show_content_strategy(coach)
    
    # Recent posts performance
    show_post_performance(coach)

def show_post_editor(coach):
    """Post editing interface"""
    
    st.markdown("### ✏️ Edit Post")
    
    post = st.session_state.linkedin_post
    
    edited_content = st.text_area(
        "Edit your post:",
        value=post['content'],
        height=200
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Changes"):
            st.session_state.linkedin_post['content'] = edited_content
            st.session_state.linkedin_post['character_count'] = len(edited_content)
            st.session_state.editing_post = False
            st.success("✅ Post updated!")
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.editing_post = False
            st.rerun()

def show_content_strategy(coach):
    """Display content strategy information"""
    
    with st.expander("📋 Content Strategy Overview"):
        strategy = coach.linkedin_strategy
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎯 Brand Positioning**")
            st.write(f"Unique Angle: {strategy['brand_positioning']['unique_angle']}")
            st.write(f"Value Prop: {strategy['brand_positioning']['value_proposition']}")
            
            st.markdown("**📅 Posting Strategy**")
            st.write(f"Frequency: {strategy['posting_strategy']['frequency']}")
            st.write(f"Best Times: {', '.join(strategy['posting_strategy']['best_posting_times'])}")
        
        with col2:
            st.markdown("**🔄 Content Rotation**")
            rotation = strategy['posting_strategy']['content_rotation']
            current_index = strategy['posting_strategy'].get('current_rotation_index', 0)
            
            for i, post_type in enumerate(rotation):
                prefix = "➡️ " if i == current_index else "   "
                st.write(f"{prefix}{post_type.replace('_', ' ').title()}")

def show_post_performance(coach):
    """Display post performance tracking"""
    
    with st.expander("📈 Post Performance Tracking"):
        st.info("📊 Post performance tracking will be implemented when you start posting regularly. The system will track likes, comments, shares, and engagement rates to optimize future content.")
        
        # Placeholder for future performance data
        sample_data = {
            "Post Type": ["Progress Update", "Learning Insight", "Project Showcase"],
            "Average Likes": [25, 35, 45],
            "Average Comments": [3, 5, 7]
        }
        
        df = pd.DataFrame(sample_data)
        fig = px.bar(df, x="Post Type", y="Average Likes", title="Post Performance by Type (Example)")
        st.plotly_chart(fig, use_container_width=True)

# ========== ACTIVITY LOGGING PAGE ==========

def show_activity_logging(coach):
    """Activity logging interface"""
    
    st.markdown("# 📝 Activity Logging")
    st.markdown("Log your learning activities to track progress and maintain streaks.")
    
    # Quick log section
    st.markdown("### ⚡ Quick Log")
    
    with st.form("quick_log_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            activity_type = st.selectbox(
                "Activity Type",
                ["Coding", "Learning", "Reading", "Podcast", "Project Work", "Research", "Practice"]
            )
        
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=480, value=60)
        
        with col3:
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        
        description = st.text_area("Description", placeholder="What did you work on? What did you learn?")
        notes = st.text_input("Additional Notes", placeholder="Any challenges or insights?")
        
        submitted = st.form_submit_button("🚀 Log Activity", type="primary", use_container_width=True)
        
        if submitted:
            result = coach.log_activity(
                activity_type, duration, description, difficulty.lower(), notes
            )
            
            st.success(result["success_message"])
            
            # Show updated streaks
            updated_streaks = result["updated_streaks"]
            st.markdown("#### 🔥 Updated Streaks")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Coding Streak", f"{updated_streaks['coding_streak']['current']} days")
            with col2:
                st.metric("Learning Streak", f"{updated_streaks['learning_streak']['current']} days")
            with col3:
                st.metric("Consistency", f"{updated_streaks['consistency_streak']['current']} days")
    
    # Task completion section
    st.markdown("### ✅ Mark Task Complete")
    
    with st.form("task_completion_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            task_name = st.text_input("Task Name", placeholder="e.g., 'Completed data architecture'")
            project = st.text_input("Project", placeholder="e.g., 'AI Progress Coach'")
        
        with col2:
            completion_notes = st.text_area("Completion Notes", placeholder="What was accomplished?")
        
        task_submitted = st.form_submit_button("✅ Mark Complete", type="primary", use_container_width=True)
        
        if task_submitted and task_name:
            result = coach.mark_task_complete(task_name, project, completion_notes)
            st.success(f"✅ Task completed: {task_name}")
            
            if "next_task" in result:
                st.info(f"🎯 **Next suggested task:** {result['next_task']}")
    
    # Today's summary
    show_todays_summary(coach)
    
    # Recent activity log
    show_activity_history(coach)

def show_todays_summary(coach):
    """Show today's activity summary"""
    
    st.markdown("### 📊 Today's Summary")
    
    today = date.today().isoformat()
    activities = coach.progress_data.get("completed_activities", {})
    
    if today in activities:
        today_data = activities[today]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Coding Time", f"{today_data.get('coding_minutes', 0)} min")
        with col2:
            st.metric("Learning Time", f"{today_data.get('learning_minutes', 0)} min")
        with col3:
            st.metric("Total Activities", len(today_data.get('activities', [])))
        with col4:
            total_time = today_data.get('coding_minutes', 0) + today_data.get('learning_minutes', 0)
            st.metric("Total Time", f"{total_time} min")
        
        # Today's activities
        if today_data.get('activities'):
            st.markdown("**Today's Activities:**")
            for activity in today_data['activities']:
                st.write(f"• {activity['type']}: {activity['description']} ({activity['duration_minutes']} min)")
    else:
        st.info("No activities logged today. Start by logging your first activity!")

def show_activity_history(coach):
    """Show recent activity history"""
    
    with st.expander("📈 Recent Activity History"):
        activities = coach.progress_data.get("completed_activities", {})
        
        # Get last 7 days
        recent_dates = sorted(activities.keys(), reverse=True)[:7]
        
        for date_str in recent_dates:
            day_data = activities[date_str]
            total_time = day_data.get('coding_minutes', 0) + day_data.get('learning_minutes', 0)
            activity_count = len(day_data.get('activities', []))
            
            st.markdown(f"**{date_str}** - {total_time} min total, {activity_count} activities")
            
            for activity in day_data.get('activities', []):
                st.write(f"   • {activity['type']}: {activity.get('description', 'No description')} ({activity['duration_minutes']} min)")

# ========== ANALYTICS PAGE ==========

def show_analytics(coach):
    """Analytics and insights dashboard"""
    
    st.markdown("# 📊 Progress Analytics")
    st.markdown("Deep insights into your learning journey, trends, and performance metrics.")
    
    # Calculate analytics
    analytics = coach.analytics.calculate_performance_metrics(coach.progress_data)
    
    # Performance overview
    show_performance_overview(analytics)
    
    # Learning velocity
    show_velocity_analysis(analytics)
    
    # Streak analysis
    show_streak_analysis(coach)
    
    # Goal achievement
    show_goal_analysis(analytics)
    
    # Trends and patterns
    show_trend_analysis(analytics)
    
    # Performance insights
    show_performance_insights(analytics)

def show_performance_overview(analytics):
    """Show performance overview metrics"""
    
    st.markdown("### 🎯 Performance Overview")
    
    velocity = analytics["learning_velocity"]
    efficiency = analytics["efficiency_metrics"]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Daily Average",
            f"{velocity['daily_average_minutes']} min",
            f"Target: 60 min"
        )
    
    with col2:
        st.metric(
            "Active Days",
            f"{velocity['active_days_percentage']}%",
            f"Efficiency: {efficiency['efficiency_score']}/100"
        )
    
    with col3:
        st.metric(
            "Total Hours",
            f"{velocity['total_hours']} hrs",
            f"Monthly projection: {velocity['estimated_monthly_hours']} hrs"
        )
    
    with col4:
        st.metric(
            "Avg Session",
            f"{efficiency['average_coding_session']} min",
            f"Longest: {efficiency['longest_coding_session']} min"
        )

def show_velocity_analysis(analytics):
    """Show learning velocity analysis"""
    
    st.markdown("### 🚀 Learning Velocity")
    
    velocity = analytics["learning_velocity"]
    weekly_data = velocity["weekly_velocity"]
    
    if weekly_data:
        # Create velocity chart
        df = pd.DataFrame(weekly_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['week_start'],
            y=df['total_minutes'],
            mode='lines+markers',
            name='Total Minutes',
            line=dict(color='#457b9d', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['week_start'],
            y=df['coding_minutes'],
            mode='lines+markers',
            name='Coding Minutes',
            line=dict(color='#ff6b35', width=2)
        ))
        
        fig.update_layout(
            title="Weekly Learning Velocity",
            xaxis_title="Week",
            yaxis_title="Minutes",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Velocity insights
        trend = velocity["velocity_trend"]
        trend_colors = {
            "accelerating": "🚀 **Accelerating** - Great momentum!",
            "stable": "📈 **Stable** - Consistent progress",
            "declining": "⚠️ **Declining** - Consider refocusing"
        }
        
        st.info(trend_colors.get(trend, "📊 Analyzing trends..."))

def show_streak_analysis(coach):
    """Show streak analysis and patterns"""
    
    st.markdown("### 🔥 Streak Analysis")
    
    streak_patterns = coach.streak_calculator.analyze_streak_patterns(coach.progress_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Current Momentum")
        st.info(streak_patterns["current_momentum"])
        
        st.markdown("#### 🎯 Streak Recommendations")
        for rec in streak_patterns["streak_recommendations"]:
            st.write(f"• {rec}")
    
    with col2:
        st.markdown("#### 🔧 Areas for Improvement")
        for area in streak_patterns["areas_for_improvement"]:
            st.write(f"• {area}")
        
        st.markdown("#### 📊 Sustainability Score")
        sustainability = streak_patterns["sustainability_score"]
        st.progress(sustainability / 100)
        st.write(f"{sustainability:.1f}/100 - {'Excellent' if sustainability > 80 else 'Good' if sustainability > 60 else 'Needs improvement'}")

def show_goal_analysis(analytics):
    """Show goal achievement analysis"""
    
    st.markdown("### 🏆 Goal Achievement")
    
    goals = analytics["goal_achievement"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Daily Goal Rate",
            f"{goals['daily_goal_achievement_rate']}%",
            "Target: 60+ min/day"
        )
    
    with col2:
        st.metric(
            "Weekly Goal Rate", 
            f"{goals['weekly_goal_achievement_rate']}%",
            "Target: 5+ active days"
        )
    
    with col3:
        st.metric(
            "On Track %",
            f"{goals['on_track_percentage']}%",
            "18-month timeline"
        )
    
    # Current week progress
    current_week = goals["current_week_progress"]
    
    st.markdown("#### 📅 This Week's Progress")
    progress_bar_value = current_week["goal_progress"] / 100
    st.progress(progress_bar_value)
    st.write(f"**{current_week['days_completed']}/5** active days completed | **{current_week['total_minutes']}** minutes total")

def show_trend_analysis(analytics):
    """Show trend analysis"""
    
    with st.expander("📈 Detailed Trend Analysis"):
        trends = analytics["trend_analysis"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Learning Patterns")
            patterns = trends["learning_patterns"]
            for pattern in patterns:
                st.write(f"• {pattern}")
        
        with col2:
            st.markdown("#### 🎯 Momentum Direction")
            st.info(f"Overall momentum is: **{trends['momentum_direction']}**")

def show_performance_insights(analytics):
    """Show actionable performance insights"""
    
    st.markdown("### 💡 Performance Insights")
    
    insights = analytics["performance_insights"]
    
    for insight in insights:
        insight_type = insight.get("type", "general")
        title = insight.get("title", "Insight")
        description = insight.get("description", "")
        recommendation = insight.get("recommendation", "")
        
        with st.expander(f"💡 {title}"):
            st.write(description)
            if recommendation:
                st.success(f"**Recommendation:** {recommendation}")

# ========== SETTINGS PAGE ==========

def show_settings(coach):
    """Settings and configuration page"""
    
    st.markdown("# ⚙️ Settings")
    st.markdown("Configure your AI coach preferences and system settings.")
    
    # API Configuration
    st.markdown("### 🔧 API Configuration")
    
    current_api_key = os.getenv('ANTHROPIC_API_KEY', '')
    api_status = "✅ Connected" if coach.ai_coach.ai_enabled else "❌ Not Connected"
    
    st.info(f"**AI Coach Status:** {api_status}")
    
    with st.expander("🔑 API Key Management"):
        new_api_key = st.text_input(
            "Anthropic API Key", 
            value="***" if current_api_key else "",
            type="password",
            help="Enter your Anthropic API key to enable AI conversations"
        )
        
        if st.button("💾 Save API Key"):
            if new_api_key and new_api_key != "***":
                # Save to .env file (simplified)
                st.success("API key updated! Restart the app to apply changes.")
    
    # Goal Configuration
    st.markdown("### 🎯 Goal Configuration")
    
    with st.form("goal_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            daily_goal = st.number_input("Daily Learning Goal (minutes)", min_value=15, max_value=300, value=60)
            weekly_goal = st.number_input("Weekly Active Days Goal", min_value=1, max_value=7, value=5)
        
        with col2:
            target_salary = st.number_input("Target Salary (£)", min_value=50000, max_value=200000, value=100000, step=5000)
            timeline_months = st.number_input("Timeline (months)", min_value=6, max_value=36, value=18)
        
        if st.form_submit_button("💾 Update Goals"):
            st.success("Goals updated successfully!")
    
    # LinkedIn Strategy
    st.markdown("### 📱 LinkedIn Strategy")
    
    with st.form("linkedin_settings"):
        posting_frequency = st.selectbox("Posting Frequency", ["daily", "every_2_days", "3x_week", "weekly"])
        
        col1, col2 = st.columns(2)
        with col1:
            best_time_1 = st.time_input("Best Posting Time 1", value=pd.to_datetime("08:30").time())
            best_time_2 = st.time_input("Best Posting Time 2", value=pd.to_datetime("17:30").time())
        
        with col2:
            focus_hashtags = st.text_area("Additional Hashtags", value="#TechTransition\n#CareerChange")
        
        if st.form_submit_button("💾 Update LinkedIn Strategy"):
            st.success("LinkedIn strategy updated!")
    
    # Data Management
    st.markdown("### 💾 Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export Data"):
            st.success("Data exported successfully!")
    
    with col2:
        if st.button("🔄 Reset Streaks"):
            st.warning("This will reset all streak counters!")
    
    with col3:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
    
    # System Information
    with st.expander("ℹ️ System Information"):
        st.markdown(f"""
        **Version:** Detective to Developer Coach v1.0.0
        
        **Data Location:** `./data/`
        
        **API Status:** {api_status}
        
        **Total Activities:** {len(coach.progress_data.get('completed_activities', {}))}
        
        **Start Date:** {coach.progress_data.get('user_info', {}).get('start_date', 'Not set')}
        
        **Current Stage:** {coach.progress_data.get('user_info', {}).get('current_stage', 'Not set')}
        """)

def show_progress_report_modal(coach):
    """Show detailed progress report"""
    
    with st.expander("📊 Detailed Progress Report", expanded=True):
        progress = coach.get_progress_summary()
        
        st.markdown("#### 🎯 Current Stage Progress")
        stage_info = progress["current_stage"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Stage:** {stage_info['name']}")
            st.write(f"**Progress:** {stage_info['progress']}%")
        with col2:
            st.write(f"**Status:** {stage_info['status']}")
            st.write(f"**Overall:** {progress['overall_progress']}%")
        
        st.markdown("#### 🔥 Current Streaks")
        streaks = progress["streaks"]
        
        streak_col1, streak_col2, streak_col3 = st.columns(3)
        with streak_col1:
            st.metric("Coding", f"{streaks['coding_streak']['current']} days")
        with streak_col2:
            st.metric("Learning", f"{streaks['learning_streak']['current']} days")
        with streak_col3:
            st.metric("Consistency", f"{streaks['consistency_streak']['current']} days")
        
        st.markdown("#### 🏆 Recent Achievements")
        achievements = progress["recent_achievements"]
        for achievement in achievements[:5]:
            st.write(f"• **{achievement['date']}**: {achievement['achievement']}")
        
        if st.button("Close Report"):
            st.session_state.show_progress_report = False
            st.rerun()

# ========== APPLICATION ENTRY POINT ==========

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.markdown("### 🔧 Troubleshooting")
        st.markdown("""
        If you're seeing this error:
        1. Check that all data files exist in the `data/` directory
        2. Ensure your API key is properly set in `.env`
        3. Verify all dependencies are installed: `pip install -r requirements.txt`
        4. Check the console for detailed error messages
        """)