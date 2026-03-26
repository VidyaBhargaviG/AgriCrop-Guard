"""
Chatbot Module for Crop Advisory System
Answers farmer questions about crops, diseases, pests, and treatments
using the database as the knowledge source.
Supports guided conversation flow with quick-reply buttons.
"""

from backend.models import db, Crop, Disease, Pest


# Keywords mapped to intents
INTENT_KEYWORDS = {
    'greeting': ['hello', 'hi', 'hey', 'namaste', 'namaskar', 'help', 'namaskara',
                  'ನಮಸ್ಕಾರ', 'ಹಲೋ', 'ನಮಸ್ತೆ', 'ಸಹಾಯ',
                  'नमस्ते', 'नमस्कार', 'हेलो', 'मदद'],
    'list_crops': ['crops', 'all crops', 'which crops', 'what crops', 'available crops',
                   'ಬೆಳೆಗಳು', 'ಯಾವ ಬೆಳೆ', 'ಎಲ್ಲಾ ಬೆಳೆ',
                   'फसलें', 'कौन सी फसल', 'सभी फसलें'],
    'list_diseases': ['diseases', 'all diseases', 'disease list',
                      'ರೋಗಗಳು', 'ಎಲ್ಲಾ ರೋಗ', 'ರೋಗ ಪಟ್ಟಿ',
                      'रोग', 'सभी रोग', 'बीमारियां'],
    'list_pests': ['pests', 'all pests', 'pest list', 'insects',
                   'ಕೀಟಗಳು', 'ಎಲ್ಲಾ ಕೀಟ',
                   'कीट', 'सभी कीट', 'कीड़े'],
    'symptom': ['symptom', 'symptoms', 'sign', 'signs', 'yellowing', 'wilting',
                'spots', 'lesion', 'curling', 'browning', 'drying',
                'ಲಕ್ಷಣ', 'ಹಳದಿ', 'ಒಣಗುವಿಕೆ', 'ಕಲೆ',
                'लक्षण', 'पीलापन', 'मुरझाना', 'धब्बे'],
    'treatment': ['treatment', 'cure', 'remedy', 'how to treat', 'medicine', 'spray',
                  'chemical', 'organic', 'fungicide', 'pesticide',
                  'ಚಿಕಿತ್ಸೆ', 'ಔಷಧ', 'ಸ್ಪ್ರೇ',
                  'उपचार', 'दवा', 'इलाज', 'स्प्रे'],
    'prevention': ['prevent', 'prevention', 'avoid', 'protect', 'how to prevent',
                   'ತಡೆಗಟ್ಟು', 'ರಕ್ಷಣೆ', 'ತಡೆ',
                   'रोकथाम', 'बचाव', 'कैसे रोकें'],
    'season': ['season', 'when', 'which month', 'time', 'kharif', 'rabi',
               'ಋತು', 'ಯಾವಾಗ', 'ಸಮಯ', 'ಮುಂಗಾರು', 'ಹಿಂಗಾರು',
               'मौसम', 'कब', 'कौन सा महीना'],
    'growing_guide': ['grow', 'growing', 'cultivate', 'cultivation', 'how to grow',
                      'farming', 'planting', 'sowing',
                      'ಬೆಳೆಸು', 'ಬೆಳೆಯುವ', 'ಕೃಷಿ', 'ಬಿತ್ತನೆ', 'ನಾಟಿ', 'ಬೆಳೆಯುವ ಮಾರ್ಗದರ್ಶಿ',
                      'उगाना', 'खेती', 'बुवाई', 'कैसे उगाएं', 'रोपण'],
    'tips': ['tips', 'advice', 'best practices', 'suggestions', 'recommend',
             'ಸಲಹೆ', 'ಉಪಾಯ', 'ಸೂಚನೆ', 'ಟಿಪ್ಸ್',
             'सुझाव', 'सलाह', 'टिप्स'],
}

# Crop name mappings (multilingual)
CROP_ALIASES = {
    'paddy': 'paddy', 'rice': 'paddy', 'dhan': 'paddy', 'chawal': 'paddy',
    'ಭತ್ತ': 'paddy', 'ಅಕ್ಕಿ': 'paddy',
    'धान': 'paddy', 'चावल': 'paddy',
    'chilli': 'chilli', 'chili': 'chilli', 'mirchi': 'chilli', 'pepper': 'chilli',
    'ಮೆಣಸಿನಕಾಯಿ': 'chilli', 'ಮೆಣಸು': 'chilli',
    'मिर्च': 'chilli', 'मिर्ची': 'chilli',
    'coffee': 'coffee', 'kaafi': 'coffee',
    'ಕಾಫಿ': 'coffee',
    'कॉफी': 'coffee', 'काफी': 'coffee',
}

