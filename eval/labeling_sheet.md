# Groundedness labeling sheet

For each plan, decide: are the plan's tasks/advice supported by the
RETRIEVED CONTEXT? Mark **1 = grounded** or **0 = not grounded** in
`human_labels.jsonl`. Judge independently — do not run the LLM judge first.

---

## case_01  — Mochi (Persian, 4y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: persian daily brushing required to prevent matting regular eye cleaning (tear staining) sensitive to heat and humidity age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition water_refresh litter_maintenance grooming feeding eye_care playtime feeding_twice_daily

**Plan tasks:**
- `eye_care` — This task is recommended by the retrieved cat care knowledge.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_01:** ___ (1 grounded / 0 not)

---

## case_02  — Luna (Bengal, 2y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: bengal extremely active - needs lots of exercise intelligent and can learn tricks needs environmental enrichment age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition water_refresh exercise training feeding grooming litter_maintenance playtime feeding_twice_daily

**Plan tasks:**
- `exercise` — Play helps meet activity needs and reduces stress or boredom.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_02:** ___ (1 grounded / 0 not)

---

## case_03  — Shadow (Siamese, 3y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: siamese very vocal and social - needs attention intelligent - requires mental stimulation prone to separation anxiety age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition water_refresh training feeding grooming litter_maintenance interaction playtime feeding_twice_daily

**Plan tasks:**
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `interaction` — This task is recommended by the retrieved cat care knowledge.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_03:** ___ (1 grounded / 0 not)

---

## case_04  — Biscuit (Maine Coon, 5y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: maine coon large breed - needs more food and water thicker coat requires regular brushing playful and dog-like personality age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition water_refresh training feeding grooming litter_maintenance playtime feeding_twice_daily

**Plan tasks:**
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_04:** ___ (1 grounded / 0 not)

---

## case_05  — Pixel (Abyssinian, 2y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: abyssinian extremely active and athletic - needs lots of vertical space intelligent and curious - requires mental stimulation social and people-oriented - dislikes being alone needs interactive play and climbing structures age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition playtime_intensive water_refresh exercise environmental_enrichment feeding training grooming litter_maintenance playtime feeding_twice_daily

**Plan tasks:**
- `environmental_enrichment` — This task is recommended by the retrieved cat care knowledge.
- `exercise` — Play helps meet activity needs and reduces stress or boredom.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `playtime_intensive` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_05:** ___ (1 grounded / 0 not)

---

## case_06  — Tiny (Domestic Shorthair, 0y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: kitten high energy and playfulness rapid growth and development needs frequent meals learning and socialization critical socialization feeding_frequent water_refresh playtime_multiple training feeding playtime monitoring

**Plan tasks:**
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_frequent` — This task is recommended by the retrieved cat care knowledge.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `playtime_multiple` — Play helps meet activity needs and reduces stress or boredom.
- `socialization` — This task is recommended by the retrieved cat care knowledge.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_06:** ___ (1 grounded / 0 not)

---

## case_07  — Whiskers (Domestic Shorthair, 10y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet water_access feeding_senior_formula gentle_play comfort_monitoring feeding grooming vet_visits_frequent playtime medication_if_needed monitoring

**Plan tasks:**
- `comfort_monitoring` — Monitoring helps catch behavior or appetite changes early.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_senior_formula` — This task is recommended by the retrieved cat care knowledge.
- `gentle_play` — Play helps meet activity needs and reduces stress or boredom.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `medication_if_needed` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `vet_visits_frequent` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_access` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_07:** ___ (1 grounded / 0 not)

---

## case_08  — Ginger (Ragdoll, 6y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: ragdoll semi-long coat requires regular brushing docile and gentle - enjoys human company can be sensitive to stress age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition water_refresh litter_maintenance feeding grooming interaction playtime feeding_twice_daily

**Plan tasks:**
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `interaction` — This task is recommended by the retrieved cat care knowledge.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_08:** ___ (1 grounded / 0 not)

---

## case_09  — Smokey (Siamese, 11y)
*Conditions:* Chronic Kidney Disease  |  *plan source:* fallback

**Retrieved context:**
> breed: siamese very vocal and social - needs attention intelligent - requires mental stimulation prone to separation anxiety age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: chronic kidney disease (ckd) prescription kidney diet (low protein, low phosphorus) frequent water access and hydration monitoring playtime medication water_access feeding_senior_formula feeding_specialized gentle_play comfort_monitoring training feeding grooming interaction water_bowl_refresh vet_visits_frequent monitoring me...

**Plan tasks:**
- `comfort_monitoring` — Monitoring helps catch behavior or appetite changes early.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_senior_formula` — This task is recommended by the retrieved cat care knowledge.
- `feeding_specialized` — This task is recommended by the retrieved cat care knowledge.
- `gentle_play` — Play helps meet activity needs and reduces stress or boredom.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `interaction` — This task is recommended by the retrieved cat care knowledge.
- `medication` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `medication_if_needed` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `vet_visits_frequent` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_access` — Fresh water supports hydration and helps with common feline health risks.
- `water_bowl_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_09:** ___ (1 grounded / 0 not)

