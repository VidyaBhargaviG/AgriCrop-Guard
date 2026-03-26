"""
AI Disease Detection Module — Hybrid Approach
1. CNN model (MobileNetV2) for primary prediction
2. Color-analysis fallback when CNN confidence is low or model unavailable
The CNN result is preferred; color analysis boosts / validates it.
"""

import os
import json
from collections import Counter

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'crop_disease_model.h5')
LABELS_PATH = os.path.join(BASE_DIR, 'class_labels.json')

# ---------- Model state ----------
_model = None
_class_labels = None
_model_loaded = False

# ================================================================
# DISEASE KNOWLEDGE — used by color-analysis AND as recommendation
# source for CNN labels.
# ================================================================
DISEASE_KNOWLEDGE = {
    # -------- PADDY --------
    'Paddy Blast Disease': {
        'crop': 'Paddy',
        'disease': 'Blast Disease',
        'description': 'Diamond-shaped lesions on leaves with grey/white center and brown border. Neck blast causes panicle to fall.',
        'recommendation': 'Spray Tricyclazole 75% WP (0.6 g/L) or Isoprothiolane 40% EC (1.5 ml/L). Use resistant varieties like IR-64, CO-39.',
        'severity': 'High',
        'color_profile': {
            'brown_range': ([10, 50, 50], [25, 255, 200]),
            'grey_range': ([0, 0, 120], [180, 40, 200]),
            'min_brown_pct': 8, 'min_grey_pct': 5
        }
    },
    'Paddy Bacterial Leaf Blight': {
        'crop': 'Paddy',
        'disease': 'Bacterial Leaf Blight',
        'description': 'Water-soaked yellowish stripes on leaf margins turning white/grey. Milky bacterial ooze in early morning.',
        'recommendation': 'Spray Streptomycin sulphate + Copper oxychloride 50% WP (2.5 g/L). Use disease-free seeds and resistant varieties.',
        'severity': 'High',
        'color_profile': {
            'yellow_range': ([15, 50, 60], [35, 255, 255]),
            'white_range': ([0, 0, 180], [180, 50, 255]),
            'min_yellow_pct': 3, 'min_white_pct': 3
        }
    },
    'Paddy Brown Spot': {
        'crop': 'Paddy',
        'disease': 'Brown Spot',
        'description': 'Oval brown spots with grey center on leaves, glumes, and leaf sheaths.',
        'recommendation': 'Spray Mancozeb 75% WP (2.5 g/L). Apply potassium fertilizer (60 kg K₂O/ha). Use resistant varieties.',
        'severity': 'Medium',
        'color_profile': {
            'brown_range': ([8, 80, 40], [22, 255, 180]),
            'dark_range': ([0, 30, 20], [20, 150, 100]),
            'min_brown_pct': 8, 'min_dark_pct': 5
        }
    },
    'Paddy Leaf Smut': {
        'crop': 'Paddy',
        'disease': 'Leaf Smut',
        'description': 'Small black powdery smut spots (sori) on leaves. Spots rupture releasing dark spores.',
        'recommendation': 'Spray Propiconazole 25% EC (1 ml/L) or Mancozeb 75% WP (2.5 g/L). Remove and destroy infected debris.',
        'severity': 'Medium',
        'color_profile': {
            'black_range': ([0, 0, 0], [180, 150, 35]),
            'dark_range': ([0, 30, 20], [180, 120, 60]),
            'min_black_pct': 15, 'min_dark_pct': 10
        }
    },
    'Paddy Leaf Scald': {
        'crop': 'Paddy',
        'disease': 'Leaf Scald',
        'description': 'Zonate lesions starting from leaf tips with alternating light and dark brown bands.',
        'recommendation': 'Spray Mancozeb 75% WP (2.5 g/L) or Carbendazim 50% WP (1 g/L). Avoid excess nitrogen. Use balanced fertilization.',
        'severity': 'Medium',
        'color_profile': {
            'brown_range': ([10, 40, 60], [25, 200, 200]),
            'tan_range': ([15, 30, 150], [30, 120, 255]),
            'min_brown_pct': 5, 'min_tan_pct': 3
        }
    },
    'Paddy Tungro Virus': {
        'crop': 'Paddy',
        'disease': 'Tungro Virus',
        'description': 'Yellow to orange discoloration of leaves from tip downward. Stunted growth with reduced tillering.',
        'recommendation': 'Control leafhopper vector with Imidacloprid 17.8% SL (0.5 ml/L). Use resistant varieties. No direct chemical cure.',
        'severity': 'High',
        'color_profile': {
            'yellow_range': ([18, 100, 100], [35, 255, 255]),
            'orange_range': ([5, 100, 100], [18, 255, 255]),
            'min_yellow_pct': 12, 'min_orange_pct': 5
        }
    },
    'Paddy Healthy': {
        'crop': 'Paddy',
        'disease': 'Healthy',
        'description': 'The paddy plant appears healthy with no visible signs of disease.',
        'recommendation': 'Continue regular care: maintain proper water levels, apply balanced NPK fertilizer, and monitor for pests.',
        'severity': 'None',
        'color_profile': {
            'green_range': ([35, 60, 40], [85, 255, 255]),
            'min_green_pct': 35
        }
    },

    # -------- CHILLI --------
    'Chilli Anthracnose': {
        'crop': 'Chilli',
        'disease': 'Anthracnose',
        'description': 'Dark sunken circular lesions with concentric rings on fruits. Fruits shrivel and drop prematurely.',
        'recommendation': 'Spray Mancozeb 75% WP (2.5 g/L) + Carbendazim 50% WP (1 g/L) alternately at 15-day intervals. Use disease-free seeds.',
        'severity': 'High',
        'color_profile': {
            'dark_range': ([0, 30, 0], [20, 255, 80]),
            'brown_range': ([5, 80, 40], [20, 255, 180]),
            'min_dark_pct': 12, 'min_brown_pct': 8
        }
    },
    'Chilli Healthy': {
        'crop': 'Chilli',
        'disease': 'Healthy',
        'description': 'The chilli plant appears healthy with no visible signs of disease.',
        'recommendation': 'Continue regular care: water adequately, apply balanced NPK fertilizer, and monitor for pests.',
        'severity': 'None',
        'color_profile': {
            'green_range': ([35, 60, 40], [85, 255, 255]),
            'min_green_pct': 30
        }
    },

    # -------- COFFEE --------
    'Coffee Leaf Rust': {
        'crop': 'Coffee',
        'disease': 'Leaf Rust',
        'description': 'Yellow-orange powdery spots (urediniospores) on the underside of leaves. Severe defoliation.',
        'recommendation': 'Spray Tridemorph 80% EC (0.5 ml/L) or Propiconazole 25% EC (0.5 ml/L). Maintain 40-50% shade.',
        'severity': 'High',
        'color_profile': {
            'orange_range': ([5, 100, 100], [20, 255, 255]),
            'yellow_range': ([18, 80, 80], [35, 255, 255]),
            'min_orange_pct': 5, 'min_yellow_pct': 3
        }
    },
    'Coffee Red Spider Mite': {
        'crop': 'Coffee',
        'disease': 'Red Spider Mite',
        'description': 'Tiny red/brown mites on leaf underside causing bronzing and stippling. Leaves become pale and dry.',
        'recommendation': 'Spray Dicofol 18.5% EC (2.5 ml/L) or wettable sulphur (3 g/L). Maintain shade and humidity. Release predatory mites.',
        'severity': 'Medium',
        'color_profile': {
            'red_range': ([0, 80, 50], [10, 255, 255]),
            'brown_range': ([8, 60, 40], [22, 200, 200]),
            'min_red_pct': 3, 'min_brown_pct': 4
        }
    },
    'Coffee Healthy': {
        'crop': 'Coffee',
        'disease': 'Healthy',
        'description': 'The coffee plant appears healthy with no visible signs of disease.',
        'recommendation': 'Continue regular care: maintain 40-50% shade, apply organic mulch, and monitor for pests.',
        'severity': 'None',
        'color_profile': {
            'green_range': ([35, 60, 40], [85, 255, 255]),
            'min_green_pct': 30
        }
    },
}


