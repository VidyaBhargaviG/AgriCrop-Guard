/**
 * Crop Disease & Pest Advisory System
 * Main JavaScript - Shared utilities, navigation, and i18n
 */

// ---------- XSS Protection ----------
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ---------- Mobile Navigation ----------
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('navToggle');
    const menu = document.getElementById('navMenu');

    if (toggle && menu) {
        toggle.addEventListener('click', function () {
            menu.classList.toggle('active');
        });

        // Close menu on link click
        document.querySelectorAll('.nav-link').forEach(function (link) {
            link.addEventListener('click', function () {
                menu.classList.remove('active');
            });
        });
    }

    // Initialize language
    initLanguage();
});


// ---------- Multilingual (i18n) ----------
let currentLang = localStorage.getItem('cropguard_lang') || 'en';
let translations = {};

async function initLanguage() {
    const selector = document.getElementById('langSelector');
    if (selector) {
        selector.value = currentLang;
        selector.addEventListener('change', function () {
            currentLang = this.value;
            localStorage.setItem('cropguard_lang', currentLang);
            loadTranslations(currentLang);
        });
    }

    if (currentLang !== 'en') {
        await loadTranslations(currentLang);
    }
}

async function loadTranslations(lang) {
    try {
        const response = await fetch('/api/translations/' + encodeURIComponent(lang));
        translations = await response.json();
        applyTranslations();
    } catch (error) {
        // Silently fall back to English
    }
}

function applyTranslations() {
    // Translate text content
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
        const key = el.getAttribute('data-i18n');
        if (translations[key]) {
            el.textContent = translations[key];
        }
    });

    // Translate placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
        const key = el.getAttribute('data-i18n-placeholder');
        if (translations[key]) {
            el.placeholder = translations[key];
        }
    });

    // Re-render dynamic content if functions exist
    if (typeof loadCrops === 'function') {
        loadCrops();
    }
}

// Helper: get translation by key with fallback
function t(key, fallback) {
    return (translations && translations[key]) ? translations[key] : (fallback || key);
}


// ---------- Chatbot ----------
let chatLang = currentLang;

