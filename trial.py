import streamlit as st
import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json

# Configure page
st.set_page_config(
    page_title="🎮 GameDev Learning Platform",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for AAA Gaming Experience
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Orbitron', monospace;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .game-title {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 2.5rem;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .xp-bar-container {
        background: rgba(0,0,0,0.3);
        border-radius: 25px;
        padding: 5px;
        margin: 15px 0;
    }
    
    .xp-bar {
        background: linear-gradient(90deg, #4ade80, #3b82f6, #8b5cf6);
        height: 25px;
        border-radius: 20px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .xp-bar::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .quest-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .quest-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .level-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .locked-card {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #d1d5db;
        opacity: 0.6;
        border: 2px dashed rgba(255,255,255,0.3);
    }
    
    .contest-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .skill-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #374151;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .stat-box {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .character-avatar {
        font-size: 4rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        max-width: 500px;
        margin: 2rem auto;
    }
</style>
""", unsafe_allow_html=True)

# --- MainGame (Core Engine & Game Theory Manager) ---
class MainGame:
    LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 3500, 5500, 8000, 12000]
    LEVEL_NAMES = [
        "Origin I", "Origin II", "Breaker I", "Breaker II", "Breaker III",
        "Dragon I", "Dragon II", "Dragon III", "Legend I", "Legend II"
    ]
    
    def __init__(self):
        self.player_xp = 0
        self.level = 1
        self.streak = 1
        self.total_quests_completed = 0
        self.achievements = []
        self.last_login = datetime.date.today()
        
        # Enhanced quest system with categories
        self.quests = [
            {"title": "Solve: Two Sum Problem", "xp_reward": 50, "completed": False, "category": "DSA", "difficulty": "Easy"},
            {"title": "Build a Responsive Landing Page", "xp_reward": 75, "completed": False, "category": "Development", "difficulty": "Medium"},
            {"title": "Complete CTF Challenge", "xp_reward": 100, "completed": False, "category": "Cybersecurity", "difficulty": "Hard"},
            {"title": "Implement Linear Regression", "xp_reward": 80, "completed": False, "category": "ML", "difficulty": "Medium"},
            {"title": "Analyze Dataset with Pandas", "xp_reward": 60, "completed": False, "category": "Data Science", "difficulty": "Easy"},
        ]
        
        # Contest system
        self.contests = [
            {"name": "Weekly Code Sprint", "date": "2025-06-15", "type": "DSA", "rewards": "300 XP + Badge", "status": "upcoming"},
            {"name": "Hackathon Challenge", "date": "2025-06-20", "type": "Development", "rewards": "500 XP + Title", "status": "upcoming"},
            {"name": "Security CTF", "date": "2025-06-25", "type": "Cybersecurity", "rewards": "400 XP + Certificate", "status": "upcoming"},
        ]

    def calculate_xp(self, points):
        old_level = self.level
        self.player_xp += points
        self.update_level()
        
        # Check for level up achievement
        if self.level > old_level:
            self.achievements.append(f"Reached {self.get_level_name()}!")
            return True  # Level up occurred
        return False

    def update_level(self):
        for i, xp_req in enumerate(self.LEVEL_THRESHOLDS):
            if self.player_xp < xp_req:
                self.level = max(1, i)
                break
        else:
            self.level = len(self.LEVEL_THRESHOLDS)

    def get_level_name(self):
        level_index = min(self.level - 1, len(self.LEVEL_NAMES) - 1)
        return self.LEVEL_NAMES[level_index]
    
    def get_xp_progress(self):
        if self.level >= len(self.LEVEL_THRESHOLDS):
            return 100
        
        current_xp = self.LEVEL_THRESHOLDS[self.level - 1] if self.level > 1 else 0
        next_xp = self.LEVEL_THRESHOLDS[self.level] if self.level < len(self.LEVEL_THRESHOLDS) else self.LEVEL_THRESHOLDS[-1]
        
        if next_xp == current_xp:
            return 100
            
        progress = ((self.player_xp - current_xp) / (next_xp - current_xp)) * 100
        return min(max(progress, 0), 100)

    def complete_quest(self, idx):
        if idx < len(self.quests) and not self.quests[idx]["completed"]:
            self.quests[idx]["completed"] = True
            xp_gained = self.quests[idx]["xp_reward"]
            level_up = self.calculate_xp(xp_gained)
            self.total_quests_completed += 1
            
            # Achievement system
            if self.total_quests_completed == 1:
                self.achievements.append("First Quest Completed! 🎉")
            elif self.total_quests_completed == 10:
                self.achievements.append("Quest Master - 10 Quests! 🏆")
            
            return level_up, xp_gained
        return False, 0

    def update_streak(self):
        today = datetime.date.today()
        if self.last_login == today - datetime.timedelta(days=1):
            self.streak += 1
        elif self.last_login != today:
            self.streak = 1
        self.last_login = today

# --- CharacterManager (Player Avatar & Skill Loadout System) ---
class CharacterManager:
    AVAILABLE_AVATARS = {
        "Warrior": "⚔️",
        "Mage": "🧙‍♂️",
        "Hacker": "👨‍💻",
        "Rogue": "🥷",
        "Scientist": "👩‍🔬",
        "AI Engineer": "🤖",
    }

    SKILL_PATHS = {
        "Development": {"icon": "💻", "description": "Build amazing web applications"},
        "Cybersecurity": {"icon": "🛡️", "description": "Protect digital assets"},
        "Machine Learning": {"icon": "🧠", "description": "Create intelligent systems"},
        "Data Science": {"icon": "📊", "description": "Extract insights from data"},
        "Competitive Programming": {"icon": "🏆", "description": "Master algorithmic challenges"},
        "DevOps": {"icon": "⚙️", "description": "Streamline development workflows"}
    }

    def __init__(self, username):
        self.username = username
        self.avatar = "Warrior"  # Default avatar
        self.primary_skill = "Development"
        self.secondary_skills = []
        self.customization = {
            "theme": "default",
            "badge_display": True,
            "notification_preferences": "all"
        }
        self.game = MainGame()
        self.game.update_streak()

    def select_avatar(self, avatar_name):
        if avatar_name in self.AVAILABLE_AVATARS:
            self.avatar = avatar_name
            return True
        return False

    def set_primary_skill(self, skill_path):
        if skill_path in self.SKILL_PATHS:
            self.primary_skill = skill_path

    def add_secondary_skill(self, skill_path):
        if skill_path in self.SKILL_PATHS and skill_path not in self.secondary_skills and skill_path != self.primary_skill:
            self.secondary_skills.append(skill_path)

    def remove_secondary_skill(self, skill_path):
        if skill_path in self.secondary_skills:
            self.secondary_skills.remove(skill_path)

# --- AuthenticationModule (Enhanced with Session Management) ---
class AuthenticationModule:
    def __init__(self):
        # In production, this would connect to a database
        if 'users_db' not in st.session_state:
            st.session_state.users_db = {"igris": {"password": "gamedev123", "email": "igris@gamedev.com", "created_date": "2025-06-09", "character_data": CharacterManager("igris")}}
    def login(self, username, password):
        if username in st.session_state.users_db:
            stored_data = st.session_state.users_db[username]
            if stored_data["password"] == password:
                return True, stored_data.get("character_data")
        return False, None

    def signup(self, username, password, email=""):
        if username in st.session_state.users_db:
            return False, "Username already exists"
        
        # Create new user with default character
        character_manager = CharacterManager(username)
        st.session_state.users_db[username] = {
            "password": password,
            "email": email,
            "created_date": datetime.date.today().isoformat(),
            "character_data": character_manager
        }
        return True, "Account created successfully"

    def save_character_data(self, username, character_manager):
        if username in st.session_state.users_db:
            st.session_state.users_db[username]["character_data"] = character_manager

# --- UI Components ---
def render_login_screen():
    st.markdown('<div class="game-title">🎮 GameDev Academy</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="login-container">
                <h2 style="text-align: center; margin-bottom: 2rem;">🚀 Enter the Arena</h2>
            </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
            
            auth = AuthenticationModule()
            
            with tab1:
                with st.form("login_form"):
                    username = st.text_input("👤 Username", placeholder="Enter your username")
                    password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                    login_btn = st.form_submit_button("🎮 Enter Game", use_container_width=True)
                    
                    if login_btn and username and password:
                        success, character_data = auth.login(username, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user = username
                            st.session_state.character_manager = character_data
                            st.success(f"🎉 Welcome back, {username}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Try again!")
            
            with tab2:
                with st.form("signup_form"):
                    new_username = st.text_input("👤 Choose Username", placeholder="Your unique username")
                    new_email = st.text_input("📧 Email", placeholder="your.email@example.com")
                    new_password = st.text_input("🔒 Create Password", type="password", placeholder="Strong password")
                    signup_btn = st.form_submit_button("🌟 Create Account", use_container_width=True)
                    
                    if signup_btn and new_username and new_password:
                        success, message = auth.signup(new_username, new_password, new_email)
                        if success:
                            st.success(f"✅ {message} Please login!")
                        else:
                            st.error(f"❌ {message}")

def render_dashboard(char_mgr):
    # Main header with stats
    st.markdown(f"""
    <div class="main-header">
        <div class="character-avatar">{CharacterManager.AVAILABLE_AVATARS[char_mgr.avatar]}</div>
        <h1>{char_mgr.username}</h1>
        <h3>{char_mgr.game.get_level_name()}</h3>
        <div style="display: flex; justify-content: space-around; margin-top: 2rem;">
            <div class="stat-box">
                <div style="font-size: 1.5rem;">🔥</div>
                <div style="font-size: 1.2rem; font-weight: bold;">{char_mgr.game.streak}</div>
                <small>Day Streak</small>
            </div>
            <div class="stat-box">
                <div style="font-size: 1.5rem;">⚡</div>
                <div style="font-size: 1.2rem; font-weight: bold;">{char_mgr.game.player_xp}</div>
                <small>Total XP</small>
            </div>
            <div class="stat-box">
                <div style="font-size: 1.5rem;">🎯</div>
                <div style="font-size: 1.2rem; font-weight: bold;">{char_mgr.game.total_quests_completed}</div>
                <small>Quests Done</small>
            </div>
            <div class="stat-box">
                <div style="font-size: 1.5rem;">🏆</div>
                <div style="font-size: 1.2rem; font-weight: bold;">{len(char_mgr.game.achievements)}</div>
                <small>Achievements</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # XP Progress Bar
    progress = char_mgr.game.get_xp_progress()
    current_level_xp = char_mgr.game.LEVEL_THRESHOLDS[char_mgr.game.level - 1] if char_mgr.game.level > 1 else 0
    next_level_xp = char_mgr.game.LEVEL_THRESHOLDS[char_mgr.game.level] if char_mgr.game.level < len(char_mgr.game.LEVEL_THRESHOLDS) else char_mgr.game.LEVEL_THRESHOLDS[-1]
    
    st.markdown(f"""
    <div style="margin: 2rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <strong>🚀 Level Progress: {char_mgr.game.get_level_name()}</strong>
            <span>{progress:.1f}% ({char_mgr.game.player_xp - current_level_xp}/{next_level_xp - current_level_xp} XP)</span>
        </div>
        <div class="xp-bar-container">
            <div class="xp-bar" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_quests(char_mgr):
    st.markdown("## 🎯 Daily Quests & Challenges")
    
    # Quest categories
    categories = list(set(quest["category"] for quest in char_mgr.game.quests))
    selected_category = st.selectbox("🔍 Filter by Category", ["All"] + categories)
    
    filtered_quests = char_mgr.game.quests
    if selected_category != "All":
        filtered_quests = [q for q in char_mgr.game.quests if q["category"] == selected_category]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for idx, quest in enumerate(filtered_quests):
            difficulty_colors = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
            difficulty_icon = difficulty_colors.get(quest["difficulty"], "⚪")
            
            quest_idx = char_mgr.game.quests.index(quest)  # Get original index
            
            st.markdown(f"""
            <div class="quest-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>{'✅' if quest['completed'] else '⏳'} {quest['title']}</h4>
                        <p style="margin: 0.5rem 0;">
                            {difficulty_icon} {quest['difficulty']} • 
                            📚 {quest['category']} • 
                            ⚡ +{quest['xp_reward']} XP
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if not quest["completed"]:
                if st.button(f"🚀 Complete Quest", key=f"quest_{quest_idx}", use_container_width=True):
                    level_up, xp_gained = char_mgr.game.complete_quest(quest_idx)
                    if level_up:
                        st.balloons()
                        st.success(f"🎉 LEVEL UP! You reached {char_mgr.game.get_level_name()}!")
                    st.success(f"✅ Quest completed! +{xp_gained} XP earned!")
                    st.rerun()
    
    with col2:
        # Quest statistics
        completed = sum(1 for q in char_mgr.game.quests if q["completed"])
        total = len(char_mgr.game.quests)
        
        st.markdown(f"""
        <div class="stat-box" style="margin: 0;">
            <h4>📊 Quest Progress</h4>
            <p style="font-size: 1.5rem; margin: 1rem 0;">{completed}/{total}</p>
            <div style="background: #e0e0e0; border-radius: 10px; height: 10px;">
                <div style="background: linear-gradient(90deg, #4ade80, #3b82f6); 
                            width: {(completed/total)*100 if total > 0 else 0}%; 
                            height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Recent achievements
        if char_mgr.game.achievements:
            st.markdown("### 🏆 Recent Achievements")
            for achievement in char_mgr.game.achievements[-3:]:  # Show last 3
                st.success(achievement)

def render_character_customization(char_mgr):
    st.markdown("## 🎨 Character Customization")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <div style="font-size: 6rem; margin-bottom: 1rem;">{CharacterManager.AVAILABLE_AVATARS[char_mgr.avatar]}</div>
            <h3>{char_mgr.username}</h3>
            <p>{char_mgr.avatar}</p>
            <p>Level {char_mgr.game.level} • {char_mgr.game.get_level_name()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Avatar selection
        st.markdown("### 👤 Choose Your Avatar")
        avatar_cols = st.columns(3)
        
        for i, (name, emoji) in enumerate(CharacterManager.AVAILABLE_AVATARS.items()):
            col_idx = i % 3
            with avatar_cols[col_idx]:
                is_selected = char_mgr.avatar == name
                button_style = "🌟 " if is_selected else ""
                if st.button(f"{button_style}{emoji} {name}", key=f"avatar_{name}", use_container_width=True):
                    char_mgr.select_avatar(name)
                    st.success(f"Avatar changed to {name}!")
                    st.rerun()
        
        # Skill path management
        st.markdown("### 🎯 Skill Specialization")
        
        primary_skill = st.selectbox(
            "🥇 Primary Skill Path",
            list(CharacterManager.SKILL_PATHS.keys()),
            index=list(CharacterManager.SKILL_PATHS.keys()).index(char_mgr.primary_skill)
        )
        
        if primary_skill != char_mgr.primary_skill:
            char_mgr.set_primary_skill(primary_skill)
            st.success(f"Primary skill set to {primary_skill}!")
            st.rerun()
        
        # Display primary skill info
        skill_info = CharacterManager.SKILL_PATHS[char_mgr.primary_skill]
        st.info(f"{skill_info['icon']} {skill_info['description']}")
        
        # Secondary skills
        st.markdown("### 🔧 Secondary Skills")
        available_secondary = [skill for skill in CharacterManager.SKILL_PATHS.keys() 
                              if skill != char_mgr.primary_skill and skill not in char_mgr.secondary_skills]
        
        if available_secondary:
            add_skill = st.selectbox("Add secondary skill", ["Select..."] + available_secondary)
            if add_skill != "Select..." and st.button("Add Skill"):
                char_mgr.add_secondary_skill(add_skill)
                st.success(f"Added {add_skill} as secondary skill!")
                st.rerun()
        
        # Display current secondary skills
        if char_mgr.secondary_skills:
            for skill in char_mgr.secondary_skills:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    skill_info = CharacterManager.SKILL_PATHS[skill]
                    st.write(f"{skill_info['icon']} {skill}")
                with col_b:
                    if st.button("Remove", key=f"remove_{skill}"):
                        char_mgr.remove_secondary_skill(skill)
                        st.rerun()

def render_leaderboard_contests(char_mgr):
    tab1, tab2 = st.tabs(["🏆 Contests", "📈 Leaderboard"])
    
    with tab1:
        st.markdown("## 🎪 Upcoming Contests")
        
        for contest in char_mgr.game.contests:
            st.markdown(f"""
            <div class="contest-card">
                <h3>🎯 {contest['name']}</h3>
                <p><strong>📅 Date:</strong> {contest['date']}</p>
                <p><strong>🏷️ Type:</strong> {contest['type']}</p>
                <p><strong>🎁 Rewards:</strong> {contest['rewards']}</p>
                <p><strong>📊 Status:</strong> {contest['status'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🚀 Register for {contest['name']}", key=f"contest_{contest['name']}"):
                st.success(f"✅ Successfully registered for {contest['name']}!")
    
    with tab2:
        st.markdown("## 🏅 Global Leaderboard")
        
        # Mock leaderboard data
        leaderboard_data = [
            {"rank": 1, "username": "CodeMaster", "xp": 12500, "level": "Legend I"},
            {"rank": 2, "username": "AlgoQueen", "xp": 11200, "level": "Dragon III"},
            {"rank": 3, "username": char_mgr.username, "xp": char_mgr.game.player_xp, "level": char_mgr.game.get_level_name()},
            {"rank": 4, "username": "DataWizard", "xp": 8900, "level": "Dragon II"},
            {"rank": 5, "username": "CyberNinja", "xp": 7600, "level": "Dragon I"},
        ]
        
        for player in leaderboard_data:
            highlight = "background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: black;" if player["username"] == char_mgr.username else "background: rgba(255,255,255,0.1);"
            
            st.markdown(f"""
            <div style="{highlight} padding: 1rem; border-radius: 10px; margin: 0.5rem 0; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>#{player['rank']} {player['username']}</strong>
                    {'👑' if player['username'] == char_mgr.username else ''}
                </div>
                <div>
                    <span>{player['level']} • {player['xp']} XP</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- Main Application ---
def main():
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "character_manager" not in st.session_state:
        st.session_state.character_manager = None

    # Show login screen if not logged in
    if not st.session_state.logged_in:
        render_login_screen()
        return

    # Main application for logged-in users
    char_mgr = st.session_state.character_manager
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 1rem;">
            <div style="font-size: 3rem;">{CharacterManager.AVAILABLE_AVATARS[char_mgr.avatar]}</div>
            <h3>{char_mgr.username}</h3>
            <p>{char_mgr.game.get_level_name()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        page = st.selectbox(
            "🎮 Navigate",
            ["🏠 Dashboard", "🎯 Quests", "🎨 Character", "🏆 Contests", "📚 Learning Hub"]
        )
        
        st.markdown("---")
        
        # Quick stats in sidebar
        st.metric("🔥 Streak", f"{char_mgr.game.streak} days")
        st.metric("⚡ Total XP", char_mgr.game.player_xp)
        st.metric("🎯 Quests", char_mgr.game.total_quests_completed)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            # Save character data before logout
            auth = AuthenticationModule()
            auth.save_character_data(st.session_state.user, char_mgr)
            
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.character_manager = None
            st.rerun()

    # Main content area
    if page == "🏠 Dashboard":
        render_dashboard(char_mgr)
        
        # Additional dashboard content
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("## 📈 Recent Activity")
            # Mock recent activity
            activities = [
                "✅ Completed 'Two Sum Problem' quest (+50 XP)",
                "🏆 Reached Dragon I level!",
                "📚 Started Machine Learning skill path",
                "🎯 Maintained 7-day streak",
                "🚀 Registered for Weekly Code Sprint"
            ]
            
            for activity in activities[:5]:
                st.info(activity)
        
        with col2:
            st.markdown("## 🎯 Quick Actions")
            
            if st.button("🎲 Random Quest", use_container_width=True):
                incomplete_quests = [i for i, q in enumerate(char_mgr.game.quests) if not q["completed"]]
                if incomplete_quests:
                    import random
                    quest_idx = random.choice(incomplete_quests)
                    level_up, xp_gained = char_mgr.game.complete_quest(quest_idx)
                    if level_up:
                        st.balloons()
                        st.success(f"🎉 LEVEL UP! You reached {char_mgr.game.get_level_name()}!")
                    st.success(f"✅ Random quest completed! +{xp_gained} XP earned!")
                    st.rerun()
                else:
                    st.info("No incomplete quests available!")
            
            if st.button("💰 Daily Bonus", use_container_width=True):
                bonus_xp = 25 * char_mgr.game.streak
                level_up = char_mgr.game.calculate_xp(bonus_xp)
                if level_up:
                    st.balloons()
                    st.success(f"🎉 LEVEL UP! You reached {char_mgr.game.get_level_name()}!")
                st.success(f"🎁 Daily bonus claimed! +{bonus_xp} XP!")
                st.rerun()
            
            st.markdown("### 🏅 Skill Progress")
            skills_progress = {
                char_mgr.primary_skill: 85,
                **{skill: 60 for skill in char_mgr.secondary_skills[:2]}
            }
            
            for skill, progress in skills_progress.items():
                st.markdown(f"**{CharacterManager.SKILL_PATHS[skill]['icon']} {skill}**")
                st.progress(progress / 100)

    elif page == "🎯 Quests":
        render_quests(char_mgr)
        
        # Add quest creation section
        st.markdown("---")
        st.markdown("## ➕ Create Custom Quest")
        
        with st.expander("🛠️ Quest Builder"):
            col1, col2 = st.columns(2)
            
            with col1:
                custom_title = st.text_input("Quest Title", placeholder="e.g., Build a Calculator App")
                custom_category = st.selectbox("Category", ["Development", "DSA", "ML", "Data Science", "Cybersecurity"])
                custom_difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            
            with col2:
                custom_xp = st.slider("XP Reward", 25, 200, 50)
                custom_description = st.text_area("Description", placeholder="Describe the quest objectives...")
            
            if st.button("🚀 Add Custom Quest") and custom_title:
                new_quest = {
                    "title": custom_title,
                    "xp_reward": custom_xp,
                    "completed": False,
                    "category": custom_category,
                    "difficulty": custom_difficulty
                }
                char_mgr.game.quests.append(new_quest)
                st.success("✅ Custom quest added successfully!")
                st.rerun()

    elif page == "🎨 Character":
        render_character_customization(char_mgr)
        
        # Add theme customization
        st.markdown("---")
        st.markdown("### 🎨 Theme Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            theme_options = ["Default", "Dark Mode", "Neon", "Retro", "Minimal"]
            selected_theme = st.selectbox("Choose Theme", theme_options)
            
            if st.button("Apply Theme"):
                char_mgr.customization["theme"] = selected_theme
                st.success(f"Theme changed to {selected_theme}!")
        
        with col2:
            badge_display = st.checkbox("Show Achievement Badges", value=char_mgr.customization["badge_display"])
            notification_pref = st.selectbox("Notifications", ["All", "Important Only", "None"])
            
            char_mgr.customization["badge_display"] = badge_display
            char_mgr.customization["notification_preferences"] = notification_pref

    elif page == "🏆 Contests":
        render_leaderboard_contests(char_mgr)

    elif page == "📚 Learning Hub":
        st.markdown("## 📚 Learning Resources Hub")
        
        # Learning paths
        tab1, tab2, tab3 = st.tabs(["🛤️ Learning Paths", "📖 Resources", "🎓 Certificates"])
        
        with tab1:
            st.markdown("### 🚀 Recommended Learning Paths")
            
            learning_paths = [
                {
                    "title": "Full Stack Development",
                    "description": "Master both frontend and backend development",
                    "duration": "12 weeks",
                    "difficulty": "Intermediate",
                    "skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "Database"],
                    "xp_reward": 1000
                },
                {
                    "title": "Data Science Mastery",
                    "description": "From basics to advanced machine learning",
                    "duration": "16 weeks",
                    "difficulty": "Advanced",
                    "skills": ["Python", "Pandas", "Scikit-learn", "Deep Learning", "Visualization"],
                    "xp_reward": 1500
                },
                {
                    "title": "Cybersecurity Fundamentals",
                    "description": "Essential security concepts and practices",
                    "duration": "10 weeks",
                    "difficulty": "Beginner",
                    "skills": ["Network Security", "Cryptography", "Ethical Hacking", "Risk Assessment"],
                    "xp_reward": 800
                }
            ]
            
            for path in learning_paths:
                st.markdown(f"""
                <div class="skill-card">
                    <h3>🎯 {path['title']}</h3>
                    <p>{path['description']}</p>
                    <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                        <span>⏱️ {path['duration']}</span>
                        <span>📊 {path['difficulty']}</span>
                        <span>⚡ +{path['xp_reward']} XP</span>
                    </div>
                    <div style="margin: 1rem 0;">
                        <strong>Skills:</strong> {', '.join(path['skills'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🚀 Start {path['title']}", key=f"path_{path['title']}"):
                    st.success(f"✅ Started learning path: {path['title']}!")
        
        with tab2:
            st.markdown("### 📖 Curated Resources")
            
            resource_categories = {
                "💻 Development": [
                    "MDN Web Docs - Complete web development reference",
                    "freeCodeCamp - Interactive coding lessons",
                    "The Odin Project - Full-stack curriculum"
                ],
                "🧠 Machine Learning": [
                    "Coursera ML Course - Andrew Ng's famous course",
                    "Kaggle Learn - Free micro-courses",
                    "Papers With Code - Latest research papers"
                ],
                "🛡️ Cybersecurity": [
                    "OWASP Top 10 - Web security risks",
                    "Cybrary - Free cybersecurity training",
                    "TryHackMe - Hands-on security challenges"
                ]
            }
            
            for category, resources in resource_categories.items():
                st.markdown(f"#### {category}")
                for resource in resources:
                    st.markdown(f"• {resource}")
                st.markdown("")
        
        with tab3:
            st.markdown("### 🎓 Available Certificates")
            
            certificates = [
                {"name": "GameDev Academy Graduate", "requirement": "Complete 50 quests", "progress": f"{char_mgr.game.total_quests_completed}/50"},
                {"name": "Code Master", "requirement": "Reach Legend level", "progress": f"Level {char_mgr.game.level}/10"},
                {"name": "Streak Warrior", "requirement": "Maintain 30-day streak", "progress": f"{char_mgr.game.streak}/30 days"},
                {"name": "Quest Hunter", "requirement": "Complete 100 quests", "progress": f"{char_mgr.game.total_quests_completed}/100"}
            ]
            
            for cert in certificates:
                progress_parts = cert["progress"].split("/")
                if len(progress_parts) == 2:
                    current = int(progress_parts[0])
                    total = int(progress_parts[1].split()[0])
                    progress_percent = min((current / total) * 100, 100)
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 1rem; border-radius: 10px; margin: 1rem 0; color: #374151;">
                        <h4>🏆 {cert['name']}</h4>
                        <p>{cert['requirement']}</p>
                        <div style="background: rgba(0,0,0,0.1); border-radius: 10px; height: 20px; margin: 0.5rem 0;">
                            <div style="background: linear-gradient(90deg, #4ade80, #3b82f6); width: {progress_percent}%; height: 100%; border-radius: 10px;"></div>
                        </div>
                        <small>{cert['progress']} ({progress_percent:.1f}%)</small>
                    </div>
                    """, unsafe_allow_html=True)

    # Auto-save character data periodically
    auth = AuthenticationModule()
    auth.save_character_data(st.session_state.user, char_mgr)

if __name__ == "__main__":
    main()
