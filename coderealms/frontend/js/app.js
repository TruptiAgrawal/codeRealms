class CodeRealmsApp {
    constructor() {
        this.apiBase = 'http://localhost:3000/api';
        this.token = localStorage.getItem('token');
        this.currentUser = null;
        this.currentView = 'dashboard';
        
        // Avatar options
        this.avatars = [
            { id: 'warrior', name: 'Warrior', icon: '⚔️' },
            { id: 'mage', name: 'Mage', icon: '🧙‍♂️' },
            { id: 'hacker', name: 'Hacker', icon: '👨‍💻' },
            { id: 'rogue', name: 'Rogue', icon: '🥷' },
            { id: 'scientist', name: 'Scientist', icon: '🔬' },
            { id: 'ai-engineer', name: 'AI Engineer', icon: '🤖' }
        ];

        // Theme options
        this.themes = [
            { id: 'dark', name: 'Dark', class: 'theme-dark' },
            { id: 'light', name: 'Light', class: 'theme-light' },
            { id: 'cyberpunk', name: 'Cyberpunk', class: 'theme-cyberpunk' },
            { id: 'forest', name: 'Forest', class: 'theme-forest' },
            { id: 'ocean', name: 'Ocean', class: 'theme-ocean' },
            { id: 'sunset', name: 'Sunset', class: 'theme-sunset' }
        ];

        this.init();
    }

    async init() {
        this.showLoading();
        await this.checkAuth();
        this.setupEventListeners();
        this.hideLoading();
    }

    // Authentication Methods
    async checkAuth() {
        if (this.token) {
            try {
                const response = await this.apiCall('/users/profile', 'GET');
                if (response.user) {
                    this.currentUser = response.user;
                    this.showMainApp();
                    this.updateDashboard();
                } else {
                    this.showAuth();
                }
            } catch (error) {
                console.error('Auth check failed:', error);
                this.token = null;
                localStorage.removeItem('token');
                this.showAuth();
            }
        } else {
            this.showAuth();
        }
    }

    async login(email, password) {
        try {
            const response = await this.apiCall('/auth/login', 'POST', { email, password });
            
            this.token = response.token;
            this.currentUser = response.user;
            localStorage.setItem('token', this.token);
            
            this.showMessage('Login successful!', 'success');
            this.showMainApp();
            this.updateDashboard();
        } catch (error) {
            this.showMessage(error.message || 'Login failed', 'error');
        }
    }

    async register(username, email, password) {
        try {
            const response = await this.apiCall('/auth/register', 'POST', {
                username, email, password, avatar: 'warrior', theme: 'dark'
            });
            
            this.token = response.token;
            this.currentUser = response.user;
            localStorage.setItem('token', this.token);
            
            this.showMessage('Registration successful!', 'success');
            this.showMainApp();
            this.updateDashboard();
        } catch (error) {
            this.showMessage(error.message || 'Registration failed', 'error');
        }
    }

    logout() {
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem('token');
        this.showAuth();
        this.showMessage('Logged out successfully', 'success');
    }

    // API Methods
    async apiCall(endpoint, method = 'GET', data = null) {
        const config = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        if (data) {
            config.body = JSON.stringify(data);
        }

        const response = await fetch(this.apiBase + endpoint, config);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'API call failed');
        }

        return result;
    }

    // UI Methods
    showLoading() {
        document.getElementById('loading-screen').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loading-screen').classList.add('hidden');
    }

    showAuth() {
        document.getElementById('auth-screen').classList.remove('hidden');
        document.getElementById('main-content').classList.add('hidden');
        document.getElementById('navbar').classList.add('hidden');
    }

    showMainApp() {
        document.getElementById('auth-screen').classList.add('hidden');
        document.getElementById('main-content').classList.remove('hidden');
        document.getElementById('navbar').classList.remove('hidden');
        this.updateNavbar();
    }

    showView(viewName) {
        // Hide all views
        document.querySelectorAll('[id$="-view"]').forEach(view => {
            view.classList.add('hidden');
        });

        // Show selected view
        document.getElementById(`${viewName}-view`).classList.remove('hidden');
        this.currentView = viewName;

        // Load view-specific data
        if (viewName === 'leaderboard') {
            this.loadLeaderboard();
        } else if (viewName === 'profile') {
            this.loadProfile();
        }
    }

    updateNavbar() {
        if (!this.currentUser) return;

        document.getElementById('user-name').textContent = this.currentUser.username;
        document.getElementById('user-level').textContent = `Level ${this.currentUser.level}`;
        document.getElementById('user-xp').textContent = `${this.currentUser.xp} XP`;
        
        // Set avatar (using emoji for now)
        const avatar = this.avatars.find(a => a.id === this.currentUser.avatar);
        document.getElementById('user-avatar').textContent = avatar?.icon || '⚔️';
    }

    updateDashboard() {
        if (!this.currentUser) return;

        document.getElementById('total-xp').textContent = this.currentUser.xp;
        document.getElementById('current-level').textContent = this.currentUser.level;
        document.getElementById('quest-count').textContent = this.currentUser.completedQuests?.length || 0;
        document.getElementById('streak-count').textContent = this.currentUser.streak || 0;

        // Update progress bar
        const currentLevelXP = this.currentUser.currentLevelXP || 0;
        const nextLevelXP = this.currentUser.nextLevelXP || 100;
        const progress = Math.min((currentLevelXP / nextLevelXP) * 100, 100);
        
        document.getElementById('progress-bar').style.width = `${progress}%`;
        document.getElementById('current-level-xp').textContent = `${currentLevelXP} XP`;
        document.getElementById('next-level-xp').textContent = nextLevelXP ? `${nextLevelXP} XP` : 'MAX';
    }

    loadProfile() {
        // Populate avatar selection
        const avatarContainer = document.getElementById('avatar-selection');
        avatarContainer.innerHTML = '';
        
        this.avatars.forEach(avatar => {
            const avatarDiv = document.createElement('div');
            avatarDiv.className = `avatar-option bg-gray-700 p-4 rounded-lg text-center ${
                this.currentUser.avatar === avatar.id ? 'selected' : ''
            }`;
            avatarDiv.innerHTML = `
                <div class="text-3xl mb-2">${avatar.icon}</div>
                <div class="text-sm">${avatar.name}</div>
            `;
            avatarDiv.addEventListener('click', (event) => this.selectAvatar(event, avatar.id));
            avatarContainer.appendChild(avatarDiv);
        });

        // Populate theme selection
        const themeContainer = document.getElementById('theme-selection');
        themeContainer.innerHTML = '';
        
        this.themes.forEach(theme => {
            const themeDiv = document.createElement('div');
            themeDiv.className = `theme-option ${theme.class} rounded-lg ${
                this.currentUser.theme === theme.id ? 'selected' : ''
            }`;
            themeDiv.innerHTML = `<span class="font-bold">${theme.name}</span>`;
            themeDiv.addEventListener('click', (event) => this.selectTheme(event, theme.id));
            themeContainer.appendChild(themeDiv);
        });
    }

    selectAvatar(event, avatarId) {
        document.querySelectorAll('.avatar-option').forEach(el => el.classList.remove('selected'));
        event.currentTarget.classList.add('selected');
        this.currentUser.avatar = avatarId;
    }

    selectTheme(event, themeId) {
        document.querySelectorAll('.theme-option').forEach(el => el.classList.remove('selected'));
        event.currentTarget.classList.add('selected');
        this.currentUser.theme = themeId;
    }

    async saveProfile() {
        try {
            await this.apiCall('/users/profile', 'PUT', {
                avatar: this.currentUser.avatar,
                theme: this.currentUser.theme
            });
            
            this.showMessage('Profile updated successfully!', 'success');
            this.updateNavbar();
            this.showView('dashboard');
        } catch (error) {
            this.showMessage(error.message || 'Failed to update profile', 'error');
        }
    }

    async loadLeaderboard() {
        try {
            const response = await this.apiCall('/users/leaderboard', 'GET');
            const container = document.getElementById('leaderboard-content');
            
            container.innerHTML = response.leaderboard.map((user, index) => `
                <div class="leaderboard-entry bg-gray-700 p-4 rounded-lg flex items-center justify-between">
                    <div class="flex items-center space-x-4">
                        <div class="text-2xl font-bold ${
                            index === 0 ? 'text-yellow-400' : 
                            index === 1 ? 'text-gray-400' : 
                            index === 2 ? 'text-orange-400' : 'text-gray-500'
                        }">
                            #${user.rank}
                        </div>
                        <div class="text-2xl">${this.avatars.find(a => a.id === user.avatar)?.icon || '⚔️'}</div>
                        <div>
                            <div class="font-bold">${user.username}</div>
                            <div class="text-sm text-gray-400">${user.levelName}</div>
                        </div>
                    </div>
                    <div class="text-right">
                        <div class="font-bold text-yellow-400">${user.xp} XP</div>
                        <div class="text-sm text-gray-400">Level ${user.level}</div>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            this.showMessage('Failed to load leaderboard', 'error');
        }
    }

    showMessage(message, type = 'info') {
        const container = document.getElementById('message-container');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        container.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    // Event Listeners
    setupEventListeners() {
        // Auth forms
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            this.login(email, password);
        });

        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('register-username').value;
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            this.register(username, email, password);
        });

        // Toggle between login/register
        document.getElementById('show-register').addEventListener('click', () => {
            document.getElementById('login-form').classList.add('hidden');
            document.getElementById('register-form').classList.remove('hidden');
        });

        document.getElementById('show-login').addEventListener('click', () => {
            document.getElementById('register-form').classList.add('hidden');
            document.getElementById('login-form').classList.remove('hidden');
        });

        // Navigation
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());
        document.getElementById('start-quest-btn').addEventListener('click', () => {
            this.showMessage('Quest system coming soon!', 'info');
        });
        document.getElementById('view-profile-btn').addEventListener('click', () => this.showView('profile'));
        document.getElementById('leaderboard-btn').addEventListener('click', () => this.showView('leaderboard'));
        document.getElementById('back-dashboard-btn').addEventListener('click', () => this.showView('dashboard'));
        document.getElementById('back-from-leaderboard-btn').addEventListener('click', () => this.showView('dashboard'));
        
        // Profile actions
        document.getElementById('save-profile-btn').addEventListener('click', () => this.saveProfile());
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CodeRealmsApp();
});