# Response templates
RESPONSES = {
    'en': {
        'greeting': "Hello! I'm your Crop Advisory Assistant 🌾\n\n"
                    "What would you like to know about? Choose a crop below or type your question:",
        'greeting_buttons': [
            {'label': '🌾 Paddy (Rice)', 'value': 'paddy'},
            {'label': '🌶️ Chilli', 'value': 'chilli'},
            {'label': '☕ Coffee', 'value': 'coffee'},
        ],
        'crop_menu': "What would you like to know about **{crop}**?",
        'crop_menu_buttons': [
            {'label': '📖 Growing Guide', 'value': '{crop_key} growing guide'},
            {'label': '💡 Tips & Best Practices', 'value': '{crop_key} tips'},
            {'label': '🦠 Diseases', 'value': '{crop_key} diseases'},
            {'label': '🐛 Pests', 'value': '{crop_key} pests'},
            {'label': '🛡️ Disease Prevention', 'value': '{crop_key} prevention'},
            {'label': '💊 Treatments', 'value': '{crop_key} treatment'},
        ],
        'not_understood': "I'm not sure I understand. Choose an option below or type your question:",
        'not_understood_buttons': [
            {'label': '🌾 Paddy', 'value': 'paddy'},
            {'label': '🌶️ Chilli', 'value': 'chilli'},
            {'label': '☕ Coffee', 'value': 'coffee'},
            {'label': '🦠 All Diseases', 'value': 'all diseases'},
            {'label': '🐛 All Pests', 'value': 'all pests'},
        ],
        'crop_list': "We support **3 crops**:\n\n",
        'disease_list': "Here are the diseases for **{crop}**:\n\n",
        'pest_list': "Here are the pests for **{crop}**:\n\n",
        'all_diseases': "Here are all diseases in our database:\n\n",
        'all_pests': "Here are all pests in our database:\n\n",
    },
    'hi': {
        'greeting': "नमस्ते! मैं आपका फसल सलाहकार सहायक हूं 🌾\n\n"
                    "आप किस बारे में जानना चाहते हैं? नीचे फसल चुनें या अपना सवाल लिखें:",
        'greeting_buttons': [
            {'label': '🌾 धान (चावल)', 'value': 'धान'},
            {'label': '🌶️ मिर्च', 'value': 'मिर्च'},
            {'label': '☕ कॉफी', 'value': 'कॉफी'},
        ],
        'crop_menu': "**{crop}** के बारे में आप क्या जानना चाहते हैं?",
        'crop_menu_buttons': [
            {'label': '📖 उगाने की गाइड', 'value': '{crop_key} उगाना'},
            {'label': '💡 सुझाव और टिप्स', 'value': '{crop_key} सुझाव'},
            {'label': '🦠 रोग', 'value': '{crop_key} रोग'},
            {'label': '🐛 कीट', 'value': '{crop_key} कीट'},
            {'label': '🛡️ रोग रोकथाम', 'value': '{crop_key} रोकथाम'},
            {'label': '💊 उपचार', 'value': '{crop_key} उपचार'},
        ],
        'not_understood': "मैं समझ नहीं पाया। नीचे विकल्प चुनें या अपना सवाल लिखें:",
        'not_understood_buttons': [
            {'label': '🌾 धान', 'value': 'धान'},
            {'label': '🌶️ मिर्च', 'value': 'मिर्च'},
            {'label': '☕ कॉफी', 'value': 'कॉफी'},
            {'label': '🦠 सभी रोग', 'value': 'सभी रोग'},
            {'label': '🐛 सभी कीट', 'value': 'सभी कीट'},
        ],
        'crop_list': "हम **3 फसलों** का समर्थन करते हैं:\n\n",
        'disease_list': "**{crop}** के रोग:\n\n",
        'pest_list': "**{crop}** के कीट:\n\n",
        'all_diseases': "हमारे डेटाबेस में सभी रोग:\n\n",
        'all_pests': "हमारे डेटाबेस में सभी कीट:\n\n",
    },
    'kn': {
        'greeting': "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಬೆಳೆ ಸಲಹಾ ಸಹಾಯಕ 🌾\n\n"
                    "ನೀವು ಏನು ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ? ಕೆಳಗಿನ ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಬರೆಯಿರಿ:",
        'greeting_buttons': [
            {'label': '🌾 ಭತ್ತ (ಅಕ್ಕಿ)', 'value': 'ಭತ್ತ'},
            {'label': '🌶️ ಮೆಣಸಿನಕಾಯಿ', 'value': 'ಮೆಣಸಿನಕಾಯಿ'},
            {'label': '☕ ಕಾಫಿ', 'value': 'ಕಾಫಿ'},
        ],
        'crop_menu': "**{crop}** ಬಗ್ಗೆ ನೀವು ಏನು ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ?",
        'crop_menu_buttons': [
            {'label': '📖 ಬೆಳೆಯುವ ಮಾರ್ಗದರ್ಶಿ', 'value': '{crop_key} ಬೆಳೆಯುವ ಮಾರ್ಗದರ್ಶಿ'},
            {'label': '💡 ಸಲಹೆ ಮತ್ತು ಉಪಾಯಗಳು', 'value': '{crop_key} ಸಲಹೆ'},
            {'label': '🦠 ರೋಗಗಳು', 'value': '{crop_key} ರೋಗಗಳು'},
            {'label': '🐛 ಕೀಟಗಳು', 'value': '{crop_key} ಕೀಟಗಳು'},
            {'label': '🛡️ ರೋಗ ತಡೆಗಟ್ಟುವಿಕೆ', 'value': '{crop_key} ತಡೆಗಟ್ಟು'},
            {'label': '💊 ಚಿಕಿತ್ಸೆ', 'value': '{crop_key} ಚಿಕಿತ್ಸೆ'},
        ],
        'not_understood': "ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ. ಕೆಳಗಿನ ಆಯ್ಕೆ ಆರಿಸಿ ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಬರೆಯಿರಿ:",
        'not_understood_buttons': [
            {'label': '🌾 ಭತ್ತ', 'value': 'ಭತ್ತ'},
            {'label': '🌶️ ಮೆಣಸಿನಕಾಯಿ', 'value': 'ಮೆಣಸಿನಕಾಯಿ'},
            {'label': '☕ ಕಾಫಿ', 'value': 'ಕಾಫಿ'},
            {'label': '🦠 ಎಲ್ಲಾ ರೋಗ', 'value': 'ಎಲ್ಲಾ ರೋಗ'},
            {'label': '🐛 ಎಲ್ಲಾ ಕೀಟ', 'value': 'ಎಲ್ಲಾ ಕೀಟ'},
        ],
        'crop_list': "ನಾವು **3 ಬೆಳೆಗಳನ್ನು** ಬೆಂಬಲಿಸುತ್ತೇವೆ:\n\n",
        'disease_list': "**{crop}** ರೋಗಗಳು:\n\n",
        'pest_list': "**{crop}** ಕೀಟಗಳು:\n\n",
        'all_diseases': "ನಮ್ಮ ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಎಲ್ಲಾ ರೋಗಗಳು:\n\n",
        'all_pests': "ನಮ್ಮ ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಎಲ್ಲಾ ಕೀಟಗಳು:\n\n",
    },
}

