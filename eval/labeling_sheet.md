# Groundedness labeling sheet

Decide for each plan: are ALL task rationales supported by the RETRIEVED
CONTEXT? Mark **1 = grounded** or **0 = not grounded** in `human_labels.jsonl`.
Label independently — the judge's verdict is intentionally hidden here.

Rule to apply consistently: a task is ungrounded if its rationale asserts
something not present in the retrieved context, even if it is generally
true cat-care advice (e.g. dental care / vet visits not in the context).

---

## case_01  — Mochi (Persian, 4y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: persian daily brushing required to prevent matting regular eye cleaning (tear staining) sensitive to heat and humidity age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition feeding litter_maintenance eye_care water_refresh grooming playtime feeding_twice_daily

**Plan tasks:**
- `Feeding` — Ensures Mochi receives adequate nutrition for an adult cat.
- `Water Refresh` — Hydration is crucial for overall health.
- `Litter Box Maintenance` — Maintains hygiene and prevents litter box aversion.
- `Grooming` — Persian cats require daily brushing to prevent matting and hairballs due to their long coats.
- `Eye Care` — Persian cats are prone to tear staining and require regular eye cleaning to maintain hygiene and comfort.
- `Playtime` — Provides mental stimulation and physical exercise for an adult cat in its most active years.
- `Veterinary Check-up` — Ensures Mochi's continued maintenance health care and early detection of any potential issues.

**Your label for case_01:** ___ (1 grounded / 0 not)

---

## case_02  — Luna (Bengal, 2y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: bengal extremely active - needs lots of exercise intelligent and can learn tricks needs environmental enrichment age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition feeding exercise litter_maintenance water_refresh grooming training playtime feeding_twice_daily

**Plan tasks:**
- `Feeding` — Ensures Luna receives essential nutrition for her active lifestyle.
- `Water Refresh` — Hydration is crucial for overall health, especially for an active cat.
- `Litter Box Maintenance` — Maintains a clean environment for Luna and prevents health issues.
- `Playtime` — Bengal cats are extremely active and intelligent, requiring significant exercise and mental stimulation to prevent boredom and destructive behavior. Interactive toys align with her preferences.
- `Training` — Bengals are intelligent and benefit from mental challenges to prevent boredom and reinforce good behavior.
- `Grooming` — Regular brushing helps keep Luna's coat healthy and reduces shedding.
- `Veterinary Visit` — Ensures Luna's continued health and allows for early detection of any potential issues.

**Your label for case_02:** ___ (1 grounded / 0 not)

---

## case_03  — Shadow (Siamese, 3y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: siamese very vocal and social - needs attention intelligent - requires mental stimulation prone to separation anxiety age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition feeding litter_maintenance water_refresh grooming training playtime feeding_twice_daily interaction

**Plan tasks:**
- `Feeding` — Ensures Shadow receives adequate nutrition for an adult cat, aligning with general feeding guidelines.
- `Water Refresh` — Essential for hydration and overall health, preventing dehydration.
- `Litter Box Maintenance` — Maintains a hygienic environment for Shadow and reduces odors, promoting good litter habits.
- `Interactive Playtime` — Siamese cats are intelligent and energetic; regular playtime provides mental stimulation and physical exercise, preventing boredom and behavioral issues.
- `Social Interaction` — Siamese cats are very vocal and social, prone to separation anxiety. Consistent interaction fulfills their need for attention and strengthens your bond.
- `Grooming` — Even short-haired Siamese cats benefit from regular brushing to reduce shedding and prevent hairballs, also serving as a bonding activity.
- `Dental Care` — Essential for preventing dental disease, which is a common health issue in adult cats and contributes to overall well-being.

**Your label for case_03:** ___ (1 grounded / 0 not)

---

## case_04  — Biscuit (Maine Coon, 5y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: maine coon large breed - needs more food and water thicker coat requires regular brushing playful and dog-like personality age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition feeding litter_maintenance water_refresh grooming training playtime feeding_twice_daily

