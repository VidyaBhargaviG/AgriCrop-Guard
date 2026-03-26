"""
Crop Advisory System - Main Flask Application
"""

import os
import secrets
from flask import Flask, jsonify, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from backend.models import db, Crop, Disease, Pest
from backend.seed_data import seed_database
from backend.chatbot import get_chatbot_response

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'backend', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='frontend'
)

app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'crop_advisory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

db.init_app(app)

with app.app_context():
    db.create_all()
    seed_database(db, Crop, Disease, Pest)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== PAGE ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/crop/<int:crop_id>')
def crop_detail_page(crop_id):
    return render_template('crop_detail.html')


@app.route('/disease/<int:disease_id>')
def disease_detail_page(disease_id):
    return render_template('disease_detail.html')


@app.route('/pest/<int:pest_id>')
def pest_detail_page(pest_id):
    return render_template('pest_detail.html')


@app.route('/search')
def search_page():
    return render_template('search.html')


@app.route('/detect')
def detect_page():
    return render_template('detect.html')


# ==================== API ROUTES ====================

@app.route('/api/crops', methods=['GET'])
def get_crops():
    """Get all crops (summary)."""
    lang = request.args.get('lang', 'en')
    crops = Crop.query.all()
    return jsonify([c.to_summary(lang) for c in crops])


@app.route('/api/crops/<int:crop_id>', methods=['GET'])
def get_crop(crop_id):
    """Get a single crop with all diseases and pests."""
    lang = request.args.get('lang', 'en')
    crop = db.session.get(Crop, crop_id)
    if not crop:
        return jsonify({'error': 'Crop not found'}), 404
    return jsonify(crop.to_dict(lang))


@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get all diseases."""
    lang = request.args.get('lang', 'en')
    diseases = Disease.query.all()
    return jsonify([d.to_dict(lang) for d in diseases])


@app.route('/api/diseases/<int:disease_id>', methods=['GET'])
def get_disease(disease_id):
    """Get a single disease."""
    lang = request.args.get('lang', 'en')
    disease = db.session.get(Disease, disease_id)
    if not disease:
        return jsonify({'error': 'Disease not found'}), 404
    return jsonify(disease.to_dict(lang))


@app.route('/api/pests', methods=['GET'])
def get_pests():
    """Get all pests."""
    lang = request.args.get('lang', 'en')
    pests = Pest.query.all()
    return jsonify([p.to_dict(lang) for p in pests])


@app.route('/api/pests/<int:pest_id>', methods=['GET'])
def get_pest(pest_id):
    """Get a single pest."""
    lang = request.args.get('lang', 'en')
    pest = db.session.get(Pest, pest_id)
    if not pest:
        return jsonify({'error': 'Pest not found'}), 404
    return jsonify(pest.to_dict(lang))


@app.route('/api/search', methods=['GET'])
def search():
    """Search crops, diseases, and pests by keyword."""
    query = request.args.get('q', '').strip()
    lang = request.args.get('lang', 'en')
    if not query or len(query) < 2:
        return jsonify({'crops': [], 'diseases': [], 'pests': []})

    # Use parameterized queries (safe from SQL injection)
    search_term = f'%{query}%'

    crops = Crop.query.filter(
        db.or_(
            Crop.name.ilike(search_term),
            Crop.name_hi.ilike(search_term),
            Crop.name_kn.ilike(search_term),
            Crop.scientific_name.ilike(search_term),
            Crop.description.ilike(search_term)
        )
    ).all()

    diseases = Disease.query.filter(
        db.or_(
            Disease.name.ilike(search_term),
            Disease.name_hi.ilike(search_term),
            Disease.name_kn.ilike(search_term),
            Disease.symptoms.ilike(search_term),
            Disease.cause.ilike(search_term),
            Disease.prevention.ilike(search_term)
        )
    ).all()

    pests = Pest.query.filter(
        db.or_(
            Pest.name.ilike(search_term),
            Pest.name_hi.ilike(search_term),
            Pest.name_kn.ilike(search_term),
            Pest.symptoms.ilike(search_term),
            Pest.scientific_name.ilike(search_term),
            Pest.damage_type.ilike(search_term)
        )
    ).all()

    return jsonify({
        'crops': [c.to_summary(lang) for c in crops],
        'diseases': [d.to_dict(lang) for d in diseases],
        'pests': [p.to_dict(lang) for p in pests]
    })


@app.route('/api/detect', methods=['POST'])
def detect_disease():
    """Upload an image for AI-based disease detection."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add random prefix to prevent filename collisions
        safe_name = f"{secrets.token_hex(8)}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        # Run AI detection
        from backend.ai_model.detector import predict_disease
        selected_crop = request.form.get('crop', '').strip()
        selected_lang = request.form.get('lang', 'en').strip()
        if selected_lang not in ('en', 'hi', 'kn'):
            selected_lang = 'en'
        result = predict_disease(filepath, crop_filter=selected_crop if selected_crop else None, lang=selected_lang)

        return jsonify(result)

    return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, webp'}), 400


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ==================== MULTILINGUAL SUPPORT ====================