# Growing guide content (multilingual)
GROWING_GUIDES = {
    'paddy': {
        'en': "**🌾 Paddy (Rice) Growing Guide**\n\n"
              "**Soil:** Clay or clay-loam soil with good water retention.\n"
              "**Climate:** Warm and humid, 20–37°C, rainfall 100–200 cm.\n"
              "**Seasons:** Kharif (June–Nov, main crop), Rabi/Boro (Nov–May in eastern/southern India), Summer (Jan–May in irrigated areas).\n\n"
              "**Steps:**\n"
              "1. **Land Preparation:** Plough field 2–3 times, level and puddle.\n"
              "2. **Nursery:** Sow pre-germinated seeds in nursery beds (20–25 days before transplanting).\n"
              "3. **Transplanting:** Transplant 20–25 day old seedlings.\n"
              "4. **Spacing:** 20×15 cm (conventional) or 25×25 cm (SRI method for higher yield).\n"
              "5. **Water Management:** Maintain 2–5 cm standing water; use AWD (alternate wetting & drying) to save 20–30% water.\n"
              "6. **Fertilizer:** Apply NPK (120:60:60 kg/ha) in 3 splits — basal, tillering, and panicle initiation.\n"
              "7. **Weeding:** First weeding at 20 days, second at 40 days after transplanting.\n"
              "8. **Harvest:** When 80% grains turn golden (120–150 days). Don't delay — over-ripening causes grain shattering.",
        'hi': "**🌾 धान (चावल) उगाने की गाइड**\n\n"
              "**मिट्टी:** अच्छी जल धारण क्षमता वाली चिकनी या दोमट मिट्टी।\n"
              "**जलवायु:** गर्म और नम, 20–37°C, वर्षा 100–200 सेमी।\n"
              "**मौसम:** खरीफ (जून–नवं, मुख्य फसल), रबी/बोरो (नवं–मई पूर्वी/दक्षिण भारत), ग्रीष्म (जनवरी–मई सिंचित क्षेत्रों में)।\n\n"
              "**चरण:**\n"
              "1. **भूमि तैयारी:** खेत को 2–3 बार जोतें, समतल करें।\n"
              "2. **नर्सरी:** अंकुरित बीजों को नर्सरी में बोएं (रोपाई से 20–25 दिन पहले)।\n"
              "3. **रोपाई:** 20–25 दिन पुरानी पौध की रोपाई करें।\n"
              "4. **दूरी:** 20×15 सेमी (पारंपरिक) या 25×25 सेमी (SRI विधि से अधिक उपज)।\n"
              "5. **जल प्रबंधन:** 2–5 सेमी पानी खड़ा रखें; AWD (वैकल्पिक गीला-सूखा) से 20–30% पानी बचता है।\n"
              "6. **उर्वरक:** NPK (120:60:60 किग्रा/हेक्टेयर) 3 बार में दें — आधार, कल्ले और बाली अवस्था।\n"
              "7. **निराई:** पहली 20 दिन पर, दूसरी 40 दिन पर।\n"
              "8. **कटाई:** जब 80% दाने सुनहरे हो जाएं (120–150 दिन)। देरी न करें — अधिक पकने से दाने झड़ते हैं।",
        'kn': "**🌾 ಭತ್ತ (ಅಕ್ಕಿ) ಬೆಳೆಯುವ ಮಾರ್ಗದರ್ಶಿ**\n\n"
              "**ಮಣ್ಣು:** ಉತ್ತಮ ನೀರು ಹಿಡಿದಿಟ್ಟುಕೊಳ್ಳುವ ಜೇಡಿ ಅಥವಾ ಮರಳು-ಜೇಡಿ ಮಣ್ಣು.\n"
              "**ಹವಾಮಾನ:** ಬೆಚ್ಚಗಿನ ಮತ್ತು ತೇವ, 20–37°C, ಮಳೆ 100–200 ಸೆಂ.\n"
              "**ರುತುಗಳು:** ಮುಂಗಾರು (ಜೂನ್–ನವೆಂ, ಮುಖ್ಯ ಬೆಳೆ), ಹಿಂಗಾರು/ಬೋರೋ (ನವೆಂ–ಮೇ ಪೂರ್ವ/ದಕ್ಷಿಣ ಭಾರತ), ಬೇಸಿಗೆ (ಜನವರಿ–ಮೇ ನೀರಾವರಿ ಪ್ರದೇಶಗಳಲ್ಲಿ).\n\n"
              "**ಹಂತಗಳು:**\n"
              "1. **ಭೂಮಿ ಸಿದ್ಧತೆ:** ಹೊಲವನ್ನು 2–3 ಬಾರಿ ಉಳುಮೆ ಮಾಡಿ, ಸಮತಟ್ಟು ಮಾಡಿ.\n"
              "2. **ನಾಟಿ ಮಡಿ:** ಮೊಳಕೆಯೊಡೆದ ಬೀಜಗಳನ್ನು ನಾಟಿ ಮಡಿಯಲ್ಲಿ ಬಿತ್ತಿ (ನಾಟಿಗೆ 20–25 ದಿನ ಮುಂಚೆ).\n"
              "3. **ನಾಟಿ:** 20–25 ದಿನಗಳ ಸಸಿಗಳನ್ನು ನಾಟಿ ಮಾಡಿ.\n"
              "4. **ಅಂತರ:** 20×15 ಸೆಂ (ಪಾರಂಪರಿಕ) ಅಥವಾ 25×25 ಸೆಂ (SRI ವಿಧಾನ ಹೆಚ್ಚಿನ ಇಳುವರಿಗೆ).\n"
              "5. **ನೀರಾವರಿ:** 2–5 ಸೆಂ ನಿಂತ ನೀರು ಇರಿಸಿ; AWD (ಪರ್ಯಾಯ ಒದ್ದೆ-ಒಣಗಿಸುವಿಕೆ) 20–30% ನೀರು ಉಳಿಸುತ್ತದೆ.\n"
              "6. **ಗೊಬ್ಬರ:** NPK (120:60:60 ಕೆಜಿ/ಹೆಕ್ಟೇರ್) 3 ಕಂತುಗಳಲ್ಲಿ — ಮೂಲ, ಎಲೆ, ತೆನೆ ಹಂತ.\n"
              "7. **ಕಳೆ ಕೀಳುವಿಕೆ:** ಮೊದಲನೆ 20 ದಿನ, ಎರಡನೆ 40 ದಿನ.\n"
              "8. **ಕೊಯ್ಲು:** 80% ಕಾಳುಗಳು ಚಿನ್ನದ ಬಣ್ಣಕ್ಕೆ ತಿರುಗಿದಾಗ (120–150 ದಿನ). ವಿಳಂಬ ಮಾಡಬೇಡಿ — ಅತಿಯಾದ ಪಕ್ವತೆ ಕಾಳು ಉದುರಿಸುತ್ತದೆ.",
    },
    'chilli': {
        'en': "**🌶️ Chilli Growing Guide**\n\n"
              "**Soil:** Well-drained loamy soil, pH 6.0–7.0.\n"
              "**Climate:** Warm, 20–30°C. Cannot tolerate frost.\n"
              "**Season:** Can be grown year-round in tropical areas.\n\n"
              "**Steps:**\n"
              "1. **Nursery:** Sow seeds in raised nursery beds.\n"
              "2. **Transplanting:** At 6–8 weeks (15–20 cm tall).\n"
              "3. **Spacing:** 60×45 cm between plants.\n"
              "4. **Irrigation:** Regular watering, avoid waterlogging.\n"
              "5. **Fertilizer:** Apply NPK (100:50:50 kg/ha) in splits.\n"
              "6. **Mulching:** Use straw or plastic mulch to retain moisture.\n"
              "7. **Harvest:** First picking at 60–70 days. Continue every 10–15 days.\n"
              "8. **Yield:** 8–10 tonnes/hectare (green chilli).",
        'hi': "**🌶️ मिर्च उगाने की गाइड**\n\n"
              "**मिट्टी:** अच्छी जल निकासी वाली दोमट मिट्टी, pH 6.0–7.0।\n"
              "**जलवायु:** गर्म, 20–30°C। पाला सहन नहीं कर सकती।\n"
              "**मौसम:** उष्णकटिबंधीय क्षेत्रों में साल भर उगाई जा सकती है।\n\n"
              "**चरण:**\n"
              "1. **नर्सरी:** ऊंची क्यारियों में बीज बोएं।\n"
              "2. **रोपाई:** 6–8 सप्ताह में (15–20 सेमी ऊंचे)।\n"
              "3. **दूरी:** पौधों के बीच 60×45 सेमी।\n"
              "4. **सिंचाई:** नियमित पानी दें, जलभराव से बचें।\n"
              "5. **उर्वरक:** NPK (100:50:50 किग्रा/हेक्टेयर) बांट कर डालें।\n"
              "6. **मल्चिंग:** नमी बनाए रखने के लिए पुआल या प्लास्टिक मल्च।\n"
              "7. **कटाई:** पहली तोड़ाई 60–70 दिन। फिर हर 10–15 दिन।\n"
              "8. **उपज:** 8–10 टन/हेक्टेयर (हरी मिर्च)।",
        'kn': "**🌶️ ಮೆಣಸಿನಕಾಯಿ ಬೆಳೆಯುವ ಮಾರ್ಗದರ್ಶಿ**\n\n"
              "**ಮಣ್ಣು:** ಉತ್ತಮ ಒಳಚರಂಡಿ ಹೊಂದಿರುವ ಮರಳು-ಜೇಡಿ ಮಣ್ಣು, pH 6.0–7.0.\n"
              "**ಹವಾಮಾನ:** ಬೆಚ್ಚಗಿನ, 20–30°C. ಹಿಮ ಸಹಿಸುವುದಿಲ್ಲ.\n"
              "**ಋತು:** ಉಷ್ಣವಲಯ ಪ್ರದೇಶಗಳಲ್ಲಿ ವರ್ಷವಿಡೀ ಬೆಳೆಯಬಹುದು.\n\n"
              "**ಹಂತಗಳು:**\n"
              "1. **ನಾಟಿ ಮಡಿ:** ಎತ್ತರದ ಮಡಿಯಲ್ಲಿ ಬೀಜ ಬಿತ್ತಿ.\n"
              "2. **ನಾಟಿ:** 6–8 ವಾರಗಳಲ್ಲಿ (15–20 ಸೆಂ ಎತ್ತರ).\n"
              "3. **ಅಂತರ:** ಗಿಡಗಳ ನಡುವೆ 60×45 ಸೆಂ.\n"
              "4. **ನೀರಾವರಿ:** ನಿಯಮಿತ ನೀರು, ನೀರು ನಿಲ್ಲದಂತೆ.\n"
              "5. **ಗೊಬ್ಬರ:** NPK (100:50:50 ಕೆಜಿ/ಹೆಕ್ಟೇರ್) ಭಾಗಗಳಲ್ಲಿ.\n"
              "6. **ಮಲ್ಚಿಂಗ್:** ತೇವಾಂಶ ಉಳಿಸಲು ಹುಲ್ಲು ಅಥವಾ ಪ್ಲಾಸ್ಟಿಕ್ ಮಲ್ಚ್.\n"
              "7. **ಕೊಯ್ಲು:** ಮೊದಲ ಕೊಯ್ಲು 60–70 ದಿನ. ನಂತರ ಪ್ರತಿ 10–15 ದಿನ.\n"
              "8. **ಇಳುವರಿ:** 8–10 ಟನ್/ಹೆಕ್ಟೇರ್ (ಹಸಿ ಮೆಣಸಿನಕಾಯಿ).",
    },
    'coffee': {
        'en': "**☕ Coffee Growing Guide**\n\n"
              "**Soil:** Deep, well-drained, slightly acidic (pH 5.5–6.5).\n"
              "**Climate:** Tropical highland, 15–28°C, rainfall 150–250 cm, shade required.\n"
              "**Varieties:** Arabica (higher altitude) and Robusta (lower altitude).\n\n"
              "**Steps:**\n"
              "1. **Nursery:** Raise seedlings in polybags for 6–8 months.\n"
              "2. **Shade Trees:** Plant silver oak or dadap as shade trees first.\n"
              "3. **Planting:** Dig pits (45×45×45 cm), plant during monsoon.\n"
              "4. **Spacing:** Arabica: 6×6 ft, Robusta: 8×8 ft.\n"
              "5. **Mulching:** Apply thick organic mulch around plants.\n"
              "6. **Fertilizer:** NPK (40:30:40 kg/ha) for young plants.\n"
              "7. **Pruning:** Regular pruning to maintain shape.\n"
              "8. **Harvest:** Hand-pick ripe red cherries (Nov–Feb). First yield in 3–4 years.",
        'hi': "**☕ कॉफी उगाने की गाइड**\n\n"
              "**मिट्टी:** गहरी, अच्छी जल निकासी, हल्की अम्लीय (pH 5.5–6.5)।\n"
              "**जलवायु:** उष्णकटिबंधीय पर्वतीय, 15–28°C, वर्षा 150–250 सेमी, छाया आवश्यक।\n"
              "**किस्में:** अरेबिका (ऊंचाई पर) और रोबस्टा (नीचे)।\n\n"
              "**चरण:**\n"
              "1. **नर्सरी:** 6–8 महीने पॉलीबैग में पौध तैयार करें।\n"
              "2. **छाया पेड़:** पहले सिल्वर ओक या ददाप लगाएं।\n"
              "3. **रोपण:** गड्ढे (45×45×45 सेमी) खोदें, मानसून में लगाएं।\n"
              "4. **दूरी:** अरेबिका: 6×6 फीट, रोबस्टा: 8×8 फीट।\n"
              "5. **मल्चिंग:** पौधों के चारों ओर घनी जैविक मल्च।\n"
              "6. **उर्वरक:** NPK (40:30:40 किग्रा/हेक्टेयर) नए पौधों के लिए।\n"
              "7. **कटाई-छंटाई:** आकार बनाए रखने के लिए नियमित छंटाई।\n"
              "8. **फल तोड़ाई:** पके लाल बेरी हाथ से तोड़ें (नवंबर–फरवरी)। पहली उपज 3–4 साल में।",
        'kn': "**☕ ಕಾಫಿ ಬೆಳೆಯುವ ಮಾರ್ಗದರ್ಶಿ**\n\n"
              "**ಮಣ್ಣು:** ಆಳವಾದ, ಉತ್ತಮ ಒಳಚರಂಡಿ, ಸ್ವಲ್ಪ ಆಮ್ಲೀಯ (pH 5.5–6.5).\n"
              "**ಹವಾಮಾನ:** ಉಷ್ಣವಲಯ ಎತ್ತರ, 15–28°C, ಮಳೆ 150–250 ಸೆಂ, ನೆರಳು ಅಗತ್ಯ.\n"
              "**ತಳಿಗಳು:** ಅರೇಬಿಕಾ (ಹೆಚ್ಚಿನ ಎತ್ತರ) ಮತ್ತು ರೊಬಸ್ಟಾ (ಕಡಿಮೆ ಎತ್ತರ).\n\n"
              "**ಹಂತಗಳು:**\n"
              "1. **ನಾಟಿ ಮಡಿ:** 6–8 ತಿಂಗಳು ಪಾಲಿಬ್ಯಾಗ್‌ನಲ್ಲಿ ಸಸಿ ಬೆಳೆಸಿ.\n"
              "2. **ನೆರಳು ಮರಗಳು:** ಮೊದಲು ಸಿಲ್ವರ್ ಓಕ್ ಅಥವಾ ದಡಪ್ ನೆಡಿ.\n"
              "3. **ನಾಟಿ:** ಗುಂಡಿ (45×45×45 ಸೆಂ) ತೆಗೆದು, ಮಳೆಗಾಲದಲ್ಲಿ ನೆಡಿ.\n"
              "4. **ಅಂತರ:** ಅರೇಬಿಕಾ: 6×6 ಅಡಿ, ರೊಬಸ್ಟಾ: 8×8 ಅಡಿ.\n"
              "5. **ಮಲ್ಚಿಂಗ್:** ಗಿಡಗಳ ಸುತ್ತ ದಪ್ಪ ಸಾವಯವ ಮಲ್ಚ್ ಹಾಕಿ.\n"
              "6. **ಗೊಬ್ಬರ:** NPK (40:30:40 ಕೆಜಿ/ಹೆಕ್ಟೇರ್) ಎಳೆ ಗಿಡಗಳಿಗೆ.\n"
              "7. **ಕತ್ತರಿಸುವಿಕೆ:** ಆಕಾರ ಕಾಯ್ದುಕೊಳ್ಳಲು ನಿಯಮಿತ ಕತ್ತರಿಸುವಿಕೆ.\n"
              "8. **ಕೊಯ್ಲು:** ಹಣ್ಣಾದ ಕೆಂಪು ಹಣ್ಣನ್ನು ಕೈಯಿಂದ ಕೊಯ್ಯಿರಿ (ನವೆಂ–ಫೆಬ್ರ). ಮೊದಲ ಇಳುವರಿ 3–4 ವರ್ಷದಲ್ಲಿ.",
    },
}