**Plan tasks:**
- `feeding` — Maine Coons are a large breed and require more food to maintain their health and energy levels. Twice-daily feeding supports a healthy metabolism.
- `water_refresh` — Ensuring constant access to fresh water is crucial for hydration, especially for a large breed like a Maine Coon.
- `litter_maintenance` — A clean litter box encourages proper litter habits and prevents health issues.
- `grooming` — Maine Coons have long, thick fur that requires regular brushing to prevent matting and maintain skin health.
- `playtime` — Maine Coons are known for their playful and dog-like personalities, requiring regular mental and physical stimulation to stay happy and healthy.
- `dental_care` — Regular dental care is important for adult cats to prevent plaque buildup and maintain oral health.
- `vet_visit` — Annual vet visits are essential for preventative care, vaccinations, and early detection of any potential health issues for adult cats.

**Your label for case_04:** ___ (1 grounded / 0 not)

---

## case_05  — Pixel (Abyssinian, 2y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: abyssinian extremely active and athletic - needs lots of vertical space intelligent and curious - requires mental stimulation social and people-oriented - dislikes being alone needs interactive play and climbing structures age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition feeding exercise playtime_intensive litter_maintenance water_refresh grooming training playtime feeding_twice_daily environmental_enrichment

**Plan tasks:**
- `Feeding` — Ensures consistent nutrition for an active Abyssinian, maintaining peak physical condition.
- `Water Refresh` — Consistent access to fresh water is crucial for hydration and overall health.
- `Litter Box Cleaning` — A clean litter box promotes good hygiene and prevents potential health issues.
- `Interactive Play` — Abyssinians are highly active, intelligent, and require significant mental and physical stimulation to prevent boredom and destructive behavior.
- `Environmental Enrichment` — Abyssinians are athletic and enjoy climbing; providing vertical space fulfills their natural instincts and preference for high vantage points.
- `Grooming & Health Check` — While Abyssinians have short coats, regular checks help monitor overall health and strengthen your bond.

**Your label for case_05:** ___ (1 grounded / 0 not)

---

## case_06  — Tiny (Domestic Shorthair, 0y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: kitten high energy and playfulness rapid growth and development needs frequent meals learning and socialization critical feeding feeding_frequent water_refresh playtime_multiple playtime training socialization monitoring

**Plan tasks:**
- `Feeding` — Kittens require frequent meals to support their rapid growth and high energy levels, which are characteristic of their age group.
- `Water Refresh` — Consistent access to fresh water is vital for a kitten's hydration and overall health, supporting their active metabolism.
- `Litter Box Cleaning` — A clean litter box encourages proper litter habits and prevents potential health issues, especially important for young kittens.
- `Playtime` — Kittens have high energy and playfulness; regular playtime is essential for physical exercise, mental stimulation, and bonding.
- `Socialization` — Early socialization is critical for a kitten's learning and development, helping them become well-adjusted and adaptable adults.
- `Basic Training` — Early training helps establish good behaviors, strengthens the bond, and is crucial during a kitten's learning phase.
- `Veterinary Check-up` — Regular vet visits are crucial for monitoring a kitten's rapid growth, administering necessary vaccinations, and ensuring overall health.

**Your label for case_06:** ___ (1 grounded / 0 not)

---

## case_07  — Whiskers (Domestic Shorthair, 10y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet feeding gentle_play medication_if_needed vet_visits_frequent grooming playtime feeding_senior_formula comfort_monitoring monitoring water_access

**Plan tasks:**
- `feeding` — Senior cats benefit from diets tailored to their age, supporting their changing nutritional needs and overall health.
- `water_access` — Consistent hydration is crucial for a cat's overall health, particularly for senior cats to support kidney function.
- `litter_box_maintenance` — A clean litter box promotes good hygiene, prevents accidents, and helps monitor Whiskers' urinary and bowel health.
- `playtime` — Even senior cats benefit from mental and physical stimulation, helping to maintain mobility and prevent boredom.
- `grooming` — Regular brushing helps maintain coat health, reduces hairballs, and provides an opportunity to check for any lumps or skin changes.
- `vet_visit` — Frequent vet visits are essential for senior cats to detect and manage age-related conditions early, ensuring optimal health.
- `monitoring` — Close monitoring helps identify potential health issues early, which is crucial for senior cats who may hide symptoms.

**Your label for case_07:** ___ (1 grounded / 0 not)

---

## case_08  — Ginger (Ragdoll, 6y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: ragdoll semi-long coat requires regular brushing docile and gentle - enjoys human company can be sensitive to stress age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition feeding litter_maintenance water_refresh grooming playtime feeding_twice_daily interaction