function initChatbot() {
    // Inject chatbot widget HTML into page
    const chatbotHTML = `
        <button class="chatbot-toggle" id="chatbotToggle" aria-label="Open chat">
            <i class="fas fa-comments"></i>
        </button>
        <div class="chatbot-window" id="chatbotWindow">
            <div class="chatbot-header">
                <h4><i class="fas fa-robot"></i> <span data-i18n="chatbot_title">${t('chatbot_title', 'Crop Assistant')}</span></h4>
                <div class="chatbot-header-actions">
                    <select id="chatLangSelector" class="chat-lang-select" aria-label="Chat language">
                        <option value="en">EN</option>
                        <option value="hi">हिं</option>
                        <option value="kn">ಕನ್</option>
                    </select>
                    <button class="chatbot-close" id="chatbotClose" aria-label="Close chat">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="chatbot-messages" id="chatMessages">
                <div class="chat-msg bot">${t('chatbot_welcome', 'Hello! I\'m your Crop Advisory Assistant. Ask me about diseases, pests, or treatments for Paddy, Chilli, and Coffee.')}</div>
            </div>
            <div class="chat-typing" id="chatTyping" data-i18n="thinking">${t('thinking', 'Thinking...')}</div>
            <div class="chatbot-input">
                <input type="text" id="chatInput" data-i18n-placeholder="chatbot_placeholder" placeholder="${t('chatbot_placeholder', 'Ask about crops, diseases...')}" maxlength="1000" autocomplete="off">
                <button id="chatSendBtn" aria-label="Send message"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);

    // Set chat language selector to current language
    var chatLangSel = document.getElementById('chatLangSelector');
    chatLang = currentLang;
    chatLangSel.value = chatLang;
    chatLangSel.addEventListener('change', function () {
        chatLang = this.value;
        _resetChatForLanguage();
    });

    // Reapply translations if non-English
    if (currentLang !== 'en' && Object.keys(translations).length > 0) {
        applyTranslations();
    }

    // Event listeners
    document.getElementById('chatbotToggle').addEventListener('click', function () {
        document.getElementById('chatbotWindow').classList.toggle('open');
    });

    document.getElementById('chatbotClose').addEventListener('click', function () {
        document.getElementById('chatbotWindow').classList.remove('open');
    });

    document.getElementById('chatSendBtn').addEventListener('click', sendChatMessage);
    document.getElementById('chatInput').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendChatMessage();
    });

    // Add initial crop selection buttons
    _addWelcomeButtons();
}

var CHAT_WELCOME = {
    'en': 'Hello! I\'m your Crop Advisory Assistant. Ask me about diseases, pests, or treatments for Paddy, Chilli, and Coffee.',
    'hi': 'नमस्ते! मैं आपका फसल सलाहकार सहायक हूं। धान, मिर्च और कॉफी के रोग, कीट या उपचार के बारे में पूछें।',
    'kn': 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಬೆಳೆ ಸಲಹಾ ಸಹಾಯಕ. ಭತ್ತ, ಮೆಣಸಿನಕಾಯಿ ಮತ್ತು ಕಾಫಿಯ ರೋಗ, ಕೀಟ ಅಥವಾ ಚಿಕಿತ್ಸೆ ಬಗ್ಗೆ ಕೇಳಿ.'
};

function _resetChatForLanguage() {
    var messagesDiv = document.getElementById('chatMessages');
    if (!messagesDiv) return;
    messagesDiv.innerHTML = '';
    var welcome = document.createElement('div');
    welcome.className = 'chat-msg bot';
    welcome.textContent = CHAT_WELCOME[chatLang] || CHAT_WELCOME['en'];
    messagesDiv.appendChild(welcome);
    _addWelcomeButtons();
}

function _addWelcomeButtons() {
    var messagesDiv = document.getElementById('chatMessages');
    if (!messagesDiv) return;
    var cropBtns = [
        {label: '🌾 ' + (chatLang === 'kn' ? 'ಭತ್ತ (ಅಕ್ಕಿ)' : chatLang === 'hi' ? 'धान (चावल)' : 'Paddy (Rice)'), value: chatLang === 'kn' ? 'ಭತ್ತ' : chatLang === 'hi' ? 'धान' : 'paddy'},
        {label: '🌶️ ' + (chatLang === 'kn' ? 'ಮೆಣಸಿನಕಾಯಿ' : chatLang === 'hi' ? 'मिर्च' : 'Chilli'), value: chatLang === 'kn' ? 'ಮೆಣಸಿನಕಾಯಿ' : chatLang === 'hi' ? 'मिर्च' : 'chilli'},
        {label: '☕ ' + (chatLang === 'kn' ? 'ಕಾಫಿ' : chatLang === 'hi' ? 'कॉफी' : 'Coffee'), value: chatLang === 'kn' ? 'ಕಾಫಿ' : chatLang === 'hi' ? 'कॉफी' : 'coffee'},
    ];
    var btnContainer = document.createElement('div');
    btnContainer.className = 'chat-buttons';
    cropBtns.forEach(function (btn) {
        var button = document.createElement('button');
        button.className = 'chat-quick-btn';
        button.textContent = btn.label;
        button.addEventListener('click', function () {
            document.querySelectorAll('.chat-buttons').forEach(function (el) { el.remove(); });
            document.getElementById('chatInput').value = btn.value;
            sendChatMessage();
        });
        btnContainer.appendChild(button);
    });
    messagesDiv.appendChild(btnContainer);
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;

    const messagesDiv = document.getElementById('chatMessages');
    const typing = document.getElementById('chatTyping');

    // Add user message
    const userBubble = document.createElement('div');
    userBubble.className = 'chat-msg user';
    userBubble.textContent = msg;
    messagesDiv.appendChild(userBubble);
    input.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Show typing indicator
    typing.classList.add('visible');

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, lang: chatLang })
        });
        const data = await res.json();
        typing.classList.remove('visible');

        const botBubble = document.createElement('div');
        botBubble.className = 'chat-msg bot';
        // Simple markdown-to-HTML: bold (**text**) and line breaks
        let reply = escapeHtml(data.reply || data.error || t('chat_error', 'Sorry, something went wrong.'));
        reply = reply.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        botBubble.innerHTML = reply;
        messagesDiv.appendChild(botBubble);

        // Render quick-reply buttons if present
        if (data.buttons && data.buttons.length > 0) {
            const btnContainer = document.createElement('div');
            btnContainer.className = 'chat-buttons';
            data.buttons.forEach(function (btn) {
                const button = document.createElement('button');
                button.className = 'chat-quick-btn';
                button.textContent = btn.label;
                button.addEventListener('click', function () {
                    // Remove all button containers
                    document.querySelectorAll('.chat-buttons').forEach(function (el) { el.remove(); });
                    // Send button value as message
                    document.getElementById('chatInput').value = btn.value;
                    sendChatMessage();
                });
                btnContainer.appendChild(button);
            });
            messagesDiv.appendChild(btnContainer);
        }
    } catch (err) {
        typing.classList.remove('visible');
        const errBubble = document.createElement('div');
        errBubble.className = 'chat-msg bot';
        errBubble.textContent = t('chat_connect_error', 'Sorry, could not connect. Please try again.');
        messagesDiv.appendChild(errBubble);
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Initialize chatbot after DOM ready
document.addEventListener('DOMContentLoaded', initChatbot);