# Tips content (multilingual)
CROP_TIPS = {
    'paddy': {
        'en': "**💡 Paddy Growing Tips & Best Practices**\n\n"
              "✅ **Seed Treatment:** Soak seeds in Carbendazim solution before sowing.\n"
              "✅ **Water Management:** Alternate wetting and drying (AWD) saves 20–30% water.\n"
              "✅ **Spacing:** Use SRI method (25×25 cm) for higher yields.\n"
              "✅ **Weed Control:** Apply herbicides within 3 days of transplanting.\n"
              "✅ **Fertilizer Timing:** Apply nitrogen in 3 splits (basal, tillering, panicle).\n"
              "✅ **Pest Watch:** Monitor for stem borers during vegetative stage.\n"
              "✅ **Disease Alert:** Watch for blast disease during humid weather.\n"
              "✅ **Harvest Timing:** Don't delay harvest; over-ripening causes grain shattering.",
        'hi': "**💡 धान उगाने के सुझाव और सर्वोत्तम तरीके**\n\n"
              "✅ **बीज उपचार:** बुवाई से पहले बीजों को कार्बेन्डाजिम घोल में भिगोएं।\n"
              "✅ **जल प्रबंधन:** वैकल्पिक गीला-सूखा (AWD) 20–30% पानी बचाता है।\n"
              "✅ **दूरी:** अधिक उपज के लिए SRI विधि (25×25 सेमी) अपनाएं।\n"
              "✅ **खरपतवार नियंत्रण:** रोपाई के 3 दिन के भीतर शाकनाशी डालें।\n"
              "✅ **उर्वरक समय:** नाइट्रोजन 3 बार में दें (आधार, कल्ले, बाली)।\n"
              "✅ **कीट निगरानी:** वानस्पतिक अवस्था में तना छेदक की निगरानी करें।\n"
              "✅ **रोग चेतावनी:** नम मौसम में ब्लास्ट रोग की सतर्कता रखें।\n"
              "✅ **कटाई समय:** कटाई में देरी न करें; अधिक पकने से दाने झड़ते हैं।",
        'kn': "**💡 ಭತ್ತ ಬೆಳೆಯುವ ಸಲಹೆ ಮತ್ತು ಉತ್ತಮ ಅಭ್ಯಾಸಗಳು**\n\n"
              "✅ **ಬೀಜ ಸಂಸ್ಕರಣೆ:** ಬಿತ್ತುವ ಮೊದಲು ಬೀಜಗಳನ್ನು ಕಾರ್ಬೆಂಡಜಿಮ್ ದ್ರಾವಣದಲ್ಲಿ ನೆನೆಸಿ.\n"
              "✅ **ನೀರಾವರಿ:** ಪರ್ಯಾಯ ಒದ್ದೆ-ಒಣಗಿಸುವಿಕೆ (AWD) 20–30% ನೀರು ಉಳಿಸುತ್ತದೆ.\n"
              "✅ **ಅಂತರ:** ಹೆಚ್ಚಿನ ಇಳುವರಿಗೆ SRI ವಿಧಾನ (25×25 ಸೆಂ) ಬಳಸಿ.\n"
              "✅ **ಕಳೆ ನಿಯಂತ್ರಣ:** ನಾಟಿಯ 3 ದಿನಗಳಲ್ಲಿ ಕಳೆನಾಶಕ ಸಿಂಪಡಿಸಿ.\n"
              "✅ **ಗೊಬ್ಬರ ಸಮಯ:** ಸಾರಜನಕ 3 ಕಂತುಗಳಲ್ಲಿ (ಮೂಲ, ಎಲೆ, ತೆನೆ).\n"
              "✅ **ಕೀಟ ಎಚ್ಚರಿಕೆ:** ಸಸ್ಯಕ ಹಂತದಲ್ಲಿ ಕಾಂಡ ಕೊರಕಕ್ಕೆ ಗಮನಿಸಿ.\n"
              "✅ **ರೋಗ ಎಚ್ಚರಿಕೆ:** ತೇವ ಹವಾಮಾನದಲ್ಲಿ ಬ್ಲಾಸ್ಟ್ ರೋಗದ ಬಗ್ಗೆ ಎಚ್ಚರ.\n"
              "✅ **ಕೊಯ್ಲು ಸಮಯ:** ಕೊಯ್ಲು ವಿಳಂಬ ಮಾಡಬೇಡಿ; ಅತಿಯಾದ ಪಕ್ವತೆ ಕಾಳು ಉದುರಿಸುತ್ತದೆ.",
    },
    'chilli': {
        'en': "**💡 Chilli Growing Tips & Best Practices**\n\n"
              "✅ **Seed Selection:** Use certified hybrid seeds for better yield.\n"
              "✅ **Hardening:** Harden seedlings before transplanting.\n"
              "✅ **Staking:** Support tall varieties with stakes.\n"
              "✅ **Pinching:** Pinch first flower to promote branching.\n"
              "✅ **Pest Watch:** Regularly check for thrips and aphids.\n"
              "✅ **Fungal Prevention:** Avoid overhead irrigation; use drip irrigation.\n"
              "✅ **Neem Spray:** Apply neem oil spray every 15 days as preventive measure.\n"
              "✅ **Drying:** For dry chilli, harvest when fully red and sun-dry for 8–10 days.",
        'hi': "**💡 मिर्च उगाने के सुझाव और सर्वोत्तम तरीके**\n\n"
              "✅ **बीज चयन:** बेहतर उपज के लिए प्रमाणित संकर बीज उपयोग करें।\n"
              "✅ **कड़ाई:** रोपाई से पहले पौधों को कठोर बनाएं।\n"
              "✅ **सहारा:** लंबी किस्मों को डंडों से सहारा दें।\n"
              "✅ **चुटकी:** शाखाओं को बढ़ावा देने के लिए पहला फूल तोड़ दें।\n"
              "✅ **कीट निगरानी:** थ्रिप्स और एफिड्स की नियमित जांच करें।\n"
              "✅ **फफूंद रोकथाम:** ऊपर से सिंचाई से बचें; ड्रिप सिंचाई करें।\n"
              "✅ **नीम स्प्रे:** हर 15 दिन नीम तेल का छिड़काव करें।\n"
              "✅ **सुखाना:** सूखी मिर्च के लिए पूरी लाल होने पर तोड़ें, 8–10 दिन धूप में सुखाएं।",
        'kn': "**💡 ಮೆಣಸಿನಕಾಯಿ ಬೆಳೆಯುವ ಸಲಹೆ ಮತ್ತು ಉತ್ತಮ ಅಭ್ಯಾಸಗಳು**\n\n"
              "✅ **ಬೀಜ ಆಯ್ಕೆ:** ಉತ್ತಮ ಇಳುವರಿಗೆ ಪ್ರಮಾಣಿತ ಸಂಕರ ಬೀಜ ಬಳಸಿ.\n"
              "✅ **ಗಟ್ಟಿಗೊಳಿಸುವಿಕೆ:** ನಾಟಿ ಮೊದಲು ಸಸಿಗಳನ್ನು ಗಟ್ಟಿಮಾಡಿ.\n"
              "✅ **ಆಧಾರ:** ಎತ್ತರದ ತಳಿಗಳಿಗೆ ಕೋಲಿನ ಆಧಾರ ಕೊಡಿ.\n"
              "✅ **ಚಿಮ್ಮುವಿಕೆ:** ಕೊಂಬೆಗಳ ಬೆಳವಣಿಗೆಗೆ ಮೊದಲ ಹೂವನ್ನು ತೆಗೆಯಿರಿ.\n"
              "✅ **ಕೀಟ ಗಮನ:** ಥ್ರಿಪ್ಸ್ ಮತ್ತು ಹೇನುಗಳ ನಿಯಮಿತ ಪರೀಕ್ಷೆ.\n"
              "✅ **ಶಿಲೀಂಧ್ರ ತಡೆ:** ಮೇಲಿನ ಸಿಂಪರಣೆ ಬಿಡಿ; ಹನಿ ನೀರಾವರಿ ಬಳಸಿ.\n"
              "✅ **ಬೇವಿನ ಸಿಂಪಡಣೆ:** ಪ್ರತಿ 15 ದಿನಕ್ಕೆ ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ.\n"
              "✅ **ಒಣಗಿಸುವಿಕೆ:** ಒಣ ಮೆಣಸಿಗೆ ಪೂರ್ಣ ಕೆಂಪಾದಾಗ ಕೊಯ್ದು 8–10 ದಿನ ಬಿಸಿಲಿನಲ್ಲಿ ಒಣಗಿಸಿ.",
    },
    'coffee': {
        'en': "**💡 Coffee Growing Tips & Best Practices**\n\n"
              "✅ **Shade Management:** Maintain 40–50% shade for optimal growth.\n"
              "✅ **Organic Matter:** Add compost and coffee pulp to soil annually.\n"
              "✅ **Drainage:** Ensure good drainage; coffee hates waterlogged soil.\n"
              "✅ **Selective Picking:** Pick only ripe red cherries for quality.\n"
              "✅ **Pest Watch:** Watch for white stem borer and berry borer.\n"
              "✅ **Fungal Prevention:** Spray Bordeaux mixture before monsoon.\n"
              "✅ **Pruning:** Prune after harvest to maintain canopy shape.\n"
              "✅ **Soil Testing:** Test soil pH annually; coffee needs acidic soil.",
        'hi': "**💡 कॉफी उगाने के सुझाव और सर्वोत्तम तरीके**\n\n"
              "✅ **छाया प्रबंधन:** इष्टतम विकास के लिए 40–50% छाया बनाए रखें।\n"
              "✅ **जैविक पदार्थ:** सालाना मिट्टी में खाद और कॉफी गूदा मिलाएं।\n"
              "✅ **जल निकासी:** अच्छी जल निकासी सुनिश्चित करें; कॉफी जलभराव सहन नहीं करती।\n"
              "✅ **चयनात्मक तोड़ाई:** गुणवत्ता के लिए केवल पके लाल बेरी तोड़ें।\n"
              "✅ **कीट निगरानी:** सफेद तना छेदक और बेरी छेदक की सतर्कता।\n"
              "✅ **फफूंद रोकथाम:** मानसून से पहले बोर्डो मिश्रण का छिड़काव।\n"
              "✅ **छंटाई:** फसल कटाई के बाद छत्र आकार के लिए छंटाई करें।\n"
              "✅ **मिट्टी परीक्षण:** सालाना pH जांच करें; कॉफी को अम्लीय मिट्टी चाहिए।",
        'kn': "**💡 ಕಾಫಿ ಬೆಳೆಯುವ ಸಲಹೆ ಮತ್ತು ಉತ್ತಮ ಅಭ್ಯಾಸಗಳು**\n\n"
              "✅ **ನೆರಳು ನಿರ್ವಹಣೆ:** ಉತ್ತಮ ಬೆಳವಣಿಗೆಗೆ 40–50% ನೆರಳು ಇರಿಸಿ.\n"
              "✅ **ಸಾವಯವ ಪದಾರ್ಥ:** ವಾರ್ಷಿಕವಾಗಿ ಕಾಂಪೋಸ್ಟ್ ಮತ್ತು ಕಾಫಿ ತಿರುಳು ಸೇರಿಸಿ.\n"
              "✅ **ಒಳಚರಂಡಿ:** ಉತ್ತಮ ಒಳಚರಂಡಿ ಖಚಿತಪಡಿಸಿ; ಕಾಫಿ ನೀರು ನಿಲ್ಲುವ ಮಣ್ಣನ್ನು ಸಹಿಸುವುದಿಲ್ಲ.\n"
              "✅ **ಆಯ್ದ ಕೊಯ್ಲು:** ಗುಣಮಟ್ಟಕ್ಕೆ ಕೇವಲ ಪಕ್ವ ಕೆಂಪು ಹಣ್ಣುಗಳನ್ನು ಕೊಯ್ಯಿ.\n"
              "✅ **ಕೀಟ ಗಮನ:** ಬಿಳಿ ಕಾಂಡ ಕೊರಕ ಮತ್ತು ಹಣ್ಣಿನ ಕೊರಕಕ್ಕೆ ಗಮನಿಸಿ.\n"
              "✅ **ಶಿಲೀಂಧ್ರ ತಡೆ:** ಮಳೆಗಾಲದ ಮೊದಲು ಬೋರ್ಡೋ ಮಿಶ್ರಣ ಸಿಂಪಡಿಸಿ.\n"
              "✅ **ಕತ್ತರಿಸುವಿಕೆ:** ಕೊಯ್ಲಿನ ನಂತರ ಮೇಲ್ಛಾವಣಿ ಆಕಾರಕ್ಕೆ ಕತ್ತರಿಸಿ.\n"
              "✅ **ಮಣ್ಣು ಪರೀಕ್ಷೆ:** ವಾರ್ಷಿಕವಾಗಿ pH ಪರೀಕ್ಷಿಸಿ; ಕಾಫಿಗೆ ಆಮ್ಲೀಯ ಮಣ್ಣು ಬೇಕು.",
    },
}