**Plan tasks:**
- `Feeding` — Essential for providing consistent nutrition and maintaining her stable energy levels.
- `Water Refresh` — Ensures proper hydration, which is crucial for overall health.
- `Litter Box Cleaning` — Maintains a hygienic environment and helps prevent stress, which Ragdolls can be sensitive to.
- `Grooming` — Ragdolls have semi-long coats that require regular brushing to prevent matting and hairballs.
- `Playtime` — Provides mental and physical stimulation, strengthens your bond, and supports her docile and social nature.
- `Dental Care` — Important for preventing dental disease and maintaining overall health as an adult cat.
- `Vet Visit` — Essential for preventative care, monitoring her peak physical condition, and ensuring long-term health.

**Your label for case_08:** ___ (1 grounded / 0 not)

---

## case_09  — Smokey (Siamese, 11y)
*Conditions:* Chronic Kidney Disease  |  *plan source:* gemini

**Retrieved context:**
> breed: siamese very vocal and social - needs attention intelligent - requires mental stimulation prone to separation anxiety age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: chronic kidney disease (ckd) prescription kidney diet (low protein, low phosphorus) frequent water access and hydration monitoring feeding gentle_play medication_if_needed medication vet_visits_frequent interaction grooming playtime water_bowl_refresh training feeding_senior_formula comfort_monitoring monitoring water_access feeding_specialized chronic kidney disease (ckd) prescription kidney diet (low protein, low phosphoru...

**Plan tasks:**
- `feeding_specialized` — Essential for managing Chronic Kidney Disease and supporting kidney function by reducing the workload on his kidneys.
- `water_access` — Crucial for managing Chronic Kidney Disease, preventing dehydration, and supporting overall kidney health.
- `litter_box_cleaning` — Maintains a clean environment, encourages consistent litter box use, and helps in monitoring changes in urination patterns, which is important for CKD.
- `vet_visits_frequent` — Frequent vet visits are vital for monitoring Chronic Kidney Disease, ensuring the effectiveness of the care plan, and addressing any new health concerns for a senior cat.
- `monitoring` — Early detection of subtle changes is crucial for managing Chronic Kidney Disease and addressing age-related issues promptly, improving quality of life.
- `gentle_play` — Siamese cats are very social and intelligent, requiring mental stimulation and attention. Gentle play supports well-being for a senior cat with decreased activity.
- `grooming` — Supports coat health, provides comfort, and allows for early detection of any physical changes or health issues common in senior cats.

**Your label for case_09:** ___ (1 grounded / 0 not)

---

## case_10  — Boots (Maine Coon, 8y)
*Conditions:* Diabetes  |  *plan source:* gemini

**Retrieved context:**
> breed: maine coon large breed - needs more food and water thicker coat requires regular brushing playful and dog-like personality age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: feline diabetes insulin injections (typically twice daily) high-protein, low-carb diet feeding gentle_play medication_if_needed exercise vet_visits_frequent grooming playtime training medication_injection feeding_senior_formula comfort_monitoring monitoring water_access feeding_specialized feline diabetes insulin injections (typically twice daily) high-protein, low-carb diet regular glucose monitoring weight management ...

**Plan tasks:**
- `feeding_specialized` — Essential for managing feline diabetes and providing appropriate nutrition for a senior Maine Coon.
- `water_access` — Crucial for overall hydration, especially for a large breed senior cat, and supports kidney health.
- `litter_box_cleaning` — Maintains hygiene and comfort for Boots, encouraging consistent litter box use.
- `medication_injection` — Absolutely essential for managing Boots' diabetes and maintaining stable blood glucose levels.
- `monitoring` — Vital for effective diabetes management and adjusting insulin dosages if needed.
- `grooming` — Maine Coons have thick coats that require regular grooming to maintain skin and coat health.
- `gentle_play` — Helps maintain a healthy weight and provides mental stimulation, important for a senior cat with diabetes.

**Your label for case_10:** ___ (1 grounded / 0 not)

---

## case_11  — Cleo (Domestic Shorthair, 9y)
*Conditions:* Hyperthyroidism  |  *plan source:* gemini

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: hyperthyroidism thyroid medication (typically twice daily) regular thyroid level monitoring feeding gentle_play medication_if_needed medication vet_visits_frequent grooming playtime feeding_senior_formula comfort_monitoring monitoring feeding_controlled water_access vet_visits hyperthyroidism thyroid medication (typically twice daily) regular thyroid level monitoring calorie-controlled diet monitor we...

**Plan tasks:**
- `Feeding` — Essential for managing hyperthyroidism, maintaining a healthy weight, and providing appropriate nutrition for a senior cat.
- `Water Access` — Crucial for hydration and kidney function, which can be impacted by age and health conditions like hyperthyroidism.
- `Litter Box Cleaning` — A clean litter box is vital for a cat's comfort, prevents inappropriate urination, and allows for monitoring of elimination patterns.
- `Medication Administration` — Directly addresses Cleo's hyperthyroidism, crucial for her health, well-being, and preventing complications.
- `Health Monitoring` — Early detection of changes can prevent complications and ensure effective management of hyperthyroidism and other age-related issues.
- `Veterinary Visits` — Frequent vet visits are critical for adjusting medication, monitoring the progression of hyperthyroidism, and addressing any new health concerns.
- `Gentle Playtime` — Supports mental well-being, provides appropriate physical activity, and strengthens the bond with your senior cat.

**Your label for case_11:** ___ (1 grounded / 0 not)

---

## case_12  — Felix (Ragdoll, 7y)
*Conditions:* Hypertrophic Cardiomyopathy  |  *plan source:* gemini

**Retrieved context:**
> breed: ragdoll semi-long coat requires regular brushing docile and gentle - enjoys human company can be sensitive to stress age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: hypertrophic cardiomyopathy (hcm) heart medication as prescribed stress reduction and quiet environment feeding gentle_play medication_if_needed rest_monitoring medication vet_visits_frequent grooming playtime feeding_senior_formula comfort_monitoring vet_visits water_access interaction hypertrophic cardiomyopathy (hcm) heart medication as prescribed stress reduction and quiet environment limited intense exercise regular card...

**Plan tasks:**
- `feeding` — Supports his nutritional needs as a senior cat and helps maintain overall health.
- `water_access` — Hydration is vital for overall health, kidney function, and is especially important for cats with heart conditions.
- `litter_box_cleaning` — Maintains a clean environment, reduces stress, and encourages proper litter box use.
- `medication` — Essential for managing Felix's heart condition and improving his quality of life.
- `grooming` — Ragdolls have semi-long coats that require regular brushing to maintain coat health and prevent discomfort.
- `gentle_play` — Ragdolls enjoy human company and gentle interaction. Limited intense exercise is crucial due to HCM, and stress reduction is key.
- `vet_visits` — Frequent monitoring is vital for managing Hypertrophic Cardiomyopathy and addressing potential age-related conditions in senior cats.

**Your label for case_12:** ___ (1 grounded / 0 not)

---

## case_13  — Patches (Domestic Shorthair, 4y)
*Conditions:* Feline Lower Urinary Tract Disease  |  *plan source:* gemini

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition condition: feline lower urinary tract disease (flutd) prescription urinary diet increased water intake feeding litter_box_cleaning litter_maintenance water_refresh feeding_twice_daily grooming playtime water_bowl_refresh monitoring feeding_specialized feline lower urinary tract disease (flutd) prescription urinary diet increased water intake clean litter box (multiple boxes recommended) stress reduction regular monitoring ...

**Plan tasks:**
- `feeding_specialized` — Essential for managing Feline Lower Urinary Tract Disease (FLUTD) and preventing recurrence.
- `water_refresh` — Increased water intake is crucial for flushing the urinary tract and managing FLUTD.
- `litter_box_cleaning` — A clean litter environment reduces stress and encourages urination, which is vital for cats with FLUTD.
- `monitoring` — Early detection of FLUTD symptoms can prevent complications and ensure timely veterinary intervention.
- `playtime` — Playtime helps maintain a healthy weight, reduces stress, and strengthens your bond, which can indirectly benefit FLUTD management.
- `grooming` — Maintains coat health and provides an opportunity for bonding and a quick health check.

**Your label for case_13:** ___ (1 grounded / 0 not)

---

## case_14  — Oreo (Persian, 12y)
*Conditions:* Arthritis  |  *plan source:* gemini

**Retrieved context:**
> breed: persian daily brushing required to prevent matting regular eye cleaning (tear staining) sensitive to heat and humidity age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: arthritis / osteoarthritis pain medication as prescribed gentle, low-impact exercise feeding gentle_play medication_if_needed medication eye_care water_access vet_visits_frequent grooming monitoring_mobility playtime feeding_senior_formula comfort_monitoring feeding_ground_level arthritis / osteoarthritis pain medication as prescribed gentle, low-impact exercise easy access to food, water, and litter comfortable resting are...

**Plan tasks:**
- `Feeding` — Supports nutritional needs for senior cats and reduces strain on joints due to arthritis.
- `Water Access` — Critical for overall health, especially kidney health, and easy access is vital for cats with arthritis.
- `Litter Box Cleaning` — Maintains hygiene and ensures comfortable, easy access for a cat with arthritis.
- `Medication` — Essential for managing pain and improving quality of life for a cat with arthritis.
- `Grooming` — Persian cats require daily grooming to maintain coat health and prevent discomfort, and eye care is important for the breed.
- `Gentle Exercise & Monitoring` — Gentle exercise helps maintain joint flexibility, and monitoring is crucial for managing arthritis and detecting discomfort.
- `Vet Visit` — Regular veterinary oversight is vital for senior cats, especially those with chronic conditions like arthritis, to adjust care as needed.

**Your label for case_14:** ___ (1 grounded / 0 not)

---

## case_15  — Milo (Bengal, 3y)
*Conditions:* Feline Immunodeficiency Virus  |  *plan source:* gemini

**Retrieved context:**
> breed: bengal extremely active - needs lots of exercise intelligent and can learn tricks needs environmental enrichment age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition condition: feline immunodeficiency virus (fiv) keep indoors to prevent spread regular veterinary monitoring feeding exercise litter_maintenance feeding_quality medication_as_needed water_refresh feeding_twice_daily grooming playtime training monitoring vet_visits feline immunodeficiency virus (fiv) keep indoors to prevent spread regular veterinary monitoring vaccinations and preventive care monitor for secondary infections nutritious diet to support i...

**Plan tasks:**
- `feeding` — A consistent, high-quality diet is crucial for maintaining Milo's overall health and supporting his immune system, especially with FIV.
- `water_refresh` — Hydration is vital for all cats, supporting kidney function and overall well-being.
- `litter_maintenance` — A clean litter box promotes good hygiene and prevents potential health issues, especially important for an FIV-positive cat.
- `playtime` — As a Bengal, Milo is extremely active and intelligent, requiring significant exercise and mental stimulation to prevent boredom and maintain physical health.
- `vet_visits` — Regular veterinary monitoring is essential for managing Milo's FIV, tracking his immune health, and addressing any potential secondary infections promptly.
- `environmental_management` — Keeping Milo indoors is crucial to prevent the spread of FIV to other cats and to protect his compromised immune system from outdoor pathogens.
- `monitoring` — Early detection of secondary infections or other health issues is vital for FIV-positive cats, allowing for timely intervention.

**Your label for case_15:** ___ (1 grounded / 0 not)

---

## case_16  — Nala (Siamese, 5y)
*Conditions:* Asthma  |  *plan source:* gemini

**Retrieved context:**
> breed: siamese very vocal and social - needs attention intelligent - requires mental stimulation prone to separation anxiety age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition condition: feline asthma inhalers or medications as prescribed minimize environmental triggers (dust, smoke, allergens) feeding medication litter_maintenance monitoring_breathing water_refresh interaction feeding_twice_daily playtime training grooming environment_control vet_visits feline asthma inhalers or medications as prescribed minimize environmental triggers (dust, smoke, allergens) regular vet monitoring avoid stress weight management medi...

**Plan tasks:**
- `feeding` — Ensures Nala receives adequate nutrition for her age and activity level.
- `water_refresh` — Essential for hydration and overall health.
- `litter_maintenance` — Maintains hygiene and prevents discomfort, especially important for respiratory health.
- `medication` — Manages Nala's asthma symptoms and prevents flare-ups, crucial for her health.
- `monitoring_breathing` — Early detection of asthma exacerbations allows for timely intervention and veterinary consultation.
- `environment_control` — Reduces exposure to irritants that can trigger asthma attacks and worsen respiratory health.
- `playtime` — Siamese cats are intelligent and social; playtime provides mental stimulation and prevents separation anxiety.

**Your label for case_16:** ___ (1 grounded / 0 not)

---

## case_17  — Simba (Maine Coon, 1y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: maine coon large breed - needs more food and water thicker coat requires regular brushing playful and dog-like personality age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition feeding litter_maintenance water_refresh grooming training playtime feeding_twice_daily

**Plan tasks:**
- `feeding` — Essential for nutrition and energy, especially for a large breed like Maine Coon.
- `water_refresh` — Crucial for hydration, particularly for a large breed cat that needs more water.
- `litter_maintenance` — Maintains hygiene, prevents odors, and encourages consistent litter box use.
- `grooming` — Maine Coons have thick coats that require regular grooming to prevent matting and maintain skin health.
- `playtime` — Supports physical activity and mental stimulation for a playful and active Maine Coon.
- `dental_care` — Essential for preventing dental disease and maintaining oral health in adult cats.
- `vet_visit` — Ensures overall health monitoring, vaccinations, and early detection of potential issues.

**Your label for case_17:** ___ (1 grounded / 0 not)

---

## case_18  — Coco (Abyssinian, 9y)
*Conditions:* Hyperthyroidism  |  *plan source:* gemini

**Retrieved context:**
> breed: abyssinian extremely active and athletic - needs lots of vertical space intelligent and curious - requires mental stimulation social and people-oriented - dislikes being alone needs interactive play and climbing structures age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: hyperthyroidism thyroid medication (typically twice daily) regular thyroid level monitoring feeding gentle_play medication_if_needed exercise medication playtime_intensive water_access vet_visits_frequent grooming training feeding_senior_formula comfort_monitoring monitoring feeding_controlled environmental_enrichment vet...

**Plan tasks:**
- `Feeding` — Supports hyperthyroidism management and meets the nutritional needs of a senior cat.
- `Water Access` — Crucial for hydration and kidney health, particularly important for senior cats and those with health conditions.
- `Litter Box Cleaning` — Maintains a clean environment, promoting good hygiene and preventing litter box aversion.
- `Medication Administration` — Essential for managing Coco's hyperthyroidism and maintaining stable thyroid levels.
- `Health Monitoring` — Early detection of changes is vital for managing hyperthyroidism and addressing age-related conditions promptly.
- `Veterinary Check-ups` — Crucial for adjusting medication, monitoring hyperthyroidism progression, and addressing other senior cat health concerns.
- `Gentle Play & Enrichment` — Supports the intelligent and active nature of Abyssinians while being mindful of her senior age and health condition, preventing boredom.

**Your label for case_18:** ___ (1 grounded / 0 not)

---

## case_19  — Bella (Persian, 0y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: persian daily brushing required to prevent matting regular eye cleaning (tear staining) sensitive to heat and humidity age group: kitten high energy and playfulness rapid growth and development needs frequent meals learning and socialization critical feeding feeding_frequent eye_care water_refresh playtime_multiple grooming playtime training socialization

**Plan tasks:**
- `Feeding` — Kittens require frequent meals for rapid growth and development.
- `Water Refresh` — Ensures Bella stays hydrated, especially important for overall health.
- `Litter Box Cleaning` — A clean litter box promotes good hygiene and prevents health issues.
- `Grooming` — Persian cats require daily brushing to prevent painful matting and hairballs.
- `Eye Care` — Persian cats are prone to tear staining and require regular eye cleaning to prevent irritation and infection.
- `Playtime & Socialization` — Kittens need frequent play for physical development and socialization for behavioral health.
- `Vet Visit` — Essential for kitten vaccinations, deworming, and monitoring rapid growth and development.

**Your label for case_19:** ___ (1 grounded / 0 not)

---

## case_20  — Jasper (Domestic Shorthair, 5y)
*Conditions:* none  |  *plan source:* gemini

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition feeding litter_maintenance water_refresh grooming playtime monitoring feeding_twice_daily

**Plan tasks:**
- `feeding` — Ensures Jasper receives adequate nutrition for an adult cat's stable energy level.
- `water_refresh` — Hydration is crucial for overall health and supports vital organ function.
- `litter_maintenance` — Maintains a clean and hygienic environment, preventing odors and encouraging proper litter box use.
- `playtime` — Provides mental stimulation and physical exercise, important for an active adult cat's well-being.
- `grooming` — Helps remove loose fur, reduces hairballs, and strengthens the bond, despite Domestic Shorthairs having minimal grooming needs.
- `monitoring` — Early detection of health issues is key for an adult cat in peak physical condition, ensuring maintenance health care.
- `vet_visit` — Ensures preventative health care and early detection of potential issues for an adult cat.

**Your label for case_20:** ___ (1 grounded / 0 not)

---

## case_21  — Lily (Ragdoll, 13y)
*Conditions:* Chronic Kidney Disease  |  *plan source:* gemini

**Retrieved context:**
> breed: ragdoll semi-long coat requires regular brushing docile and gentle - enjoys human company can be sensitive to stress age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: chronic kidney disease (ckd) prescription kidney diet (low protein, low phosphorus) frequent water access and hydration monitoring feeding gentle_play medication_if_needed medication vet_visits_frequent interaction grooming playtime water_bowl_refresh feeding_senior_formula comfort_monitoring monitoring water_access feeding_specialized chronic kidney disease (ckd) prescription kidney diet (low protein, low phosphorus) frequen...

**Plan tasks:**
- `feeding_specialized` — Essential for managing Chronic Kidney Disease, slowing its progression, and supporting her overall health as a senior cat.
- `water_access` — Frequent water access and good hydration are vital for kidney function and preventing dehydration in cats with CKD.
- `litter_box_cleaning` — A clean litter box is crucial for hygiene and allows for observation of urinary habits, which can indicate changes in kidney health.
- `grooming` — Ragdolls have semi-long coats that require regular grooming to prevent tangles and discomfort, especially as they age.
- `monitoring` — Close monitoring is crucial for early detection of changes related to CKD progression or other age-related conditions.
- `vet_visits_frequent` — Frequent veterinary oversight is essential for monitoring CKD progression, adjusting treatment plans, and managing Lily's senior health.
- `gentle_play` — Provides mental stimulation and strengthens the bond, important for a docile Ragdoll, while being mindful of her senior age and health condition.

**Your label for case_21:** ___ (1 grounded / 0 not)

---

## case_22  — Rocky (Bengal, 6y)
*Conditions:* Hypertrophic Cardiomyopathy  |  *plan source:* gemini

**Retrieved context:**
> breed: bengal extremely active - needs lots of exercise intelligent and can learn tricks needs environmental enrichment age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition condition: hypertrophic cardiomyopathy (hcm) heart medication as prescribed stress reduction and quiet environment feeding gentle_play rest_monitoring exercise medication litter_maintenance water_refresh feeding_twice_daily grooming playtime training vet_visits hypertrophic cardiomyopathy (hcm) heart medication as prescribed stress reduction and quiet environment limited intense exercise regular cardiac monitoring (echocardiogram) medication gentle_pl...

**Plan tasks:**
- `feeding` — Ensures consistent nutritional intake essential for Rocky's health and energy.
- `water_refresh` — Crucial for hydration, especially important for cats with health conditions.
- `litter_maintenance` — Maintains a hygienic environment and encourages proper litter box use.
- `medication` — Essential for managing Hypertrophic Cardiomyopathy and maintaining heart health.
- `gentle_play_and_rest_monitoring` — Bengals are active and intelligent, but intense exercise must be limited due to HCM. Gentle play provides enrichment while minimizing cardiac strain.
- `environmental_enrichment_and_stress_reduction` — Stress reduction is vital for cats with HCM, and Bengals require environmental enrichment to prevent boredom and anxiety.
- `vet_visits_cardiac_monitoring` — Crucial for ongoing management and monitoring of Rocky's Hypertrophic Cardiomyopathy and overall health.

**Your label for case_22:** ___ (1 grounded / 0 not)

---

## case_23  — Daisy (Abyssinian, 14y)
*Conditions:* Arthritis  |  *plan source:* gemini

**Retrieved context:**
> breed: abyssinian extremely active and athletic - needs lots of vertical space intelligent and curious - requires mental stimulation social and people-oriented - dislikes being alone needs interactive play and climbing structures age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: arthritis / osteoarthritis pain medication as prescribed gentle, low-impact exercise feeding environmental_enrichment gentle_play medication_if_needed exercise medication playtime_intensive water_access vet_visits_frequent grooming monitoring_mobility training feeding_senior_formula comfort_monitoring feeding_ground_level...

**Plan tasks:**
- `Feeding` — A senior formula supports her age-related nutritional needs, and ground-level feeding reduces strain on her arthritic joints.
- `Hydration` — Consistent access to fresh water is vital for Daisy's kidney health and overall well-being, particularly as a senior cat.
- `Litter Box Maintenance` — Regular cleaning maintains hygiene, and an easily accessible, low-sided litter box prevents discomfort for Daisy's arthritic joints.
- `Medication` — Managing Daisy's arthritis pain is crucial for her comfort and quality of life.
- `Playtime` — As an intelligent Abyssinian, Daisy needs mental stimulation, but her arthritis requires play to be gentle and low-impact to avoid joint strain.
- `Health Monitoring` — Close monitoring helps in early detection of changes in her arthritis, allowing for timely veterinary intervention and adjustment of care.
- `Vet Visit` — Frequent vet visits are essential for senior cats, especially those with chronic conditions like arthritis, to ensure optimal health management and pain control.

**Your label for case_23:** ___ (1 grounded / 0 not)

---

## case_24  — Max (Domestic Shorthair, 7y)
*Conditions:* Diabetes, Arthritis  |  *plan source:* gemini

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: feline diabetes insulin injections (typically twice daily) high-protein, low-carb diet condition: arthritis / osteoarthritis pain medication as prescribed gentle, low-impact exercise feeding gentle_play medication_if_needed exercise medication water_access vet_visits_frequent grooming monitoring_mobility playtime medication_injection feeding_senior_formula comfort_monitoring monitoring feeding_ground_...

**Plan tasks:**
- `medication_injection` — Essential for managing Max's diabetes and maintaining stable blood glucose levels.
- `feeding_specialized` — Supports diabetes management and reduces joint strain for arthritis.
- `medication` — Manages pain and improves mobility for Max's arthritis.
- `water_access` — Hydration is vital for overall health, especially for senior cats and those with health conditions. Easy access supports arthritis.
- `litter_box_cleaning` — Maintains hygiene and ensures Max, with arthritis, has comfortable and easy access.
- `gentle_play` — Helps with weight management for diabetes and maintains joint flexibility without stressing arthritic joints.
- `vet_visits_frequent` — Essential for adjusting medication, monitoring disease progression, and ensuring overall well-being.

**Your label for case_24:** ___ (1 grounded / 0 not)

---

## case_25  — Olive (Persian, 10y)
*Conditions:* Hypertrophic Cardiomyopathy, Arthritis  |  *plan source:* gemini

**Retrieved context:**
> breed: persian daily brushing required to prevent matting regular eye cleaning (tear staining) sensitive to heat and humidity age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: hypertrophic cardiomyopathy (hcm) heart medication as prescribed stress reduction and quiet environment condition: arthritis / osteoarthritis pain medication as prescribed gentle, low-impact exercise feeding gentle_play medication_if_needed rest_monitoring medication eye_care water_access vet_visits_frequent grooming monitoring_mobility playtime feeding_senior_formula comfort_monitoring vet_visits feeding_ground_level hyper...

**Plan tasks:**
- `Medication Administration` — Essential for managing Olive's chronic health conditions, improving heart function and alleviating pain to maintain her quality of life.
- `Feeding and Hydration` — Supports Olive's senior nutritional needs and makes eating/drinking comfortable despite arthritis. Fresh water is crucial for overall health, especially kidney function.
- `Litter Box Cleaning` — Maintains hygiene and ensures Olive can comfortably use the litter box without strain, which is important for her arthritis.
- `Grooming and Eye Care` — Crucial for Persian cats to prevent painful mats and maintain eye hygiene, contributing to overall comfort and preventing skin issues.
- `Gentle Exercise and Mobility Monitoring` — Promotes gentle activity beneficial for arthritis without over-exerting her heart. Monitoring helps detect any changes in her condition early.
- `Veterinary and Cardiac Monitoring` — Essential for ongoing management of Hypertrophic Cardiomyopathy and monitoring overall senior health, allowing for timely adjustments to her care plan.
- `Environmental Comfort and Stress Reduction` — A calm environment is vital for managing HCM, and comfortable resting spots alleviate discomfort from arthritis, enhancing Olive's well-being.

**Your label for case_25:** ___ (1 grounded / 0 not)

---