# ================================================================
# CNN model loading
# ================================================================
def _load_model():
    """Load the trained CNN model and class labels."""
    global _model, _class_labels, _model_loaded

    if _model_loaded:
        return _model is not None

    _model_loaded = True

    if not os.path.exists(MODEL_PATH):
        print(f"[AI] Trained model not found at {MODEL_PATH}.")
        return False

    if not os.path.exists(LABELS_PATH):
        print(f"[AI] Class labels not found at {LABELS_PATH}.")
        return False

    try:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        import tensorflow as tf
        _model = tf.keras.models.load_model(MODEL_PATH)
        with open(LABELS_PATH, 'r') as f:
            _class_labels = json.load(f)
        print(f"[AI] CNN model loaded successfully. Classes: {len(_class_labels)}")
        return True
    except ImportError:
        print("[AI] TensorFlow not installed. Will use color-analysis fallback.")
        return False
    except Exception as e:
        print(f"[AI] Error loading model: {e}")
        return False


# ================================================================
# CNN prediction
# ================================================================
def _predict_with_cnn(image_path):
    """Run prediction using the trained CNN model. Returns list sorted by confidence."""
    import tensorflow as tf
    import numpy as np

    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = _model.predict(img_array, verbose=0)

    # Aggregate duplicate class labels
    aggregated = {}
    for idx in range(len(predictions[0])):
        label = _class_labels.get(str(idx), f"Class_{idx}")
        confidence = float(predictions[0][idx])
        if label in aggregated:
            aggregated[label] += confidence
        else:
            aggregated[label] = confidence

    sorted_labels = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
    return sorted_labels  # list of (label, confidence)