def _detect_intent(message):
    """Detect user intent from message."""
    msg_lower = message.lower()
    intents = []
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in msg_lower:
                intents.append(intent)
                break
    return intents


def _detect_crop(message):
    """Detect which crop the user is asking about."""
    msg_lower = message.lower()
    for alias, crop in CROP_ALIASES.items():
        if alias in msg_lower:
            return crop
    return None


def _detect_disease_name(message):
    """Detect specific disease names mentioned in the message."""
    msg_lower = message.lower()
    diseases = Disease.query.all()
    for d in diseases:
        if d.name.lower() in msg_lower:
            return d
        # Check partial matches
        name_parts = d.name.lower().split()
        for part in name_parts:
            if len(part) > 3 and part in msg_lower:
                return d
    return None


def _detect_pest_name(message):
    """Detect specific pest names mentioned in the message."""
    msg_lower = message.lower()
    pests = Pest.query.all()
    for p in pests:
        if p.name.lower() in msg_lower:
            return p
        name_parts = p.name.lower().split()
        for part in name_parts:
            if len(part) > 3 and part in msg_lower:
                return p
    return None


def _format_disease_info(disease, lang='en'):
    """Format a disease into a readable response."""
    labels = {
        'en': {'crop': 'Crop', 'severity': 'Severity', 'symptoms': 'Symptoms', 'cause': 'Cause',
               'prevention': 'Prevention', 'organic': 'Organic Treatment', 'chemical': 'Chemical Treatment',
               'composition': 'Chemical Composition'},
        'hi': {'crop': 'फसल', 'severity': 'गंभीरता', 'symptoms': 'लक्षण', 'cause': 'कारण',
               'prevention': 'रोकथाम', 'organic': 'जैविक उपचार', 'chemical': 'रासायनिक उपचार',
               'composition': 'रासायनिक संरचना'},
        'kn': {'crop': 'ಬೆಳೆ', 'severity': 'ತೀವ್ರತೆ', 'symptoms': 'ಲಕ್ಷಣಗಳು', 'cause': 'ಕಾರಣ',
               'prevention': 'ತಡೆಗಟ್ಟುವಿಕೆ', 'organic': 'ಸಾವಯವ ಚಿಕಿತ್ಸೆ', 'chemical': 'ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ',
               'composition': 'ರಾಸಾಯನಿಕ ಸಂಯೋಜನೆ'},
    }
    l = labels.get(lang, labels['en'])
    lines = [f"**{disease.get_name(lang)}** ({l['crop']}: {disease.crop.get_name(lang)})"]
    lines.append(f"• {l['severity']}: {disease.severity}")
    lines.append(f"• {l['symptoms']}: {disease._l('symptoms', lang)}")
    lines.append(f"• {l['cause']}: {disease._l('cause', lang)}")
    lines.append(f"• {l['prevention']}: {disease._l('prevention', lang)}")
    lines.append(f"• {l['organic']}: {disease._l('organic_treatment', lang)}")
    lines.append(f"• {l['chemical']}: {disease._l('chemical_treatment', lang)}")
    lines.append(f"• {l['composition']}: {disease._l('chemical_composition', lang)}")
    return '\n'.join(lines)


