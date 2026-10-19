"""Plain-language information about each condition the app can predict.

General educational content only. It is not medical advice.
"""


def _norm(name):
    return " ".join(str(name).lower().split())


RAW_DISEASE_INFO = {
    "Fungal infection": {
        "about": "Fungal infections are skin or nail conditions caused by fungi, such as ringworm or athlete's foot.",
        "how_it_occurs": "Fungi thrive in warm, moist areas. They spread through skin contact, shared towels, damp socks and shoes.",
        "precautions": ["Keep skin clean and dry, especially between toes and skin folds.", "Wear breathable cotton clothes and change socks daily.", "Do not share towels, clothes or footwear.", "Use antifungal creams exactly as prescribed."],
        "diet_follow": ["Yogurt with live cultures", "Garlic", "Fresh fruits and vegetables", "Whole grains", "Plenty of water"],
        "diet_avoid": ["Excess sugar and sweets", "Refined carbohydrates", "Alcohol", "Highly processed foods", "Leftover or mouldy food"],
    },
    "Allergy": {
        "about": "An allergy is an overreaction of the immune system to a harmless substance such as pollen, dust, food or medicine.",
        "how_it_occurs": "The immune system wrongly treats the trigger as harmful and releases histamine, causing itching, rash, sneezing or swelling.",
        "precautions": ["Identify your triggers and avoid them where possible.", "Keep the home dust-free and use allergy-proof bedding.", "Take antihistamines as advised by a doctor.", "Carry prescribed adrenaline (epinephrine) if you have a severe allergy."],
        "diet_follow": ["Fruits and vegetables rich in vitamin C", "Omega-3 foods such as fish", "Ginger", "Probiotic foods", "Plenty of water"],
        "diet_avoid": ["Foods you know trigger your allergy", "Alcohol", "Highly processed foods", "Food additives that cause reactions"],
    },
    "GERD": {
        "about": "Gastro-oesophageal reflux disease (GERD) is a long-term condition where stomach acid repeatedly flows back into the food pipe.",
        "how_it_occurs": "A weak valve between the stomach and food pipe lets acid rise. Excess weight, pregnancy, large meals, smoking and lying down after eating make it worse.",
        "precautions": ["Eat smaller meals more often.", "Avoid lying down for 2 to 3 hours after eating.", "Raise the head of your bed slightly.", "Maintain a healthy weight and stop smoking."],
        "diet_follow": ["Oatmeal", "Bananas and melons", "Green vegetables", "Lean protein", "Ginger tea"],
        "diet_avoid": ["Spicy food", "Citrus fruits and tomatoes", "Chocolate, coffee and mint", "Fried or fatty food", "Carbonated drinks and alcohol"],
    },
    "Chronic cholestasis": {
        "about": "Chronic cholestasis is a long-lasting condition where the flow of bile from the liver is reduced or blocked.",
        "how_it_occurs": "Bile salts build up and cause itching, and bilirubin can cause yellowing of the skin and eyes. Causes include liver disease, bile duct problems and some medicines.",
        "precautions": ["See a liver specialist for proper tests.", "Do not start any medicine without medical advice.", "Track itching and yellowing and report changes to your doctor.", "Avoid alcohol completely."],
        "diet_follow": ["Low-fat balanced meals", "Oats and high-fibre foods", "Fruits and vegetables", "Lean protein", "Plenty of water"],
        "diet_avoid": ["Alcohol", "Fried and fatty foods", "High-fat dairy", "Large, heavy meals", "Processed foods"],
    },
    "Drug Reaction": {
        "about": "A drug reaction is an unwanted response to a medicine, ranging from a mild rash to a serious, life-threatening reaction.",
        "how_it_occurs": "The body reacts abnormally to a drug through allergy or side effects. Risk rises with several medicines, high doses or a past reaction.",
        "precautions": ["Tell every doctor and pharmacist about past reactions.", "Keep an up-to-date list of your medicines and allergies.", "Do not stop or change medicines without speaking to a doctor.", "Get urgent care for facial swelling, breathing trouble or a rapidly spreading rash."],
        "diet_follow": ["Plenty of fluids", "Light, easy-to-digest meals", "Fruits and vegetables", "Cool, soothing foods if mouth or throat is sore"],
        "diet_avoid": ["Alcohol while on medicines", "Self-prescribed supplements", "Grapefruit juice with certain medicines (check with a pharmacist)"],
    },
    "Peptic ulcer disease": {
        "about": "A peptic ulcer is an open sore in the lining of the stomach or the upper small intestine.",
        "how_it_occurs": "Most are caused by Helicobacter pylori infection or long-term use of painkillers such as ibuprofen and aspirin. Smoking and alcohol can make them worse.",
        "precautions": ["Complete the full course of any prescribed treatment.", "Avoid frequent painkiller use without medical advice.", "Stop smoking and limit alcohol.", "Seek urgent care for black stools or vomiting blood."],
        "diet_follow": ["Oatmeal and bananas", "Yogurt", "Cooked vegetables", "Lean meats", "Small, frequent meals"],
        "diet_avoid": ["Spicy food", "Coffee and alcohol", "Carbonated drinks", "Fried and fatty foods", "Citrus if it causes pain"],
    },
    "AIDS": {
        "about": "AIDS is the most advanced stage of HIV infection, when the immune system is severely weakened.",
        "how_it_occurs": "HIV spreads through unprotected sex, shared needles, and from mother to child. It gradually destroys immune cells if left untreated.",
        "precautions": ["Get tested regularly and know your status.", "Use condoms and practise safer sex.", "Never share needles or injecting equipment.", "Take antiretroviral treatment daily as prescribed."],
        "diet_follow": ["Balanced meals with vegetables and fruit", "Lean protein", "Whole grains", "Clean, safe drinking water", "Regular meals to support medicines"],
        "diet_avoid": ["Undercooked meat, eggs or seafood", "Unpasteurised dairy", "Unwashed raw produce", "Alcohol and smoking", "Skipping medicine doses"],
    },
    "Diabetes": {
        "about": "Diabetes is a long-term condition in which blood sugar (glucose) levels stay too high.",
        "how_it_occurs": "In type 1, the body makes little or no insulin. In type 2, the body resists insulin. Family history, excess weight, inactivity and age increase risk.",
        "precautions": ["Check blood sugar as advised by your doctor.", "Take medicines or insulin on time.", "Exercise regularly, such as a daily walk.", "Check your feet daily and have eye and kidney checks yearly."],
        "diet_follow": ["High-fibre vegetables", "Whole grains and legumes", "Lean protein", "Nuts and olive oil", "Regular meals at set times"],
        "diet_avoid": ["Sugary drinks and sweets", "Large amounts of white bread and white rice", "Fried foods", "Processed meats", "Excess fruit juice"],
    },
    "Gastroenteritis": {
        "about": "Gastroenteritis is inflammation of the stomach and intestines, often called stomach flu.",
        "how_it_occurs": "It is usually caused by viruses such as norovirus or rotavirus, or by bacteria in contaminated food or water. It spreads through unwashed hands.",
        "precautions": ["Wash hands with soap often, especially after using the toilet.", "Drink safe, boiled or filtered water.", "Cook food thoroughly and store it properly.", "Stay away from work or school until 48 hours after symptoms end."],
        "diet_follow": ["Oral rehydration solution (ORS)", "Clear fluids and soups", "Bananas, rice, toast and plain potatoes", "Yogurt once recovering"],
        "diet_avoid": ["Dairy until fully recovered", "Fatty or fried foods", "Caffeine and alcohol", "Sugary drinks and fruit juice", "Spicy food"],
    },
    "Bronchial Asthma": {
        "about": "Asthma is a long-term condition in which the airways become inflamed and narrow, making breathing difficult.",
        "how_it_occurs": "Triggers include allergens, smoke, cold air, exercise, infections and stress. The airways tighten and produce mucus, causing wheezing and cough.",
        "precautions": ["Use inhalers exactly as prescribed.", "Always carry your rescue inhaler.", "Avoid triggers such as smoke, dust and strong fumes.", "Create an asthma action plan with your doctor and get the flu vaccine."],
        "diet_follow": ["Fruits and vegetables rich in antioxidants", "Omega-3 fish", "Whole grains", "Ginger and turmeric in cooking", "Plenty of water"],
        "diet_avoid": ["Smoking and second-hand smoke", "Foods or drinks you know trigger symptoms", "Very salty or processed foods", "Excess alcohol"],
    },
    "Hypertension": {
        "about": "Hypertension (high blood pressure) means blood pushes too hard against the artery walls over time.",
        "how_it_occurs": "Causes include age, excess salt, obesity, stress, smoking, alcohol, inactivity and family history. It often has no symptoms.",
        "precautions": ["Check your blood pressure regularly.", "Take prescribed medicines every day.", "Reduce salt and be physically active.", "Stop smoking, manage stress and sleep 7 to 8 hours a night."],
        "diet_follow": ["Vegetables and fruits", "Whole grains", "Low-fat dairy", "Beans, nuts and fish", "Potassium-rich foods such as bananas and sweet potato (unless a kidney doctor advises otherwise)"],
        "diet_avoid": ["Salt and salty snacks", "Pickles and cured meats", "Processed and packaged foods", "Sugary drinks", "Excess alcohol and caffeine"],
    },
    "Migraine": {
        "about": "A migraine is a recurring headache, often on one side, with throbbing pain, nausea and sensitivity to light and sound.",
        "how_it_occurs": "It involves changes in brain activity and blood vessels. Triggers include stress, poor sleep, skipped meals, hormonal changes, bright light and some foods.",
        "precautions": ["Keep a headache diary to identify your triggers.", "Keep regular sleep times.", "Rest in a dark, quiet room during an attack.", "Take preventive or rescue medicines only as prescribed."],
        "diet_follow": ["Regular meals", "Plenty of water", "Magnesium-rich foods such as leafy greens, nuts and seeds", "Whole grains", "Ginger tea"],
        "diet_avoid": ["Aged cheese", "Processed meats with nitrates", "Alcohol, especially red wine", "Excess caffeine", "Skipping meals and artificial sweeteners"],
    },
    "Cervical spondylosis": {
        "about": "Cervical spondylosis is age-related wear and tear of the bones and discs in the neck.",
        "how_it_occurs": "Discs lose water and thin, bone spurs form, and joints wear down. This can press on nerves and cause neck pain, stiffness or arm numbness. Poor posture adds strain.",
        "precautions": ["Keep good posture, especially when using phones and computers.", "Take breaks from screens every 30 minutes.", "Use a supportive pillow.", "Do gentle neck exercises and see a physiotherapist if pain persists."],
        "diet_follow": ["Calcium and vitamin D foods such as milk, yogurt and eggs", "Fish and omega-3 foods", "Leafy greens", "Plenty of water"],
        "diet_avoid": ["Smoking, which slows disc healing", "Excess sugar and processed foods", "Excess alcohol", "Weight gain from inactivity"],
    },
    "Paralysis (brain hemorrhage)": {
        "about": "Paralysis after a brain haemorrhage is loss of movement or feeling, usually on one side of the body, after bleeding in the brain.",
        "how_it_occurs": "A blood vessel in the brain bursts or leaks and damages brain tissue. Causes include high blood pressure, aneurysms, blood thinners and head injury.",
        "precautions": ["This is a medical emergency. Call emergency services immediately.", "Control blood pressure with prescribed medicines.", "Attend rehabilitation sessions regularly.", "Prevent falls at home with grab rails and clear walkways."],
        "diet_follow": ["Low-salt diet with fruits and vegetables", "Whole grains and lean protein", "Omega-3 fish", "Soft, easy-to-swallow foods if swallowing is weak, as advised by a therapist"],
        "diet_avoid": ["Salty and processed food", "Smoking and alcohol", "Fatty and fried foods", "Taking blood thinners without medical supervision"],
    },
    "Jaundice": {
        "about": "Jaundice is yellowing of the skin and the whites of the eyes, caused by high levels of bilirubin in the blood.",
        "how_it_occurs": "Bilirubin is a waste product from broken-down red blood cells that the liver normally clears. Jaundice happens when the liver is damaged, bile flow is blocked, or many red cells break down.",
        "precautions": ["See a doctor promptly if your eyes or skin turn yellow.", "Avoid alcohol and do not take extra painkillers.", "Get vaccinated against hepatitis A and B.", "Seek urgent care for confusion, bleeding or severe abdominal pain."],
        "diet_follow": ["Light, nutritious meals", "Fruits and vegetables", "Whole grains and lean protein", "Plenty of boiled or purified water"],
        "diet_avoid": ["Alcohol", "Fried, fatty and processed foods", "Raw shellfish", "Excess salt"],
    },
    "Malaria": {
        "about": "Malaria is a serious illness caused by Plasmodium parasites, spread by infected Anopheles mosquitoes.",
        "how_it_occurs": "A mosquito bite injects parasites into the blood. They multiply in the liver and red blood cells, causing fever, chills and sweating in cycles.",
        "precautions": ["Sleep under insecticide-treated mosquito nets.", "Use mosquito repellent and wear long sleeves in the evening.", "Remove standing water around the home.", "Get tested quickly for any fever, especially after travel to risk areas."],
        "diet_follow": ["Fluids and oral rehydration solution", "Light, nutritious meals", "Fruits and vegetables", "Iron-rich foods after recovery"],
        "diet_avoid": ["Alcohol", "Heavy, fatty meals during fever", "Skipping fluids", "Unprescribed or unknown medicines"],
    },
    "Chicken pox": {
        "about": "Chickenpox is a highly contagious viral infection that causes itchy, fluid-filled red spots over the body.",
        "how_it_occurs": "It is caused by the varicella-zoster virus, spread through airborne droplets or contact with blister fluid. It can spread a day or two before the rash appears.",
        "precautions": ["Stay home until all blisters have crusted over.", "Avoid scratching to prevent scars and infection.", "Use calamine lotion and cool baths to relieve itching.", "Get urgent care for high fever, breathing trouble or a rash near the eyes."],
        "diet_follow": ["Plenty of fluids", "Soft, easy-to-swallow foods", "Vitamin C fruits", "Porridge and yogurt"],
        "diet_avoid": ["Salty, spicy or acidic foods that sting mouth sores", "Aspirin for children (use only as a doctor advises)", "Alcohol", "Very hot drinks that increase sweating and itching"],
    },
    "Dengue": {
        "about": "Dengue is a viral infection spread by Aedes mosquitoes, causing high fever, severe body pain and sometimes bleeding.",
        "how_it_occurs": "A mosquito bite transmits the virus. Symptoms often start 4 to 10 days later. Warning signs include severe stomach pain, persistent vomiting and bleeding.",
        "precautions": ["Empty and clean water containers at least once a week.", "Use mosquito nets and repellent, even during the day.", "Do not take aspirin or ibuprofen for dengue; use paracetamol only as advised.", "Get your platelet count checked and go to hospital if warning signs appear."],
        "diet_follow": ["Oral rehydration solution", "Coconut water and clear soups", "Fruits and vegetables", "Light, easily digested meals"],
        "diet_avoid": ["Aspirin and ibuprofen (they increase bleeding risk)", "Alcohol", "Fried and spicy food", "Letting yourself become dehydrated"],
    },
    "Typhoid": {
        "about": "Typhoid is a bacterial infection caused by Salmonella Typhi, causing prolonged fever, weakness and stomach pain.",
        "how_it_occurs": "It spreads through contaminated food and water and poor hygiene. The bacteria pass into the intestine and then the bloodstream.",
        "precautions": ["Drink only boiled or filtered water.", "Wash hands with soap before eating and after using the toilet.", "Eat freshly cooked, hot food.", "Take vaccination before travelling and complete the full antibiotic course."],
        "diet_follow": ["Boiled water", "Soft, easily digested foods such as khichdi, dal and rice", "Boiled vegetables and bananas", "Yogurt and plenty of fluids"],
        "diet_avoid": ["Street food", "Raw salads and cut fruit from unknown sources", "Unpasteurised milk", "Spicy and oily food", "Alcohol"],
    },
    "hepatitis A": {
        "about": "Hepatitis A is a short-term liver infection caused by the hepatitis A virus.",
        "how_it_occurs": "It spreads through contaminated food or water and close contact with infected stool. It usually clears within weeks and does not become long-term.",
        "precautions": ["Get vaccinated.", "Wash hands after using the toilet and before cooking.", "Drink safe water and avoid sharing utensils.", "Rest during illness and avoid alcohol."],
        "diet_follow": ["Fluids", "Light, balanced meals", "Well-washed fruits and vegetables", "Rice, oats and lean protein"],
        "diet_avoid": ["Alcohol", "Fried and fatty food", "Raw shellfish", "Unwashed produce", "High doses of painkillers without advice"],
    },
    "Hepatitis B": {
        "about": "Hepatitis B is a viral liver infection that can become long-term and lead to scarring or liver cancer.",
        "how_it_occurs": "It spreads through infected blood, unprotected sex, shared needles, and from mother to baby at birth. It can stay silent for years.",
        "precautions": ["Get vaccinated, including infants.", "Do not share razors, toothbrushes or needles.", "Use condoms during sex.", "Have regular liver check-ups as advised."],
        "diet_follow": ["Balanced diet with fruits and vegetables", "Whole grains and lean protein", "Plenty of water", "Regular check-ups"],
        "diet_avoid": ["Alcohol", "Fried and fatty foods", "Unprescribed herbal supplements that may stress the liver", "Raw shellfish"],
    },
    "Hepatitis C": {
        "about": "Hepatitis C is a viral liver infection that often becomes long-term and can lead to cirrhosis (scarring of the liver).",
        "how_it_occurs": "It spreads mainly through blood, such as shared needles and unsterile medical or tattoo equipment. Many people have no symptoms for years.",
        "precautions": ["Get tested, especially if you have risk factors.", "Effective antiviral treatment is available. Discuss it with your doctor.", "Do not share needles or personal items such as razors.", "Avoid alcohol and get regular liver monitoring."],
        "diet_follow": ["Vegetables, fruits and whole grains", "Lean protein", "Plenty of water", "Balanced meals with less processed food"],
        "diet_avoid": ["Alcohol", "Fatty and processed foods", "Sugary drinks", "Unnecessary supplements"],
    },
    "Hepatitis D": {
        "about": "Hepatitis D is a liver infection that only occurs together with hepatitis B, making the illness more severe.",
        "how_it_occurs": "The hepatitis D virus needs hepatitis B to infect liver cells. It spreads through blood and sexual contact, like hepatitis B.",
        "precautions": ["Get vaccinated against hepatitis B, which also protects against hepatitis D.", "Do not share needles or personal items.", "Practise safer sex.", "Follow up regularly with a liver specialist."],
        "diet_follow": ["Balanced diet with vegetables and fruits", "Whole grains and lean protein", "Adequate fluids"],
        "diet_avoid": ["Alcohol", "Fried and fatty foods", "Excess sugar", "Unprescribed supplements"],
    },
    "hepatitis E": {
        "about": "Hepatitis E is an acute liver infection usually caused by contaminated drinking water.",
        "how_it_occurs": "It spreads through faecal contamination of water and sometimes undercooked pork or game meat. It is usually short-lived but can be dangerous in pregnancy.",
        "precautions": ["Drink safe, treated water.", "Practise good hand hygiene.", "Cook meat thoroughly.", "Pregnant women should seek medical care early."],
        "diet_follow": ["Fluids", "Easy-to-digest meals", "Well-washed fruits and vegetables", "Rice, oats and well-cooked lean protein"],
        "diet_avoid": ["Undercooked meat", "Raw shellfish", "Alcohol", "Oily food", "Unwashed produce"],
    },
    "Alcoholic hepatitis": {
        "about": "Alcoholic hepatitis is inflammation of the liver caused by heavy alcohol use over time.",
        "how_it_occurs": "Alcohol damages liver cells and causes fat build-up and inflammation. It can progress to cirrhosis if drinking continues.",
        "precautions": ["Stop drinking completely and seek medical support if needed.", "Take prescribed medicines and attend all liver check-ups.", "Get vaccinated against hepatitis A and B.", "Never exceed painkiller doses."],
        "diet_follow": ["High-protein balanced meals", "Vegetables and fruits", "Oats and whole grains", "Small, frequent meals if appetite is low", "Plenty of water"],
        "diet_avoid": ["All alcohol", "Salty and processed foods, which cause fluid retention", "Fried and fatty foods", "Sugary drinks"],
    },
    "Tuberculosis": {
        "about": "Tuberculosis (TB) is a bacterial infection, usually of the lungs, caused by Mycobacterium tuberculosis.",
        "how_it_occurs": "It spreads through the air when an infected person coughs, sneezes or speaks. Risk rises with weak immunity, malnutrition, smoking and crowded living conditions.",
        "precautions": ["Finish the full course of TB medicine, even when you feel better.", "Cover your mouth when coughing and wear a mask in crowded places.", "Keep rooms well ventilated.", "Get screened if you have a cough lasting more than two weeks."],
        "diet_follow": ["Protein-rich foods such as eggs, lentils, fish and paneer", "Fruits and vegetables", "Whole grains and nuts", "Milk and plenty of water"],
        "diet_avoid": ["Smoking and tobacco", "Alcohol", "Skipping medicine doses", "Long periods of poor nutrition"],
    },
    "Common Cold": {
        "about": "The common cold is a mild viral infection of the nose and throat.",
        "how_it_occurs": "Mostly caused by rhinoviruses. It spreads through droplets from coughs and sneezes and through touching contaminated surfaces.",
        "precautions": ["Wash hands often and avoid touching your eyes and nose.", "Cover coughs and sneezes and dispose of tissues properly.", "Rest and stay home while contagious.", "Keep the air humid and drink plenty of fluids."],
        "diet_follow": ["Warm soups and herbal teas", "Honey for cough (adults and children over one year)", "Vitamin C foods", "Plenty of fluids"],
        "diet_avoid": ["Smoking", "Alcohol", "Excess sugary drinks", "Very cold drinks if they worsen throat pain", "Fried and greasy food"],
    },
    "Pneumonia": {
        "about": "Pneumonia is an infection of the lungs that fills the air sacs with fluid or pus.",
        "how_it_occurs": "It is caused by bacteria, viruses or fungi, often after a cold or flu. Risk is higher in young children, older adults, smokers and people with weak immunity.",
        "precautions": ["Get vaccinated against flu and pneumococcus, as advised.", "Wash hands regularly and quit smoking.", "Rest and finish any prescribed antibiotics.", "Seek urgent help for fast breathing, chest pain or blue lips."],
        "diet_follow": ["Plenty of fluids and soups", "Protein-rich foods", "Fruits and vegetables", "Small, frequent meals if appetite is low"],
        "diet_avoid": ["Smoking and second-hand smoke", "Alcohol", "Skipping fluids", "Very greasy food during recovery"],
    },
    "Hemorrhoids (piles)": {
        "about": "Haemorrhoids (piles) are swollen veins in or around the anus and lower rectum.",
        "how_it_occurs": "They are caused by straining during bowel movements, constipation, long periods of sitting, pregnancy, heavy lifting and a low-fibre diet.",
        "precautions": ["Drink plenty of water every day.", "Avoid straining and do not sit on the toilet for long periods.", "Exercise regularly.", "Use warm sitz baths and see a doctor if you notice bleeding."],
        "diet_follow": ["High-fibre foods such as fruits, vegetables, oats and beans", "Whole grains", "Prunes", "Plenty of water"],
        "diet_avoid": ["Low-fibre processed foods", "Excess red meat", "Fried and spicy food", "Alcohol", "Too much caffeine if it causes constipation"],
    },
    "Heart attack": {
        "about": "A heart attack happens when blood flow to part of the heart muscle is suddenly blocked.",
        "how_it_occurs": "It is usually caused by a blood clot in a narrowed heart artery, often due to plaque build-up. Risks include high blood pressure, high cholesterol, smoking, diabetes and obesity.",
        "precautions": ["This is an emergency. Call emergency services at once for chest pain or pressure that spreads to the arm, jaw or back.", "Control blood pressure, cholesterol and blood sugar.", "Stop smoking and exercise regularly.", "Take heart medicines as prescribed and attend regular check-ups."],
        "diet_follow": ["Vegetables and fruits", "Whole grains and oats", "Nuts and olive oil", "Fish rich in omega-3", "Legumes and low-fat dairy"],
        "diet_avoid": ["Trans fats and fried food", "Processed meats", "Excess salt", "Sugary drinks", "Smoking and excess alcohol"],
    },
    "Varicose veins": {
        "about": "Varicose veins are enlarged, twisted veins, usually in the legs, that can look bulging and blue or purple.",
        "how_it_occurs": "Weakened valves in leg veins let blood pool. Risks include standing or sitting for long periods, pregnancy, age, obesity and family history.",
        "precautions": ["Exercise often, such as walking.", "Avoid standing or sitting still for long periods.", "Raise your legs when resting.", "Wear compression stockings if your doctor advises."],
        "diet_follow": ["Fibre-rich fruits and vegetables", "Whole grains and legumes", "Lean protein", "Plenty of water"],
        "diet_avoid": ["Excess salt", "Processed foods", "Excess sugar", "Very heavy meals", "Excess alcohol"],
    },
    "Hypothyroidism": {
        "about": "Hypothyroidism is an underactive thyroid gland that produces too little thyroid hormone.",
        "how_it_occurs": "Common causes include autoimmune disease (such as Hashimoto's), iodine deficiency, thyroid surgery and some medicines. It can cause tiredness, weight gain, cold intolerance and constipation.",
        "precautions": ["Take thyroid medicine every day exactly as prescribed.", "Get regular blood tests to check thyroid levels.", "Take levothyroxine on an empty stomach, as your doctor advises.", "Never change your dose without medical advice."],
        "diet_follow": ["Iodised salt in moderation", "Eggs, fish and dairy", "Brazil nuts and seeds", "High-fibre foods", "Plenty of water"],
        "diet_avoid": ["Very large amounts of raw cabbage, broccoli and soy", "Taking calcium or fibre supplements at the same time as thyroid medicine", "Highly processed, sugary foods"],
    },
    "Hyperthyroidism": {
        "about": "Hyperthyroidism is an overactive thyroid gland that produces too much thyroid hormone.",
        "how_it_occurs": "Common causes include Graves' disease, thyroid nodules and inflammation of the gland. Symptoms include weight loss, a fast heartbeat, sweating, anxiety and heat intolerance.",
        "precautions": ["Take prescribed medicines and attend regular monitoring.", "Protect your eyes if you have Graves' disease.", "Avoid iodine supplements such as kelp unless prescribed.", "Seek urgent care for chest pain or a very fast heartbeat."],
        "diet_follow": ["Nutritious, calorie-rich regular meals", "Calcium and vitamin D foods such as milk and fish, to protect bones", "Fibre-rich foods", "Plenty of fluids"],
        "diet_avoid": ["Excess caffeine and energy drinks", "Iodine supplements or kelp", "Very spicy food", "Alcohol", "Skipping meals"],
    },
    "Hypoglycemia": {
        "about": "Hypoglycaemia (low blood sugar) is when blood glucose drops too low, usually below about 70 mg/dL.",
        "how_it_occurs": "Causes include too much diabetes medicine or insulin, not eating enough, skipping meals, intense exercise and alcohol on an empty stomach.",
        "precautions": ["Carry fast-acting sugar such as glucose tablets or juice for emergencies.", "Do not skip meals.", "Adjust medicine only with your doctor's guidance.", "Tell family members how to help if you feel faint or confused."],
        "diet_follow": ["Regular small meals with complex carbohydrates and protein", "Fruits", "Whole grains", "Nuts and yogurt", "Plenty of fluids"],
        "diet_avoid": ["Skipping meals", "Alcohol on an empty stomach", "Large sugar intakes without a plan (use fast sugar only to treat a low)", "Crash diets without medical advice"],
    },
    "Osteoarthritis": {
        "about": "Osteoarthritis is wear and tear of joint cartilage, causing pain, stiffness and swelling, usually in the knees, hips, hands and spine.",
        "how_it_occurs": "Cartilage gradually breaks down. Risks include age, obesity, previous joint injury, repetitive stress and family history.",
        "precautions": ["Maintain a healthy weight to reduce joint load.", "Do low-impact exercise such as walking, swimming or cycling.", "Wear supportive footwear.", "Ask a physiotherapist about strengthening exercises and use heat or cold for pain."],
        "diet_follow": ["Omega-3 fish", "Leafy greens and berries", "Nuts, olive oil and legumes", "Whole grains", "Calcium and vitamin D foods"],
        "diet_avoid": ["Excess sugar and refined carbohydrates", "Fried and processed foods", "Very salty foods", "Excess alcohol", "Weight gain"],
    },
    "Arthritis": {
        "about": "Arthritis is a general term for joint inflammation. Rheumatoid arthritis is an autoimmune type that affects joints on both sides of the body.",
        "how_it_occurs": "In rheumatoid arthritis the immune system attacks the joint lining. Other types come from injury, infection, gout or metabolic causes. Smoking and family history raise risk.",
        "precautions": ["Follow your prescribed treatment plan.", "Do gentle daily movement to keep joints flexible.", "Protect joints when lifting or working.", "See a rheumatologist for swelling or morning stiffness lasting more than an hour."],
        "diet_follow": ["Fatty fish", "Olive oil", "Berries and leafy greens", "Nuts", "Turmeric and whole grains", "Plenty of water"],
        "diet_avoid": ["Smoking", "Excess sugar", "Processed and fried foods", "Excess red meat", "Excess salt and alcohol"],
    },
    "Benign positional vertigo": {
        "about": "Benign positional vertigo (BPPV) causes brief spinning dizziness triggered by certain head movements, such as turning over in bed.",
        "how_it_occurs": "Tiny calcium crystals in the inner ear move to the wrong place and send confusing signals to the brain. Age, head injury and inner-ear problems raise risk.",
        "precautions": ["Move slowly when changing position.", "Sit on the edge of the bed for a minute before standing.", "Avoid sudden head tilting or looking up for long periods.", "Ask a trained professional about the Epley manoeuvre. Seek urgent care for sudden severe dizziness with weakness or speech problems."],
        "diet_follow": ["Plenty of fluids", "Balanced meals with fibre", "Calcium and vitamin D foods", "Regular sleep"],
        "diet_avoid": ["Alcohol", "Excess salt", "High caffeine", "Large, heavy meals that cause tiredness"],
    },
    "Acne": {
        "about": "Acne is a common skin condition in which pores become blocked with oil and dead skin, causing pimples, blackheads and inflammation.",
        "how_it_occurs": "Hormones increase oil production, and clogged pores can become infected. Triggers include puberty, stress, genetics, some medicines and certain cosmetics.",
        "precautions": ["Wash your face gently twice a day.", "Do not squeeze or pick pimples.", "Use non-comedogenic (non-pore-blocking) products.", "Use prescribed creams and see a dermatologist for scarring or severe acne."],
        "diet_follow": ["Vegetables and fruits", "Whole grains and legumes", "Lean protein and omega-3 fish", "Zinc-rich foods", "Plenty of water"],
        "diet_avoid": ["Sugary drinks and white bread", "Fast food and very greasy food", "Dairy or chocolate if you notice they make acne worse"],
    },
    "Urinary tract infection": {
        "about": "A urinary tract infection (UTI) is an infection of the bladder, urethra or kidneys, most often caused by bacteria.",
        "how_it_occurs": "Usually E. coli bacteria enter through the urethra. Risk is higher in women, sexually active people, during pregnancy, with diabetes, and with poor hydration.",
        "precautions": ["Drink plenty of water.", "Urinate soon after sex.", "Wipe from front to back and keep the genital area clean.", "See a doctor for fever, back pain, blood in urine, or symptoms that do not improve."],
        "diet_follow": ["Plenty of water", "Unsweetened cranberry juice (may help prevention)", "Probiotic yogurt", "Fruits and vegetables"],
        "diet_avoid": ["Caffeine and alcohol", "Spicy foods", "Sugary and acidic drinks that irritate the bladder", "Large amounts of artificial sweeteners"],
    },
    "Psoriasis": {
        "about": "Psoriasis is a long-lasting autoimmune skin condition that causes thick, red, scaly patches.",
        "how_it_occurs": "Skin cells renew too quickly because the immune system is overactive. Triggers include stress, infections, cold weather, skin injury, smoking and alcohol.",
        "precautions": ["Moisturise your skin every day.", "Use prescribed topical treatments as directed.", "Manage stress and get enough sleep.", "Avoid skin injury and see a dermatologist if joint pain develops."],
        "diet_follow": ["Omega-3 fish", "Leafy greens and fruits", "Nuts and olive oil", "Whole grains", "Vitamin D foods", "Plenty of water"],
        "diet_avoid": ["Alcohol and smoking", "Excess sugar", "Fried and processed foods", "Excess red meat", "Dairy or gluten only if you notice they trigger flares"],
    },
    "Impetigo": {
        "about": "Impetigo is a contagious bacterial skin infection that causes red sores which burst and form honey-coloured crusts, mostly on the face and hands.",
        "how_it_occurs": "It is usually caused by Staphylococcus or Streptococcus bacteria entering through cuts, scratches or insect bites. It spreads by touch and shared towels.",
        "precautions": ["Gently wash the affected area with soap and water.", "Cover sores and do not share towels or clothes.", "Keep nails short and wash hands often.", "Stay away from school or work until treated, as your doctor advises, and finish any prescribed antibiotics."],
        "diet_follow": ["Fluids", "Fruits and vegetables for vitamin C", "Protein-rich foods", "Yogurt and whole grains"],
        "diet_avoid": ["Scratching or picking sores", "Sharing towels", "Very sugary foods", "Smoking and alcohol"],
    },
    # ---- Added for the medical-data tasks ----
    "Chronic kidney disease": {
        "about": "Chronic kidney disease (CKD) is a gradual loss of kidney function over months or years. The kidneys struggle to filter waste and extra fluid from the blood.",
        "how_it_occurs": "The most common causes are diabetes and high blood pressure. Other causes include glomerulonephritis, polycystic kidney disease, repeated kidney infections, and long-term use of some painkillers. Many people have no symptoms until the disease is advanced.",
        "precautions": ["Control blood sugar and blood pressure with the treatment your doctor prescribes.", "Have urine (protein) and blood (creatinine, eGFR) tests at the frequency your doctor advises.", "Avoid regular use of painkillers such as ibuprofen and naproxen without medical advice.", "Do not smoke, and keep a healthy weight.", "Seek urgent care for very low urine output, severe swelling, breathlessness or confusion."],
        "diet_follow": ["Fruits and vegetables, adjusted to your potassium level as your doctor advises", "Whole grains and legumes", "Lean protein in moderate portions", "Plenty of water unless your doctor limits fluids", "Herbs and spices for flavour instead of salt"],
        "diet_avoid": ["Salt and salty processed foods", "Processed and red meats", "Colas and sugary drinks", "High-potassium foods if your potassium is raised (e.g. bananas, oranges, potatoes, tomatoes) until advised", "Excess protein supplements and unprescribed herbal remedies", "Alcohol and smoking"],
    },
    "Liver disease": {
        "about": "Liver disease covers conditions that damage the liver and reduce its ability to process nutrients, filter the blood and make important proteins. It can be acute or long-term.",
        "how_it_occurs": "Common causes include long-term heavy alcohol use, viral hepatitis, fatty liver linked to obesity and diabetes, and some medicines or toxins. Damage builds up quietly, and blood tests such as bilirubin and liver enzymes (ALT, AST) often show the first changes.",
        "precautions": ["Stop or greatly reduce alcohol.", "Check that over-the-counter medicines are safe for the liver, and never exceed painkiller doses.", "Vaccinate against hepatitis A and B, and use protection to avoid hepatitis C.", "Maintain a healthy weight and get regular physical activity.", "Attend liver check-ups as your doctor advises. Seek urgent care for yellow skin or eyes, vomiting blood, or confusion."],
        "diet_follow": ["Balanced meals with vegetables, fruits and whole grains", "Lean protein such as fish, eggs, beans and poultry", "Coffee in moderation, if your doctor agrees", "Plenty of water", "Small, regular meals if appetite is low"],
        "diet_avoid": ["All alcohol", "Fried, fatty and processed foods", "Sugary drinks and sweets", "Raw or undercooked shellfish", "Unprescribed herbal and dietary supplements", "Excess salt, which can cause fluid build-up"],
    },
    "Heart disease": {
        "about": "Heart disease is a general term for conditions that affect the heart, most often coronary artery disease, where the heart's blood vessels narrow.",
        "how_it_occurs": "Plaque builds up in the arteries over years. High blood pressure, high cholesterol, smoking, diabetes, inactivity, obesity and family history all increase the risk.",
        "precautions": ["Have blood pressure, cholesterol and blood sugar checked regularly.", "Stop smoking and limit alcohol.", "Exercise for at least 150 minutes a week, as your doctor advises.", "Seek emergency care for chest pain, breathlessness or fainting."],
        "diet_follow": ["Vegetables, fruits and whole grains", "Oats, beans and lentils", "Fatty fish rich in omega-3", "Nuts and olive oil", "Low-fat dairy"],
        "diet_avoid": ["Trans fats and fried foods", "Processed and cured meats", "Excess salt", "Sugary drinks", "Smoking and excess alcohol"],
    },
    "Breast cancer": {
        "about": "Breast cancer is a disease in which cells in the breast grow abnormally and can form a tumour. A malignant tumour can spread if untreated; a benign one does not spread.",
        "how_it_occurs": "Causes include age, genetics (such as BRCA gene changes), hormone exposure, obesity, alcohol and family history. Many cases occur without a clear cause.",
        "precautions": ["Attend regular breast screening as recommended for your age.", "Report any new lump, skin change or nipple discharge promptly.", "Keep a healthy weight and stay physically active.", "Limit alcohol and avoid smoking."],
        "diet_follow": ["Vegetables and fruits, especially cruciferous vegetables", "Whole grains", "Legumes and nuts", "Fish and lean protein", "Olive oil"],
        "diet_avoid": ["Alcohol", "Processed and red meats", "Sugary foods and drinks", "Excess body weight gain"],
    },
}

DISEASE_INFO = {_norm(name): info for name, info in RAW_DISEASE_INFO.items()}

DEFAULT_INFO = {
    "about": "Detailed information for this condition is not available yet.",
    "how_it_occurs": "Please speak with a doctor to learn more about this condition.",
    "precautions": ["See a qualified healthcare professional for guidance."],
    "diet_follow": ["A balanced diet with vegetables, fruits, whole grains and plenty of water."],
    "diet_avoid": ["Excess alcohol, smoking, and highly processed foods."],
}


def get_disease_info(name):
    """Return the information block for a condition name (case and spacing insensitive)."""
    return DISEASE_INFO.get(_norm(name), DEFAULT_INFO)