---

## case_10  — Boots (Maine Coon, 8y)
*Conditions:* Diabetes  |  *plan source:* fallback

**Retrieved context:**
> breed: maine coon large breed - needs more food and water thicker coat requires regular brushing playful and dog-like personality age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: feline diabetes insulin injections (typically twice daily) high-protein, low-carb diet playtime water_access exercise medication_injection feeding_specialized feeding_senior_formula gentle_play comfort_monitoring training feeding grooming vet_visits_frequent monitoring medication_if_needed feline diabetes insulin injectio...

**Plan tasks:**
- `comfort_monitoring` — Monitoring helps catch behavior or appetite changes early.
- `exercise` — Play helps meet activity needs and reduces stress or boredom.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_senior_formula` — This task is recommended by the retrieved cat care knowledge.
- `feeding_specialized` — This task is recommended by the retrieved cat care knowledge.
- `gentle_play` — Play helps meet activity needs and reduces stress or boredom.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `medication_if_needed` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `medication_injection` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `vet_visits_frequent` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_access` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_10:** ___ (1 grounded / 0 not)

---

## case_11  — Cleo (Domestic Shorthair, 9y)
*Conditions:* Hyperthyroidism  |  *plan source:* fallback

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: hyperthyroidism thyroid medication (typically twice daily) regular thyroid level monitoring playtime medication vet_visits water_access feeding_senior_formula gentle_play feeding_controlled comfort_monitoring feeding grooming vet_visits_frequent monitoring medication_if_needed hyperthyroidism thyroid me...

**Plan tasks:**
- `comfort_monitoring` — Monitoring helps catch behavior or appetite changes early.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_controlled` — This task is recommended by the retrieved cat care knowledge.
- `feeding_senior_formula` — This task is recommended by the retrieved cat care knowledge.
- `gentle_play` — Play helps meet activity needs and reduces stress or boredom.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `medication` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `medication_if_needed` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `vet_visits` — Regular veterinary care is recommended in the retrieved knowledge.
- `vet_visits_frequent` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_access` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_11:** ___ (1 grounded / 0 not)

---

## case_12  — Felix (Ragdoll, 7y)
*Conditions:* Hypertrophic Cardiomyopathy  |  *plan source:* fallback

**Retrieved context:**
> breed: ragdoll semi-long coat requires regular brushing docile and gentle - enjoys human company can be sensitive to stress age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: hypertrophic cardiomyopathy (hcm) heart medication as prescribed stress reduction and quiet environment rest_monitoring medication vet_visits water_access gentle_play feeding_senior_formula comfort_monitoring feeding grooming interaction vet_visits_frequent playtime medication_if_needed hypertrophic cardiomyopathy (hcm) heart m...

