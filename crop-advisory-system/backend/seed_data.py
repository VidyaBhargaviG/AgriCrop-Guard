"""
Seed data for Crop Advisory System
3 Crops: Paddy, Chilli, Coffee
Each crop has 3-5 diseases and 2-3 pests
"""


def seed_database(db, Crop, Disease, Pest):
    """Populate the database with initial crop, disease, and pest data."""

    # Check if data already exists
    if Crop.query.first():
        return

    # ==================== PADDY ====================
    paddy = Crop(
        name="Paddy (Rice)",
        name_hi="धान (चावल)",
        name_kn="ಭತ್ತ (ಅಕ್ಕಿ)",
        scientific_name="Oryza sativa",
        description="Paddy is one of the most important staple food crops, "
                    "cultivated widely in tropical and subtropical regions. "
                    "It requires warm climate (20–37°C) and abundant water supply. "
                    "India is the second-largest producer of rice globally.",
        description_hi="धान सबसे महत्वपूर्ण खाद्य फसलों में से एक है, "
                       "जो उष्णकटिबंधीय और उपोष्णकटिबंधीय क्षेत्रों में व्यापक रूप से उगाई जाती है। "
                       "इसे गर्म जलवायु (20–37°C) और प्रचुर जल आपूर्ति की आवश्यकता होती है। "
                       "भारत विश्व में चावल का दूसरा सबसे बड़ा उत्पादक है।",
        description_kn="ಭತ್ತವು ಅತ್ಯಂತ ಪ್ರಮುಖ ಆಹಾರ ಬೆಳೆಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ, "
                       "ಉಷ್ಣವಲಯ ಮತ್ತು ಉಪೋಷ್ಣವಲಯ ಪ್ರದೇಶಗಳಲ್ಲಿ ವ್ಯಾಪಕವಾಗಿ ಬೆಳೆಯಲಾಗುತ್ತದೆ। "
                       "ಇದಕ್ಕೆ ಬೆಚ್ಚನೆಯ ಹವಾಮಾನ (20–37°C) ಮತ್ತು ಸಮೃದ್ಧ ನೀರಿನ ಪೂರೈಕೆ ಬೇಕು। "
                       "ಭಾರತವು ವಿಶ್ವದಲ್ಲಿ ಅಕ್ಕಿಯ ಎರಡನೇ ಅತಿದೊಡ್ಡ ಉತ್ಪಾದಕ ರಾಷ್ಟ್ರವಾಗಿದೆ.",
        season="Kharif (June–Nov), Rabi/Boro (Nov–May), Summer (Jan–May) in irrigated areas",
        season_hi="खरीफ (जून–नवंबर), रबी/बोरो (नवंबर–मई), ग्रीष्म (जनवरी–मई) सिंचित क्षेत्रों में",
        season_kn="ಖರೀಫ್ (ಜೂನ್–ನವೆಂಬರ್), ರಬಿ/ಬೋರೋ (ನವೆಂಬರ್–ಮೇ), ಬೇಸಿಗೆ (ಜನವರಿ–ಮೇ) ನೀರಾವರಿ ಪ್ರದೇಶಗಳಲ್ಲಿ",
        image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Pana_Banaue_Rice_Terraces_%28Cropped%29.jpg/400px-Pana_Banaue_Rice_Terraces_%28Cropped%29.jpg"
    )
    db.session.add(paddy)
    db.session.flush()

    paddy_diseases = [
        Disease(
            name="Blast Disease",
            name_hi="ब्लास्ट रोग",
            name_kn="ಬ್ಲಾಸ್ಟ್ ರೋಗ",
            crop_id=paddy.id,
            symptoms="Diamond-shaped lesions on leaves with grey or white center and brown border. "
                     "Infected nodes turn black and break. Neck blast causes panicle to fall over.",
            symptoms_hi="पत्तियों पर हीरे के आकार के धब्बे जिनमें भूरे किनारे और सफ़ेद/भूरा केंद्र होता है। "
                        "संक्रमित गांठें काली हो जाती हैं और टूट जाती हैं। गर्दन ब्लास्ट से बालियां गिर जाती हैं।",
            symptoms_kn="ಎಲೆಗಳ ಮೇಲೆ ವಜ್ರಾಕಾರದ ಕಲೆಗಳು, ಬೂದು ಅಥವಾ ಬಿಳಿ ಕೇಂದ್ರ ಮತ್ತು ಕಂದು ಅಂಚು. "
                        "ಸೋಂಕಿತ ಗಂಟುಗಳು ಕಪ್ಪಾಗಿ ಮುರಿಯುತ್ತವೆ. ಕತ್ತಿನ ಬ್ಲಾಸ್ಟ್ ತೆನೆ ಬೀಳಲು ಕಾರಣವಾಗುತ್ತದೆ.",
            cause="Fungus Magnaporthe oryzae; favored by high humidity, low temperature, and excess nitrogen.",
            cause_hi="फफूंद मैग्नापोर्थे ओराइज़ी; अधिक आर्द्रता, कम तापमान और अधिक नाइट्रोजन से फैलता है।",
            cause_kn="ಶಿಲೀಂಧ್ರ ಮ್ಯಾಗ್ನಪೋರ್ಥೆ ಒರೈಜೇ; ಹೆಚ್ಚಿನ ತೇವಾಂಶ, ಕಡಿಮೆ ತಾಪಮಾನ ಮತ್ತು ಹೆಚ್ಚಿನ ಸಾರಜನಕದಿಂದ ಹರಡುತ್ತದೆ.",
            prevention="Use resistant varieties (e.g., CO-39, IR-64). Avoid excessive nitrogen fertilizer. "
                       "Maintain proper spacing. Remove and destroy infected crop residues.",
            prevention_hi="प्रतिरोधी किस्मों का उपयोग करें (जैसे CO-39, IR-64)। अत्यधिक नाइट्रोजन उर्वरक से बचें। "
                          "उचित दूरी बनाए रखें। संक्रमित फसल अवशेषों को हटाकर नष्ट करें।",
            prevention_kn="ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ (ಉದಾ., CO-39, IR-64). ಅತಿಯಾದ ಸಾರಜನಕ ಗೊಬ್ಬರ ಬಳಸಬೇಡಿ. "
                          "ಸರಿಯಾದ ಅಂತರ ಕಾಪಾಡಿ. ಸೋಂಕಿತ ಬೆಳೆ ಅವಶೇಷಗಳನ್ನು ತೆಗೆದು ನಾಶಮಾಡಿ.",
            organic_treatment="Apply Trichoderma viride (5g/kg seed) as seed treatment. "
                              "Spray Pseudomonas fluorescens (10g/L). Use neem oil spray (5ml/L).",
            organic_treatment_hi="बीज उपचार के रूप में ट्राइकोडर्मा विरिडी (5 ग्राम/किग्रा बीज) लगाएं। "
                                 "स्यूडोमोनास फ्लोरेसेंस (10 ग्राम/लीटर) का छिड़काव करें। नीम तेल (5 मिली/लीटर) का उपयोग करें।",
            organic_treatment_kn="ಬೀಜೋಪಚಾರಕ್ಕೆ ಟ್ರೈಕೋಡರ್ಮಾ ವಿರಿಡೆ (5 ಗ್ರಾಂ/ಕೆಜಿ ಬೀಜ) ಹಾಕಿ. "
                                 "ಸ್ಯೂಡೋಮೋನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ (10 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. ಬೇವಿನ ಎಣ್ಣೆ (5 ಮಿಲೀ/ಲೀ) ಬಳಸಿ.",
            chemical_treatment="Spray Tricyclazole 75% WP (0.6g/L) or Isoprothiolane 40% EC (1.5ml/L). "
                               "Apply Carbendazim 50% WP (1g/L) at boot leaf stage.",
            chemical_treatment_hi="ट्राइसाइक्लाज़ोल 75% WP (0.6 ग्राम/लीटर) या आइसोप्रोथियोलेन 40% EC (1.5 मिली/ली) का छिड़काव करें। "
                                  "बूट लीफ अवस्था में कार्बेन्डाज़िम 50% WP (1 ग्राम/ली) लगाएं।",
            chemical_treatment_kn="ಟ್ರೈಸೈಕ್ಲಜೋಲ್ 75% WP (0.6 ಗ್ರಾಂ/ಲೀ) ಅಥವಾ ಐಸೋಪ್ರೊಥಿಯೋಲೇನ್ 40% EC (1.5 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಬೂಟ್ ಲೀಫ್ ಹಂತದಲ್ಲಿ ಕಾರ್ಬೆಂಡಜಿಮ್ 50% WP (1 ಗ್ರಾಂ/ಲೀ) ಹಾಕಿ.",
            chemical_composition="Tricyclazole (C₉H₇N₃S): Systemic fungicide inhibiting melanin biosynthesis. "
                                 "Carbendazim (C₉H₉N₃O₂): Broad-spectrum benzimidazole fungicide.",
            chemical_composition_hi="ट्राइसाइक्लाज़ोल (C₉H₇N₃S): मेलेनिन जैवसंश्लेषण को रोकने वाला प्रणालीगत कवकनाशी। "
                                    "कार्बेन्डाज़िम (C₉H₉N₃O₂): व्यापक-स्पेक्ट्रम बेंज़िमिडाज़ोल कवकनाशी।",
            chemical_composition_kn="ಟ್ರೈಸೈಕ್ಲಜೋಲ್ (C₉H₇N₃S): ಮೆಲನಿನ್ ಜೈವ ಸಂಶ್ಲೇಷಣೆಯನ್ನು ತಡೆಯುವ ವ್ಯವಸ್ಥಿತ ಶಿಲೀಂಧ್ರನಾಶಕ. "
                                    "ಕಾರ್ಬೆಂಡಜಿಮ್ (C₉H₉N₃O₂): ವಿಶಾಲ-ವ್ಯಾಪ್ತಿಯ ಬೆಂಜಿಮಿಡಜೋಲ್ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Rice_blast_Magnaporthe_grisea.jpg/400px-Rice_blast_Magnaporthe_grisea.jpg"
        ),
        Disease(
            name="Bacterial Leaf Blight",
            name_hi="जीवाणु पत्ती झुलसा",
            name_kn="ಬ್ಯಾಕ್ಟೀರಿಯಾ ಎಲೆ ಸುಡು ರೋಗ",
            crop_id=paddy.id,
            symptoms="Water-soaked, yellowish stripes on leaf margins that enlarge and turn white/grey. "
                     "Leaves dry up from tip to base. Milky bacterial ooze in early morning.",
            symptoms_hi="पत्ती के किनारों पर पानी भरी पीली धारियां जो बड़ी होकर सफ़ेद/भूरी हो जाती हैं। "
                        "पत्तियां सिरे से आधार तक सूख जाती हैं। सुबह दूधिया जीवाणु स्राव दिखता है।",
            symptoms_kn="ಎಲೆಯ ಅಂಚುಗಳಲ್ಲಿ ನೀರು ತುಂಬಿದ ಹಳದಿ ಪಟ್ಟೆಗಳು, ಅವು ದೊಡ್ಡದಾಗಿ ಬಿಳಿ/ಬೂದುಬಣ್ಣಕ್ಕೆ ತಿರುಗುತ್ತವೆ. "
                        "ಎಲೆಗಳು ತುದಿಯಿಂದ ಬುಡಕ್ಕೆ ಒಣಗುತ್ತವೆ. ಬೆಳಿಗ್ಗೆ ಹಾಲಿನಂತಹ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸ್ರಾವ ಕಾಣುತ್ತದೆ.",
            cause="Bacterium Xanthomonas oryzae pv. oryzae; spreads through wind, rain, and contaminated irrigation.",
            cause_hi="जीवाणु ज़ैंथोमोनास ओराइज़ी; हवा, बारिश और दूषित सिंचाई से फैलता है।",
            cause_kn="ಬ್ಯಾಕ್ಟೀರಿಯಾ ಕ್ಸಾಂಥೋಮೋನಾಸ್ ಒರೈಜೇ; ಗಾಳಿ, ಮಳೆ ಮತ್ತು ಕಲುಷಿತ ನೀರಾವರಿಯಿಂದ ಹರಡುತ್ತದೆ.",
            prevention="Use certified disease-free seeds. Grow resistant varieties (e.g., Improved Samba Mahsuri). "
                       "Avoid clipping seedling tips during transplanting. Balanced fertilization.",
            prevention_hi="प्रमाणित रोगमुक्त बीजों का उपयोग करें। प्रतिरोधी किस्में उगाएं (जैसे इम्प्रूव्ड सांबा महसूरी)। "
                          "रोपाई के दौरान पौध की नोक काटने से बचें। संतुलित उर्वरक दें।",
            prevention_kn="ಪ್ರಮಾಣಿತ ರೋಗಮುಕ್ತ ಬೀಜಗಳನ್ನು ಬಳಸಿ. ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬೆಳೆಸಿ (ಉದಾ., ಇಂಪ್ರೂವ್ಡ್ ಸಾಂಬ ಮಹಸೂರಿ). "
                          "ನಾಟಿ ಮಾಡುವಾಗ ಸಸಿ ತುದಿಗಳನ್ನು ಕತ್ತರಿಸಬೇಡಿ. ಸಮತೋಲಿತ ಗೊಬ್ಬರ ಕೊಡಿ.",
            organic_treatment="Spray neem oil (5ml/L) mixed with Pseudomonas fluorescens. "
                              "Apply fermented buttermilk spray (10% concentration).",
            organic_treatment_hi="नीम तेल (5 मिली/लीटर) को स्यूडोमोनास फ्लोरेसेंस के साथ मिलाकर छिड़काव करें। "
                                 "किण्वित छाछ (10% सांद्रता) का छिड़काव करें।",
            organic_treatment_kn="ಬೇವಿನ ಎಣ್ಣೆ (5 ಮಿಲೀ/ಲೀ) ಅನ್ನು ಸ್ಯೂಡೋಮೋನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ ಜೊತೆ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ. "
                                 "ಹುದುಗಿಸಿದ ಮಜ್ಜಿಗೆ (10% ಸಾಂದ್ರತೆ) ಸಿಂಪಡಿಸಿ.",
            chemical_treatment="Spray Streptomycin sulphate + Tetracycline (300g/ha) mixed with Copper oxychloride 50% WP (2.5g/L). "
                               "Soak seeds in Agrimycin-100 (0.025%) for 12 hours.",
            chemical_treatment_hi="स्ट्रेप्टोमाइसिन सल्फेट + टेट्रासाइक्लिन (300 ग्राम/हे.) को कॉपर ऑक्सीक्लोराइड 50% WP (2.5 ग्राम/ली) के साथ मिलाकर छिड़काव करें। "
                                  "बीजों को एग्रीमाइसिन-100 (0.025%) में 12 घंटे भिगोएं।",
            chemical_treatment_kn="ಸ್ಟ್ರೆಪ್ಟೋಮೈಸಿನ್ ಸಲ್ಫೇಟ್ + ಟೆಟ್ರಾಸೈಕ್ಲಿನ್ (300 ಗ್ರಾಂ/ಹೆ.) ಅನ್ನು ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ 50% WP (2.5 ಗ್ರಾಂ/ಲೀ) ಜೊತೆ ಬೆರೆಸಿ ಸಿಂಪಡಿಸಿ. "
                                  "ಬೀಜಗಳನ್ನು ಅಗ್ರಿಮೈಸಿನ್-100 (0.025%) ನಲ್ಲಿ 12 ಗಂಟೆ ನೆನೆಸಿ.",
            chemical_composition="Streptomycin (C₂₁H₃₉N₇O₁₂): Aminoglycoside antibiotic. "
                                 "Copper oxychloride (3Cu(OH)₂·CuCl₂): Protective copper fungicide/bactericide.",
            chemical_composition_hi="स्ट्रेप्टोमाइसिन (C₂₁H₃₉N₇O₁₂): एमिनोग्लाइकोसाइड एंटीबायोटिक। "
                                    "कॉपर ऑक्सीक्लोराइड (3Cu(OH)₂·CuCl₂): सुरक्षात्मक तांबा कवकनाशी/जीवाणुनाशक।",
            chemical_composition_kn="ಸ್ಟ್ರೆಪ್ಟೋಮೈಸಿನ್ (C₂₁H₃₉N₇O₁₂): ಅಮಿನೋಗ್ಲೈಕೋಸೈಡ್ ಪ್ರತಿಜೀವಕ. "
                                    "ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ (3Cu(OH)₂·CuCl₂): ರಕ್ಷಣಾತ್ಮಕ ತಾಮ್ರ ಶಿಲೀಂಧ್ರನಾಶಕ/ಬ್ಯಾಕ್ಟೀರಿಯಾನಾಶಕ.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Bacterial_blight_of_rice.jpeg/400px-Bacterial_blight_of_rice.jpeg"
        ),
        Disease(
            name="Sheath Blight",
            name_hi="शीथ ब्लाइट",
            name_kn="ಪೊರೆ ಸುಡು ರೋಗ",
            crop_id=paddy.id,
            symptoms="Oval or irregular greenish-grey lesions on leaf sheaths near water level. "
                     "Lesions enlarge and coalesce causing blighted appearance. "
                     "White fungal mycelium visible on lesions in humid conditions.",
            symptoms_hi="जल स्तर के पास पत्ती के म्यान पर अंडाकार या अनियमित हरे-भूरे धब्बे। "
                        "धब्बे बड़े होकर मिल जाते हैं जिससे झुलसा दिखाई देता है। "
                        "नम परिस्थितियों में धब्बों पर सफ़ेद कवक माइसीलियम दिखाई देता है।",
            symptoms_kn="ನೀರಿನ ಮಟ್ಟದ ಬಳಿ ಎಲೆ ಪೊರೆಗಳ ಮೇಲೆ ಅಂಡಾಕಾರ ಅಥವಾ ಅನಿಯಮಿತ ಹಸಿರು-ಬೂದು ಕಲೆಗಳು. "
                        "ಕಲೆಗಳು ದೊಡ್ಡದಾಗಿ ಸೇರಿಕೊಂಡು ಸುಟ್ಟಂತೆ ಕಾಣುತ್ತವೆ. "
                        "ತೇವಾಂಶ ಪರಿಸ್ಥಿತಿಗಳಲ್ಲಿ ಕಲೆಗಳ ಮೇಲೆ ಬಿಳಿ ಶಿಲೀಂಧ್ರ ಮೈಸೀಲಿಯಂ ಕಾಣುತ್ತದೆ.",
            cause="Fungus Rhizoctonia solani; favored by dense planting, high nitrogen, and warm humid weather.",
            cause_hi="फफूंद रिज़ोक्टोनिया सोलानी; सघन रोपण, अधिक नाइट्रोजन और गर्म आर्द्र मौसम से फैलता है।",
            cause_kn="ಶಿಲೀಂಧ್ರ ರೈಜೋಕ್ಟೋನಿಯಾ ಸೋಲಾನಿ; ದಟ್ಟ ನಾಟಿ, ಹೆಚ್ಚಿನ ಸಾರಜನಕ ಮತ್ತು ಬೆಚ್ಚಗಿನ ತೇವ ಹವಾಮಾನದಿಂದ ಹರಡುತ್ತದೆ.",
            prevention="Avoid dense planting — maintain 20×15cm spacing. "
                       "Use balanced NPK fertilization. Remove weed hosts. Drain fields periodically.",
            prevention_hi="सघन रोपण से बचें — 20×15 सेमी दूरी बनाए रखें। "
                          "संतुलित NPK उर्वरक का उपयोग करें। खरपतवार हटाएं। खेतों से समय-समय पर पानी निकालें।",
            prevention_kn="ದಟ್ಟ ನಾಟಿ ಮಾಡಬೇಡಿ — 20×15 ಸೆಂ.ಮೀ ಅಂತರ ಕಾಪಾಡಿ. "
                          "ಸಮತೋಲಿತ NPK ಗೊಬ್ಬರ ಬಳಸಿ. ಕಳೆ ಆಶ್ರಯದಾತರನ್ನು ತೆಗೆಯಿರಿ. ಹೊಲಗಳಿಂದ ನಿಯಮಿತವಾಗಿ ನೀರು ಬಸಿಯಿರಿ.",
            organic_treatment="Apply Trichoderma harzianum (2.5 kg/ha) to soil. "
                              "Spray Pseudomonas fluorescens (10g/L). Use neem cake at 150 kg/ha.",
            organic_treatment_hi="मिट्टी में ट्राइकोडर्मा हार्ज़ियानम (2.5 किग्रा/हे.) डालें। "
                                 "स्यूडोमोनास फ्लोरेसेंस (10 ग्राम/लीटर) का छिड़काव करें। नीम की खली 150 किग्रा/हे. उपयोग करें।",
            organic_treatment_kn="ಮಣ್ಣಿಗೆ ಟ್ರೈಕೋಡರ್ಮಾ ಹರ್ಜಿಯಾನಮ್ (2.5 ಕೆಜಿ/ಹೆ.) ಹಾಕಿ. "
                                 "ಸ್ಯೂಡೋಮೋನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ (10 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. ಬೇವಿನ ಹಿಂಡಿ 150 ಕೆಜಿ/ಹೆ. ಬಳಸಿ.",
            chemical_treatment="Spray Validamycin 3% SL (2.5ml/L) or Hexaconazole 5% EC (2ml/L). "
                               "Apply Propiconazole 25% EC (1ml/L) at tillering stage.",
            chemical_treatment_hi="वैलिडामाइसिन 3% SL (2.5 मिली/ली) या हेक्साकोनाज़ोल 5% EC (2 मिली/ली) का छिड़काव करें। "
                                  "टिलरिंग अवस्था में प्रोपिकोनाज़ोल 25% EC (1 मिली/ली) लगाएं।",
            chemical_treatment_kn="ವ್ಯಾಲಿಡಾಮೈಸಿನ್ 3% SL (2.5 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಹೆಕ್ಸಾಕೋನಜೋಲ್ 5% EC (2 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ತಿಲ್ಲರಿಂಗ್ ಹಂತದಲ್ಲಿ ಪ್ರೊಪಿಕೋನಜೋಲ್ 25% EC (1 ಮಿಲೀ/ಲೀ) ಹಾಕಿ.",
            chemical_composition="Validamycin (C₂₀H₃₅NO₁₃): Antibiotic targeting trehalase enzyme. "
                                 "Hexaconazole (C₁₄H₁₇Cl₂N₃O): Triazole systemic fungicide.",
            chemical_composition_hi="वैलिडामाइसिन (C₂₀H₃₅NO₁₃): ट्रीहैलेज़ एंजाइम को लक्षित करने वाला एंटीबायोटिक। "
                                    "हेक्साकोनाज़ोल (C₁₄H₁₇Cl₂N₃O): ट्राइएज़ोल प्रणालीगत कवकनाशी।",
            chemical_composition_kn="ವ್ಯಾಲಿಡಾಮೈಸಿನ್ (C₂₀H₃₅NO₁₃): ಟ್ರೆಹಲೇಸ್ ಕಿಣ್ವವನ್ನು ಗುರಿಯಾಗಿಸುವ ಪ್ರತಿಜೀವಕ. "
                                    "ಹೆಕ್ಸಾಕೋನಜೋಲ್ (C₁₄H₁₇Cl₂N₃O): ಟ್ರೈಅಜೋಲ್ ವ್ಯವಸ್ಥಿತ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="Medium",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/RiceSheathArk.jpg/400px-RiceSheathArk.jpg"
        ),
        Disease(
            name="Brown Spot",
            name_hi="भूरा धब्बा",
            name_kn="ಕಂದು ಕಲೆ ರೋಗ",
            crop_id=paddy.id,
            symptoms="Oval brown spots with grey center on leaves, glumes, and leaf sheaths. "
                     "Spots may coalesce causing large blighted areas. Seeds become discolored.",
            symptoms_hi="पत्तियों, शूलों और पत्ती की म्यान पर भूरे केंद्र वाले अंडाकार भूरे धब्बे। "
                        "धब्बे मिलकर बड़े झुलसे क्षेत्र बना सकते हैं। बीज रंगहीन हो जाते हैं।",
            symptoms_kn="ಎಲೆಗಳು, ಹೂಗಳು ಮತ್ತು ಎಲೆ ಪೊರೆಗಳ ಮೇಲೆ ಬೂದು ಕೇಂದ್ರದ ಅಂಡಾಕಾರ ಕಂದು ಕಲೆಗಳು. "
                        "ಕಲೆಗಳು ಸೇರಿಕೊಂಡು ದೊಡ್ಡ ಸುಟ್ಟ ಪ್ರದೇಶಗಳಾಗುತ್ತವೆ. ಬೀಜಗಳು ಬಣ್ಣ ಕಳೆದುಕೊಳ್ಳುತ್ತವೆ.",
            cause="Fungus Bipolaris oryzae (Helminthosporium oryzae); associated with nutrient-deficient soils, "
                  "particularly potassium and silicon deficiency.",
            cause_hi="फफूंद बाइपोलेरिस ओराइज़ी; पोषक तत्वों की कमी वाली मिट्टी, विशेषकर पोटाश और सिलिकॉन की कमी से जुड़ी।",
            cause_kn="ಶಿಲೀಂಧ್ರ ಬೈಪೋಲಾರಿಸ್ ಒರೈಜೇ; ಪೋಷಕಾಂಶ ಕೊರತೆಯ ಮಣ್ಣಿಗೆ ಸಂಬಂಧಿಸಿದೆ, ವಿಶೇಷವಾಗಿ ಪೊಟ್ಯಾಷಿಯಂ ಮತ್ತು ಸಿಲಿಕಾನ್ ಕೊರತೆ.",
            prevention="Apply balanced fertilization, especially potassium (60 kg K₂O/ha). "
                       "Treat seeds with fungicide before sowing. Use resistant varieties.",
            prevention_hi="संतुलित उर्वरक दें, विशेषकर पोटाश (60 किग्रा K₂O/हे.)। "
                          "बुआई से पहले बीजों को कवकनाशी से उपचारित करें। प्रतिरोधी किस्में उपयोग करें।",
            prevention_kn="ಸಮತೋಲಿತ ಗೊಬ್ಬರ ಕೊಡಿ, ವಿಶೇಷವಾಗಿ ಪೊಟ್ಯಾಷಿಯಂ (60 ಕೆಜಿ K₂O/ಹೆ.). "
                          "ಬಿತ್ತನೆ ಮಾಡುವ ಮುನ್ನ ಬೀಜಗಳನ್ನು ಶಿಲೀಂಧ್ರನಾಶಕದಿಂದ ಉಪಚರಿಸಿ. ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ.",
            organic_treatment="Seed treatment with Trichoderma viride (4g/kg). "
                              "Foliar spray of Pseudomonas fluorescens (10g/L). Apply potassium-rich organic manures.",
            organic_treatment_hi="बीज उपचार ट्राइकोडर्मा विरिडी (4 ग्राम/किग्रा) से। "
                                 "स्यूडोमोनास फ्लोरेसेंस (10 ग्राम/ली) का पर्ण छिड़काव। पोटाश समृद्ध जैविक खाद लगाएं।",
            organic_treatment_kn="ಬೀಜ ಉಪಚಾರ ಟ್ರೈಕೋಡರ್ಮಾ ವಿರಿಡೆ (4 ಗ್ರಾಂ/ಕೆಜಿ). "
                                 "ಸ್ಯೂಡೋಮೋನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ (10 ಗ್ರಾಂ/ಲೀ) ಎಲೆ ಸಿಂಪಡಿಸಿ. ಪೊಟ್ಯಾಷಿಯಂ ಸಮೃದ್ಧ ಸಾವಯವ ಗೊಬ್ಬರ ಹಾಕಿ.",
            chemical_treatment="Spray Mancozeb 75% WP (2.5g/L) or Zineb 75% WP (2.5g/L). "
                               "Seed treatment with Carbendazim 50% WP (2g/kg).",
            chemical_treatment_hi="मैंकोज़ेब 75% WP (2.5 ग्राम/ली) या ज़ीनेब 75% WP (2.5 ग्राम/ली) का छिड़काव करें। "
                                  "कार्बेन्डाज़िम 50% WP (2 ग्राम/किग्रा) से बीज उपचार।",
            chemical_treatment_kn="ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP (2.5 ಗ್ರಾಂ/ಲೀ) ಅಥವಾ ಜಿನೆಬ್ 75% WP (2.5 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಕಾರ್ಬೆಂಡಜಿಮ್ 50% WP (2 ಗ್ರಾಂ/ಕೆಜಿ) ಬೀಜ ಉಪಚಾರ.",
            chemical_composition="Mancozeb (C₄H₆MnN₂S₄·Zn): Dithiocarbamate contact fungicide. "
                                 "Zineb (C₄H₆N₂S₄Zn): Multi-site contact fungicide.",
            chemical_composition_hi="मैंकोज़ेब (C₄H₆MnN₂S₄·Zn): डाइथियोकार्बामेट संपर्क कवकनाशी। "
                                    "ज़ीनेब (C₄H₆N₂S₄Zn): बहु-स्थल संपर्क कवकनाशी।",
            chemical_composition_kn="ಮ್ಯಾಂಕೋಜೆಬ್ (C₄H₆MnN₂S₄·Zn): ಡೈಥಿಯೋಕಾರ್ಬಮೇಟ್ ಸಂಪರ್ಕ ಶಿಲೀಂಧ್ರನಾಶಕ. "
                                    "ಜಿನೆಬ್ (C₄H₆N₂S₄Zn): ಬಹು-ಸ್ಥಳ ಸಂಪರ್ಕ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="Medium",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Cochliobolus_miyabeanus.jpg/400px-Cochliobolus_miyabeanus.jpg"
        ),
        Disease(
            name="Tungro Virus Disease",
            name_hi="टुंग्रो वायरस रोग",
            name_kn="ಟಂಗ್ರೋ ವೈರಸ್ ರೋಗ",
            crop_id=paddy.id,
            symptoms="Yellow to orange discoloration of leaves from tip downward. "
                     "Stunted plant growth with reduced tillering. Delayed flowering and incomplete panicle emergence.",
            symptoms_hi="पत्तियों के सिरे से नीचे की ओर पीले से नारंगी रंग परिवर्तन। "
                        "कम कल्लों के साथ पौधे की वृद्धि रुक जाती है। फूल आने में देरी और अपूर्ण बालियों का उदभव।",
            symptoms_kn="ಎಲೆಗಳ ತುದಿಯಿಂದ ಕೆಳಗೆ ಹಳದಿಯಿಂದ ಕಿತ್ತಳೆ ಬಣ್ಣಕ್ಕೆ ಬದಲಾವಣೆ. "
                        "ಕಡಿಮೆ ಕವಲುಗಳೊಂದಿಗೆ ಗಿಡ ಬೆಳವಣಿಗೆ ಕುಂಠಿತ. ಹೂಬಿಡುವಿಕೆ ತಡವಾಗುತ್ತದೆ ಮತ್ತು ಅಪೂರ್ಣ ತೆನೆ ಹೊರಬರುವಿಕೆ.",
            cause="Caused by Rice tungro bacilliform virus (RTBV) and Rice tungro spherical virus (RTSV); "
                  "transmitted by green leafhopper (Nephotettix virescens).",
            cause_hi="धान टुंग्रो बैसिलीफॉर्म वायरस (RTBV) और गोलाकार वायरस (RTSV) के कारण; "
                     "हरे पत्ता फुदके (नेफोटेटिक्स विरेसेंस) द्वारा फैलता है।",
            cause_kn="ಅಕ್ಕಿ ಟಂಗ್ರೋ ಬೆಸಿಲಿಫಾರ್ಮ್ ವೈರಸ್ (RTBV) ಮತ್ತು ಗೋಳಾಕಾರ ವೈರಸ್ (RTSV) ಕಾರಣ; "
                     "ಹಸಿರು ಎಲೆ ಕೀಟ (ನೆಫೋಟೆಟಿಕ್ಸ್ ವಿರೆಸೆನ್ಸ್) ಮೂಲಕ ಹರಡುತ್ತದೆ.",
            prevention="Use resistant varieties (e.g., IR-36, Vikramarya). "
                       "Synchronize planting dates in the community. Control leafhopper vectors early.",
            prevention_hi="प्रतिरोधी किस्में उपयोग करें (जैसे IR-36, विक्रमार्य)। "
                          "समुदाय में रोपण तिथियों को समकालित करें। पत्ता फुदकों को जल्दी नियंत्रित करें।",
            prevention_kn="ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ (ಉದಾ., IR-36, ವಿಕ್ರಮಾರ್ಯ). "
                          "ಸಮುದಾಯದಲ್ಲಿ ನಾಟಿ ದಿನಾಂಕಗಳನ್ನು ಸಮಕಾಲಿಕ ಮಾಡಿ. ಎಲೆ ಕೀಟಗಳನ್ನು ಬೇಗನೆ ನಿಯಂತ್ರಿಸಿ.",
            organic_treatment="Install yellow sticky traps (25/ha) to monitor leafhoppers. "
                              "Spray neem seed kernel extract (NSKE 5%). Remove and destroy infected plants.",
            organic_treatment_hi="पत्ता फुदकों की निगरानी के लिए पीले चिपचिपे जाल (25/हे.) लगाएं। "
                                 "नीम कर्नेल अर्क (NSKE 5%) का छिड़काव करें। संक्रमित पौधों को हटाकर नष्ट करें।",
            organic_treatment_kn="ಎಲೆ ಕೀಟಗಳ ನಿಗಾ ಇಡಲು ಹಳದಿ ಅಂಟಿಕೆ ಜಾಲಗಳು (25/ಹೆ.) ಅಳವಡಿಸಿ. "
                                 "ಬೇವಿನ ಬೀಜದ ಕರ್ನಲ್ ಸಾರ (NSKE 5%) ಸಿಂಪಡಿಸಿ. ಸೋಂಕಿತ ಗಿಡಗಳನ್ನು ತೆಗೆದು ನಾಶಮಾಡಿ.",
            chemical_treatment="Control leafhopper vector: spray Imidacloprid 17.8% SL (0.5ml/L) or "
                               "Thiamethoxam 25% WG (0.3g/L). No direct chemical cure for the virus.",
            chemical_treatment_hi="पत्ता फुदके वाहक नियंत्रण: इमिडाक्लोप्रिड 17.8% SL (0.5 मिली/ली) या "
                                  "थियामेथोक्साम 25% WG (0.3 ग्राम/ली) का छिड़काव करें। वायरस का कोई सीधा रासायनिक उपचार नहीं।",
            chemical_treatment_kn="ಎಲೆ ಕೀಟ ವಾಹಕ ನಿಯಂತ್ರಣ: ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ 17.8% SL (0.5 ಮಿಲೀ/ಲೀ) ಅಥವಾ "
                                  "ಥಿಯಾಮೆಥೊಕ್ಸಾಮ್ 25% WG (0.3 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. ವೈರಸ್ಗೆ ನೇರ ರಾಸಾಯನಿಕ ಉಪಚಾರ ಇಲ್ಲ.",
            chemical_composition="Imidacloprid (C₉H₁₀ClN₅O₂): Neonicotinoid systemic insecticide. "
                                 "Thiamethoxam (C₈H₁₀ClN₅O₃S): Second-generation neonicotinoid.",
            chemical_composition_hi="इमिडाक्लोप्रिड (C₉H₁₀ClN₅O₂): नियोनिकोटिनॉइड प्रणालीगत कीटनाशक। "
                                    "थियामेथोक्साम (C₈H₁₀ClN₅O₃S): दूसरी पीढ़ी का नियोनिकोटिनॉइड।",
            chemical_composition_kn="ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ (C₉H₁₀ClN₅O₂): ನಿಯೋನಿಕೋಟಿನಾಯ್ಡ್ ವ್ಯವಸ್ಥಿತ ಕೀಟನಾಶಕ. "
                                    "ಥಿಯಾಮೆಥೊಕ್ಸಾಮ್ (C₈H₁₀ClN₅O₃S): ಎರಡನೇ ತಲೆಮಾರಿನ ನಿಯೋನಿಕೋಟಿನಾಯ್ಡ್.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Green_leafhopper_%28Nephotettix_virescens%29_UGA5190052.jpg/400px-Green_leafhopper_%28Nephotettix_virescens%29_UGA5190052.jpg"
        )
    ]

    paddy_pests = [
        Pest(
            name="Brown Plant Hopper (BPH)",
            name_hi="भूरा फुदका (बीपीएच)",
            name_kn="ಕಂದು ಗಿಡ ಕೀಟ (ಬಿಪಿಎಚ್)",
            crop_id=paddy.id,
            scientific_name="Nilaparvata lugens",
            symptoms="'Hopper burn' — circular patches of drying and browning in the field. "
                     "Plants turn yellow, then brown, and wilt. Honeydew deposits lead to sooty mold.",
            symptoms_hi="'हॉपर बर्न' — खेत में गोलाकार सूखने और भूरे होने के धब्बे। "
                        "पौधे पीले, फिर भूरे हो जाते हैं और मुरझा जाते हैं। मधुरस जमा से काली फफूंद लगती है।",
            symptoms_kn="'ಹಾಪರ್ ಬರ್ನ್' — ಹೊಲದಲ್ಲಿ ಒಣಗುವ ಮತ್ತು ಕಂದು ಬಣ್ಣಕ್ಕೆ ತಿರುಗುವ ವೃತ್ತಾಕಾರ ಪ್ರದೇಶಗಳು. "
                        "ಗಿಡಗಳು ಹಳದಿ, ನಂತರ ಕಂದು ಬಣ್ಣಕ್ಕೆ ಬದಲಾಗಿ ಬಾಡುತ್ತವೆ. ಮಧುರಸ ಕಪ್ಪು ಬೂಷ್ಟಿಗೆ ಕಾರಣವಾಗುತ್ತದೆ.",
            damage_type="Sap-sucking; causes wilting, drying, and complete crop loss in severe cases.",
            damage_type_hi="रस चूसने वाला; गंभीर मामलों में मुरझाना, सूखना और पूर्ण फसल नुकसान।",
            damage_type_kn="ರಸ ಹೀರುವ; ತೀವ್ರ ಸಂದರ್ಭಗಳಲ್ಲಿ ಒಣಗುವಿಕೆ, ಬಾಡುವಿಕೆ ಮತ್ತು ಸಂಪೂರ್ಣ ಬೆಳೆ ನಷ್ಟ.",
            prevention="Use BPH-resistant varieties. Avoid excessive nitrogen. "
                       "Allow natural enemies (spiders, wasps). Drain fields intermittently.",
            prevention_hi="बीपीएच-प्रतिरोधी किस्में उपयोग करें। अत्यधिक नाइट्रोजन से बचें। "
                          "प्राकृतिक शत्रुओं (मकड़ी, ततैया) को अनुमति दें। खेतों को बीच-बीच में सुखाएं।",
            prevention_kn="BPH-ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ. ಅತಿಯಾದ ಸಾರಜನಕ ಬಳಸಬೇಡಿ. "
                          "ನೈಸರ್ಗಿಕ ಶತ್ರುಗಳಿಗೆ (ಜೇಡ, ಕಣಜ) ಅವಕಾಶ ಕೊಡಿ. ಹೊಲಗಳಿಂದ ನಿಯಮಿತವಾಗಿ ನೀರು ಬಸಿಯಿರಿ.",
            organic_treatment="Release Lycosa pseudoannulata (wolf spider) at 500/ha. "
                              "Spray neem oil (5ml/L). Use light traps to monitor population.",
            organic_treatment_hi="लाइकोसा (भेड़िया मकड़ी) 500/हे. पर छोड़ें। "
                                 "नीम तेल (5 मिली/ली) का छिड़काव करें। आबादी निगरानी के लिए प्रकाश जाल लगाएं।",
            organic_treatment_kn="ಲೈಕೋಸಾ (ತೋಳ ಜೇಡ) 500/ಹೆ. ಬಿಡುಗಡೆ ಮಾಡಿ. "
                                 "ಬೇವಿನ ಎಣ್ಣೆ (5 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. ಜನಸಂಖ್ಯೆ ನಿಗಾಗೆ ಬೆಳಕಿನ ಜಾಲ ಬಳಸಿ.",
            chemical_treatment="Spray Pymetrozine 50% WG (0.6g/L) or Dinotefuran 20% SG (0.5g/L). "
                               "Avoid using synthetic pyrethroids as they cause BPH resurgence.",
            chemical_treatment_hi="पाइमेट्रोज़ीन 50% WG (0.6 ग्राम/ली) या डिनोटेफ्यूरान 20% SG (0.5 ग्राम/ली) छिड़कें। "
                                  "कृत्रिम पाइरेथ्रॉइड्स से बचें क्योंकि वे बीपीएच का पुनरुत्थान करते हैं।",
            chemical_treatment_kn="ಪೈಮೆಟ್ರೋಜಿನ್ 50% WG (0.6 ಗ್ರಾಂ/ಲೀ) ಅಥವಾ ಡಿನೋಟೆಫ್ಯೂರಾನ್ 20% SG (0.5 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಕೃತಕ ಪೈರೆಥ್ರಾಯ್ಡ್ ಬಳಸಬೇಡಿ ಏಕೆಂದರೆ ಅವು BPH ಪುನರುತ್ಥಾನಕ್ಕೆ ಕಾರಣವಾಗುತ್ತವೆ.",
            chemical_composition="Pymetrozine (C₁₀H₁₁N₅O): Selective feeding blocker for Hemiptera.",
            chemical_composition_hi="पाइमेट्रोज़ीन (C₁₀H₁₁N₅O): हेमिप्टेरा के लिए चयनात्मक भोजन अवरोधक।",
            chemical_composition_kn="ಪೈಮೆಟ್ರೋಜಿನ್ (C₁₀H₁₁N₅O): ಹೆಮಿಪ್ಟೆರಾಗೆ ಆಯ್ದ ಆಹಾರ ತಡೆಗಟ್ಟುವಿಕೆ.",
            severity="High",
            active_season="August–October (Kharif); also during Rabi/Boro crop",
            active_season_hi="अगस्त–अक्टूबर (खरीफ); रबी/बोरो फसल के दौरान भी",
            active_season_kn="ಆಗಸ್ಟ್–ಅಕ್ಟೋಬರ್ (ಖರೀಫ್); ರಬಿ/ಬೋರೋ ಬೆಳೆಯ ಸಮಯದಲ್ಲೂ",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Nilaparvata_lugens_439632934.jpg/400px-Nilaparvata_lugens_439632934.jpg"
        ),
        Pest(
            name="Stem Borer",
            name_hi="तना छेदक",
            name_kn="ಕಾಂಡ ಕೊರಕ",
            crop_id=paddy.id,
            scientific_name="Scirpophaga incertulas (Yellow Stem Borer)",
            symptoms="'Dead hearts' in vegetative stage — central shoot dries. "
                     "'White ears' in reproductive stage — panicles emerge white and empty.",
            symptoms_hi="वनस्पति अवस्था में 'डेड हार्ट' — केंद्रीय तना सूख जाता है। "
                        "प्रजनन अवस्था में 'सफ़ेद बाली' — बालियां सफ़ेद और खाली निकलती हैं।",
            symptoms_kn="ತરಕಾರಿ ಹಂತದಲ್ಲಿ 'ಡೆಡ್ ಹಾರ್ಟ್' — ಮಧ್ಯ ಚಿಗುರು ಒಣಗುತ್ತದೆ. "
                        "ಸಂತಾನೋತ್ಪತ್ತಿ ಹಂತದಲ್ಲಿ 'ಬಿಳಿ ತೆನೆ' — ತೆನೆಗಳು ಬಿಳಿಯಾಗಿ ಖಾಲಿಯಾಗಿ ಹೊರಬರುತ್ತವೆ.",
            damage_type="Internal feeder — larvae bore into stems and feed on inner tissues.",
            damage_type_hi="आंतरिक भक्षक — लार्वा तनों में छेद करके आंतरिक ऊतकों को खाते हैं।",
            damage_type_kn="ಆಂತರಿಕ ಹುಳು — ಲಾರ್ವಾ ಕಾಂಡಗಳಲ್ಲಿ ಕೊರೆದು ಒಳ ಅಂಗಾಂಶಗಳನ್ನು ತಿನ್ನುತ್ತದೆ.",
            prevention="Use light traps (1/ha) to monitor moths. Clip and destroy egg masses. "
                       "Harvest at ground level and destroy stubbles. Use early-maturing varieties.",
            prevention_hi="पतंगों की निगरानी के लिए प्रकाश जाल (1/हे.) लगाएं। अंडा समूहों को काटकर नष्ट करें। "
                          "जमीनी स्तर पर कटाई करें और ठूंठ नष्ट करें। जल्दी पकने वाली किस्में उपयोग करें।",
            prevention_kn="ಪತಂಗಗಳ ನಿಗಾಗೆ ಬೆಳಕಿನ ಜಾಲ (1/ಹೆ.) ಅಳವಡಿಸಿ. ಮೊಟ್ಟೆ ಗುಂಪುಗಳನ್ನು ಕತ್ತರಿಸಿ ನಾಶಮಾಡಿ. "
                          "ನೆಲಮಟ್ಟದಲ್ಲಿ ಕೊಯ್ಲು ಮಾಡಿ ಕೂಳೆ ನಾಶಮಾಡಿ. ಬೇಗ ಬೆಳೆಯುವ ತಳಿಗಳನ್ನು ಬಳಸಿ.",
            organic_treatment="Release Trichogramma japonicum (egg parasitoid) at 1 lakh/ha, 6 times at weekly intervals. "
                              "Apply neem cake at 150 kg/ha in standing water.",
            organic_treatment_hi="ट्राइकोग्रामा जैपोनिकम (अंडा परजीवी) 1 लाख/हे. पर 6 बार साप्ताहिक अंतराल पर छोड़ें। "
                                 "खड़े पानी में नीम की खली 150 किग्रा/हे. डालें।",
            organic_treatment_kn="ಟ್ರೈಕೋಗ್ರಾಮಾ ಜಪಾನಿಕಮ್ (ಮೊಟ್ಟೆ ಪರಾವಲಂಬಿ) 1 ಲಕ್ಷ/ಹೆ. ವಾರಕ್ಕೊಮ್ಮೆ 6 ಬಾರಿ ಬಿಡುಗಡೆ ಮಾಡಿ. "
                                 "ನಿಂತ ನೀರಿನಲ್ಲಿ ಬೇವಿನ ಹಿಂಡಿ 150 ಕೆಜಿ/ಹೆ. ಹಾಕಿ.",
            chemical_treatment="Apply Cartap hydrochloride 4G (25 kg/ha) in paddy water. "
                               "Spray Chlorantraniliprole 18.5% SC (0.3ml/L) at egg-laying stage.",
            chemical_treatment_hi="धान के पानी में कार्टैप हाइड्रोक्लोराइड 4G (25 किग्रा/हे.) डालें। "
                                  "अंडा देने की अवस्था में क्लोरैंट्रानिलिप्रोल 18.5% SC (0.3 मिली/ली) छिड़कें।",
            chemical_treatment_kn="ಭತ್ತದ ನೀರಿನಲ್ಲಿ ಕಾರ್ಟ್ಯಾಪ್ ಹೈಡ್ರೋಕ್ಲೋರೈಡ್ 4G (25 ಕೆಜಿ/ಹೆ.) ಹಾಕಿ. "
                                  "ಮೊಟ್ಟೆ ಇಡುವ ಹಂತದಲ್ಲಿ ಕ್ಲೋರಾಂಟ್ರಾನಿಲಿಪ್ರೋಲ್ 18.5% SC (0.3 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ.",
            chemical_composition="Cartap hydrochloride (C₇H₁₅NO₂S₂·HCl): Nereistoxin analogue insecticide. "
                                 "Chlorantraniliprole (C₁₈H₁₄BrCl₂N₅O₂): Ryanodine receptor activator.",
            chemical_composition_hi="कार्टैप हाइड्रोक्लोराइड (C₇H₁₅NO₂S₂·HCl): नेरीस्टॉक्सिन एनालॉग कीटनाशक। "
                                    "क्लोरैंट्रानिलिप्रोल (C₁₈H₁₄BrCl₂N₅O₂): राइनोडीन रिसेप्टर सक्रियक।",
            chemical_composition_kn="ಕಾರ್ಟ್ಯಾಪ್ ಹೈಡ್ರೋಕ್ಲೋರೈಡ್ (C₇H₁₅NO₂S₂·HCl): ನೆರೈಸ್ಟಾಕ್ಸಿನ್ ಅನಲಾಗ್ ಕೀಟನಾಶಕ. "
                                    "ಕ್ಲೋರಾಂಟ್ರಾನಿಲಿಪ್ರೋಲ್ (C₁₈H₁₄BrCl₂N₅O₂): ರಯನೋಡಿನ್ ಗ್ರಾಹಕ ಸಕ್ರಿಯಕ.",
            severity="High",
            active_season="July–November",
            active_season_hi="जुलाई–नवंबर",
            active_season_kn="ಜುಲೈ–ನವೆಂಬರ್",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Scirpophaga_incertulas_female_moth.png/400px-Scirpophaga_incertulas_female_moth.png"
        )
    ]

    # ==================== CHILLI ====================
    chilli = Crop(
        name="Chilli",
        name_hi="मिर्च",
        name_kn="ಮೆಣಸಿನಕಾಯಿ",
        scientific_name="Capsicum annuum",
        description="Chilli is an important spice crop grown extensively in India. "
                    "It is used as a spice, condiment, sauce, and vegetable. "
                    "India is the world's largest producer, consumer, and exporter of chilli. "
                    "Andhra Pradesh, Telangana, Karnataka, and Maharashtra are major producing states.",
        description_hi="मिर्च भारत में व्यापक रूप से उगाई जाने वाली एक महत्वपूर्ण मसाला फसल है। "
                       "इसका उपयोग मसाले, चटनी, सॉस और सब्जी के रूप में किया जाता है। "
                       "भारत विश्व का सबसे बड़ा मिर्च उत्पादक, उपभोक्ता और निर्यातक है। "
                       "आंध्र प्रदेश, तेलंगाना, कर्नाटक और महाराष्ट्र प्रमुख उत्पादक राज्य हैं।",
        description_kn="ಮೆಣಸಿನಕಾಯಿ ಭಾರತದಲ್ಲಿ ವ್ಯಾಪಕವಾಗಿ ಬೆಳೆಯುವ ಪ್ರಮುಖ ಸಂಬಾರ ಬೆಳೆಯಾಗಿದೆ. "
                       "ಇದನ್ನು ಮಸಾಲೆ, ಚಟ್ನಿ, ಸಾಸ್ ಮತ್ತು ತರಕಾರಿಯಾಗಿ ಬಳಸಲಾಗುತ್ತದೆ. "
                       "ಭಾರತವು ವಿಶ್ವದ ಅತಿದೊಡ್ಡ ಮೆಣಸಿನಕಾಯಿ ಉತ್ಪಾದಕ, ಬಳಕೆದಾರ ಮತ್ತು ರಫ್ತುದಾರ ರಾಷ್ಟ್ರ. "
                       "ಆಂಧ್ರ ಪ್ರದೇಶ, ತೆಲಂಗಾಣ, ಕರ್ನಾಟಕ ಮತ್ತು ಮಹಾರಾಷ್ಟ್ರ ಪ್ರಮುಖ ಉತ್ಪಾದಕ ರಾಜ್ಯಗಳು.",
        season="Kharif & Rabi (Year-round in tropical areas)",
        season_hi="खरीफ और रबी (उष्णकटिबंधीय क्षेत्रों में वर्ष भर)",
        season_kn="ಖರೀಫ್ ಮತ್ತು ರಬಿ (ಉಷ್ಣವಲಯ ಪ್ರದೇಶಗಳಲ್ಲಿ ವರ್ಷವಿಡೀ)",
        image_url="https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=400"
    )
    db.session.add(chilli)
    db.session.flush()

    chilli_diseases = [
        Disease(
            name="Anthracnose (Fruit Rot)",
            name_hi="एन्थ्रेक्नोज (फल सड़न)",
            name_kn="ಆಂಥ್ರಾಕ್ನೋಸ್ (ಹಣ್ಣು ಕೊಳೆ)",
            crop_id=chilli.id,
            symptoms="Dark, sunken, circular lesions on ripe fruits with concentric rings. "
                     "Lesions may show salmon-colored spore masses. Fruits shrivel and drop prematurely.",
            symptoms_hi="पके फलों पर गहरे, धंसे, गोलाकार घाव जिनमें संकेंद्रित वलय होते हैं। "
                        "घावों पर सैल्मन रंग के बीजाणु दिख सकते हैं। फल सिकुड़कर समय से पहले गिर जाते हैं।",
            symptoms_kn="ಹಣ್ಣಾದ ಕಾಯಿಗಳ ಮೇಲೆ ಕಪ್ಪು, ಕುಳಿಬಿದ್ದ, ವೃತ್ತಾಕಾರ ಗಾಯಗಳು ಕೇಂದ್ರೀಕೃತ ವಲಯಗಳೊಂದಿಗೆ. "
                        "ಗಾಯಗಳಲ್ಲಿ ಸಾಲ್ಮನ್ ಬಣ್ಣದ ಬೀಜಕ ರಾಶಿಗಳು ಕಾಣಬಹುದು. ಕಾಯಿಗಳು ಸುಕ್ಕಾಗಿ ಅಕಾಲಿಕವಾಗಿ ಉದುರುತ್ತವೆ.",
            cause="Fungus Colletotrichum capsici; spreads through infected seeds, rain splash, and wind.",
            cause_hi="फफूंद कोलेटोट्राइकम कैप्सिकी; संक्रमित बीजों, बारिश के छींटों और हवा से फैलता है।",
            cause_kn="ಶಿಲೀಂಧ್ರ ಕೊಲೆಟೊಟ್ರೈಕಮ್ ಕ್ಯಾಪ್ಸಿಕಿ; ಸೋಂಕಿತ ಬೀಜಗಳು, ಮಳೆ ಸಿಂಪರಣೆ ಮತ್ತು ಗಾಳಿಯ ಮೂಲಕ ಹರಡುತ್ತದೆ.",
            prevention="Use disease-free certified seeds. Practice crop rotation (3-year cycle). "
                       "Avoid overhead irrigation. Remove and destroy infected fruits promptly.",
            prevention_hi="रोगमुक्त प्रमाणित बीज उपयोग करें। फसल चक्र (3 वर्ष) अपनाएं। "
                          "ऊपरी सिंचाई से बचें। संक्रमित फलों को तुरंत हटाकर नष्ट करें।",
            prevention_kn="ರೋಗಮುಕ್ತ ಪ್ರಮಾಣಿತ ಬೀಜಗಳನ್ನು ಬಳಸಿ. ಬೆಳೆ ಆವರ್ತನೆ (3 ವರ್ಷ ಚಕ್ರ) ಅನುಸರಿಸಿ. "
                          "ಮೇಲಿನ ನೀರಾವರಿ ಬಳಸಬೇಡಿ. ಸೋಂಕಿತ ಹಣ್ಣುಗಳನ್ನು ತಕ್ಷಣ ತೆಗೆದು ನಾಶಮಾಡಿ.",
            organic_treatment="Seed treatment with Trichoderma viride (4g/kg). "
                              "Spray Pseudomonas fluorescens (10g/L) at flowering stage. "
                              "Apply neem oil (5ml/L) fortnightly.",
            organic_treatment_hi="ट्राइकोडर्मा विरिडी (4 ग्राम/किग्रा) से बीज उपचार। "
                                 "फूल आने की अवस्था में स्यूडोमोनास फ्लोरेसेंस (10 ग्राम/ली) का छिड़काव। "
                                 "पाक्षिक रूप से नीम तेल (5 मिली/ली) लगाएं।",
            organic_treatment_kn="ಟ್ರೈಕೋಡರ್ಮಾ ವಿರಿಡೆ (4 ಗ್ರಾಂ/ಕೆಜಿ) ಬೀಜ ಉಪಚಾರ. "
                                 "ಹೂಬಿಡುವ ಹಂತದಲ್ಲಿ ಸ್ಯೂಡೋಮೋನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ (10 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                 "ಪಾಕ್ಷಿಕವಾಗಿ ಬೇವಿನ ಎಣ್ಣೆ (5 ಮಿಲೀ/ಲೀ) ಹಾಕಿ.",
            chemical_treatment="Spray Mancozeb 75% WP (2.5g/L) + Carbendazim 50% WP (1g/L) alternately at 15-day intervals. "
                               "Seed treatment with Thiram 75% WP (3g/kg).",
            chemical_treatment_hi="मैंकोज़ेब 75% WP (2.5 ग्राम/ली) + कार्बेन्डाज़िम 50% WP (1 ग्राम/ली) को 15 दिन के अंतराल पर बारी-बारी छिड़कें। "
                                  "थीरम 75% WP (3 ग्राम/किग्रा) से बीज उपचार।",
            chemical_treatment_kn="ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP (2.5 ಗ್ರಾಂ/ಲೀ) + ಕಾರ್ಬೆಂಡಜಿಮ್ 50% WP (1 ಗ್ರಾಂ/ಲೀ) 15 ದಿನ ಅಂತರದಲ್ಲಿ ಪರ್ಯಾಯವಾಗಿ ಸಿಂಪಡಿಸಿ. "
                                  "ಥೈರಮ್ 75% WP (3 ಗ್ರಾಂ/ಕೆಜಿ) ಬೀಜ ಉಪಚಾರ.",
            chemical_composition="Mancozeb (C₄H₆MnN₂S₄·Zn): Multi-site dithiocarbamate fungicide. "
                                 "Carbendazim (C₉H₉N₃O₂): Systemic benzimidazole fungicide.",
            chemical_composition_hi="मैंकोज़ेब (C₄H₆MnN₂S₄·Zn): बहु-स्थल डाइथियोकार्बामेट कवकनाशी। "
                                    "कार्बेन्डाज़िम (C₉H₉N₃O₂): प्रणालीगत बेंज़िमिडाज़ोल कवकनाशी।",
            chemical_composition_kn="ಮ್ಯಾಂಕೋಜೆಬ್ (C₄H₆MnN₂S₄·Zn): ಬಹು-ಸ್ಥಳ ಡೈಥಿಯೋಕಾರ್ಬಮೇಟ್ ಶಿಲೀಂಧ್ರನಾಶಕ. "
                                    "ಕಾರ್ಬೆಂಡಜಿಮ್ (C₉H₉N₃O₂): ವ್ಯವಸ್ಥಿತ ಬೆಂಜಿಮಿಡಜೋಲ್ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Pepper_Disease_in_Tropical_Bonakanda.jpg/400px-Pepper_Disease_in_Tropical_Bonakanda.jpg"
        ),
        Disease(
            name="Powdery Mildew",
            name_hi="चूर्णिल आसिता",
            name_kn="ಬೂದಿ ರೋಗ",
            crop_id=chilli.id,
            symptoms="White powdery fungal growth on upper and lower leaf surfaces. "
                     "Affected leaves curl upward, become chlorotic, and defoliate. Reduced fruit set.",
            symptoms_hi="पत्तियों की ऊपरी और निचली सतह पर सफ़ेद चूर्णी फफूंद वृद्धि। "
                        "प्रभावित पत्तियां ऊपर मुड़ जाती हैं, पीली हो जाती हैं और गिर जाती हैं। फल लगना कम हो जाता है।",
            symptoms_kn="ಎಲೆಗಳ ಮೇಲ್ಮೈ ಮತ್ತು ಕೆಳಮೈ ಮೇಲೆ ಬಿಳಿ ಪುಡಿಯಂತಹ ಶಿಲೀಂಧ್ರ ಬೆಳವಣಿಗೆ. "
                        "ಬಾಧಿತ ಎಲೆಗಳು ಮೇಲಕ್ಕೆ ಮುದುಡಿ, ಹಳದಿಯಾಗಿ ಉದುರುತ್ತವೆ. ಹಣ್ಣು ಕಟ್ಟುವಿಕೆ ಕಡಿಮೆಯಾಗುತ್ತದೆ.",
            cause="Fungus Leveillula taurica; favored by dry weather with moderate temperatures (20-25°C).",
            cause_hi="फफूंद लेवेइलुला टॉरिका; शुष्क मौसम और मध्यम तापमान (20-25°C) से फैलता है।",
            cause_kn="ಶಿಲೀಂಧ್ರ ಲೆವೆಲ್ಲುಲಾ ಟಾರಿಕಾ; ಒಣ ಹವಾಮಾನ ಮತ್ತು ಮಧ್ಯಮ ತಾಪಮಾನ (20-25°C) ದಿಂದ ಹರಡುತ್ತದೆ.",
            prevention="Maintain proper plant spacing for good air circulation. "
                       "Avoid water stress. Remove and destroy infected plant parts.",
            prevention_hi="अच्छी वायु संचार के लिए उचित पौधा दूरी बनाएं। "
                          "जल तनाव से बचें। संक्रमित पौधों के भागों को हटाकर नष्ट करें।",
            prevention_kn="ಉತ್ತಮ ಗಾಳಿ ಸಂಚಾರಕ್ಕೆ ಸರಿಯಾದ ಅಂತರ ಕಾಪಾಡಿ. "
                          "ನೀರಿನ ಒತ್ತಡ ಬರಬೇಡಿ. ಸೋಂಕಿತ ಗಿಡದ ಭಾಗಗಳನ್ನು ತೆಗೆದು ನಾಶಮಾಡಿ.",
            organic_treatment="Spray wettable sulphur (3g/L). Apply milk spray (10% fresh milk in water). "
                              "Dust with fine sulphur powder (25 kg/ha).",
            organic_treatment_hi="घुलनशील गंधक (3 ग्राम/ली) छिड़कें। दूध का छिड़काव (10% ताज़ा दूध पानी में)। "
                                 "बारीक गंधक पाउडर (25 किग्रा/हे.) छिड़कें।",
            organic_treatment_kn="ನೆನೆಯಬಲ್ಲ ಗಂಧಕ (3 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. ಹಾಲಿನ ಸಿಂಪಡಣೆ (10% ತಾಜಾ ಹಾಲು ನೀರಿನಲ್ಲಿ). "
                                 "ಸೂಕ್ಷ್ಮ ಗಂಧಕ ಪುಡಿ (25 ಕೆಜಿ/ಹೆ.) ಉದುರಿಸಿ.",
            chemical_treatment="Spray Dinocap 48% EC (1ml/L) or Hexaconazole 5% EC (2ml/L). "
                               "Alternate with Azoxystrobin 23% SC (1ml/L) to prevent resistance.",
            chemical_treatment_hi="डिनोकैप 48% EC (1 मिली/ली) या हेक्साकोनाज़ोल 5% EC (2 मिली/ली) छिड़कें। "
                                  "प्रतिरोध रोकने के लिए एज़ोक्सिस्ट्रोबिन 23% SC (1 मिली/ली) के साथ बारी-बारी करें।",
            chemical_treatment_kn="ಡೈನೋಕ್ಯಾಪ್ 48% EC (1 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಹೆಕ್ಸಾಕೋನಜೋಲ್ 5% EC (2 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಪ್ರತಿರೋಧ ತಡೆಗೆ ಅಜೋಕ್ಸಿಸ್ಟ್ರೋಬಿನ್ 23% SC (1 ಮಿಲೀ/ಲೀ) ಜೊತೆ ಪರ್ಯಾಯ ಮಾಡಿ.",
            chemical_composition="Dinocap (C₁₈H₂₄N₂O₆): Contact fungicide and acaricide. "
                                 "Azoxystrobin (C₂₂H₁₇N₃O₅): Strobilurin systemic fungicide.",
            chemical_composition_hi="डिनोकैप (C₁₈H₂₄N₂O₆): सम्पर्क कवकनाशी और एकारिसाइड। "
                                    "एज़ोक्सिस्ट्रोबिन (C₂₂H₁₇N₃O₅): स्ट्रोबिलुरिन प्रणालीगत कवकनाशी।",
            chemical_composition_kn="ಡೈನೋಕ್ಯಾಪ್ (C₁₈H₂₄N₂O₆): ಸಂಪರ್ಕ ಶಿಲೀಂಧ್ರನಾಶಕ ಮತ್ತು ಹುಳುನಾಶಕ. "
                                    "ಅಜೋಕ್ಸಿಸ್ಟ್ರೋಬಿನ್ (C₂₂H₁₇N₃O₅): ಸ್ಟ್ರೋಬಿಲ್ಯುರಿನ್ ವ್ಯವಸ್ಥಿತ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="Medium",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Golovinomyces_sordidus_on_Broadleaf_Plantain_-_Plantago_major_%2844171864324%29.jpg/400px-Golovinomyces_sordidus_on_Broadleaf_Plantain_-_Plantago_major_%2844171864324%29.jpg"
        ),
        Disease(
            name="Bacterial Wilt",
            name_hi="जीवाणु म्लानि",
            name_kn="ಬ್ಯಾಕ್ಟೀರಿಯಾ ಬಾಡುವಿಕೆ",
            crop_id=chilli.id,
            symptoms="Sudden wilting of whole plant without yellowing. "
                     "Cut stem placed in water shows milky white bacterial ooze streaming out. "
                     "Brown discoloration of vascular tissue.",
            symptoms_hi="बिना पीला हुए पूरे पौधे का अचानक मुरझाना। "
                        "कटे तने को पानी में रखने पर दूधिया सफ़ेद जीवाणु स्राव निकलता है। "
                        "संवहनी ऊतक का भूरा रंग परिवर्तन।",
            symptoms_kn="ಹಳದಿಯಾಗದೆ ಇಡೀ ಗಿಡ ಇದ್ದಕ್ಕಿದ್ದಂತೆ ಬಾಡುವಿಕೆ. "
                        "ಕತ್ತರಿಸಿದ ಕಾಂಡವನ್ನು ನೀರಿನಲ್ಲಿ ಇಟ್ಟಾಗ ಹಾಲಿನಂತಹ ಬಿಳಿ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸ್ರಾವ ಹೊರಬರುತ್ತದೆ. "
                        "ನಾಳೀಯ ಅಂಗಾಂಶದ ಕಂದು ಬಣ್ಣ ಬದಲಾವಣೆ.",
            cause="Bacterium Ralstonia solanacearum; soil-borne, spreads through irrigation water and infected transplants.",
            cause_hi="जीवाणु रैल्स्टोनिया सोलानेसिएरम; मिट्टी जनित, सिंचाई जल और संक्रमित पौधों से फैलता है।",
            cause_kn="ಬ್ಯಾಕ್ಟೀರಿಯಾ ರಾಲ್ಸ್ಟೋನಿಯಾ ಸೋಲನಿಸಿಯೇರಂ; ಮಣ್ಣಿನಲ್ಲಿ ಹುಟ್ಟುವ, ನೀರಾವರಿ ನೀರು ಮತ್ತು ಸೋಂಕಿತ ಸಸಿಗಳ ಮೂಲಕ ಹರಡುತ್ತದೆ.",
            prevention="Use resistant varieties. Practice crop rotation with non-solanaceous crops (cereals/pulses). "
                       "Raise nursery in disease-free soil. Improve drainage.",
            prevention_hi="प्रतिरोधी किस्में उपयोग करें। गैर-सोलेनेसियस फसलों (अनाज/दालें) के साथ फसल चक्र अपनाएं। "
                          "रोगमुक्त मिट्टी में नर्सरी तैयार करें। जल निकासी सुधारें।",
            prevention_kn="ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ. ಸೋಲನೇಸಿಯಸ್ ಅಲ್ಲದ ಬೆಳೆಗಳ (ಧಾನ್ಯ/ಬೇಳೆ) ಜೊತೆ ಬೆಳೆ ಆವರ್ತನೆ ಮಾಡಿ. "
                          "ರೋಗಮುಕ್ತ ಮಣ್ಣಿನಲ್ಲಿ ಸಸಿಮನೆ ಮಾಡಿ. ಬಸಿ ಸುಧಾರಿಸಿ.",
            organic_treatment="Drench soil with Pseudomonas fluorescens (20g/L). "
                              "Apply Trichoderma harzianum at 2.5 kg/ha mixed with FYM. "
                              "Use bio-fumigation with mustard cake.",
            organic_treatment_hi="स्यूडोमोनास फ्लोरेसेंस (20 ग्राम/ली) से मिट्टी को भिगोएं। "
                                 "ट्राइकोडर्मा हार्ज़ियानम 2.5 किग्रा/हे. को FYM के साथ मिलाकर डालें। "
                                 "सरसों की खली से जैव-धूमन करें।",
            organic_treatment_kn="ಸ್ಯೂಡೋಮೋನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ (20 ಗ್ರಾಂ/ಲೀ) ಮಣ್ಣಿಗೆ ಸುರಿಯಿರಿ. "
                                 "ಟ್ರೈಕೋಡರ್ಮಾ ಹರ್ಜಿಯಾನಮ್ 2.5 ಕೆಜಿ/ಹೆ. FYM ಜೊತೆ ಬೆರೆಸಿ ಹಾಕಿ. "
                                 "ಸಾಸಿವೆ ಹಿಂಡಿಯಿಂದ ಜೈವಿಕ ಧೂಮೀಕರಣ ಮಾಡಿ.",
            chemical_treatment="No effective chemical cure once plants are infected. "
                               "Preventive soil drenching with Copper oxychloride 50% WP (3g/L) + Streptocycline (0.5g/10L).",
            chemical_treatment_hi="एक बार संक्रमित होने पर कोई प्रभावी रासायनिक उपचार नहीं। "
                                  "निवारक मिट्टी भिगोना: कॉपर ऑक्सीक्लोराइड 50% WP (3 ग्राम/ली) + स्ट्रेप्टोसाइक्लिन (0.5 ग्राम/10ली)।",
            chemical_treatment_kn="ಸೋಂಕಿತ ನಂತರ ಯಾವುದೇ ಪರಿಣಾಮಕಾರಿ ರಾಸಾಯನಿಕ ಉಪಚಾರ ಇಲ್ಲ. "
                                  "ತಡೆಗಟ್ಟುವ ಮಣ್ಣು ತೊಯ್ಸುವಿಕೆ: ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ 50% WP (3 ಗ್ರಾಂ/ಲೀ) + ಸ್ಟ್ರೆಪ್ಟೋಸೈಕ್ಲಿನ್ (0.5 ಗ್ರಾಂ/10ಲೀ).",
            chemical_composition="Copper oxychloride (3Cu(OH)₂·CuCl₂): Contact copper fungicide/bactericide. "
                                 "Streptocycline: Streptomycin + Tetracycline antibiotic combination.",
            chemical_composition_hi="कॉपर ऑक्सीक्लोराइड (3Cu(OH)₂·CuCl₂): सम्पर्क तांबा कवकनाशी/जीवाणुनाशक। "
                                    "स्ट्रेप्टोसाइक्लिन: स्ट्रेप्टोमाइसिन + टेट्रासाइक्लिन एंटीबायोटिक संयोजन।",
            chemical_composition_kn="ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ (3Cu(OH)₂·CuCl₂): ಸಂಪರ್ಕ ತಾಮ್ರ ಶಿಲೀಂಧ್ರನಾಶಕ/ಬ್ಯಾಕ್ಟೀರಿಯಾನಾಶಕ. "
                                    "ಸ್ಟ್ರೆಪ್ಟೋಸೈಕ್ಲಿನ್: ಸ್ಟ್ರೆಪ್ಟೋಮೈಸಿನ್ + ಟೆಟ್ರಾಸೈಕ್ಲಿನ್ ಪ್ರತಿಜೀವಕ ಸಂಯೋಜನೆ.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Ralstonia_solanacearum_symptoms.jpg/400px-Ralstonia_solanacearum_symptoms.jpg"
        ),
        Disease(
            name="Leaf Curl Virus",
            name_hi="पत्ती मोड़ विषाणु",
            name_kn="ಎಲೆ ಮುದುಡು ವೈರಸ್",
            crop_id=chilli.id,
            symptoms="Upward curling and crinkling of leaves. Leaves become thick and leathery. "
                     "Stunted growth with short internodes giving bushy appearance. Severe yield loss.",
            symptoms_hi="पत्तियों का ऊपर की ओर मुड़ना और सिकुड़ना। पत्तियां मोटी और चमड़े जैसी हो जाती हैं। "
                        "छोटी गांठों के साथ बौनी वृद्धि जो झाड़ीनुमा दिखती है। गंभीर उपज हानि।",
            symptoms_kn="ಎಲೆಗಳ ಮೇಲಕ್ಕೆ ಮುದುಡುವಿಕೆ ಮತ್ತು ಕುಗ್ಗುವಿಕೆ. ಎಲೆಗಳು ದಪ್ಪ ಮತ್ತು ಚರ್ಮದಂತಹ ಆಗುತ್ತವೆ. "
                        "ಸಣ್ಣ ಗಂಟುಗಳೊಂದಿಗೆ ಕುಂಠಿತ ಬೆಳವಣಿಗೆ ಪೊದೆಯಂತೆ ಕಾಣುತ್ತದೆ. ತೀವ್ರ ಇಳುವರಿ ನಷ್ಟ.",
            cause="Chilli leaf curl virus (ChiLCV) transmitted by whitefly (Bemisia tabaci).",
            cause_hi="मिर्च पत्ती मोड़ विषाणु (ChiLCV) सफ़ेद मक्खी (बेमिसिया टबासी) द्वारा फैलता है।",
            cause_kn="ಮೆಣಸಿನ ಎಲೆ ಮುದುಡು ವೈರಸ್ (ChiLCV) ಬಿಳಿ ನೊಣ (ಬೆಮಿಸಿಯಾ ಟಬಾಸಿ) ಮೂಲಕ ಹರಡುತ್ತದೆ.",
            prevention="Use virus-resistant varieties. Install yellow sticky traps (25/ha) to monitor whitefly. "
                       "Remove and destroy infected plants. Use reflective silver mulch.",
            prevention_hi="विषाणु-प्रतिरोधी किस्में उपयोग करें। सफ़ेद मक्खी निगरानी के लिए पीले चिपचिपे जाल (25/हे.) लगाएं। "
                          "संक्रमित पौधों को हटाकर नष्ट करें। परावर्तक सिल्वर मल्च का उपयोग करें।",
            prevention_kn="ವೈರಸ್-ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬಳಸಿ. ಬಿಳಿ ನೊಣ ನಿಗಾಗೆ ಹಳದಿ ಅಂಟಿಕೆ ಜಾಲ (25/ಹೆ.) ಅಳವಡಿಸಿ. "
                          "ಸೋಂಕಿತ ಗಿಡಗಳನ್ನು ತೆಗೆದು ನಾಶಮಾಡಿ. ಪ್ರತಿಫಲಿಸುವ ಬೆಳ್ಳಿ ಮಲ್ಚ್ ಬಳಸಿ.",
            organic_treatment="Spray neem oil (5ml/L) or NSKE 5% to control whitefly. "
                              "Release Encarsia formosa (whitefly parasitoid). "
                              "Grow trap crops (marigold) along borders.",
            organic_treatment_hi="सफ़ेद मक्खी नियंत्रण के लिए नीम तेल (5 मिली/ली) या NSKE 5% छिड़कें। "
                                 "एन्कार्सिया फॉर्मोसा (सफ़ेद मक्खी परजीवी) छोड़ें। "
                                 "किनारों पर जाल फसलें (गेंदा) उगाएं।",
            organic_treatment_kn="ಬಿಳಿ ನೊಣ ನಿಯಂತ್ರಣಕ್ಕೆ ಬೇವಿನ ಎಣ್ಣೆ (5 ಮಿಲೀ/ಲೀ) ಅಥವಾ NSKE 5% ಸಿಂಪಡಿಸಿ. "
                                 "ಎನ್ಕಾರ್ಸಿಯಾ ಫಾರ್ಮೋಸಾ (ಬಿಳಿ ನೊಣ ಪರಾವಲಂಬಿ) ಬಿಡುಗಡೆ ಮಾಡಿ. "
                                 "ಅಂಚುಗಳಲ್ಲಿ ಬಲೆ ಬೆಳೆ (ಚೆಂಡು ಹೂವು) ಬೆಳೆಸಿ.",
            chemical_treatment="Spray Imidacloprid 17.8% SL (0.3ml/L) or Diafenthiuron 50% WP (1.2g/L) to control whitefly vector. "
                               "Seed treatment with Thiamethoxam 70% WS (5g/kg).",
            chemical_treatment_hi="सफ़ेद मक्खी नियंत्रण: इमिडाक्लोप्रिड 17.8% SL (0.3 मिली/ली) या डायफेन्थियूरॉन 50% WP (1.2 ग्राम/ली) छिड़कें। "
                                  "थियामेथोक्साम 70% WS (5 ग्राम/किग्रा) से बीज उपचार।",
            chemical_treatment_kn="ಬಿಳಿ ನೊಣ ನಿಯಂತ್ರಣ: ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ 17.8% SL (0.3 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಡಯಫೆಂಥಿಯೂರಾನ್ 50% WP (1.2 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಥಿಯಾಮೆಥೊಕ್ಸಾಮ್ 70% WS (5 ಗ್ರಾಂ/ಕೆಜಿ) ಬೀಜ ಉಪಚಾರ.",
            chemical_composition="Imidacloprid (C₉H₁₀ClN₅O₂): Neonicotinoid systemic insecticide. "
                                 "Diafenthiuron (C₂₃H₃₂N₂OS): Thiourea insecticide/acaricide.",
            chemical_composition_hi="इमिडाक्लोप्रिड (C₉H₁₀ClN₅O₂): नियोनिकोटिनॉइड प्रणालीगत कीटनाशक। "
                                    "डायफेन्थियूरॉन (C₂₃H₃₂N₂OS): थियोयूरिया कीटनाशक/एकारिसाइड।",
            chemical_composition_kn="ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ (C₉H₁₀ClN₅O₂): ನಿಯೋನಿಕೋಟಿನಾಯ್ಡ್ ವ್ಯವಸ್ಥಿತ ಕೀಟನಾಶಕ. "
                                    "ಡಯಾಫೆನ್ಥಿಯುರಾನ್ (C₂₃H₃₂N₂OS): ಥಿಯೋಯೂರಿಯಾ ಕೀಟನಾಶಕ/ಹುಳುನಾಶಕ.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Taphrina_deformans_1.jpg/400px-Taphrina_deformans_1.jpg"
        )
    ]

    chilli_pests = [
        Pest(
            name="Thrips",
            name_hi="थ्रिप्स",
            name_kn="ಥ್ರಿಪ್ಸ್",
            crop_id=chilli.id,
            scientific_name="Scirtothrips dorsalis",
            symptoms="Upward curling of leaves with silvery sheen on undersurface. "
                     "Leaves become brittle. Flower buds drop. 'Murda' complex (leaf curl) in severe infestation.",
            symptoms_hi="पत्तियों का ऊपर मुड़ना और निचली सतह पर चांदी जैसी चमक। "
                        "पत्तियां भंगुर हो जाती हैं। फूलों की कलियां गिर जाती हैं। गंभीर प्रकोप में 'मुर्दा' रोग (पत्ती मोड़)।",
            symptoms_kn="ಎಲೆಗಳ ಮೇಲಕ್ಕೆ ಮುದುಡುವಿಕೆ ಮತ್ತು ಕೆಳಮೈಯಲ್ಲಿ ಬೆಳ್ಳಿ ಹೊಳಪು. "
                        "ಎಲೆಗಳು ಸುಲಭವಾಗಿ ಮುರಿಯುತ್ತವೆ. ಹೂಮೊಗ್ಗುಗಳು ಉದುರುತ್ತವೆ. ತೀವ್ರ ಬಾಧೆಯಲ್ಲಿ 'ಮುರ್ದಾ' ಸಂಕೀರ್ಣ.",
            damage_type="Rasping-sucking; causes leaf curl, flower drop, and reduced fruit quality.",
            damage_type_hi="खरोंच-चूसने वाला; पत्ती मोड़, फूल गिरना और फल गुणवत्ता कम होना।",
            damage_type_kn="ಕೆರೆತ-ಹೀರುವ; ಎಲೆ ಮುದುಡು, ಹೂ ಉದುರುವಿಕೆ ಮತ್ತು ಹಣ್ಣಿನ ಗುಣಮಟ್ಟ ಕಡಿಮೆ.",
            prevention="Use blue sticky traps (25/ha). Intercrop with coriander or maize. "
                       "Spray water jets to dislodge nymphs. Avoid water stress.",
            prevention_hi="नीले चिपचिपे जाल (25/हे.) लगाएं। धनिया या मक्का के साथ अंतर-फसल करें। "
                          "निम्फ हटाने के लिए पानी की तेज धार मारें। जल तनाव से बचें।",
            prevention_kn="ನೀಲಿ ಅಂಟಿಕೆ ಜಾಲ (25/ಹೆ.) ಬಳಸಿ. ಕೊತ್ತಂಬರಿ ಅಥವಾ ಜೋಳದೊಂದಿಗೆ ಅಂತರ ಬೆಳೆ ಮಾಡಿ. "
                          "ನಿಂಫ್ ತೆಗೆಯಲು ನೀರಿನ ಜೆಟ್ ಹೊಡೆಯಿರಿ. ನೀರಿನ ಒತ್ತಡ ಬರಬೇಡಿ.",
            organic_treatment="Spray neem oil (5ml/L) or NSKE 5% at 10-day intervals. "
                              "Release predatory mites (Amblyseius swirskii). Apply Beauveria bassiana (5g/L).",
            organic_treatment_hi="10 दिन के अंतराल पर नीम तेल (5 मिली/ली) या NSKE 5% छिड़कें। "
                                 "शिकारी माइट (एम्बलीसियस स्विर्स्की) छोड़ें। ब्यूवेरिया बैसियाना (5 ग्राम/ली) लगाएं।",
            organic_treatment_kn="10 ದಿನ ಅಂತರದಲ್ಲಿ ಬೇವಿನ ಎಣ್ಣೆ (5 ಮಿಲೀ/ಲೀ) ಅಥವಾ NSKE 5% ಸಿಂಪಡಿಸಿ. "
                                 "ಪರಭಕ್ಷಕ ಹುಳು (ಅಂಬ್ಲಿಸೀಯಸ್ ಸ್ವಿರ್ಸ್ಕಿ) ಬಿಡುಗಡೆ ಮಾಡಿ. ಬ್ಯೂವೇರಿಯಾ ಬ್ಯಾಸಿಯಾನಾ (5 ಗ್ರಾಂ/ಲೀ) ಹಾಕಿ.",
            chemical_treatment="Spray Fipronil 5% SC (2ml/L) or Spinetoram 11.7% SC (0.5ml/L). "
                               "Alternate with Acephate 75% SP (1g/L).",
            chemical_treatment_hi="फिप्रोनिल 5% SC (2 मिली/ली) या स्पिनेटोरैम 11.7% SC (0.5 मिली/ली) छिड़कें। "
                                  "एसीफेट 75% SP (1 ग्राम/ली) के साथ बारी-बारी करें।",
            chemical_treatment_kn="ಫಿಪ್ರೋನಿಲ್ 5% SC (2 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಸ್ಪಿನೆಟೋರಾಮ್ 11.7% SC (0.5 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಅಸೆಫೇಟ್ 75% SP (1 ಗ್ರಾಂ/ಲೀ) ಜೊತೆ ಪರ್ಯಾಯ ಮಾಡಿ.",
            chemical_composition="Fipronil (C₁₂H₄Cl₂F₆N₄OS): Phenylpyrazole insecticide. "
                                 "Spinetoram: Spinosyn insecticide derived from Saccharopolyspora.",
            chemical_composition_hi="फिप्रोनिल (C₁₂H₄Cl₂F₆N₄OS): फिनाइलपाइराज़ोल कीटनाशक। "
                                    "स्पिनेटोरैम: सैकेरोपॉलिस्पोरा से प्राप्त स्पिनोसिन कीटनाशक।",
            chemical_composition_kn="ಫಿಪ್ರೋನಿಲ್ (C₁₂H₄Cl₂F₆N₄OS): ಫೆನೈಲ್ಪೈರಜೋಲ್ ಕೀಟನಾಶಕ. "
                                    "ಸ್ಪಿನೆಟೋರಮ್: ಸ್ಯಾಕ್ಯಾರೋಪಾಲಿಸ್ಪೋರಾದಿಂದ ಪಡೆದ ಸ್ಪಿನೋಸಿನ್ ಕೀಟನಾಶಕ.",
            severity="High",
            active_season="March–June (hot dry weather)",
            active_season_hi="मार्च–जून (गर्म शुष्क मौसम)",
            active_season_kn="ಮಾರ್ಚ್–ಜೂನ್ (ಬಿಸಿ ಒಣ ಹವಾಮಾನ)",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Thysanoptera.jpg/400px-Thysanoptera.jpg"
        ),
        Pest(
            name="Fruit Borer",
            name_hi="फल छेदक",
            name_kn="ಹಣ್ಣು ಕೊರಕ",
            crop_id=chilli.id,
            scientific_name="Helicoverpa armigera",
            symptoms="Circular bore holes on fruits. Larvae feed inside the fruit. "
                     "Damaged fruits show frass at entry point and may rot. Premature fruit drop.",
            symptoms_hi="फलों पर गोलाकार छेद। लार्वा फल के अंदर खाते हैं। "
                        "क्षतिग्रस्त फलों में प्रवेश बिंदु पर मल दिखता है और सड़ सकते हैं। समय से पहले फल गिरना।",
            symptoms_kn="ಕಾಯಿಗಳ ಮೇಲೆ ವೃತ್ತಾಕಾರ ರಂಧ್ರಗಳು. ಲಾರ್ವಾ ಕಾಯಿ ಒಳಗೆ ತಿನ್ನುತ್ತದೆ. "
                        "ಹಾನಿಗೊಳಗಾದ ಕಾಯಿಗಳಲ್ಲಿ ಪ್ರವೇಶ ಭಾಗದಲ್ಲಿ ಹಿಕ್ಕೆ ಕಾಣುತ್ತದೆ ಮತ್ತು ಕೊಳೆಯಬಹುದು. ಅಕಾಲಿಕ ಕಾಯಿ ಉದುರುವಿಕೆ.",
            damage_type="Internal feeder — larvae bore into fruits and feed on seeds and placenta.",
            damage_type_hi="आंतरिक भक्षक — लार्वा फलों में छेद करके बीज और बीजांडासन खाते हैं।",
            damage_type_kn="ಆಂತರಿಕ ಹುಳು — ಲಾರ್ವಾ ಕಾಯಿಗಳಲ್ಲಿ ಕೊರೆದು ಬೀಜ ಮತ್ತು ಒಳಭಾಗವನ್ನು ತಿನ್ನುತ್ತದೆ.",
            prevention="Install pheromone traps (12/ha) to monitor moths. Hand-pick and destroy infested fruits. "
                       "Grow marigold as trap crop (1 row per 16 rows of chilli).",
            prevention_hi="पतंगों की निगरानी के लिए फेरोमोन जाल (12/हे.) लगाएं। संक्रमित फलों को हाथ से तोड़कर नष्ट करें। "
                          "गेंदे को जाल फसल के रूप में उगाएं (मिर्च की 16 पंक्तियों में 1 पंक्ति)।",
            prevention_kn="ಪತಂಗಗಳ ನಿಗಾಗೆ ಫೆರೋಮೋನ್ ಜಾಲ (12/ಹೆ.) ಅಳವಡಿಸಿ. ಬಾಧಿತ ಕಾಯಿಗಳನ್ನು ಕೈಯಿಂದ ಕಿತ್ತು ನಾಶಮಾಡಿ. "
                          "ಚೆಂಡು ಹೂವನ್ನು ಬಲೆ ಬೆಳೆಯಾಗಿ ಬೆಳೆಸಿ (ಮೆಣಸಿನ 16 ಸಾಲುಗಳಿಗೆ 1 ಸಾಲು).",
            organic_treatment="Release Trichogramma chilonis at 1.5 lakh/ha at flowering. "
                              "Spray HaNPV (Helicoverpa Nuclear Polyhedrosis Virus) at 250 LE/ha. "
                              "Apply Bt (Bacillus thuringiensis) at 2g/L.",
            organic_treatment_hi="फूल आने पर ट्राइकोग्रामा कैलोनिस 1.5 लाख/हे. छोड़ें। "
                                 "HaNPV (हेलिकोवर्पा न्यूक्लियर पॉलीहेड्रोसिस वायरस) 250 LE/हे. छिड़कें। "
                                 "बीटी (बैसिलस थूरिंजिएन्सिस) 2 ग्राम/ली लगाएं।",
            organic_treatment_kn="ಹೂಬಿಡುವಾಗ ಟ್ರೈಕೋಗ್ರಾಮಾ ಚಿಲೋನಿಸ್ 1.5 ಲಕ್ಷ/ಹೆ. ಬಿಡುಗಡೆ ಮಾಡಿ. "
                                 "HaNPV (ಹೆಲಿಕೋವರ್ಪಾ ನ್ಯೂಕ್ಲಿಯರ್ ಪಾಲಿಹೆಡ್ರೋಸಿಸ್ ವೈರಸ್) 250 LE/ಹೆ. ಸಿಂಪಡಿಸಿ. "
                                 "Bt (ಬ್ಯಾಸಿಲಸ್ ಥೂರಿಂಜಿಯೆನ್ಸಿಸ್) 2 ಗ್ರಾಂ/ಲೀ ಹಾಕಿ.",
            chemical_treatment="Spray Chlorantraniliprole 18.5% SC (0.3ml/L) or Emamectin benzoate 5% SG (0.4g/L). "
                               "Apply at 50% flowering stage.",
            chemical_treatment_hi="क्लोरैंट्रानिलिप्रोल 18.5% SC (0.3 मिली/ली) या एमामेक्टिन बेंज़ोएट 5% SG (0.4 ग्राम/ली) छिड़कें। "
                                  "50% फूल आने की अवस्था में लगाएं।",
            chemical_treatment_kn="ಕ್ಲೋರಾಂಟ್ರಾನಿಲಿಪ್ರೋಲ್ 18.5% SC (0.3 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಎಮಾಮೆಕ್ಟಿನ್ ಬೆಂಜೋಯೇಟ್ 5% SG (0.4 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "50% ಹೂಬಿಡುವ ಹಂತದಲ್ಲಿ ಹಾಕಿ.",
            chemical_composition="Emamectin benzoate (C₄₉H₇₅NO₁₃·C₇H₆O₃): Avermectin insecticide activating GABA-gated chloride channels.",
            chemical_composition_hi="एमामेक्टिन बेंज़ोएट (C₄₉H₇₅NO₁₃·C₇H₆O₃): GABA-गेटेड क्लोराइड चैनल सक्रिय करने वाला एवरमेक्टिन कीटनाशक।",
            chemical_composition_kn="ಎಮಾಮೆಕ್ಟಿನ್ ಬೆಂಜೋಯೇಟ್ (C₄₉H₇₅NO₁₃·C₇H₆O₃): GABA-ಗೇಟೆಡ್ ಕ್ಲೋರೈಡ್ ಚಾನಲ್ ಸಕ್ರಿಯಗೊಳಿಸುವ ಅವರ್ಮೆಕ್ಟಿನ್ ಕೀಟನಾಶಕ.",
            severity="High",
            active_season="October–February (during fruiting)",
            active_season_hi="अक्टूबर–फरवरी (फल लगने के दौरान)",
            active_season_kn="ಅಕ್ಟೋಬರ್–ಫೆಬ್ರವರಿ (ಕಾಯಿ ಬಿಡುವ ಸಮಯ)",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Helicoverpa_armigera.jpg/400px-Helicoverpa_armigera.jpg"
        ),
        Pest(
            name="Whitefly",
            name_hi="सफ़ेद मक्खी",
            name_kn="ಬಿಳಿ ನೊಣ",
            crop_id=chilli.id,
            scientific_name="Bemisia tabaci",
            symptoms="Tiny white winged insects on leaf undersurface. Yellowing and downward curling of leaves. "
                     "Honeydew secretion leading to sooty mold. Transmits leaf curl virus.",
            symptoms_hi="पत्ती की निचली सतह पर छोटे सफ़ेद पंखों वाले कीट। पत्तियों का पीलापन और नीचे मुड़ना। "
                        "मधुरस स्राव से काली फफूंद लगती है। पत्ती मोड़ विषाणु फैलाता है।",
            symptoms_kn="ಎಲೆ ಕೆಳಮೈಯಲ್ಲಿ ಸಣ್ಣ ಬಿಳಿ ರೆಕ್ಕೆಯ ಕೀಟಗಳು. ಎಲೆಗಳ ಹಳದಿ ಬಣ್ಣ ಮತ್ತು ಕೆಳಗೆ ಮುದುಡುವಿಕೆ. "
                        "ಮಧುರಸ ಸ್ರಾವ ಕಪ್ಪು ಬೂಷ್ಟಿಗೆ ಕಾರಣ. ಎಲೆ ಮುದುಡು ವೈರಸ್ ಹರಡುತ್ತದೆ.",
            damage_type="Sap-sucking and virus vector — causes direct damage and transmits several viral diseases.",
            damage_type_hi="रस चूसने वाला और विषाणु वाहक — सीधा नुकसान और कई विषाणु रोग फैलाता है।",
            damage_type_kn="ರಸ ಹೀರುವ ಮತ್ತು ವೈರಸ್ ವಾಹಕ — ನೇರ ಹಾನಿ ಮತ್ತು ಹಲವಾರು ವೈರಸ್ ರೋಗಗಳನ್ನು ಹರಡುತ್ತದೆ.",
            prevention="Use yellow sticky traps. Grow barrier crops (sorghum/maize 2-3 rows). "
                       "Use reflective silver-colored mulches. Avoid growing near cotton fields.",
            prevention_hi="पीले चिपचिपे जाल लगाएं। बाधा फसलें (ज्वार/मक्का 2-3 पंक्तियां) उगाएं। "
                          "परावर्तक सिल्वर मल्च उपयोग करें। कपास के खेतों के पास न उगाएं।",
            prevention_kn="ಹಳದಿ ಅಂಟಿಕೆ ಜಾಲ ಬಳಸಿ. ತಡೆ ಬೆಳೆ (ಜೋಳ/ಮೆಕ್ಕೆಜೋಳ 2-3 ಸಾಲು) ಬೆಳೆಸಿ. "
                          "ಪ್ರತಿಫಲಿಸುವ ಬೆಳ್ಳಿ ಮಲ್ಚ್ ಬಳಸಿ. ಹತ್ತಿ ಹೊಲಗಳ ಬಳಿ ಬೆಳೆಸಬೇಡಿ.",
            organic_treatment="Spray neem oil (5ml/L) at weekly intervals. "
                              "Release Chrysoperla carnea predators at 1 per plant. "
                              "Spray garlic-chilli extract (200g each in 10L water).",
            organic_treatment_hi="साप्ताहिक अंतराल पर नीम तेल (5 मिली/ली) छिड़कें। "
                                 "क्राइसोपर्ला कार्निया शिकारियों को 1 प्रति पौधा छोड़ें। "
                                 "लहसुन-मिर्च अर्क (200 ग्राम प्रत्येक 10 ली पानी में) छिड़कें।",
            organic_treatment_kn="ವಾರಕ್ಕೊಮ್ಮೆ ಬೇವಿನ ಎಣ್ಣೆ (5 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                 "ಕ್ರೈಸೋಪರ್ಲಾ ಕಾರ್ನಿಯಾ ಪರಭಕ್ಷಕಗಳನ್ನು ಪ್ರತಿ ಗಿಡಕ್ಕೆ 1 ಬಿಡುಗಡೆ ಮಾಡಿ. "
                                 "ಬೆಳ್ಳುಳ್ಳಿ-ಮೆಣಸಿನ ಸಾರ (10 ಲೀ ನೀರಿನಲ್ಲಿ ತಲಾ 200 ಗ್ರಾಂ) ಸಿಂಪಡಿಸಿ.",
            chemical_treatment="Spray Spiromesifen 22.9% SC (0.8ml/L) or Pyriproxyfen 10% EC (1.5ml/L). "
                               "Rotate insecticide groups to prevent resistance development.",
            chemical_treatment_hi="स्पीरोमेसिफेन 22.9% SC (0.8 मिली/ली) या पायरीप्रोक्सीफेन 10% EC (1.5 मिली/ली) छिड़कें। "
                                  "प्रतिरोध विकास रोकने के लिए कीटनाशक समूह बदलें।",
            chemical_treatment_kn="ಸ್ಪೈರೋಮೆಸಿಫೆನ್ 22.9% SC (0.8 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಪೈರಿಪ್ರಾಕ್ಸಿಫೆನ್ 10% EC (1.5 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಪ್ರತಿರೋಧ ಬೆಳವಣಿಗೆ ತಡೆಗೆ ಕೀಟನಾಶಕ ಗುಂಪುಗಳನ್ನು ಬದಲಿಸಿ.",
            chemical_composition="Spiromesifen (C₂₃H₃₀O₄): Lipid biosynthesis inhibitor. "
                                 "Pyriproxyfen (C₂₀H₁₉NO₃): Juvenile hormone analog (IGR).",
            chemical_composition_hi="स्पीरोमेसिफेन (C₂₃H₃₀O₄): लिपिड जैवसंश्लेषण अवरोधक। "
                                    "पायरीप्रॉक्सीफेन (C₂₀H₁₉NO₃): किशोर हॉर्मोन एनालॉग (IGR)।",
            chemical_composition_kn="ಸ್ಪೈರೋಮೆಸಿಫೆನ್ (C₂₃H₃₀O₄): ಲಿಪಿಡ್ ಜೈವಸಂಶ್ಲೇಷಣೆ ತಡೆಗಟ್ಟುವಿಕೆ. "
                                    "ಪೈರಿಪ್ರಾಕ್ಸಿಫೆನ್ (C₂₀H₁₉NO₃): ಕಿಶೋರ ಹಾರ್ಮೋನ್ ಅನಲಾಗ್ (IGR).",
            severity="High",
            active_season="Year-round, peaks in February–May",
            active_season_hi="वर्ष भर, फरवरी–मई में चरम",
            active_season_kn="ವರ್ಷವಿಡೀ, ಫೆಬ್ರವರಿ–ಮೇ ನಲ್ಲಿ ಉತ್ತುಂಗ",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Silverleaf_whitefly.jpg/400px-Silverleaf_whitefly.jpg"
        )
    ]

    # ==================== COFFEE ====================
    coffee = Crop(
        name="Coffee",
        name_hi="कॉफी",
        name_kn="ಕಾಫಿ",
        scientific_name="Coffea arabica / Coffea canephora",
        description="Coffee is a major plantation crop grown in southern India (Karnataka, Kerala, Tamil Nadu). "
                    "India produces both Arabica (grown at 1000–1500m) and Robusta (grown at 500–1000m) varieties. "
                    "Karnataka alone contributes about 70% of India's coffee production. "
                    "It requires shade, well-drained acidic soil (pH 5.5–6.5), and tropical highland climate.",
        description_hi="कॉफी दक्षिण भारत (कर्नाटक, केरल, तमिलनाडु) में उगाई जाने वाली प्रमुख बागान फसल है। "
                       "भारत अरेबिका (1000–1500 मीटर) और रोबस्टा (500–1000 मीटर) दोनों किस्में उगाता है। "
                       "अकेले कर्नाटक भारत के कॉफी उत्पादन का लगभग 70% योगदान देता है। "
                       "इसे छाया, अच्छी जल निकासी वाली अम्लीय मिट्टी (pH 5.5–6.5), और उष्णकटिबंधीय पहाड़ी जलवायु की आवश्यकता होती है।",
        description_kn="ಕಾಫಿಯು ದಕ್ಷಿಣ ಭಾರತದಲ್ಲಿ (ಕರ್ನಾಟಕ, ಕೇರಳ, ತಮಿಳುನಾಡು) ಬೆಳೆಯಲಾಗುವ ಪ್ರಮುಖ ತೋಟದ ಬೆಳೆಯಾಗಿದೆ. "
                       "ಭಾರತವು ಅರೇಬಿಕಾ (1000–1500 ಮೀ) ಮತ್ತು ರೋಬಸ್ಟಾ (500–1000 ಮೀ) ಎರಡೂ ತಳಿಗಳನ್ನು ಬೆಳೆಯುತ್ತದೆ. "
                       "ಕರ್ನಾಟಕ ಒಂದೇ ಭಾರತದ ಕಾಫಿ ಉತ್ಪಾದನೆಯ ಸುಮಾರು 70% ಕೊಡುಗೆ ನೀಡುತ್ತದೆ. "
                       "ಇದಕ್ಕೆ ನೆರಳು, ಚೆನ್ನಾಗಿ ಬಸಿಯುವ ಆಮ್ಲೀಯ ಮಣ್ಣು (pH 5.5–6.5), ಮತ್ತು ಉಷ್ಣವಲಯ ಪರ್ವತ ಹವಾಮಾನ ಬೇಕು.",
        season="Perennial; flowering March–April, harvest November–February",
        season_hi="बारहमासी; फूल मार्च–अप्रैल, कटाई नवंबर–फरवरी",
        season_kn="ಬಹುವಾರ್ಷಿಕ; ಹೂಬಿಡುವಿಕೆ ಮಾರ್ಚ್–ಏಪ್ರಿಲ್, ಕೊಯ್ಲು ನವೆಂಬರ್–ಫೆಬ್ರವರಿ",
        image_url="https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400"
    )
    db.session.add(coffee)
    db.session.flush()

    coffee_diseases = [
        Disease(
            name="Coffee Leaf Rust",
            name_hi="कॉफी पत्ती रस्ट",
            name_kn="ಕಾಫಿ ಎಲೆ ತುಕ್ಕು",
            crop_id=coffee.id,
            symptoms="Yellow to orange powdery spots (urediniospores) on the underside of leaves. "
                     "Upper surface shows pale yellow patches. Severe defoliation and die-back of branches.",
            symptoms_hi="पत्तियों की निचली सतह पर पीले से नारंगी चूर्णी धब्बे। "
                        "ऊपरी सतह पर हल्के पीले धब्बे दिखते हैं। गंभीर पत्ती गिरना और शाखाओं का सूखना।",
            symptoms_kn="ಎಲೆಗಳ ಕೆಳಮೈಯಲ್ಲಿ ಹಳದಿಯಿಂದ ಕಿತ್ತಳೆ ಪುಡಿಯಂತಹ ಕಲೆಗಳು. "
                        "ಮೇಲ್ಮೈಯಲ್ಲಿ ತಿಳಿ ಹಳದಿ ಕಲೆಗಳು ಕಾಣುತ್ತವೆ. ತೀವ್ರ ಎಲೆ ಉದುರುವಿಕೆ ಮತ್ತು ಕೊಂಬೆಗಳ ಒಣಗುವಿಕೆ.",
            cause="Fungus Hemileia vastatrix; spreads through wind-borne spores, rain splash. "
                  "Favored by warm (20-25°C), humid conditions with intermittent rain.",
            cause_hi="फफूंद हेमिलिया वास्टाट्रिक्स; हवा में उड़ने वाले बीजाणुओं, बारिश से फैलता है। "
                     "गर्म (20-25°C), नम वातावरण और रुक-रुक कर बारिश से फैलता है।",
            cause_kn="ಶಿಲೀಂಧ್ರ ಹೆಮಿಲಿಯಾ ವಾಸ್ಟಾಟ್ರಿಕ್ಸ್; ಗಾಳಿಯಲ್ಲಿ ಹರಡುವ ಬೀಜಕಗಳು, ಮಳೆ ಸಿಂಪರಣೆ. "
                     "ಬೆಚ್ಚಗಿನ (20-25°C), ತೇವ ಪರಿಸ್ಥಿತಿ ಮತ್ತು ಆಗಾಗ ಮಳೆಯಲ್ಲಿ ಹರಡುತ್ತದೆ.",
            prevention="Grow resistant varieties (e.g., Sln.6, Sln.9, Chandragiri). "
                       "Maintain proper shade (40-50%). Ensure good air circulation by pruning. "
                       "Remove heavily infected branches.",
            prevention_hi="प्रतिरोधी किस्में उगाएं (जैसे Sln.6, Sln.9, चंद्रगिरी)। "
                          "उचित छाया (40-50%) बनाएं। छंटाई से अच्छा वायु संचार सुनिश्चित करें। "
                          "अधिक संक्रमित शाखाओं को हटाएं।",
            prevention_kn="ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬೆಳೆಸಿ (ಉದಾ., Sln.6, Sln.9, ಚಂದ್ರಗಿರಿ). "
                          "ಸರಿಯಾದ ನೆರಳು (40-50%) ಕಾಪಾಡಿ. ಕತ್ತರಿಸುವಿಕೆಯಿಂದ ಉತ್ತಮ ಗಾಳಿ ಸಂಚಾರ ಖಾತ್ರಿಪಡಿಸಿ. "
                          "ಹೆಚ್ಚು ಸೋಂಕಿತ ಕೊಂಬೆಗಳನ್ನು ತೆಗೆಯಿರಿ.",
            organic_treatment="Spray Bordeaux mixture (1%) as a preventive during pre-monsoon. "
                              "Apply Trichoderma viride (10g/L) to soil. Use compost tea sprays fortnightly.",
            organic_treatment_hi="पूर्व-मानसून में निवारक रूप से बोर्डो मिश्रण (1%) छिड़कें। "
                                 "मिट्टी में ट्राइकोडर्मा विरिडी (10 ग्राम/ली) डालें। पाक्षिक रूप से कम्पोस्ट चाय छिड़कें।",
            organic_treatment_kn="ಮಾನ್ಸೂನ್ ಪೂರ್ವ ತಡೆಗಟ್ಟುವ ಕ್ರಮವಾಗಿ ಬೋರ್ಡೋ ಮಿಶ್ರಣ (1%) ಸಿಂಪಡಿಸಿ. "
                                 "ಮಣ್ಣಿಗೆ ಟ್ರೈಕೋಡರ್ಮಾ ವಿರಿಡೆ (10 ಗ್ರಾಂ/ಲೀ) ಹಾಕಿ. ಪಾಕ್ಷಿಕವಾಗಿ ಕಂಪೋಸ್ಟ್ ಚಹಾ ಸಿಂಪಡಿಸಿ.",
            chemical_treatment="Spray Tridemorph 80% EC (0.5ml/L) or Propiconazole 25% EC (0.5ml/L) at onset of monsoon. "
                               "Two rounds of spraying: pre-monsoon (June) and post-monsoon (September).",
            chemical_treatment_hi="मानसून की शुरुआत में ट्राइडेमॉर्फ 80% EC (0.5 मिली/ली) या प्रोपिकोनाज़ोल 25% EC (0.5 मिली/ली) छिड़कें। "
                                  "दो बार छिड़काव: पूर्व-मानसून (जून) और उत्तर-मानसून (सितंबर)।",
            chemical_treatment_kn="ಮಾನ್ಸೂನ್ ಆರಂಭದಲ್ಲಿ ಟ್ರೈಡೆಮಾರ್ಫ್ 80% EC (0.5 ಮಿಲೀ/ಲೀ) ಅಥವಾ ಪ್ರೊಪಿಕೋನಜೋಲ್ 25% EC (0.5 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಎರಡು ಸುತ್ತಿನ ಸಿಂಪಡಣೆ: ಮಾನ್ಸೂನ್ ಪೂರ್ವ (ಜೂನ್) ಮತ್ತು ಮಾನ್ಸೂನ್ ನಂತರ (ಸೆಪ್ಟೆಂಬರ್).",
            chemical_composition="Tridemorph (C₁₉H₃₉NO): Morpholine systemic fungicide. "
                                 "Propiconazole (C₁₅H₁₇Cl₂N₃O₂): Triazole systemic fungicide inhibiting ergosterol biosynthesis.",
            chemical_composition_hi="ट्राइडेमॉर्फ (C₁₉H₃₉NO): मॉर्फोलिन प्रणालीगत कवकनाशी। "
                                    "प्रोपिकोनाज़ोल (C₁₅H₁₇Cl₂N₃O₂): एर्गोस्टेरॉल जैवसंश्लेषण रोकने वाला ट्राइएज़ोल प्रणालीगत कवकनाशी।",
            chemical_composition_kn="ಟ್ರೈಡೆಮಾರ್ಫ್ (C₁₉H₃₉NO): ಮಾರ್ಫೋಲಿನ್ ವ್ಯವಸ್ಥಿತ ಶಿಲೀಂಧ್ರನಾಶಕ. "
                                    "ಪ್ರೋಪಿಕೋನಜೋಲ್ (C₁₅H₁₇Cl₂N₃O₂): ಎರ್ಗೋಸ್ಟೆರಾಲ್ ಜೈವಸಂಶ್ಲೇಷಣೆ ತಡೆಯುವ ಟ್ರೈಅಜೋಲ್ ವ್ಯವಸ್ಥಿತ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Hemileia_vastatrix_-_coffee_leaf_rust.jpg/400px-Hemileia_vastatrix_-_coffee_leaf_rust.jpg"
        ),
        Disease(
            name="Black Rot",
            name_hi="काला सड़न",
            name_kn="ಕಪ್ಪು ಕೊಳೆ",
            crop_id=coffee.id,
            symptoms="Black circular spots on mature leaves, usually near the margin. "
                     "Infected berries turn black and mummify on the branch. "
                     "Twigs show dark lesions and die-back.",
            symptoms_hi="परिपक्व पत्तियों पर काले गोलाकार धब्बे, आमतौर पर किनारे के पास। "
                        "संक्रमित बेरी काली होकर शाखा पर ममी बन जाती हैं। "
                        "टहनियों पर काले घाव और सूखना।",
            symptoms_kn="ಪ್ರಬುದ್ಧ ಎಲೆಗಳ ಮೇಲೆ ಕಪ್ಪು ವೃತ್ತಾಕಾರ ಕಲೆಗಳು, ಸಾಮಾನ್ಯವಾಗಿ ಅಂಚಿನ ಬಳಿ. "
                        "ಸೋಂಕಿತ ಹಣ್ಣುಗಳು ಕಪ್ಪಾಗಿ ಕೊಂಬೆಯ ಮೇಲೆ ಒಣಗುತ್ತವೆ. "
                        "ಕೊಂಬೆಗಳಲ್ಲಿ ಕಪ್ಪು ಗಾಯಗಳು ಮತ್ತು ಒಣಗುವಿಕೆ.",
            cause="Fungus Koleroga noxia (Pellicularia koleroga); occurs in heavy rainfall areas "
                  "with poor drainage and excessive shade.",
            cause_hi="फफूंद कोलेरोगा नॉक्सिया; भारी वर्षा वाले क्षेत्रों में खराब जल निकासी और अत्यधिक छाया में होता है।",
            cause_kn="ಶಿಲೀಂಧ್ರ ಕೊಲೆರೋಗಾ ನಾಕ್ಸಿಯಾ; ಭಾರೀ ಮಳೆ ಪ್ರದೇಶಗಳಲ್ಲಿ ಕಳಪೆ ಬಸಿ ಮತ್ತು ಅತಿಯಾದ ನೆರಳಿನಲ್ಲಿ ಕಾಣಿಸಿಕೊಳ್ಳುತ್ತದೆ.",
            prevention="Regulate shade to 40-50%. Improve drainage. "
                       "Prune lower branches to allow air circulation. "
                       "Remove and burn infected berries and branches.",
            prevention_hi="छाया 40-50% तक नियंत्रित करें। जल निकासी सुधारें। "
                          "वायु संचार के लिए निचली शाखाओं की छंटाई करें। "
                          "संक्रमित बेरी और शाखाओं को हटाकर जलाएं।",
            prevention_kn="ನೆರಳನ್ನು 40-50% ಕ್ಕೆ ನಿಯಂತ್ರಿಸಿ. ಬಸಿ ಸುಧಾರಿಸಿ. "
                          "ಗಾಳಿ ಸಂಚಾರಕ್ಕೆ ಕೆಳಗಿನ ಕೊಂಬೆಗಳನ್ನು ಕತ್ತರಿಸಿ. "
                          "ಸೋಂಕಿತ ಹಣ್ಣು ಮತ್ತು ಕೊಂಬೆಗಳನ್ನು ತೆಗೆದು ಸುಡಿ.",
            organic_treatment="Spray Bordeaux mixture (1%) before onset of southwest monsoon. "
                              "Apply copper-based formulations (Bordeaux paste) on affected stems.",
            organic_treatment_hi="दक्षिण-पश्चिम मानसून से पहले बोर्डो मिश्रण (1%) छिड़कें। "
                                 "प्रभावित तनों पर तांबे आधारित फार्मूलेशन (बोर्डो पेस्ट) लगाएं।",
            organic_treatment_kn="ನೈऋत्य ಮಾನ್ಸೂನ್ ಆರಂಭಕ್ಕೆ ಮುನ್ನ ಬೋರ್ಡೋ ಮಿಶ್ರಣ (1%) ಸಿಂಪಡಿಸಿ. "
                                 "ಬಾಧಿತ ಕಾಂಡಗಳ ಮೇಲೆ ತಾಮ್ರ ಆಧಾರಿತ ಸೂತ್ರಗಳನ್ನು (ಬೋರ್ಡೋ ಪೇಸ್ಟ್) ಹಚ್ಚಿ.",
            chemical_treatment="Spray Copper oxychloride 50% WP (3g/L) or Bordeaux mixture (1%) at 30-day intervals "
                               "during June–September. Apply 2-3 rounds during monsoon.",
            chemical_treatment_hi="जून–सितंबर के दौरान 30 दिन के अंतराल पर कॉपर ऑक्सीक्लोराइड 50% WP (3 ग्राम/ली) या बोर्डो मिश्रण (1%) छिड़कें। "
                                  "मानसून में 2-3 बार लगाएं।",
            chemical_treatment_kn="ಜೂನ್–ಸೆಪ್ಟೆಂಬರ್ ನಲ್ಲಿ 30 ದಿನ ಅಂತರದಲ್ಲಿ ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ 50% WP (3 ಗ್ರಾಂ/ಲೀ) ಅಥವಾ ಬೋರ್ಡೋ ಮಿಶ್ರಣ (1%) ಸಿಂಪಡಿಸಿ. "
                                  "ಮಾನ್ಸೂನ್ ನಲ್ಲಿ 2-3 ಸುತ್ತು ಹಾಕಿ.",
            chemical_composition="Copper oxychloride (3Cu(OH)₂·CuCl₂): Multi-site copper fungicide. "
                                 "Bordeaux mixture: CuSO₄ + Ca(OH)₂ — protective copper fungicide.",
            chemical_composition_hi="कॉपर ऑक्सीक्लोराइड (3Cu(OH)₂·CuCl₂): बहु-स्थल तांबा कवकनाशी। "
                                    "बोर्डो मिश्रण: CuSO₄ + Ca(OH)₂ — सुरक्षात्मक तांबा कवकनाशी।",
            chemical_composition_kn="ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ (3Cu(OH)₂·CuCl₂): ಬಹು-ಸ್ಥಳ ತಾಮ್ರ ಶಿಲೀಂಧ್ರನಾಶಕ. "
                                    "ಬೋರ್ಡೋ ಮಿಶ್ರಣ: CuSO₄ + Ca(OH)₂ — ರಕ್ಷಣಾತ್ಮಕ ತಾಮ್ರ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="Medium",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Sclerotium_rolfsii.jpg/400px-Sclerotium_rolfsii.jpg"
        ),
        Disease(
            name="Root Disease (Fusarium Wilt)",
            name_hi="जड़ रोग (फ्यूसेरियम म्लानि)",
            name_kn="ಬೇರು ರೋಗ (ಫ್ಯೂಸೇರಿಯಂ ಬಾಡು)",
            crop_id=coffee.id,
            symptoms="Gradual yellowing and wilting of leaves. Leaves drop off, starting from lower branches. "
                     "Brown discoloration of root and stem vascular tissue. Slow decline and death of plant.",
            symptoms_hi="पत्तियों का धीरे-धीरे पीला होना और मुरझाना। निचली शाखाओं से शुरू होकर पत्तियां गिर जाती हैं। "
                        "जड़ और तने के संवहनी ऊतक का भूरा रंग। पौधे का धीमा पतन और मृत्यु।",
            symptoms_kn="ಎಲೆಗಳ ಕ್ರಮೇಣ ಹಳದಿಯಾಗುವಿಕೆ ಮತ್ತು ಬಾಡುವಿಕೆ. ಕೆಳಗಿನ ಕೊಂಬೆಗಳಿಂದ ಶುರುವಾಗಿ ಎಲೆಗಳು ಉದುರುತ್ತವೆ. "
                        "ಬೇರು ಮತ್ತು ಕಾಂಡದ ನಾಳೀಯ ಅಂಗಾಂಶದ ಕಂದು ಬಣ್ಣ. ಗಿಡದ ನಿಧಾನ ಅವನತಿ ಮತ್ತು ಸಾವು.",
            cause="Fungus Fusarium oxysporum; soil-borne, enters through root wounds. "
                  "Favored by poor drainage, compacted soil, and nematode damage.",
            cause_hi="फफूंद फ्यूसेरियम ऑक्सीस्पोरम; मिट्टी जनित, जड़ के घावों से प्रवेश करता है। "
                     "खराब जल निकासी, संकुचित मिट्टी और सूत्रकृमि नुकसान से फैलता है।",
            cause_kn="ಶಿಲೀಂಧ್ರ ಫ್ಯೂಸೇರಿಯಂ ಆಕ್ಸಿಸ್ಪೋರಮ್; ಮಣ್ಣಿನಲ್ಲಿ ಹುಟ್ಟುವ, ಬೇರಿನ ಗಾಯಗಳ ಮೂಲಕ ಪ್ರವೇಶಿಸುತ್ತದೆ. "
                     "ಕಳಪೆ ಬಸಿ, ಗಟ್ಟಿ ಮಣ್ಣು ಮತ್ತು ನೆಮಟೋಡ್ ಹಾನಿಯಿಂದ ಹರಡುತ್ತದೆ.",
            prevention="Use healthy nursery stock. Improve soil drainage. "
                       "Avoid mechanical damage to roots during weeding. "
                       "Apply Trichoderma-enriched FYM during planting.",
            prevention_hi="स्वस्थ नर्सरी पौध उपयोग करें। मिट्टी की जल निकासी सुधारें। "
                          "निराई के दौरान जड़ों को यंत्रवत् नुकसान से बचाएं। "
                          "रोपण के समय ट्राइकोडर्मा समृद्ध FYM लगाएं।",
            prevention_kn="ಆರೋಗ್ಯಕರ ನರ್ಸರಿ ಸಸಿ ಬಳಸಿ. ಮಣ್ಣಿನ ಬಸಿ ಸುಧಾರಿಸಿ. "
                          "ಕಳೆ ತೆಗೆಯುವಾಗ ಬೇರುಗಳಿಗೆ ಯಾಂತ್ರಿಕ ಹಾನಿ ಮಾಡಬೇಡಿ. "
                          "ನಾಟಿ ಸಮಯದಲ್ಲಿ ಟ್ರೈಕೋಡರ್ಮಾ ಸಮೃದ್ಧ FYM ಹಾಕಿ.",
            organic_treatment="Apply Trichoderma harzianum (50g/plant) mixed with well-decomposed FYM. "
                              "Drench soil with Pseudomonas fluorescens (20g/L). Mulch with organic matter.",
            organic_treatment_hi="अच्छी तरह सड़ी FYM के साथ ट्राइकोडर्मा हार्ज़ियानम (50 ग्राम/पौधा) लगाएं। "
                                 "स्यूडोमोनास फ्लोरेसेंस (20 ग्राम/ली) से मिट्टी भिगोएं। जैविक पदार्थ से मल्चिंग करें।",
            organic_treatment_kn="ಚೆನ್ನಾಗಿ ಕೊಳೆತ FYM ಜೊತೆ ಟ್ರೈಕೋಡರ್ಮಾ ಹರ್ಜಿಯಾನಮ್ (50 ಗ್ರಾಂ/ಗಿಡ) ಹಾಕಿ. "
                                 "ಸ್ಯೂಡೋಮೋನಾಸ್ ಫ್ಲೋರೆಸೆನ್ಸ್ (20 ಗ್ರಾಂ/ಲೀ) ಮಣ್ಣಿಗೆ ಸುರಿಯಿರಿ. ಸಾವಯವ ವಸ್ತುವಿನಿಂದ ಮಲ್ಚ್ ಮಾಡಿ.",
            chemical_treatment="Drench soil around stems with Carbendazim 50% WP (1g/L) + Copper oxychloride 50% WP (3g/L). "
                               "Repeat at 45-day intervals. No complete chemical cure.",
            chemical_treatment_hi="तने के चारों ओर कार्बेन्डाज़िम 50% WP (1 ग्राम/ली) + कॉपर ऑक्सीक्लोराइड 50% WP (3 ग्राम/ली) से मिट्टी भिगोएं। "
                                  "45 दिन के अंतराल पर दोहराएं। कोई पूर्ण रासायनिक उपचार नहीं।",
            chemical_treatment_kn="ಕಾಂಡದ ಸುತ್ತ ಕಾರ್ಬೆಂಡಜಿಮ್ 50% WP (1 ಗ್ರಾಂ/ಲೀ) + ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ 50% WP (3 ಗ್ರಾಂ/ಲೀ) ಮಣ್ಣಿಗೆ ಸುರಿಯಿರಿ. "
                                  "45 ದಿನ ಅಂತರದಲ್ಲಿ ಪುನರಾವರ್ತಿಸಿ. ಸಂಪೂರ್ಣ ರಾಸಾಯನಿಕ ಉಪಚಾರ ಇಲ್ಲ.",
            chemical_composition="Carbendazim (C₉H₉N₃O₂): Systemic benzimidazole fungicide absorbed via roots.",
            chemical_composition_hi="कार्बेन्डाज़िम (C₉H₉N₃O₂): जड़ों द्वारा अवशोषित प्रणालीगत बेंज़िमिडाज़ोल कवकनाशी।",
            chemical_composition_kn="ಕಾರ್ಬೆಂಡಜಿಮ್ (C₉H₉N₃O₂): ಬೇರುಗಳ ಮೂಲಕ ಹೀರಿಕೊಳ್ಳುವ ವ್ಯವಸ್ಥಿತ ಬೆಂಜಿಮಿಡಜೋಲ್ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Fusarium_oxysporum.jpg/400px-Fusarium_oxysporum.jpg"
        ),
        Disease(
            name="Coffee Berry Disease (CBD)",
            name_hi="कॉफी बेरी रोग (सीबीडी)",
            name_kn="ಕಾಫಿ ಹಣ್ಣು ರೋಗ (ಸಿಬಿಡಿ)",
            crop_id=coffee.id,
            symptoms="Dark, sunken lesions on green developing berries. "
                     "Berries become black, shriveled, and mummified. "
                     "Affects beans inside — results in defective 'black beans'. Premature berry drop.",
            symptoms_hi="हरी विकसित होती बेरी पर गहरे, धंसे घाव। "
                        "बेरी काली, सिकुड़ी और ममी हो जाती हैं। "
                        "अंदर के बीज प्रभावित — दोषपूर्ण 'काले बीज' बनते हैं। समय से पहले बेरी गिरना।",
            symptoms_kn="ಹಸಿರು ಬೆಳೆಯುತ್ತಿರುವ ಹಣ್ಣುಗಳ ಮೇಲೆ ಕಪ್ಪು, ಕುಳಿಬಿದ್ದ ಗಾಯಗಳು. "
                        "ಹಣ್ಣುಗಳು ಕಪ್ಪಾಗಿ, ಸುಕ್ಕಾಗಿ ಒಣಗುತ್ತವೆ. "
                        "ಒಳಗಿನ ಬೀಜಗಳ ಮೇಲೆ ಪರಿಣಾಮ — ದೋಷಯುಕ್ತ 'ಕಪ್ಪು ಬೀಜಗಳು'. ಅಕಾಲಿಕ ಹಣ್ಣು ಉದುರುವಿಕೆ.",
            cause="Fungus Colletotrichum kahawae; spreads by rain splash. "
                  "Attacks expanding berries during monsoon. Most damaging in Arabica.",
            cause_hi="फफूंद कोलेटोट्राइकम कहावे; बारिश के छींटों से फैलता है। "
                     "मानसून में बढ़ती बेरी पर हमला करता है। अरेबिका में सबसे अधिक नुकसानदायक।",
            cause_kn="ಶಿಲೀಂಧ್ರ ಕೊಲೆಟೊಟ್ರೈಕಮ್ ಕಹಾವೇ; ಮಳೆ ಸಿಂಪರಣೆಯಿಂದ ಹರಡುತ್ತದೆ. "
                     "ಮಾನ್ಸೂನ್ ನಲ್ಲಿ ಬೆಳೆಯುತ್ತಿರುವ ಹಣ್ಣುಗಳ ಮೇಲೆ ದಾಳಿ ಮಾಡುತ್ತದೆ. ಅರೇಬಿಕಾದಲ್ಲಿ ಅತ್ಯಂತ ಹಾನಿಕಾರಕ.",
            prevention="Grow resistant varieties (e.g., Sln.6, Catimor). "
                       "Avoid over-shading. Maintain open canopy by pruning. "
                       "Timely harvesting of ripe berries.",
            prevention_hi="प्रतिरोधी किस्में उगाएं (जैसे Sln.6, कैटिमोर)। "
                          "अत्यधिक छाया से बचें। छंटाई से खुला छत्र बनाएं। "
                          "पकी बेरी की समय पर कटाई करें।",
            prevention_kn="ನಿರೋಧಕ ತಳಿಗಳನ್ನು ಬೆಳೆಸಿ (ಉದಾ., Sln.6, ಕ್ಯಾಟಿಮೋರ್). "
                          "ಅತಿ ನೆರಳು ಮಾಡಬೇಡಿ. ಕತ್ತರಿಸುವಿಕೆಯಿಂದ ತೆರೆದ ಮೇಲಾವರಣ ಕಾಪಾಡಿ. "
                          "ಹಣ್ಣಾದ ಹಣ್ಣುಗಳನ್ನು ಸಮಯಕ್ಕೆ ಕೊಯ್ಲು ಮಾಡಿ.",
            organic_treatment="Spray Bordeaux mixture (0.5%) at pea-berry stage. "
                              "Apply Trichoderma (10g/L) at the onset of berry development. "
                              "Remove and destroy infected berries from the plant and ground.",
            organic_treatment_hi="मटर-बेरी अवस्था में बोर्डो मिश्रण (0.5%) छिड़कें। "
                                 "बेरी विकास की शुरुआत में ट्राइकोडर्मा (10 ग्राम/ली) लगाएं। "
                                 "पौधे और जमीन से संक्रमित बेरी हटाकर नष्ट करें।",
            organic_treatment_kn="ಬಟಾಣಿ ಹಣ್ಣು ಹಂತದಲ್ಲಿ ಬೋರ್ಡೋ ಮಿಶ್ರಣ (0.5%) ಸಿಂಪಡಿಸಿ. "
                                 "ಹಣ್ಣು ಬೆಳವಣಿಗೆ ಆರಂಭದಲ್ಲಿ ಟ್ರೈಕೋಡರ್ಮಾ (10 ಗ್ರಾಂ/ಲೀ) ಹಾಕಿ. "
                                 "ಗಿಡ ಮತ್ತು ನೆಲದಿಂದ ಸೋಂಕಿತ ಹಣ್ಣುಗಳನ್ನು ತೆಗೆದು ನಾಶಮಾಡಿ.",
            chemical_treatment="Spray Chlorothalonil 75% WP (2g/L) or Carbendazim 50% WP (1g/L) at berry expansion stage. "
                               "Apply 3 rounds at 21-day intervals from June.",
            chemical_treatment_hi="बेरी विस्तार अवस्था में क्लोरोथैलोनिल 75% WP (2 ग्राम/ली) या कार्बेन्डाज़िम 50% WP (1 ग्राम/ली) छिड़कें। "
                                  "जून से 21 दिन के अंतराल पर 3 बार लगाएं।",
            chemical_treatment_kn="ಹಣ್ಣು ವಿಸ್ತರಣೆ ಹಂತದಲ್ಲಿ ಕ್ಲೋರೋಥಾಲೋನಿಲ್ 75% WP (2 ಗ್ರಾಂ/ಲೀ) ಅಥವಾ ಕಾರ್ಬೆಂಡಜಿಮ್ 50% WP (1 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಜೂನ್ ನಿಂದ 21 ದಿನ ಅಂತರದಲ್ಲಿ 3 ಸುತ್ತು ಹಾಕಿ.",
            chemical_composition="Chlorothalonil (C₈Cl₄N₂): Broad-spectrum chloronitrile contact fungicide.",
            chemical_composition_hi="क्लोरोथैलोनिल (C₈Cl₄N₂): व्यापक-स्पेक्ट्रम क्लोरोनाइट्राइल सम्पर्क कवकनाशी।",
            chemical_composition_kn="ಕ್ಲೋರೋಥಲೋನಿಲ್ (C₈Cl₄N₂): ವಿಶಾಲ-ವ್ಯಾಪ್ತಿಯ ಕ್ಲೋರೋನೈಟ್ರೈಲ್ ಸಂಪರ್ಕ ಶಿಲೀಂಧ್ರನಾಶಕ.",
            severity="High",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Cercospora_Berry_Blotch.jpg/400px-Cercospora_Berry_Blotch.jpg"
        )
    ]

    coffee_pests = [
        Pest(
            name="White Stem Borer",
            name_hi="सफ़ेद तना छेदक",
            name_kn="ಬಿಳಿ ಕಾಂಡ ಕೊರಕ",
            crop_id=coffee.id,
            scientific_name="Xylotrechus quadripes",
            symptoms="Ridges and galleries under bark with frass. "
                     "Bark peeling reveals larval tunnels. Branches wilt and dry up. "
                     "Exit holes on main stem from adult emergence.",
            symptoms_hi="छाल के नीचे उभार और सुरंगें मल सहित। "
                        "छाल छीलने पर लार्वा सुरंगें दिखती हैं। शाखाएं मुरझाकर सूख जाती हैं। "
                        "मुख्य तने पर वयस्क निकलने के छेद।",
            symptoms_kn="ತೊಗಟೆ ಅಡಿಯಲ್ಲಿ ಹಿಕ್ಕೆಯೊಂದಿಗೆ ರೇಖೆ ಮತ್ತು ಸುರಂಗಗಳು. "
                        "ತೊಗಟೆ ಸುಲಿದಾಗ ಲಾರ್ವಾ ಸುರಂಗಗಳು ಕಾಣುತ್ತವೆ. ಕೊಂಬೆಗಳು ಬಾಡಿ ಒಣಗುತ್ತವೆ. "
                        "ವಯಸ್ಕರ ಹೊರಬರುವ ರಂಧ್ರಗಳು ಮುಖ್ಯ ಕಾಂಡದ ಮೇಲೆ.",
            damage_type="Internal feeder — larvae bore into stems, disrupting water and nutrient transport.",
            damage_type_hi="आंतरिक भक्षक — लार्वा तनों में छेद करके जल और पोषक तत्व परिवहन बाधित करते हैं।",
            damage_type_kn="ಆಂತರಿಕ ಹುಳು — ಲಾರ್ವಾ ಕಾಂಡಗಳಲ್ಲಿ ಕೊರೆದು ನೀರು ಮತ್ತು ಪೋಷಕಾಂಶ ಸಾಗಣೆ ಅಡ್ಡಿಪಡಿಸುತ್ತದೆ.",
            prevention="Maintain thick overhead shade. Apply Bordeaux paste on stems up to 3 feet height. "
                       "Trace and destroy grubs in stems. Remove and burn severely infested plants.",
            prevention_hi="मोटी ऊपरी छाया बनाएं। तनों पर 3 फीट ऊंचाई तक बोर्डो पेस्ट लगाएं। "
                          "तनों में लार्वा खोजकर नष्ट करें। अधिक संक्रमित पौधों को हटाकर जलाएं।",
            prevention_kn="ದಪ್ಪ ಮೇಲಿನ ನೆರಳು ಕಾಪಾಡಿ. ಕಾಂಡಗಳ ಮೇಲೆ 3 ಅಡಿ ಎತ್ತರದ ವರೆಗೆ ಬೋರ್ಡೋ ಪೇಸ್ಟ್ ಹಚ್ಚಿ. "
                          "ಕಾಂಡಗಳಲ್ಲಿ ಹುಳುಗಳನ್ನು ಹುಡುಕಿ ನಾಶಮಾಡಿ. ತೀವ್ರ ಬಾಧಿತ ಗಿಡಗಳನ್ನು ತೆಗೆದು ಸುಡಿ.",
            organic_treatment="Apply lime wash + Bordeaux paste on main stem and primary branches. "
                              "Pad stems with Chlorpyriphos-soaked sponge at bore holes. "
                              "Use entomopathogenic fungi (Beauveria bassiana).",
            organic_treatment_hi="मुख्य तने और प्राथमिक शाखाओं पर चूने की धुलाई + बोर्डो पेस्ट लगाएं। "
                                 "छेदों पर क्लोरपाइरीफॉस भिगोई स्पंज से तने पर पैड लगाएं। "
                                 "कीट रोगजनक फफूंद (ब्यूवेरिया बैसियाना) का उपयोग करें।",
            organic_treatment_kn="ಮುಖ್ಯ ಕಾಂಡ ಮತ್ತು ಪ್ರಾಥಮಿಕ ಕೊಂಬೆಗಳ ಮೇಲೆ ಸುಣ್ಣ + ಬೋರ್ಡೋ ಪೇಸ್ಟ್ ಹಚ್ಚಿ. "
                                 "ರಂಧ್ರಗಳಲ್ಲಿ ಕ್ಲೋರ್ಪೈರಿಫಾಸ್ ನೆನೆಸಿದ ಸ್ಪಂಜ್ ಇಡಿ. "
                                 "ಕೀಟ ರೋಗಕಾರಕ ಶಿಲೀಂಧ್ರ (ಬ್ಯೂವೇರಿಯಾ ಬ್ಯಾಸಿಯಾನಾ) ಬಳಸಿ.",
            chemical_treatment="Swab main stem with Chlorpyriphos 20% EC (5ml/L) twice a year (April & October). "
                               "Inject Dichlorvos (DDVP) into bore holes using syringe and seal with mud.",
            chemical_treatment_hi="वर्ष में दो बार (अप्रैल और अक्टूबर) मुख्य तने पर क्लोरपाइरीफॉस 20% EC (5 मिली/ली) से पोंछें। "
                                  "सिरिंज से छेदों में डाइक्लोर्वोस (DDVP) इंजेक्ट करें और मिट्टी से सील करें।",
            chemical_treatment_kn="ವರ್ಷಕ್ಕೆ ಎರಡು ಬಾರಿ (ಏಪ್ರಿಲ್ ಮತ್ತು ಅಕ್ಟೋಬರ್) ಮುಖ್ಯ ಕಾಂಡಕ್ಕೆ ಕ್ಲೋರ್ಪೈರಿಫಾಸ್ 20% EC (5 ಮಿಲೀ/ಲೀ) ಹಚ್ಚಿ. "
                                  "ಸಿರಿಂಜ್ ಬಳಸಿ ರಂಧ್ರಗಳಿಗೆ ಡೈಕ್ಲೋರ್ವಾಸ್ (DDVP) ಚುಚ್ಚಿ ಮಣ್ಣಿನಿಂದ ಮುಚ್ಚಿ.",
            chemical_composition="Chlorpyriphos (C₉H₁₁Cl₃NO₃PS): Organophosphate insecticide inhibiting acetylcholinesterase.",
            chemical_composition_hi="क्लोरपाइरीफॉस (C₉H₁₁Cl₃NO₃PS): एसिटाइलकोलिनेस्टरेज़ रोकने वाला ऑर्गेनोफॉस्फेट कीटनाशक।",
            chemical_composition_kn="ಕ್ಲೋರ್ಪೈರಿಫಾಸ್ (C₉H₁₁Cl₃NO₃PS): ಅಸಿಟೈಲ್ಕೋಲಿನೆಸ್ಟರೇಸ್ ತಡೆಯುವ ಆರ್ಗಾನೋಫಾಸ್ಫೇಟ್ ಕೀಟನಾಶಕ.",
            severity="High",
            active_season="March–May (adult emergence), Year-round (larval damage)",
            active_season_hi="मार्च–मई (वयस्क उद्भव), वर्ष भर (लार्वा नुकसान)",
            active_season_kn="ಮಾರ್ಚ್–ಮೇ (ವಯಸ್ಕರ ಹೊರಹೊಮ್ಮುವಿಕೆ), ವರ್ಷವಿಡೀ (ಲಾರ್ವಾ ಹಾನಿ)",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Xylotrechus_quadripes.jpg/400px-Xylotrechus_quadripes.jpg"
        ),
        Pest(
            name="Coffee Berry Borer",
            name_hi="कॉफी बेरी छेदक",
            name_kn="ಕಾಫಿ ಹಣ್ಣು ಕೊರಕ",
            crop_id=coffee.id,
            scientific_name="Hypothenemus hampei",
            symptoms="Tiny circular bore holes (≈1mm) at the tip of berries. "
                     "Larvae feed on beans inside the berry. Damaged beans show tunnels and frass. "
                     "Infested berries may drop early.",
            symptoms_hi="बेरी की नोक पर छोटे गोलाकार छेद (≈1 मिमी)। "
                        "लार्वा बेरी के अंदर बीज खाते हैं। क्षतिग्रस्त बीज में सुरंगें और मल दिखता है। "
                        "संक्रमित बेरी जल्दी गिर सकती हैं।",
            symptoms_kn="ಹಣ್ಣುಗಳ ತುದಿಯಲ್ಲಿ ಸಣ್ಣ ವೃತ್ತಾಕಾರ ರಂಧ್ರಗಳು (≈1 ಮಿಮೀ). "
                        "ಲಾರ್ವಾ ಹಣ್ಣಿನ ಒಳಗೆ ಬೀಜಗಳನ್ನು ತಿನ್ನುತ್ತದೆ. ಹಾನಿಗೊಳಗಾದ ಬೀಜಗಳಲ್ಲಿ ಸುರಂಗ ಮತ್ತು ಹಿಕ್ಕೆ. "
                        "ಬಾಧಿತ ಹಣ್ಣುಗಳು ಬೇಗ ಉದುರಬಹುದು.",
            damage_type="Internal feeder — adult female bores into berries, lays eggs; larvae feed on beans.",
            damage_type_hi="आंतरिक भक्षक — वयस्क मादा बेरी में छेद करके अंडे देती है; लार्वा बीज खाते हैं।",
            damage_type_kn="ಆಂತರಿಕ ಹುಳು — ವಯಸ್ಕ ಹೆಣ್ಣು ಹಣ್ಣುಗಳಲ್ಲಿ ಕೊರೆದು ಮೊಟ್ಟೆ ಇಡುತ್ತದೆ; ಲಾರ್ವಾ ಬೀಜಗಳನ್ನು ತಿನ್ನುತ್ತದೆ.",
            prevention="Timely and clean harvesting — no berries left on plant or ground. "
                       "Maintain shade at 40-50%. Community-level synchronized control.",
            prevention_hi="समय पर और साफ कटाई — पौधे या जमीन पर कोई बेरी न छोड़ें। "
                          "छाया 40-50% बनाएं। समुदाय स्तर पर समकालिक नियंत्रण।",
            prevention_kn="ಸಮಯಕ್ಕೆ ಸರಿಯಾಗಿ ಕೊಯ್ಲು — ಗಿಡ ಅಥವಾ ನೆಲದ ಮೇಲೆ ಯಾವುದೇ ಹಣ್ಣು ಬಿಡಬೇಡಿ. "
                          "ನೆರಳನ್ನು 40-50% ಕಾಪಾಡಿ. ಸಮುದಾಯ ಮಟ್ಟದ ಸಮಕಾಲಿಕ ನಿಯಂತ್ರಣ.",
            organic_treatment="Use Beauveria bassiana (5×10⁸ CFU/g at 5g/L) spray on berries. "
                              "Install Brocap traps with methanol-ethanol bait. "
                              "Release Cephalonomia stephanoderis (bethylid parasitoid).",
            organic_treatment_hi="बेरी पर ब्यूवेरिया बैसियाना (5×10⁸ CFU/ग्रा, 5 ग्राम/ली) छिड़कें। "
                                 "मेथनॉल-एथनॉल चारे के साथ ब्रोकैप जाल लगाएं। "
                                 "सेफालोनोमिया स्टीफनोडेरिस (परजीवी) छोड़ें।",
            organic_treatment_kn="ಹಣ್ಣುಗಳ ಮೇಲೆ ಬ್ಯೂವೇರಿಯಾ ಬ್ಯಾಸಿಯಾನಾ (5×10⁸ CFU/ಗ್ರಾ, 5 ಗ್ರಾಂ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                 "ಮೆಥನಾಲ್-ಎಥನಾಲ್ ಆಮಿಷದೊಂದಿಗೆ ಬ್ರೋಕ್ಯಾಪ್ ಜಾಲ ಅಳವಡಿಸಿ. "
                                 "ಸೆಫಲೋನೋಮಿಯಾ ಸ್ಟೆಫನೋಡೆರಿಸ್ (ಪರಾವಲಂಬಿ) ಬಿಡುಗಡೆ ಮಾಡಿ.",
            chemical_treatment="Spray Chlorpyriphos 20% EC (3ml/L) on berries. "
                               "Endosulfan-based treatments are now banned. Use only approved insecticides.",
            chemical_treatment_hi="बेरी पर क्लोरपाइरीफॉस 20% EC (3 मिली/ली) छिड़कें। "
                                  "एंडोसल्फान आधारित उपचार अब प्रतिबंधित हैं। केवल अनुमोदित कीटनाशक उपयोग करें।",
            chemical_treatment_kn="ಹಣ್ಣುಗಳ ಮೇಲೆ ಕ್ಲೋರ್ಪೈರಿಫಾಸ್ 20% EC (3 ಮಿಲೀ/ಲೀ) ಸಿಂಪಡಿಸಿ. "
                                  "ಎಂಡೋಸಲ್ಫಾನ್ ಆಧಾರಿತ ಉಪಚಾರಗಳು ಈಗ ನಿಷೇಧಿಸಲಾಗಿದೆ. ಅನುಮೋದಿತ ಕೀಟನಾಶಕಗಳನ್ನು ಮಾತ್ರ ಬಳಸಿ.",
            chemical_composition="Beauveria bassiana: Entomopathogenic fungus causing muscardine disease in beetles.",
            chemical_composition_hi="ब्यूवेरिया बैसियाना: भृंगों में मस्करडाइन रोग पैदा करने वाला कीट रोगजनक कवक।",
            chemical_composition_kn="ಬ್ಯೂವೇರಿಯಾ ಬ್ಯಾಸಿಯಾನಾ: ಜೀರುಂಡೆಗಳಲ್ಲಿ ಮಸ್ಕರ್ಡೈನ್ ರೋಗ ಉಂಟುಮಾಡುವ ಕೀಟ ರೋಗಕಾರಕ ಶಿಲೀಂಧ್ರ.",
            severity="High",
            active_season="April–August (during berry development)",
            active_season_hi="अप्रैल–अगस्त (बेरी विकास के दौरान)",
            active_season_kn="ಏಪ್ರಿಲ್–ಆಗಸ್ಟ್ (ಹಣ್ಣು ಬೆಳವಣಿಗೆ ಸಮಯ)",
            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Coffee_berry_borer1.jpg/400px-Coffee_berry_borer1.jpg"
        )
    ]

    # Add all diseases and pests
    for disease in paddy_diseases + chilli_diseases + coffee_diseases:
        db.session.add(disease)

    for pest in paddy_pests + chilli_pests + coffee_pests:
        db.session.add(pest)

    db.session.commit()
    print("Database seeded with 3 crops, 13 diseases, and 7 pests.")