def _format_pest_info(pest, lang='en'):
    """Format a pest into a readable response."""
    labels = {
        'en': {'crop': 'Crop', 'severity': 'Severity', 'symptoms': 'Symptoms', 'damage': 'Damage',
               'season': 'Active Season', 'prevention': 'Prevention', 'organic': 'Organic Treatment',
               'chemical': 'Chemical Treatment'},
        'hi': {'crop': 'फसल', 'severity': 'गंभीरता', 'symptoms': 'लक्षण', 'damage': 'क्षति',
               'season': 'सक्रिय मौसम', 'prevention': 'रोकथाम', 'organic': 'जैविक उपचार',
               'chemical': 'रासायनिक उपचार'},
        'kn': {'crop': 'ಬೆಳೆ', 'severity': 'ತೀವ್ರತೆ', 'symptoms': 'ಲಕ್ಷಣಗಳು', 'damage': 'ಹಾನಿ',
               'season': 'ಸಕ್ರಿಯ ಋತು', 'prevention': 'ತಡೆಗಟ್ಟುವಿಕೆ', 'organic': 'ಸಾವಯವ ಚಿಕಿತ್ಸೆ',
               'chemical': 'ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ'},
    }
    l = labels.get(lang, labels['en'])
    lines = [f"**{pest.get_name(lang)}** ({pest.scientific_name}) — {l['crop']}: {pest.crop.get_name(lang)}"]
    lines.append(f"• {l['severity']}: {pest.severity}")
    lines.append(f"• {l['symptoms']}: {pest._l('symptoms', lang)}")
    lines.append(f"• {l['damage']}: {pest._l('damage_type', lang)}")
    lines.append(f"• {l['season']}: {pest._l('active_season', lang)}")
    lines.append(f"• {l['prevention']}: {pest._l('prevention', lang)}")
    lines.append(f"• {l['organic']}: {pest._l('organic_treatment', lang)}")
    lines.append(f"• {l['chemical']}: {pest._l('chemical_treatment', lang)}")
    return '\n'.join(lines)