**Plan tasks:**
- `comfort_monitoring` — Monitoring helps catch behavior or appetite changes early.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_senior_formula` — This task is recommended by the retrieved cat care knowledge.
- `gentle_play` — Play helps meet activity needs and reduces stress or boredom.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `interaction` — This task is recommended by the retrieved cat care knowledge.
- `medication` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `medication_if_needed` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `rest_monitoring` — Monitoring helps catch behavior or appetite changes early.
- `vet_visits` — Regular veterinary care is recommended in the retrieved knowledge.
- `vet_visits_frequent` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_access` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_12:** ___ (1 grounded / 0 not)

---

## case_13  — Patches (Domestic Shorthair, 4y)
*Conditions:* Feline Lower Urinary Tract Disease  |  *plan source:* fallback

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition condition: feline lower urinary tract disease (flutd) prescription urinary diet increased water intake playtime litter_box_cleaning water_refresh feeding_specialized litter_maintenance feeding grooming water_bowl_refresh monitoring feeding_twice_daily feline lower urinary tract disease (flutd) prescription urinary diet incre...

**Plan tasks:**
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_specialized` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `litter_box_cleaning` — Clean litter helps with comfort and lets you monitor elimination habits.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `water_bowl_refresh` — Fresh water supports hydration and helps with common feline health risks.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_13:** ___ (1 grounded / 0 not)

---

## case_14  — Oreo (Persian, 12y)
*Conditions:* Arthritis  |  *plan source:* fallback

**Retrieved context:**
> breed: persian daily brushing required to prevent matting regular eye cleaning (tear staining) sensitive to heat and humidity age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: arthritis / osteoarthritis pain medication as prescribed gentle, low-impact exercise monitoring_mobility medication water_access gentle_play feeding_senior_formula comfort_monitoring grooming feeding eye_care feeding_ground_level vet_visits_frequent playtime medication_if_needed arthritis / osteoarthritis pain medication as p...

**Plan tasks:**
- `comfort_monitoring` — Monitoring helps catch behavior or appetite changes early.
- `eye_care` — This task is recommended by the retrieved cat care knowledge.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_ground_level` — This task is recommended by the retrieved cat care knowledge.
- `feeding_senior_formula` — This task is recommended by the retrieved cat care knowledge.
- `gentle_play` — Play helps meet activity needs and reduces stress or boredom.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `medication` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `medication_if_needed` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `monitoring_mobility` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `vet_visits_frequent` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_access` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_14:** ___ (1 grounded / 0 not)

---

## case_15  — Milo (Bengal, 3y)
*Conditions:* Feline Immunodeficiency Virus  |  *plan source:* fallback

**Retrieved context:**
> breed: bengal extremely active - needs lots of exercise intelligent and can learn tricks needs environmental enrichment age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition condition: feline immunodeficiency virus (fiv) keep indoors to prevent spread regular veterinary monitoring playtime vet_visits water_refresh exercise feeding_quality training feeding grooming litter_maintenance feeding_twice_daily monitoring medication_as_needed feline immunodeficiency virus (fiv) keep indoors to prevent spread regular veterinary monit...

**Plan tasks:**
- `exercise` — Play helps meet activity needs and reduces stress or boredom.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_quality` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `medication_as_needed` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `vet_visits` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_15:** ___ (1 grounded / 0 not)

---

## case_16  — Nala (Siamese, 5y)
*Conditions:* Asthma  |  *plan source:* fallback

**Retrieved context:**
> breed: siamese very vocal and social - needs attention intelligent - requires mental stimulation prone to separation anxiety age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition condition: feline asthma inhalers or medications as prescribed minimize environmental triggers (dust, smoke, allergens) playtime medication vet_visits water_refresh monitoring_breathing training feeding grooming litter_maintenance interaction environment_control feeding_twice_daily feline asthma inhalers or medications as prescribed minimize enviro...