TRANSLATIONS = {
    'en': {
        'app_title': 'Crop Disease & Pest Advisory System',
        'home': 'Home',
        'search': 'Search',
        'detect': 'Disease Detection',
        'crops': 'Crops',
        'diseases': 'Diseases',
        'pests': 'Pests',
        'symptoms': 'Symptoms',
        'cause': 'Cause',
        'prevention': 'Prevention',
        'organic_treatment': 'Organic Treatment',
        'chemical_treatment': 'Chemical Treatment',
        'chemical_composition': 'Chemical Composition',
        'severity': 'Severity',
        'search_placeholder': 'Search by crop, disease, symptom...',
        'upload_image': 'Upload Image',
        'no_results': 'No results found',
        'welcome_msg': 'Helping farmers identify and manage crop diseases effectively',
        'select_crop': 'Select a crop to view diseases and pests',
        'how_it_works': 'How It Works',
        'step1_title': '1. Select Crop',
        'step1_desc': 'Choose your crop from our database of Paddy, Chilli, and Coffee.',
        'step2_title': '2. Identify Problem',
        'step2_desc': 'Browse diseases and pests or search by symptoms you observe.',
        'step3_title': '3. Get Treatment',
        'step3_desc': 'Get detailed organic and chemical treatment recommendations.',
        'step4_title': '4. AI Detection',
        'step4_desc': 'Upload a photo for AI-powered disease identification.',
        'common_diseases': 'Common Diseases',
        'common_pests': 'Common Pests',
        'damage_type': 'Damage Type',
        'active_season': 'Active Season',
        'scientific_name': 'Scientific Name',
        'sample_image': 'Sample Image',
        'season': 'Season',
        'ai_detection_title': 'AI Disease Detection',
        'ai_detection_subtitle': 'Upload a photo of the affected crop leaf or fruit for AI-powered disease identification',
        'drop_image': 'Drop an image here or click to upload',
        'file_support': 'Supports: JPG, PNG, JPEG, WEBP (Max 16MB)',
        'choose_file': 'Choose File',
        'analyze': 'Analyze Image',
        'detection_results': 'Detection Results',
        'recommendation': 'Recommendation',
        'match': 'match',
        'how_ai_works': 'How AI Detection Works',
        'capture': 'Capture',
        'capture_desc': 'Take a clear photo of the affected leaf, fruit, or plant part.',
        'upload': 'Upload',
        'upload_desc': 'Upload the image using the upload area above.',
        'ai_analysis': 'AI Analysis',
        'ai_analysis_desc': 'Our CNN model analyzes the image patterns to identify diseases.',
        'get_results': 'Get Results',
        'get_results_desc': 'Receive disease predictions with treatment recommendations.',
        'tips_title': 'Tips for Best Results',
        'tip1': 'Take photos in natural daylight',
        'tip2': 'Focus on the affected area (leaf spots, discoloration)',
        'tip3': 'Include both healthy and affected parts for comparison',
        'tip4': 'Avoid blurry or dark images',
        'tip5': 'Take close-up shots of symptoms',
        'search_crops_diseases': 'Search Crops, Diseases & Pests',
        'try_search': 'Try:',
        'view_details': 'View full details',
        'no_results_msg': 'No results found',
        'no_results_desc': 'Try different keywords or check your spelling.',
        'chatbot_title': 'Crop Assistant',
        'chatbot_placeholder': 'Ask about any crop disease...',
        'chatbot_welcome': 'Hello! I am your Crop Advisory Assistant. Ask me about diseases, pests, treatments, or symptoms for Paddy, Chilli, and Coffee.',
        'footer_desc': 'An AI-powered digital advisory system helping farmers protect crops, improve productivity, and reduce losses.',
        'quick_links': 'Quick Links',
        'supported_crops': 'Supported Crops',
        'detect_disease': 'Detect Disease',
        'loading': 'Loading...',
        'loading_crops': 'Loading crops...',
        'loading_details': 'Loading crop details...',
        'crop_label': 'Crop:',
        'no_diseases_msg': 'No diseases recorded for this crop.',
        'no_pests_msg': 'No pests recorded for this crop.',
        'crop_not_found': 'Crop not found.',
        'disease_not_found': 'Disease not found.',
        'pest_not_found': 'Pest not found.',
        'go_home': 'Go back to home',
        'copyright': '© 2026 Crop Disease & Pest Advisory System. All rights reserved.',
        'failed_load': 'Failed to load crops. Please refresh the page.',
        'search_failed': 'Search failed. Please try again.',
        'analysis_failed': 'Analysis failed. Please try again.',
        'analyzing': 'Analyzing image... Please wait',
        'invalid_file': 'Invalid file type. Please upload PNG, JPG, or WEBP images.',
        'file_too_large': 'File is too large. Maximum size is 16MB.',
        'remove': 'Remove',
        'select_your_crop': 'Select your crop:',
        'auto_detect': 'Auto-detect (all crops)',
        'paddy_rice': 'Paddy (Rice)',
        'chilli': 'Chilli',
        'coffee': 'Coffee',
        'crop_name_paddy': 'Paddy (Rice)',
        'crop_name_chilli': 'Chilli',
        'crop_name_coffee': 'Coffee',
        'crop_desc_paddy': 'Paddy is one of the most important staple food crops, cultivated widely in tropical and subtropical regions. It requires warm climate (20–37°C) and abundant water supply. India is the second-largest producer of rice globally.',
        'crop_desc_chilli': 'Chilli is an important spice crop grown extensively in India. It is used as a spice, condiment, sauce, and vegetable. India is the world\'s largest producer, consumer, and exporter of chilli. Major states: Andhra Pradesh, Telangana, Karnataka, Maharashtra.',
        'crop_desc_coffee': 'Coffee is a major plantation crop grown in southern India (Karnataka, Kerala, Tamil Nadu). India produces both Arabica (1000–1500m altitude) and Robusta (500–1000m) varieties. Karnataka contributes about 70% of India\'s coffee production.',
        'crop_season_paddy': 'Kharif (June–Nov), Rabi/Boro (Nov–May), Summer (Jan–May) in irrigated areas',
        'crop_season_chilli': 'Kharif & Rabi (Year-round in tropical areas)',
        'crop_season_coffee': 'Perennial; flowering March–April, harvest November–February',
        'stat_crops': '3 Crops',
        'stat_diseases': '13 Diseases',
        'stat_pests': '7 Pests',
        'n_diseases': 'Diseases',
        'n_pests': 'Pests',
        'search_input_placeholder': 'Type crop name, disease, symptom, pest...',
        'thinking': 'Thinking...',
        'chat_error': 'Sorry, something went wrong.',
        'chat_connect_error': 'Sorry, could not connect. Please try again.',
        'cropguard': 'CropGuard',
    },
    'hi': {
        'app_title': 'फसल रोग एवं कीट सलाहकार प्रणाली',
        'home': 'होम',
        'search': 'खोज',
        'detect': 'रोग पहचान',
        'crops': 'फसलें',
        'diseases': 'रोग',
        'pests': 'कीट',
        'symptoms': 'लक्षण',
        'cause': 'कारण',
        'prevention': 'रोकथाम',
        'organic_treatment': 'जैविक उपचार',
        'chemical_treatment': 'रासायनिक उपचार',
        'chemical_composition': 'रासायनिक संरचना',
        'severity': 'गंभीरता',
        'search_placeholder': 'फसल, रोग, लक्षण से खोजें...',
        'upload_image': 'छवि अपलोड करें',
        'no_results': 'कोई परिणाम नहीं मिला',
        'welcome_msg': 'किसानों को फसल रोगों की पहचान और प्रबंधन में मदद',
        'select_crop': 'रोग और कीट देखने के लिए फसल चुनें',
        'how_it_works': 'यह कैसे काम करता है',
        'step1_title': '1. फसल चुनें',
        'step1_desc': 'धान, मिर्च और कॉफी के हमारे डेटाबेस से अपनी फसल चुनें।',
        'step2_title': '2. समस्या पहचानें',
        'step2_desc': 'रोग और कीट ब्राउज़ करें या लक्षणों से खोजें।',
        'step3_title': '3. उपचार पाएं',
        'step3_desc': 'विस्तृत जैविक और रासायनिक उपचार सिफारिशें प्राप्त करें।',
        'step4_title': '4. AI पहचान',
        'step4_desc': 'AI-संचालित रोग पहचान के लिए फोटो अपलोड करें।',
        'common_diseases': 'सामान्य रोग',
        'common_pests': 'सामान्य कीट',
        'damage_type': 'क्षति का प्रकार',
        'active_season': 'सक्रिय मौसम',
        'scientific_name': 'वैज्ञानिक नाम',
        'sample_image': 'नमूना छवि',
        'season': 'मौसम',
        'ai_detection_title': 'AI रोग पहचान',
        'ai_detection_subtitle': 'AI-संचालित रोग पहचान के लिए प्रभावित फसल पत्ती या फल की तस्वीर अपलोड करें',
        'drop_image': 'यहां छवि डालें या अपलोड करने के लिए क्लिक करें',
        'file_support': 'समर्थित: JPG, PNG, JPEG, WEBP (अधिकतम 16MB)',
        'choose_file': 'फ़ाइल चुनें',
        'analyze': 'छवि विश्लेषण करें',
        'detection_results': 'पहचान परिणाम',
        'recommendation': 'सिफारिश',
        'match': 'मिलान',
        'how_ai_works': 'AI पहचान कैसे काम करती है',
        'capture': 'कैप्चर',
        'capture_desc': 'प्रभावित पत्ती, फल या पौधे के हिस्से की स्पष्ट तस्वीर लें।',
        'upload': 'अपलोड',
        'upload_desc': 'ऊपर अपलोड क्षेत्र का उपयोग करके छवि अपलोड करें।',
        'ai_analysis': 'AI विश्लेषण',
        'ai_analysis_desc': 'हमारा CNN मॉडल रोगों की पहचान के लिए छवि पैटर्न का विश्लेषण करता है।',
        'get_results': 'परिणाम प्राप्त करें',
        'get_results_desc': 'उपचार सिफारिशों के साथ रोग भविष्यवाणियां प्राप्त करें।',
        'tips_title': 'सर्वोत्तम परिणामों के लिए सुझाव',
        'tip1': 'प्राकृतिक दिन की रोशनी में तस्वीरें लें',
        'tip2': 'प्रभावित क्षेत्र पर ध्यान केंद्रित करें (पत्ती के धब्बे, मलिनकिरण)',
        'tip3': 'तुलना के लिए स्वस्थ और प्रभावित दोनों भागों को शामिल करें',
        'tip4': 'धुंधली या अंधेरी छवियों से बचें',
        'tip5': 'लक्षणों के क्लोज-अप शॉट लें',
        'search_crops_diseases': 'फसलें, रोग और कीट खोजें',
        'try_search': 'कोशिश करें:',
        'view_details': 'पूरा विवरण देखें',
        'no_results_msg': 'कोई परिणाम नहीं मिला',
        'no_results_desc': 'अलग-अलग कीवर्ड आज़माएं या अपनी वर्तनी जांचें।',
        'chatbot_title': 'फसल सहायक',
        'chatbot_placeholder': 'किसी भी फसल रोग के बारे में पूछें...',
        'chatbot_welcome': 'नमस्ते! मैं आपका फसल सलाहकार सहायक हूं। धान, मिर्च और कॉफी के रोगों, कीटों, उपचार या लक्षणों के बारे में पूछें।',
        'footer_desc': 'किसानों को फसलों की रक्षा करने, उत्पादकता बढ़ाने और नुकसान कम करने में मदद करने वाली AI-संचालित डिजिटल सलाहकार प्रणाली।',
        'quick_links': 'त्वरित लिंक',
        'supported_crops': 'समर्थित फसलें',
        'detect_disease': 'रोग पहचान',
        'loading': 'लोड हो रहा है...',
        'loading_crops': 'फसलें लोड हो रही हैं...',
        'loading_details': 'फसल विवरण लोड हो रहा है...',
        'crop_label': 'फसल:',
        'no_diseases_msg': 'इस फसल के लिए कोई रोग दर्ज नहीं है।',
        'no_pests_msg': 'इस फसल के लिए कोई कीट दर्ज नहीं है।',
        'crop_not_found': 'फसल नहीं मिली।',
        'disease_not_found': 'रोग नहीं मिला।',
        'pest_not_found': 'कीट नहीं मिला।',
        'go_home': 'होम पर वापस जाएं',
        'copyright': '© 2026 फसल रोग एवं कीट सलाहकार प्रणाली। सर्वाधिकार सुरक्षित।',
        'failed_load': 'फसलें लोड करने में विफल। कृपया पृष्ठ रीफ्रेश करें।',
        'search_failed': 'खोज विफल। कृपया पुनः प्रयास करें।',
        'analysis_failed': 'विश्लेषण विफल। कृपया पुनः प्रयास करें।',
        'analyzing': 'छवि विश्लेषण हो रहा है... कृपया प्रतीक्षा करें',
        'invalid_file': 'अमान्य फ़ाइल प्रकार। कृपया PNG, JPG, या WEBP छवियां अपलोड करें।',
        'file_too_large': 'फ़ाइल बहुत बड़ी है। अधिकतम आकार 16MB है।',
        'remove': 'हटाएं',
        'select_your_crop': 'अपनी फसल चुनें:',
        'auto_detect': 'स्वतः पहचान (सभी फसलें)',
        'paddy_rice': 'धान (चावल)',
        'chilli': 'मिर्च',
        'coffee': 'कॉफी',
        'crop_name_paddy': 'धान (चावल)',
        'crop_name_chilli': 'मिर्च',
        'crop_name_coffee': 'कॉफी',
        'crop_desc_paddy': 'धान सबसे महत्वपूर्ण मुख्य खाद्य फसलों में से एक है, जो उष्णकटिबंधीय और उपोष्णकटिबंधीय क्षेत्रों में व्यापक रूप से उगाई जाती है। इसके लिए गर्म जलवायु (20–37°C) और प्रचुर जल आपूर्ति की आवश्यकता होती है। भारत विश्व का दूसरा सबसे बड़ा चावल उत्पादक है।',
        'crop_desc_chilli': 'मिर्च भारत में व्यापक रूप से उगाई जाने वाली एक महत्वपूर्ण मसाला फसल है। इसका उपयोग मसाले, चटनी, सॉस और सब्जी के रूप में किया जाता है। भारत मिर्च का दुनिया का सबसे बड़ा उत्पादक, उपभोक्ता और निर्यातक है। प्रमुख राज्य: आंध्र प्रदेश, तेलंगाना, कर्नाटक, महाराष्ट्र।',
        'crop_desc_coffee': 'कॉफी दक्षिण भारत (कर्नाटक, केरल, तमिलनाडु) में उगाई जाने वाली एक प्रमुख बागान फसल है। भारत अरेबिका (1000–1500मी ऊंचाई) और रोबस्टा (500–1000मी) दोनों किस्मों का उत्पादन करता है। कर्नाटक भारत के कॉफी उत्पादन का लगभग 70% योगदान करता है।',
        'crop_season_paddy': 'खरीफ (जून–नवं), रबी/बोरो (नवं–मई), ग्रीष्म (जनवरी–मई) सिंचित क्षेत्रों में',
        'crop_season_chilli': 'खरीफ और रबी (उष्णकटिबंधीय क्षेत्रों में वर्षभर)',
        'crop_season_coffee': 'बारहमासी; फूल मार्च–अप्रैल, फसल कटाई नवंबर–फरवरी',
        'stat_crops': '3 फसलें',
        'stat_diseases': '13 रोग',
        'stat_pests': '7 कीट',
        'n_diseases': 'रोग',
        'n_pests': 'कीट',
        'search_input_placeholder': 'फसल का नाम, रोग, लक्षण, कीट टाइप करें...',
        'thinking': 'सोच रहा हूं...',
        'chat_error': 'क्षमा करें, कुछ गलत हो गया।',
        'chat_connect_error': 'क्षमा करें, कनेक्ट नहीं हो सका। कृपया पुनः प्रयास करें।',
        'cropguard': 'CropGuard',
    },
    'kn': {
        'app_title': 'ಬೆಳೆ ರೋಗ ಮತ್ತು ಕೀಟ ಸಲಹಾ ವ್ಯವಸ್ಥೆ',
        'home': 'ಮುಖಪುಟ',
        'search': 'ಹುಡುಕು',
        'detect': 'ರೋಗ ಪತ್ತೆ',
        'crops': 'ಬೆಳೆಗಳು',
        'diseases': 'ರೋಗಗಳು',
        'pests': 'ಕೀಟಗಳು',
        'symptoms': 'ಲಕ್ಷಣಗಳು',
        'cause': 'ಕಾರಣ',
        'prevention': 'ತಡೆಗಟ್ಟುವಿಕೆ',
        'organic_treatment': 'ಸಾವಯವ ಚಿಕಿತ್ಸೆ',
        'chemical_treatment': 'ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ',
        'chemical_composition': 'ರಾಸಾಯನಿಕ ಸಂಯೋಜನೆ',
        'severity': 'ತೀವ್ರತೆ',
        'search_placeholder': 'ಬೆಳೆ, ರೋಗ, ಲಕ್ಷಣದಿಂದ ಹುಡುಕಿ...',
        'upload_image': 'ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        'no_results': 'ಯಾವುದೇ ಫಲಿತಾಂಶ ಕಂಡುಬಂದಿಲ್ಲ',
        'welcome_msg': 'ರೈತರಿಗೆ ಬೆಳೆ ರೋಗಗಳ ಗುರುತಿಸುವಿಕೆ ಮತ್ತು ನಿರ್ವಹಣೆಯಲ್ಲಿ ಸಹಾಯ',
        'select_crop': 'ರೋಗ ಮತ್ತು ಕೀಟಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ',
        'how_it_works': 'ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
        'step1_title': '1. ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ',
        'step1_desc': 'ಭತ್ತ, ಮೆಣಸಿನಕಾಯಿ ಮತ್ತು ಕಾಫಿಯ ನಮ್ಮ ಡೇಟಾಬೇಸ್‌ನಿಂದ ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.',
        'step2_title': '2. ಸಮಸ್ಯೆ ಗುರುತಿಸಿ',
        'step2_desc': 'ರೋಗಗಳು ಮತ್ತು ಕೀಟಗಳನ್ನು ಬ್ರೌಸ್ ಮಾಡಿ ಅಥವಾ ಲಕ್ಷಣಗಳಿಂದ ಹುಡುಕಿ.',
        'step3_title': '3. ಚಿಕಿತ್ಸೆ ಪಡೆಯಿರಿ',
        'step3_desc': 'ವಿವರವಾದ ಸಾವಯವ ಮತ್ತು ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸಾ ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಿರಿ.',
        'step4_title': '4. AI ಪತ್ತೆ',
        'step4_desc': 'AI-ಚಾಲಿತ ರೋಗ ಗುರುತಿಸುವಿಕೆಗಾಗಿ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.',
        'common_diseases': 'ಸಾಮಾನ್ಯ ರೋಗಗಳು',
        'common_pests': 'ಸಾಮಾನ್ಯ ಕೀಟಗಳು',
        'damage_type': 'ಹಾನಿಯ ಪ್ರಕಾರ',
        'active_season': 'ಸಕ್ರಿಯ ಋತು',
        'scientific_name': 'ವೈಜ್ಞಾನಿಕ ಹೆಸರು',        'sample_image': 'ಮಾದರಿ ಚಿತ್ರ',        'season': 'ಋತು',
        'ai_detection_title': 'AI ರೋಗ ಪತ್ತೆ',
        'ai_detection_subtitle': 'AI-ಚಾಲಿತ ರೋಗ ಗುರುತಿಸುವಿಕೆಗಾಗಿ ಪೀಡಿತ ಬೆಳೆ ಎಲೆ ಅಥವಾ ಹಣ್ಣಿನ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
        'drop_image': 'ಇಲ್ಲಿ ಚಿತ್ರವನ್ನು ಬಿಡಿ ಅಥವಾ ಅಪ್‌ಲೋಡ್ ಮಾಡಲು ಕ್ಲಿಕ್ ಮಾಡಿ',
        'file_support': 'ಬೆಂಬಲಿತ: JPG, PNG, JPEG, WEBP (ಗರಿಷ್ಠ 16MB)',
        'choose_file': 'ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ',
        'analyze': 'ಚಿತ್ರ ವಿಶ್ಲೇಷಿಸಿ',
        'detection_results': 'ಪತ್ತೆ ಫಲಿತಾಂಶಗಳು',
        'recommendation': 'ಶಿಫಾರಸು',
        'match': 'ಹೊಂದಾಣಿಕೆ',
        'how_ai_works': 'AI ಪತ್ತೆ ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ',
        'capture': 'ಕ್ಯಾಪ್ಚರ್',
        'capture_desc': 'ಪೀಡಿತ ಎಲೆ, ಹಣ್ಣು ಅಥವಾ ಸಸ್ಯ ಭಾಗದ ಸ್ಪಷ್ಟ ಫೋಟೋ ತೆಗೆಯಿರಿ.',
        'upload': 'ಅಪ್‌ಲೋಡ್',
        'upload_desc': 'ಮೇಲಿನ ಅಪ್‌ಲೋಡ್ ಪ್ರದೇಶವನ್ನು ಬಳಸಿ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.',
        'ai_analysis': 'AI ವಿಶ್ಲೇಷಣೆ',
        'ai_analysis_desc': 'ನಮ್ಮ CNN ಮಾದರಿ ರೋಗಗಳನ್ನು ಗುರುತಿಸಲು ಚಿತ್ರ ಮಾದರಿಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ.',
        'get_results': 'ಫಲಿತಾಂಶ ಪಡೆಯಿರಿ',
        'get_results_desc': 'ಚಿಕಿತ್ಸಾ ಶಿಫಾರಸುಗಳೊಂದಿಗೆ ರೋಗ ಮುನ್ಸೂಚನೆಗಳನ್ನು ಪಡೆಯಿರಿ.',
        'tips_title': 'ಉತ್ತಮ ಫಲಿತಾಂಶಗಳಿಗಾಗಿ ಸಲಹೆಗಳು',
        'tip1': 'ನೈಸರ್ಗಿಕ ಹಗಲು ಬೆಳಕಿನಲ್ಲಿ ಫೋಟೋ ತೆಗೆಯಿರಿ',
        'tip2': 'ಪೀಡಿತ ಪ್ರದೇಶದ ಮೇಲೆ ಗಮನ ಕೇಂದ್ರೀಕರಿಸಿ',
        'tip3': 'ಹೋಲಿಕೆಗಾಗಿ ಆರೋಗ್ಯಕರ ಮತ್ತು ಪೀಡಿತ ಭಾಗಗಳನ್ನು ಸೇರಿಸಿ',
        'tip4': 'ಮಸುಕಾದ ಅಥವಾ ಕತ್ತಲೆಯ ಚಿತ್ರಗಳನ್ನು ತಪ್ಪಿಸಿ',
        'tip5': 'ಲಕ್ಷಣಗಳ ಕ್ಲೋಸ್-ಅಪ್ ಶಾಟ್‌ಗಳನ್ನು ತೆಗೆಯಿರಿ',
        'search_crops_diseases': 'ಬೆಳೆಗಳು, ರೋಗಗಳು ಮತ್ತು ಕೀಟಗಳನ್ನು ಹುಡುಕಿ',
        'try_search': 'ಪ್ರಯತ್ನಿಸಿ:',
        'view_details': 'ಪೂರ್ಣ ವಿವರ ವೀಕ್ಷಿಸಿ',
        'no_results_msg': 'ಯಾವುದೇ ಫಲಿತಾಂಶ ಕಂಡುಬಂದಿಲ್ಲ',
        'no_results_desc': 'ವಿವಿಧ ಕೀವರ್ಡ್‌ಗಳನ್ನು ಪ್ರಯತ್ನಿಸಿ ಅಥವಾ ನಿಮ್ಮ ಕಾಗುಣಿತ ಪರಿಶೀಲಿಸಿ.',
        'chatbot_title': 'ಬೆಳೆ ಸಹಾಯಕ',
        'chatbot_placeholder': 'ಯಾವುದೇ ಬೆಳೆ ರೋಗದ ಬಗ್ಗೆ ಕೇಳಿ...',
        'chatbot_welcome': 'ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಬೆಳೆ ಸಲಹಾ ಸಹಾಯಕ. ಭತ್ತ, ಮೆಣಸಿನಕಾಯಿ ಮತ್ತು ಕಾಫಿಯ ರೋಗಗಳು, ಕೀಟಗಳು, ಚಿಕಿತ್ಸೆ ಅಥವಾ ಲಕ್ಷಣಗಳ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ.',
        'footer_desc': 'ರೈತರಿಗೆ ಬೆಳೆಗಳನ್ನು ರಕ್ಷಿಸಲು, ಉತ್ಪಾದಕತೆ ಸುಧಾರಿಸಲು ಮತ್ತು ನಷ್ಟಗಳನ್ನು ಕಡಿಮೆ ಮಾಡಲು ಸಹಾಯ ಮಾಡುವ AI-ಚಾಲಿತ ಡಿಜಿಟಲ್ ಸಲಹಾ ವ್ಯವಸ್ಥೆ.',
        'quick_links': 'ತ್ವರಿತ ಲಿಂಕ್‌ಗಳು',
        'supported_crops': 'ಬೆಂಬಲಿತ ಬೆಳೆಗಳು',
        'detect_disease': 'ರೋಗ ಪತ್ತೆ',
        'loading': 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...',
        'loading_crops': 'ಬೆಳೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...',
        'loading_details': 'ಬೆಳೆ ವಿವರಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ...',
        'crop_label': 'ಬೆಳೆ:',
        'no_diseases_msg': 'ಈ ಬೆಳೆಗೆ ಯಾವುದೇ ರೋಗಗಳು ದಾಖಲಾಗಿಲ್ಲ.',
        'no_pests_msg': 'ಈ ಬೆಳೆಗೆ ಯಾವುದೇ ಕೀಟಗಳು ದಾಖಲಾಗಿಲ್ಲ.',
        'crop_not_found': 'ಬೆಳೆ ಕಂಡುಬಂದಿಲ್ಲ.',
        'disease_not_found': 'ರೋಗ ಕಂಡುಬಂದಿಲ್ಲ.',
        'pest_not_found': 'ಕೀಟ ಕಂಡುಬಂದಿಲ್ಲ.',
        'go_home': 'ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ',
        'copyright': '© 2026 ಬೆಳೆ ರೋಗ ಮತ್ತು ಕೀಟ ಸಲಹಾ ವ್ಯವಸ್ಥೆ. ಎಲ್ಲಾ ಹಕ್ಕುಗಳನ್ನು ಕಾಯ್ದಿರಿಸಲಾಗಿದೆ.',
        'failed_load': 'ಬೆಳೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಲು ವಿಫಲವಾಗಿದೆ. ಪುಟವನ್ನು ರಿಫ್ರೆಶ್ ಮಾಡಿ.',
        'search_failed': 'ಹುಡುಕಾಟ ವಿಫಲವಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
        'analysis_failed': 'ವಿಶ್ಲೇಷಣೆ ವಿಫಲವಾಗಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
        'analyzing': 'ಚಿತ್ರ ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ... ದಯವಿಟ್ಟು ನಿರೀಕ್ಷಿಸಿ',
        'invalid_file': 'ಅಮಾನ್ಯ ಫೈಲ್ ಪ್ರಕಾರ. ದಯವಿಟ್ಟು PNG, JPG, ಅಥವಾ WEBP ಚಿತ್ರಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.',
        'file_too_large': 'ಫೈಲ್ ತುಂಬಾ ದೊಡ್ಡದಾಗಿದೆ. ಗರಿಷ್ಠ ಗಾತ್ರ 16MB.',
        'remove': 'ತೆಗೆದುಹಾಕಿ',
        'select_your_crop': 'ನಿಮ್ಮ ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ:',
        'auto_detect': 'ಸ್ವಯಂ-ಪತ್ತೆ (ಎಲ್ಲಾ ಬೆಳೆಗಳು)',
        'paddy_rice': 'ಭತ್ತ (ಅಕ್ಕಿ)',
        'chilli': 'ಮೆಣಸಿನಕಾಯಿ',
        'coffee': 'ಕಾಫಿ',
        'crop_name_paddy': 'ಭತ್ತ (ಅಕ್ಕಿ)',
        'crop_name_chilli': 'ಮೆಣಸಿನಕಾಯಿ',
        'crop_name_coffee': 'ಕಾಫಿ',
        'crop_desc_paddy': 'ಭತ್ತವು ಅತ್ಯಂತ ಪ್ರಮುಖ ಮುಖ್ಯ ಆಹಾರ ಬೆಳೆಗಳಲ್ಲಿ ಒಂದಾಗಿದ್ದು, ಉಷ್ಣವಲಯ ಮತ್ತು ಉಪೋಷ್ಣವಲಯ ಪ್ರದೇಶಗಳಲ್ಲಿ ವ್ಯಾಪಕವಾಗಿ ಬೆಳೆಯಲಾಗುತ್ತದೆ. ಇದಕ್ಕೆ ಬೆಚ್ಚಗಿನ ಹವಾಮಾನ (20–37°C) ಮತ್ತು ಹೇರಳವಾದ ನೀರಿನ ಪೂರೈಕೆ ಅಗತ್ಯ. ಭಾರತವು ವಿಶ್ವದ ಎರಡನೇ ಅತಿದೊಡ್ಡ ಅಕ್ಕಿ ಉತ್ಪಾದಕ.',
        'crop_desc_chilli': 'ಮೆಣಸಿನಕಾಯಿ ಭಾರತದಲ್ಲಿ ವ್ಯಾಪಕವಾಗಿ ಬೆಳೆಯಲಾಗುವ ಒಂದು ಪ್ರಮುಖ ಸಂಬಾರ ಬೆಳೆ. ಇದನ್ನು ಮಸಾಲೆ, ಚಟ್ನಿ, ಸಾಸ್ ಮತ್ತು ತರಕಾರಿಯಾಗಿ ಬಳಸಲಾಗುತ್ತದೆ. ಭಾರತವು ಮೆಣಸಿನಕಾಯಿಯ ವಿಶ್ವದ ಅತಿದೊಡ್ಡ ಉತ್ಪಾದಕ, ಬಳಕೆದಾರ ಮತ್ತು ರಫ್ತುದಾರ. ಪ್ರಮುಖ ರಾಜ್ಯಗಳು: ಆಂಧ್ರ ಪ್ರದೇಶ, ತೆಲಂಗಾಣ, ಕರ್ನಾಟಕ, ಮಹಾರಾಷ್ಟ್ರ.',
        'crop_desc_coffee': 'ಕಾಫಿ ದಕ್ಷಿಣ ಭಾರತದ (ಕರ್ನಾಟಕ, ಕೇರಳ, ತಮಿಳುನಾಡು) ಪ್ರಮುಖ ತೋಟ ಬೆಳೆ. ಭಾರತವು ಅರೇಬಿಕಾ (1000–1500ಮೀ ಎತ್ತರ) ಮತ್ತು ರೊಬಸ್ಟಾ (500–1000ಮೀ) ಎರಡೂ ತಳಿಗಳನ್ನು ಉತ್ಪಾದಿಸುತ್ತದೆ. ಕರ್ನಾಟಕವು ಭಾರತದ ಕಾಫಿ ಉತ್ಪಾದನೆಯ ಸುಮಾರು 70% ಯೋಗದಾನ ನೀಡುತ್ತದೆ.',
        'crop_season_paddy': 'ಮುಂಗಾರು (ಜೂನ್–ನವೆಂ), ಹಿಂಗಾರು/ಬೋರೋ (ನವೆಂ–ಮೇ), ಬೇಸಿಗೆ (ಜನವರಿ–ಮೇ) ನೀರಾವರಿ ಪ್ರದೇಶಗಳಲ್ಲಿ',
        'crop_season_chilli': 'ಮುಂಗಾರು ಮತ್ತು ಹಿಂಗಾರು (ಉಷ್ಣವಲಯ ಪ್ರದೇಶಗಳಲ್ಲಿ ವರ್ಷವಿಡೀ)',
        'crop_season_coffee': 'ಬಹುವಾರ್ಷಿಕ; ಹೂಬಿಡುವಿಕೆ ಮಾರ್ಚ್–ಏಪ್ರಿಲ್, ಕೊಯ್ಲು ನವೆಂಬರ್–ಫೆಬ್ರವರಿ',
        'stat_crops': '3 ಬೆಳೆಗಳು',
        'stat_diseases': '13 ರೋಗಗಳು',
        'stat_pests': '7 ಕೀಟಗಳು',
        'n_diseases': 'ರೋಗಗಳು',
        'n_pests': 'ಕೀಟಗಳು',
        'search_input_placeholder': 'ಬೆಳೆ ಹೆಸರು, ರೋಗ, ಲಕ್ಷಣ, ಕೀಟ ಟೈಪ್ ಮಾಡಿ...',
        'thinking': 'ಯೋಚಿಸುತ್ತಿದೆ...',
        'chat_error': 'ಕ್ಷಮಿಸಿ, ಏನೋ ತಪ್ಪಾಗಿದೆ.',
        'chat_connect_error': 'ಕ್ಷಮಿಸಿ, ಸಂಪರ್ಕಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
        'cropguard': 'CropGuard',
    },
}


@app.route('/api/translations/<lang>', methods=['GET'])
def get_translations(lang):
    """Get translations for a specific language."""
    if lang not in TRANSLATIONS:
        lang = 'en'
    return jsonify(TRANSLATIONS[lang])


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get available languages."""
    return jsonify([
        {'code': 'en', 'name': 'English'},
        {'code': 'hi', 'name': 'हिन्दी (Hindi)'},
        {'code': 'kn', 'name': 'ಕನ್ನಡ (Kannada)'},
    ])


# ==================== CHATBOT ====================

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chatbot endpoint for crop advisory questions."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_message = data['message'].strip()
    if not user_message or len(user_message) > 1000:
        return jsonify({'error': 'Invalid message'}), 400

    lang = data.get('lang', 'en')
    response = get_chatbot_response(user_message, lang)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