# ================================================================
# Color-analysis prediction
# ================================================================
def _analyze_colors(image_path, crop_filter=None):
    """Analyze image colors and return how well each disease profile matches."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return []

    img = cv2.imread(image_path)
    if img is None:
        return []

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    total_pixels = hsv.shape[0] * hsv.shape[1]

    scores = []
    for name, info in DISEASE_KNOWLEDGE.items():
        if crop_filter and info['crop'].lower() != crop_filter.lower():
            continue

        profile = info.get('color_profile', {})
        total_ranges = 0
        matched_ranges = 0
        weighted_score = 0.0

        for key, val in profile.items():
            if key.startswith('min_') or not key.endswith('_range'):
                continue

            total_ranges += 1
            color_name = key.replace('_range', '')
            lower = np.array(val[0], dtype=np.uint8)
            upper = np.array(val[1], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)
            pct = (cv2.countNonZero(mask) / total_pixels) * 100

            min_key = f'min_{color_name}_pct'
            min_pct = profile.get(min_key, 3)

            if pct >= min_pct:
                matched_ranges += 1
                # Score based on how far above threshold (diminishing returns)
                ratio = pct / min_pct
                weighted_score += min(ratio, 5.0)

        if total_ranges == 0:
            continue

        # ALL color ranges must match for a disease to count
        if matched_ranges < total_ranges:
            continue

        # Confidence based on match quality — scale more conservatively
        confidence = min(weighted_score / (total_ranges * 3.5), 0.92)
        scores.append((name, confidence))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores


# ================================================================
# Translations for disease results (HI / KN)
# ================================================================
DISEASE_TRANSLATIONS = {
    'hi': {
        # Crops
        'Paddy': 'धान', 'Chilli': 'मिर्च', 'Coffee': 'कॉफी',
        # Diseases
        'Blast Disease': 'ब्लास्ट रोग',
        'Bacterial Leaf Blight': 'जीवाणु पत्ती झुलसा',
        'Brown Spot': 'भूरा धब्बा',
        'Leaf Smut': 'पत्ती कंड',
        'Leaf Scald': 'पत्ती झुलसा',
        'Tungro Virus': 'टुंग्रो वायरस',
        'Anthracnose': 'एन्थ्रेक्नोज',
        'Leaf Rust': 'पत्ती रतुआ',
        'Red Spider Mite': 'लाल मकड़ी',
        'Healthy': 'स्वस्थ',
        # Severity
        'High': 'उच्च', 'Medium': 'मध्यम', 'Low': 'कम', 'None': 'कोई नहीं',
        # Descriptions
        'Diamond-shaped lesions on leaves with grey/white center and brown border. Neck blast causes panicle to fall.': 'पत्तियों पर भूरे किनारे और सफेद/धूसर केंद्र वाले हीरे के आकार के धब्बे। गर्दन ब्लास्ट से बालियाँ गिर जाती हैं।',
        'Water-soaked yellowish stripes on leaf margins turning white/grey. Milky bacterial ooze in early morning.': 'पत्ती के किनारों पर पीली धारियाँ जो सफेद/धूसर हो जाती हैं। सुबह दूधिया जीवाणु स्राव दिखता है।',
        'Oval brown spots with grey center on leaves, glumes, and leaf sheaths.': 'पत्तियों पर धूसर केंद्र वाले अंडाकार भूरे धब्बे।',
        'Small black powdery smut spots (sori) on leaves. Spots rupture releasing dark spores.': 'पत्तियों पर काले चूर्णी कंड के धब्बे। धब्बे फटकर काले बीजाणु छोड़ते हैं।',
        'Zonate lesions starting from leaf tips with alternating light and dark brown bands.': 'पत्ती की नोक से शुरू होने वाले हल्के और गहरे भूरे पट्टियों वाले धब्बे।',
        'Yellow to orange discoloration of leaves from tip downward. Stunted growth with reduced tillering.': 'पत्तियों का ऊपर से नीचे पीला-नारंगी रंग बदलना। बौना विकास और कम कल्ले।',
        'Dark sunken circular lesions with concentric rings on fruits. Fruits shrivel and drop prematurely.': 'फलों पर संकेंद्रित वलयों वाले गहरे धँसे गोल धब्बे। फल सिकुड़ कर गिर जाते हैं।',
        'Yellow-orange powdery spots (urediniospores) on the underside of leaves. Severe defoliation.': 'पत्तियों के नीचे पीले-नारंगी चूर्णी धब्बे। गंभीर पत्ती झड़ना।',
        'Tiny red/brown mites on leaf underside causing bronzing and stippling. Leaves become pale and dry.': 'पत्तियों के नीचे छोटे लाल/भूरे कण जो कांस्य रंग और धब्बे बनाते हैं।',
        'The paddy plant appears healthy with no visible signs of disease.': 'धान का पौधा स्वस्थ दिखाई देता है, रोग का कोई लक्षण नहीं है।',
        'The chilli plant appears healthy with no visible signs of disease.': 'मिर्च का पौधा स्वस्थ दिखाई देता है, रोग का कोई लक्षण नहीं है।',
        'The coffee plant appears healthy with no visible signs of disease.': 'कॉफी का पौधा स्वस्थ दिखाई देता है, रोग का कोई लक्षण नहीं है।',
        # Recommendations
        'Spray Tricyclazole 75% WP (0.6 g/L) or Isoprothiolane 40% EC (1.5 ml/L). Use resistant varieties like IR-64, CO-39.': 'ट्राइसाइक्लाज़ोल 75% WP (0.6 ग्रा/ली) या आइसोप्रोथियोलेन 40% EC (1.5 मिली/ली) का छिड़काव करें। IR-64, CO-39 जैसी प्रतिरोधी किस्में उगाएं।',
        'Spray Streptomycin sulphate + Copper oxychloride 50% WP (2.5 g/L). Use disease-free seeds and resistant varieties.': 'स्ट्रेप्टोमाइसिन सल्फेट + कॉपर ऑक्सीक्लोराइड 50% WP (2.5 ग्रा/ली) का छिड़काव करें। रोग मुक्त बीज और प्रतिरोधी किस्में उपयोग करें।',
        'Spray Mancozeb 75% WP (2.5 g/L). Apply potassium fertilizer (60 kg K₂O/ha). Use resistant varieties.': 'मैंकोज़ेब 75% WP (2.5 ग्रा/ली) का छिड़काव करें। पोटेशियम उर्वरक (60 किग्रा K₂O/हे.) डालें।',
        'Spray Propiconazole 25% EC (1 ml/L) or Mancozeb 75% WP (2.5 g/L). Remove and destroy infected debris.': 'प्रोपिकोनाज़ोल 25% EC (1 मिली/ली) या मैंकोज़ेब 75% WP (2.5 ग्रा/ली) का छिड़काव करें। संक्रमित अवशेष नष्ट करें।',
        'Spray Mancozeb 75% WP (2.5 g/L) or Carbendazim 50% WP (1 g/L). Avoid excess nitrogen. Use balanced fertilization.': 'मैंकोज़ेब 75% WP (2.5 ग्रा/ली) या कार्बेन्डाज़िम 50% WP (1 ग्रा/ली) का छिड़काव करें। अधिक नाइट्रोजन से बचें।',
        'Control leafhopper vector with Imidacloprid 17.8% SL (0.5 ml/L). Use resistant varieties. No direct chemical cure.': 'इमिडाक्लोप्रिड 17.8% SL (0.5 मिली/ली) से फुदका नियंत्रण करें। प्रतिरोधी किस्में उपयोग करें। कोई सीधा रासायनिक उपचार नहीं।',
        'Spray Mancozeb 75% WP (2.5 g/L) + Carbendazim 50% WP (1 g/L) alternately at 15-day intervals. Use disease-free seeds.': 'मैंकोज़ेब 75% WP + कार्बेन्डाज़िम 50% WP को 15 दिन के अंतराल पर बारी-बारी छिड़कें। रोग मुक्त बीज उपयोग करें।',
        'Spray Tridemorph 80% EC (0.5 ml/L) or Propiconazole 25% EC (0.5 ml/L). Maintain 40-50% shade.': 'ट्राइडेमॉर्फ 80% EC (0.5 मिली/ली) या प्रोपिकोनाज़ोल 25% EC (0.5 मिली/ली) का छिड़काव करें। 40-50% छाया बनाए रखें।',
        'Spray Dicofol 18.5% EC (2.5 ml/L) or wettable sulphur (3 g/L). Maintain shade and humidity. Release predatory mites.': 'डायकोफॉल 18.5% EC (2.5 मिली/ली) या गीला गंधक (3 ग्रा/ली) छिड़कें। छाया और नमी बनाए रखें।',
        'Continue regular care: maintain proper water levels, apply balanced NPK fertilizer, and monitor for pests.': 'नियमित देखभाल जारी रखें: उचित पानी का स्तर बनाए रखें, संतुलित NPK उर्वरक डालें, कीटों पर नज़र रखें।',
        'Continue regular care: water adequately, apply balanced NPK fertilizer, and monitor for pests.': 'नियमित देखभाल जारी रखें: पर्याप्त पानी दें, संतुलित NPK उर्वरक डालें, कीटों पर नज़र रखें।',
        'Continue regular care: maintain 40-50% shade, apply organic mulch, and monitor for pests.': 'नियमित देखभाल जारी रखें: 40-50% छाया बनाए रखें, जैविक मल्च डालें, कीटों पर नज़र रखें।',
    },
    'kn': {
        # Crops
        'Paddy': 'ಭತ್ತ', 'Chilli': 'ಮೆಣಸಿನಕಾಯಿ', 'Coffee': 'ಕಾಫಿ',
        # Diseases
        'Blast Disease': 'ಬ್ಲಾಸ್ಟ್ ರೋಗ',
        'Bacterial Leaf Blight': 'ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಎಲೆ ಕೊಳೆ',
        'Brown Spot': 'ಕಂದು ಚುಕ್ಕೆ',
        'Leaf Smut': 'ಎಲೆ ಕಪ್ಪು ಹುಡಿ',
        'Leaf Scald': 'ಎಲೆ ಸುಟ್ಟ ರೋಗ',
        'Tungro Virus': 'ಟುಂಗ್ರೊ ವೈರಸ್',
        'Anthracnose': 'ಆಂಥ್ರಾಕ್ನೋಸ್',
        'Leaf Rust': 'ಎಲೆ ತುಕ್ಕು',
        'Red Spider Mite': 'ಕೆಂಪು ಜೇಡ ಹುಳು',
        'Healthy': 'ಆರೋಗ್ಯಕರ',
        # Severity
        'High': 'ಹೆಚ್ಚು', 'Medium': 'ಮಧ್ಯಮ', 'Low': 'ಕಡಿಮೆ', 'None': 'ಯಾವುದೂ ಇಲ್ಲ',
        # Descriptions
        'Diamond-shaped lesions on leaves with grey/white center and brown border. Neck blast causes panicle to fall.': 'ಎಲೆಗಳ ಮೇಲೆ ಬೂದು/ಬಿಳಿ ಕೇಂದ್ರ ಮತ್ತು ಕಂದು ಅಂಚಿನ ವಜ್ರಾಕಾರದ ಗಾಯಗಳು. ಕುತ್ತಿಗೆ ಬ್ಲಾಸ್ಟ್‌ನಿಂದ ತೆನೆ ಬೀಳುತ್ತದೆ.',
        'Water-soaked yellowish stripes on leaf margins turning white/grey. Milky bacterial ooze in early morning.': 'ಎಲೆಯ ಅಂಚಿನಲ್ಲಿ ಹಳದಿ ಪಟ್ಟೆಗಳು ಬಿಳಿ/ಬೂದು ಆಗುತ್ತವೆ. ಬೆಳಿಗ್ಗೆ ಹಾಲಿನಂತಹ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸ್ರಾವ.',
        'Oval brown spots with grey center on leaves, glumes, and leaf sheaths.': 'ಎಲೆಗಳ ಮೇಲೆ ಬೂದು ಕೇಂದ್ರವಿರುವ ಅಂಡಾಕಾರದ ಕಂದು ಚುಕ್ಕೆಗಳು.',
        'Small black powdery smut spots (sori) on leaves. Spots rupture releasing dark spores.': 'ಎಲೆಗಳ ಮೇಲೆ ಕಪ್ಪು ಹುಡಿ ಚುಕ್ಕೆಗಳು. ಒಡೆದು ಕಪ್ಪು ಬೀಜಕಗಳನ್ನು ಬಿಡುಗಡೆ ಮಾಡುತ್ತವೆ.',
        'Zonate lesions starting from leaf tips with alternating light and dark brown bands.': 'ಎಲೆಯ ತುದಿಯಿಂದ ಹಗುರ ಮತ್ತು ಗಾಢ ಕಂದು ಪಟ್ಟೆಗಳ ಗಾಯಗಳು.',
        'Yellow to orange discoloration of leaves from tip downward. Stunted growth with reduced tillering.': 'ಎಲೆಗಳ ತುದಿಯಿಂದ ಕೆಳಕ್ಕೆ ಹಳದಿ-ಕಿತ್ತಳೆ ಬಣ್ಣ ಬದಲಾವಣೆ. ಕುಂಠಿತ ಬೆಳವಣಿಗೆ.',
        'Dark sunken circular lesions with concentric rings on fruits. Fruits shrivel and drop prematurely.': 'ಹಣ್ಣುಗಳ ಮೇಲೆ ಕೇಂದ್ರೀಕೃತ ವಲಯಗಳ ಗಾಢ ಗುಳಿಬಿದ್ದ ಗೋಲಾಕಾರ ಗಾಯಗಳು. ಹಣ್ಣುಗಳು ಸುಕ್ಕಾಗಿ ಬೀಳುತ್ತವೆ.',
        'Yellow-orange powdery spots (urediniospores) on the underside of leaves. Severe defoliation.': 'ಎಲೆಗಳ ಕೆಳಭಾಗದಲ್ಲಿ ಹಳದಿ-ಕಿತ್ತಳೆ ಹುಡಿ ಚುಕ್ಕೆಗಳು. ತೀವ್ರ ಎಲೆ ಉದುರುವಿಕೆ.',
        'Tiny red/brown mites on leaf underside causing bronzing and stippling. Leaves become pale and dry.': 'ಎಲೆಯ ಕೆಳಭಾಗದಲ್ಲಿ ಸಣ್ಣ ಕೆಂಪು/ಕಂದು ಹುಳುಗಳು. ಎಲೆಗಳು ಮಸುಕಾಗಿ ಒಣಗುತ್ತವೆ.',
        'The paddy plant appears healthy with no visible signs of disease.': 'ಭತ್ತದ ಗಿಡ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತಿದೆ, ರೋಗದ ಯಾವುದೇ ಲಕ್ಷಣಗಳಿಲ್ಲ.',
        'The chilli plant appears healthy with no visible signs of disease.': 'ಮೆಣಸಿನಕಾಯಿ ಗಿಡ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತಿದೆ, ರೋಗದ ಯಾವುದೇ ಲಕ್ಷಣಗಳಿಲ್ಲ.',
        'The coffee plant appears healthy with no visible signs of disease.': 'ಕಾಫಿ ಗಿಡ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತಿದೆ, ರೋಗದ ಯಾವುದೇ ಲಕ್ಷಣಗಳಿಲ್ಲ.',
        # Recommendations
        'Spray Tricyclazole 75% WP (0.6 g/L) or Isoprothiolane 40% EC (1.5 ml/L). Use resistant varieties like IR-64, CO-39.': 'ಟ್ರೈಸೈಕ್ಲಾಜೋಲ್ 75% WP (0.6 ಗ್ರಾ/ಲೀ) ಅಥವಾ ಐಸೊಪ್ರೊಥಿಯೊಲೇನ್ 40% EC (1.5 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. IR-64, CO-39 ನಂತಹ ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ.',
        'Spray Streptomycin sulphate + Copper oxychloride 50% WP (2.5 g/L). Use disease-free seeds and resistant varieties.': 'ಸ್ಟ್ರೆಪ್ಟೋಮೈಸಿನ್ ಸಲ್ಫೇಟ್ + ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ 50% WP (2.5 ಗ್ರಾ/ಲೀ) ಸಿಂಪಡಿಸಿ. ರೋಗಮುಕ್ತ ಬೀಜ ಮತ್ತು ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ.',
        'Spray Mancozeb 75% WP (2.5 g/L). Apply potassium fertilizer (60 kg K₂O/ha). Use resistant varieties.': 'ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP (2.5 ಗ್ರಾ/ಲೀ) ಸಿಂಪಡಿಸಿ. ಪೊಟ್ಯಾಸಿಯಂ ಗೊಬ್ಬರ (60 ಕೆಜಿ K₂O/ಹೆ.) ಹಾಕಿ.',
        'Spray Propiconazole 25% EC (1 ml/L) or Mancozeb 75% WP (2.5 g/L). Remove and destroy infected debris.': 'ಪ್ರೊಪಿಕೊನಾಜೋಲ್ 25% EC (1 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP (2.5 ಗ್ರಾ/ಲೀ) ಸಿಂಪಡಿಸಿ. ಸೋಂಕಿತ ಅವಶೇಷಗಳನ್ನು ನಾಶಮಾಡಿ.',
        'Spray Mancozeb 75% WP (2.5 g/L) or Carbendazim 50% WP (1 g/L). Avoid excess nitrogen. Use balanced fertilization.': 'ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP (2.5 ಗ್ರಾ/ಲೀ) ಅಥವಾ ಕಾರ್ಬೆಂಡಾಜಿಮ್ 50% WP (1 ಗ್ರಾ/ಲೀ) ಸಿಂಪಡಿಸಿ. ಹೆಚ್ಚಿನ ಸಾರಜನಕ ಬಳಸಬೇಡಿ.',
        'Control leafhopper vector with Imidacloprid 17.8% SL (0.5 ml/L). Use resistant varieties. No direct chemical cure.': 'ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ 17.8% SL (0.5 ಮಿಲೀ/ಲೀ) ಮೂಲಕ ಜಿಗಿಹುಳು ನಿಯಂತ್ರಿಸಿ. ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ. ನೇರ ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ ಇಲ್ಲ.',
        'Spray Mancozeb 75% WP (2.5 g/L) + Carbendazim 50% WP (1 g/L) alternately at 15-day intervals. Use disease-free seeds.': 'ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP + ಕಾರ್ಬೆಂಡಾಜಿಮ್ 50% WP ಅನ್ನು 15 ದಿನಗಳ ಮಧ್ಯಂತರದಲ್ಲಿ ಪರ್ಯಾಯವಾಗಿ ಸಿಂಪಡಿಸಿ. ರೋಗಮುಕ್ತ ಬೀಜ ಬಳಸಿ.',
        'Spray Tridemorph 80% EC (0.5 ml/L) or Propiconazole 25% EC (0.5 ml/L). Maintain 40-50% shade.': 'ಟ್ರೈಡೆಮಾರ್ಫ್ 80% EC (0.5 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಪ್ರೊಪಿಕೊನಾಜೋಲ್ 25% EC (0.5 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. 40-50% ನೆರಳು ಕಾಪಾಡಿ.',
        'Spray Dicofol 18.5% EC (2.5 ml/L) or wettable sulphur (3 g/L). Maintain shade and humidity. Release predatory mites.': 'ಡೈಕೋಫಾಲ್ 18.5% EC (2.5 ಮಿಲೀ/ಲೀ) ಅಥವಾ ನೆನೆಯುವ ಗಂಧಕ (3 ಗ್ರಾ/ಲೀ) ಸಿಂಪಡಿಸಿ. ನೆರಳು ಮತ್ತು ತೇವಾಂಶ ಕಾಪಾಡಿ.',
        'Continue regular care: maintain proper water levels, apply balanced NPK fertilizer, and monitor for pests.': 'ನಿಯಮಿತ ಆರೈಕೆ ಮುಂದುವರಿಸಿ: ಸರಿಯಾದ ನೀರಿನ ಮಟ್ಟ ಕಾಪಾಡಿ, ಸಮತೋಲಿತ NPK ಗೊಬ್ಬರ ಹಾಕಿ, ಕೀಟಗಳನ್ನು ಗಮನಿಸಿ.',
        'Continue regular care: water adequately, apply balanced NPK fertilizer, and monitor for pests.': 'ನಿಯಮಿತ ಆರೈಕೆ ಮುಂದುವರಿಸಿ: ಸಾಕಷ್ಟು ನೀರು ಕೊಡಿ, ಸಮತೋಲಿತ NPK ಗೊಬ್ಬರ ಹಾಕಿ, ಕೀಟಗಳನ್ನು ಗಮನಿಸಿ.',
        'Continue regular care: maintain 40-50% shade, apply organic mulch, and monitor for pests.': 'ನಿಯಮಿತ ಆರೈಕೆ ಮುಂದುವರಿಸಿ: 40-50% ನೆರಳು ಕಾಪಾಡಿ, ಸಾವಯವ ಮಲ್ಚ್ ಹಾಕಿ, ಕೀಟಗಳನ್ನು ಗಮನಿಸಿ.',
    }
}


def _translate_result(result, lang):
    """Translate a prediction result dict to the given language."""
    if lang == 'en' or lang not in DISEASE_TRANSLATIONS:
        return result
    tr = DISEASE_TRANSLATIONS[lang]
    return {
        'crop': tr.get(result['crop'], result['crop']),
        'disease': tr.get(result['disease'], result['disease']),
        'confidence': result['confidence'],
        'description': tr.get(result['description'], result['description']),
        'recommendation': tr.get(result['recommendation'], result['recommendation']),
        'severity': tr.get(result['severity'], result['severity']),
        'severity_class': result['severity'].lower(),  # English for CSS class
    }


# ================================================================
# Build result dict from a disease name
# ================================================================
def _build_result(disease_name, confidence):
    """Create a prediction result dict from DISEASE_KNOWLEDGE or fallback."""
    info = DISEASE_KNOWLEDGE.get(disease_name, {})
    if info:
        return {
            'crop': info['crop'],
            'disease': info['disease'],
            'confidence': round(min(confidence, 1.0), 4),
            'description': info['description'],
            'recommendation': info['recommendation'],
            'severity': info['severity'],
        }
    # Fallback: parse label  "Crop Disease"
    parts = disease_name.replace('_', ' ').split(' ', 1)
    crop = parts[0] if parts else 'Unknown'
    disease = parts[1] if len(parts) > 1 else disease_name
    return {
        'crop': crop,
        'disease': disease,
        'confidence': round(min(confidence, 1.0), 4),
        'description': f'Detected: {disease_name}',
        'recommendation': 'Consult a local agricultural extension officer for treatment guidance.',
        'severity': 'Medium',
    }


# ================================================================
# Main entry point
# ================================================================
def predict_disease(image_path, crop_filter=None, lang='en'):
    """
    Hybrid prediction:
      1. Try CNN model first — CNN always decides the ranking (which disease).
      2. Run color analysis to validate and boost confidence display.
      3. If CNN unavailable → pure color analysis fallback.
      4. Translate results to the requested language.
    """
    if not os.path.exists(image_path):
        return {'success': False, 'error': 'Image file not found'}

    file_size = os.path.getsize(image_path)
    if file_size < 100:
        return {'success': False, 'error': 'Invalid image file'}

    model_available = _load_model()
    method = 'color_analysis'
    cnn_results = []

    # --- CNN predictions ---
    if model_available:
        try:
            cnn_results = _predict_with_cnn(image_path)
        except Exception as e:
            print(f"[AI] CNN prediction error: {e}")

    # --- Color-analysis predictions ---
    color_results = _analyze_colors(image_path, crop_filter)
    color_dict = {name: conf for name, conf in color_results}

    # --- Merge logic ---
    if cnn_results:
        method = 'deep_learning'

        # Apply crop filter to CNN results
        if crop_filter:
            crop_lower = crop_filter.lower()
            filtered_cnn = [(lbl, conf) for lbl, conf in cnn_results
                            if lbl.lower().startswith(crop_lower)]
        else:
            filtered_cnn = cnn_results

        if not filtered_cnn:
            filtered_cnn = cnn_results  # fallback if filter yields nothing

        top_cnn_conf = filtered_cnn[0][1] if filtered_cnn else 0
        predictions = []

        if top_cnn_conf >= 0.40:
            # ---- CNN is confident — trust CNN ranking, boost with color ----
            for label, cnn_conf in filtered_cnn:
                if cnn_conf < 0.01:
                    continue
                color_conf = color_dict.get(label, 0)
                if color_conf > 0:
                    boosted = min(cnn_conf * 2.0 + color_conf * 0.5, 0.98)
                else:
                    boosted = min(cnn_conf * 1.5, 0.90)
                predictions.append(_build_result(label, boosted))
        else:
            # ---- CNN is uncertain — combine CNN + color analysis ----
            # Build combined score: CNN provides signal, color analysis validates
            cnn_dict = {lbl: conf for lbl, conf in filtered_cnn}
            all_labels = set(cnn_dict.keys()) | set(color_dict.keys())

            # Filter to relevant crop if needed
            if crop_filter:
                crop_lower = crop_filter.lower()
                all_labels = {l for l in all_labels if l.lower().startswith(crop_lower)}

            combined = []
            for label in all_labels:
                cnn_score = cnn_dict.get(label, 0)
                color_score = color_dict.get(label, 0)

                if color_score > 0.5 and cnn_score > 0:
                    # Strong color match + CNN agrees → high confidence
                    final = min(cnn_score * 2.5 + color_score * 0.7, 0.97)
                elif color_score > 0.5:
                    # Strong color match, CNN doesn't have it → use color
                    final = color_score * 0.85
                elif cnn_score > 0 and color_score > 0:
                    # Both have it, moderate
                    final = min(cnn_score * 2.0 + color_score * 0.4, 0.95)
                elif cnn_score > 0:
                    # Only CNN has it
                    final = min(cnn_score * 1.5, 0.60)
                else:
                    continue

                if final >= 0.01:
                    combined.append((label, final))

            combined.sort(key=lambda x: x[1], reverse=True)
            predictions = [_build_result(lbl, conf) for lbl, conf in combined]

        # Inject "Healthy" if color strongly detects it and nothing else is high
        if crop_filter:
            healthy_key = f'{crop_filter.capitalize()} Healthy'
            healthy_color_conf = color_dict.get(healthy_key, 0)
            top_prediction_conf = predictions[0]['confidence'] if predictions else 0

            if healthy_color_conf > 0.5 and top_prediction_conf < 0.30:
                predictions.insert(0, _build_result(healthy_key, healthy_color_conf))

        message = 'Analysis complete using deep learning model (MobileNetV2).'

    elif color_results:
        # ---- No CNN — pure color analysis fallback ----
        predictions = [_build_result(name, conf) for name, conf in color_results]
        message = 'Analysis complete using advanced image color analysis.'
    else:
        predictions = []
        message = 'Could not determine disease from the uploaded image.'

    # Translate predictions to requested language
    translated = [_translate_result(p, lang) for p in predictions[:2]]

    # Translate the message
    messages_tr = {
        'hi': {
            'Analysis complete using deep learning model (MobileNetV2).': 'डीप लर्निंग मॉडल (MobileNetV2) का उपयोग करके विश्लेषण पूर्ण।',
            'Analysis complete using advanced image color analysis.': 'उन्नत छवि रंग विश्लेषण का उपयोग करके विश्लेषण पूर्ण।',
            'Could not determine disease from the uploaded image.': 'अपलोड की गई छवि से रोग का निर्धारण नहीं हो सका।',
        },
        'kn': {
            'Analysis complete using deep learning model (MobileNetV2).': 'ಡೀಪ್ ಲರ್ನಿಂಗ್ ಮಾಡೆಲ್ (MobileNetV2) ಬಳಸಿ ವಿಶ್ಲೇಷಣೆ ಪೂರ್ಣ.',
            'Analysis complete using advanced image color analysis.': 'ಸುಧಾರಿತ ಚಿತ್ರ ಬಣ್ಣ ವಿಶ್ಲೇಷಣೆ ಬಳಸಿ ವಿಶ್ಲೇಷಣೆ ಪೂರ್ಣ.',
            'Could not determine disease from the uploaded image.': 'ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರದಿಂದ ರೋಗವನ್ನು ನಿರ್ಧರಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ.',
        }
    }
    if lang in messages_tr and message in messages_tr[lang]:
        message = messages_tr[lang][message]

    return {
        'success': True,
        'method': method,
        'message': message,
        'predictions': translated,
        'image_path': os.path.basename(image_path),
    }


def get_model_info():
    """Return information about the AI model status."""
    model_available = _load_model()
    classes = []
    if _class_labels:
        classes = sorted(set(_class_labels.values()))
    return {
        'model_type': 'CNN (Convolutional Neural Network)',
        'architecture': 'MobileNetV2 with Transfer Learning',
        'input_size': '224x224 RGB',
        'classes': classes,
        'total_classes': len(classes),
        'model_loaded': model_available,
        'model_path': MODEL_PATH,
        'status': 'CNN model active' if model_available else 'Color analysis mode',
    }