**Plan tasks:**
- `environment_control` — This task is recommended by the retrieved cat care knowledge.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `interaction` — This task is recommended by the retrieved cat care knowledge.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `medication` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `monitoring_breathing` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `vet_visits` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_16:** ___ (1 grounded / 0 not)

---

## case_17  — Simba (Maine Coon, 1y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: maine coon large breed - needs more food and water thicker coat requires regular brushing playful and dog-like personality age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition water_refresh training feeding grooming litter_maintenance playtime feeding_twice_daily

**Plan tasks:**
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_17:** ___ (1 grounded / 0 not)

---

## case_18  — Coco (Abyssinian, 9y)
*Conditions:* Hyperthyroidism  |  *plan source:* fallback

**Retrieved context:**
> breed: abyssinian extremely active and athletic - needs lots of vertical space intelligent and curious - requires mental stimulation social and people-oriented - dislikes being alone needs interactive play and climbing structures age group: senior cat decreased activity level increased health monitoring needed possible age-related conditions may need special diet condition: hyperthyroidism thyroid medication (typically twice daily) regular thyroid level monitoring medication vet_visits playtime_intensive exercise water_access feeding_senior_formula gentle_play feeding_controlled comfort_monito...

**Plan tasks:**
- `comfort_monitoring` — Monitoring helps catch behavior or appetite changes early.
- `environmental_enrichment` — This task is recommended by the retrieved cat care knowledge.
- `exercise` — Play helps meet activity needs and reduces stress or boredom.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_controlled` — This task is recommended by the retrieved cat care knowledge.
- `feeding_senior_formula` — This task is recommended by the retrieved cat care knowledge.
- `gentle_play` — Play helps meet activity needs and reduces stress or boredom.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `medication` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `medication_if_needed` — Health conditions in the retrieved knowledge indicate medication support may be needed.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime_intensive` — Play helps meet activity needs and reduces stress or boredom.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `vet_visits` — Regular veterinary care is recommended in the retrieved knowledge.
- `vet_visits_frequent` — Regular veterinary care is recommended in the retrieved knowledge.
- `water_access` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_18:** ___ (1 grounded / 0 not)

---

## case_19  — Bella (Persian, 0y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: persian daily brushing required to prevent matting regular eye cleaning (tear staining) sensitive to heat and humidity age group: kitten high energy and playfulness rapid growth and development needs frequent meals learning and socialization critical socialization water_refresh playtime_multiple training grooming feeding eye_care playtime feeding_frequent

**Plan tasks:**
- `eye_care` — This task is recommended by the retrieved cat care knowledge.
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_frequent` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `playtime_multiple` — Play helps meet activity needs and reduces stress or boredom.
- `socialization` — This task is recommended by the retrieved cat care knowledge.
- `training` — This task is recommended by the retrieved cat care knowledge.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_19:** ___ (1 grounded / 0 not)

---

## case_20  — Jasper (Domestic Shorthair, 5y)
*Conditions:* none  |  *plan source:* fallback

**Retrieved context:**
> breed: domestic shorthair varied personalities and energy levels generally hardy and adaptable minimal grooming needs good for first-time cat owners age group: adult cat stable energy level (varies by breed) maintenance health care most active years peak physical condition water_refresh litter_maintenance feeding grooming playtime feeding_twice_daily monitoring

**Plan tasks:**
- `feeding` — This task is recommended by the retrieved cat care knowledge.
- `feeding_twice_daily` — This task is recommended by the retrieved cat care knowledge.
- `grooming` — Grooming supports coat health and helps catch skin or matting issues early.
- `litter_maintenance` — Clean litter helps with comfort and lets you monitor elimination habits.
- `monitoring` — Monitoring helps catch behavior or appetite changes early.
- `playtime` — Play helps meet activity needs and reduces stress or boredom.
- `water_refresh` — Fresh water supports hydration and helps with common feline health risks.

**Your label for case_20:** ___ (1 grounded / 0 not)

---