def _make_crop_menu(crop_name, crop_key, lang, resp_templates):
    """Generate crop menu response with buttons."""
    text = resp_templates['crop_menu'].format(crop=crop_name)
    buttons = []
    for btn in resp_templates['crop_menu_buttons']:
        buttons.append({
            'label': btn['label'],
            'value': btn['value'].replace('{crop_key}', crop_key)
        })
    return {'reply': text, 'type': 'crop_menu', 'buttons': buttons}


def get_chatbot_response(message, lang='en'):
    """
    Generate a chatbot response based on the user's message.
    Supports guided conversation with quick-reply buttons.
    """
    if lang not in RESPONSES:
        lang = 'en'
    resp_templates = RESPONSES[lang]

    intents = _detect_intent(message)
    crop_key = _detect_crop(message)

    # Check for specific disease or pest
    specific_disease = _detect_disease_name(message)
    specific_pest = _detect_pest_name(message)

    # --- Specific disease info ---
    if specific_disease:
        info = _format_disease_info(specific_disease, lang)
        return {'reply': info, 'type': 'disease_info'}

    # --- Specific pest info ---
    if specific_pest:
        info = _format_pest_info(specific_pest, lang)
        return {'reply': info, 'type': 'pest_info'}

    # --- Greeting ---
    if 'greeting' in intents and len(intents) == 1:
        return {
            'reply': resp_templates['greeting'],
            'type': 'greeting',
            'buttons': resp_templates['greeting_buttons']
        }

    # --- List all crops ---
    if 'list_crops' in intents and not crop_key:
        crops = Crop.query.all()
        text = resp_templates['crop_list']
        for c in crops:
            text += f"🌱 **{c.get_name(lang)}** ({c.scientific_name})\n"
            text += f"   {c.season}\n"
            text += f"   {len(c.diseases)} | {len(c.pests)}\n\n"
        return {
            'reply': text,
            'type': 'crop_list',
            'buttons': resp_templates['greeting_buttons']
        }

    # --- Crop-specific queries ---
    if crop_key:
        crop = Crop.query.filter(Crop.name.ilike(f'%{crop_key}%')).first()
        if not crop:
            return {
                'reply': resp_templates['not_understood'],
                'type': 'error',
                'buttons': resp_templates.get('not_understood_buttons', [])
            }

        # Growing guide
        if 'growing_guide' in intents:
            guide = GROWING_GUIDES.get(crop_key, {}).get(lang, GROWING_GUIDES.get(crop_key, {}).get('en', ''))
            if guide:
                return {'reply': guide, 'type': 'growing_guide'}

        # Tips
        if 'tips' in intents:
            tips = CROP_TIPS.get(crop_key, {}).get(lang, CROP_TIPS.get(crop_key, {}).get('en', ''))
            if tips:
                return {'reply': tips, 'type': 'tips'}

        # Diseases for this crop
        if 'list_diseases' in intents or 'symptom' in intents:
            text = resp_templates['disease_list'].format(crop=crop.get_name(lang))
            for d in crop.diseases:
                text += f"🦠 **{d.get_name(lang)}** [{d.severity}]\n"
                text += f"   {d._l('symptoms', lang)[:120]}...\n\n"
            return {'reply': text, 'type': 'disease_list'}

        # Pests for this crop
        if 'list_pests' in intents:
            text = resp_templates['pest_list'].format(crop=crop.get_name(lang))
            for p in crop.pests:
                text += f"🐛 **{p.get_name(lang)}** ({p.scientific_name}) [{p.severity}]\n"
                text += f"   {p._l('symptoms', lang)[:120]}...\n\n"
            return {'reply': text, 'type': 'pest_list'}

        # Treatment for this crop
        if 'treatment' in intents:
            l_labels = {'en': {'title': 'Treatments for', 'organic': 'Organic', 'chemical': 'Chemical'},
                        'hi': {'title': 'उपचार', 'organic': 'जैविक', 'chemical': 'रासायनिक'},
                        'kn': {'title': 'ಚಿಕಿತ್ಸೆಗಳು', 'organic': 'ಸಾವಯವ', 'chemical': 'ರಾಸಾಯನಿಕ'}}
            ll = l_labels.get(lang, l_labels['en'])
            text = f"**{ll['title']} {crop.get_name(lang)}:**\n\n"
            for d in crop.diseases:
                text += f"🦠 **{d.get_name(lang)}:**\n"
                text += f"   🌿 {ll['organic']}: {d._l('organic_treatment', lang)}\n"
                text += f"   🧪 {ll['chemical']}: {d._l('chemical_treatment', lang)}\n\n"
            return {'reply': text, 'type': 'treatment'}

        # Prevention for this crop
        if 'prevention' in intents:
            l_labels = {'en': 'Prevention methods for', 'hi': 'रोकथाम के तरीके', 'kn': 'ತಡೆಗಟ್ಟುವ ವಿಧಾನಗಳು'}
            text = f"**{l_labels.get(lang, l_labels['en'])} {crop.get_name(lang)}:**\n\n"
            for d in crop.diseases:
                text += f"🛡️ **{d.get_name(lang)}:** {d._l('prevention', lang)}\n\n"
            for p in crop.pests:
                text += f"🛡️ **{p.get_name(lang)}:** {p._l('prevention', lang)}\n\n"
            return {'reply': text, 'type': 'prevention'}

        # Season info
        if 'season' in intents:
            text = f"**{crop.get_name(lang)}**\n"
            text += f"{crop.season}\n\n"
            active_pests = [p for p in crop.pests if p.active_season]
            if active_pests:
                for p in active_pests:
                    text += f"🐛 {p.get_name(lang)}: {p._l('active_season', lang)}\n"
            return {'reply': text, 'type': 'season'}

        # General crop info → show crop menu with buttons
        return _make_crop_menu(crop.get_name(lang), crop_key, lang, resp_templates)

    # --- All diseases (no crop specified) ---
    if 'list_diseases' in intents:
        diseases = Disease.query.all()
        text = resp_templates['all_diseases']
        for d in diseases:
            text += f"🦠 **{d.get_name(lang)}** ({d.crop.get_name(lang)}) [{d.severity}]\n"
        return {'reply': text, 'type': 'disease_list'}

    # --- All pests (no crop specified) ---
    if 'list_pests' in intents:
        pests = Pest.query.all()
        text = resp_templates['all_pests']
        for p in pests:
            text += f"🐛 **{p.get_name(lang)}** ({p.crop.get_name(lang)}) [{p.severity}]\n"
        return {'reply': text, 'type': 'pest_list'}

    # --- Growing guide (no crop specified) ---
    if 'growing_guide' in intents or 'tips' in intents:
        l_labels = {'en': 'Which crop do you want to know about?',
                    'hi': 'आप किस फसल के बारे में जानना चाहते हैं?',
                    'kn': 'ನೀವು ಯಾವ ಬೆಳೆ ಬಗ್ಗೆ ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ?'}
        return {
            'reply': l_labels.get(lang, l_labels['en']),
            'type': 'ask_crop',
            'buttons': resp_templates['greeting_buttons']
        }

    # --- Symptom-based search ---
    if 'symptom' in intents or 'treatment' in intents or 'prevention' in intents:
        msg_lower = message.lower()
        matching = []
        for d in Disease.query.all():
            if any(word in d.symptoms.lower() for word in msg_lower.split() if len(word) > 3):
                matching.append(d)
        for p in Pest.query.all():
            if any(word in p.symptoms.lower() for word in msg_lower.split() if len(word) > 3):
                matching.append(p)

        if matching:
            l_labels = {'en': 'Based on your description, here are possible matches:',
                        'hi': 'आपके विवरण के आधार पर, ये संभावित मिलान हैं:',
                        'kn': 'ನಿಮ್ಮ ವಿವರಣೆ ಆಧಾರದ ಮೇಲೆ, ಸಂಭಾವ್ಯ ಹೊಂದಾಣಿಕೆಗಳು:'}
            text = f"{l_labels.get(lang, l_labels['en'])}\n\n"
            for item in matching[:5]:
                if isinstance(item, Disease):
                    text += f"🦠 **{item.get_name(lang)}** ({item.crop.get_name(lang)})\n"
                    text += f"   {item._l('symptoms', lang)[:150]}...\n\n"
                else:
                    text += f"🐛 **{item.get_name(lang)}** ({item.crop.get_name(lang)})\n"
                    text += f"   {item._l('symptoms', lang)[:150]}...\n\n"
            return {'reply': text, 'type': 'search_results'}

    # --- Default ---
    return {
        'reply': resp_templates['not_understood'],
        'type': 'help',
        'buttons': resp_templates.get('not_understood_buttons', [])
    }
