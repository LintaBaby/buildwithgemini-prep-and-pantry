# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Seed script to populate Firestore with initial healthy, sugar-free balanced meals."""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-18d3e33b1a42"

SAMPLE_MEALS = [
    {
        "id": "avocado-poached-egg-bowl",
        "name": "Avocado & Poached Egg Protein Bowl",
        "meal_type": "breakfast",
        "description": "A light and nutrient-dense breakfast with baby spinach, soft poached eggs, sliced Hass avocado, and toasted pumpkin seeds.",
        "ingredients": [
            "2 pasture-raised eggs",
            "1/2 Hass avocado, sliced",
            "2 cups fresh baby spinach",
            "1 tbsp toasted pumpkin seeds",
            "1 tsp extra virgin olive oil",
            "Pinch of sea salt and crushed red pepper"
        ],
        "prep_time_minutes": 10,
        "macros": {
            "calories": 320,
            "protein_g": 16,
            "carbs_g": 9,
            "fat_g": 26,
            "sugar_g": 1
        },
        "tags": ["zero-added-sugar", "light", "high-protein", "healthy-fats", "breakfast"]
    },
    {
        "id": "mediterranean-grilled-chicken-salad",
        "name": "Mediterranean Herb Grilled Chicken Salad",
        "meal_type": "lunch",
        "description": "Herb-marinated chicken breast served over chopped romaine, Persian cucumbers, kalamata olives, crumbled feta, and lemon oregano vinaigrette.",
        "ingredients": [
            "150g skinless chicken breast, grilled",
            "3 cups chopped romaine lettuce",
            "1 Persian cucumber, diced",
            "6 pitted kalamata olives",
            "30g sheep milk feta cheese",
            "1.5 tbsp extra virgin olive oil",
            "1 tbsp fresh lemon juice",
            "Dried oregano and black pepper"
        ],
        "prep_time_minutes": 15,
        "macros": {
            "calories": 420,
            "protein_g": 38,
            "carbs_g": 8,
            "fat_g": 26,
            "sugar_g": 2
        },
        "tags": ["zero-added-sugar", "balanced", "high-protein", "mediterranean", "lunch"]
    },
    {
        "id": "wild-salmon-roasted-broccoli",
        "name": "Pan-Seared Wild Salmon with Garlic Roasted Broccoli",
        "meal_type": "dinner",
        "description": "Crispy skin-on wild salmon fillet served with tender garlic broccoli florets tossed in avocado oil and toasted sesame.",
        "ingredients": [
            "180g wild Alaskan salmon fillet",
            "2.5 cups broccoli florets",
            "2 cloves garlic, minced",
            "1 tbsp avocado oil",
            "1 lemon wedge",
            "Himalayan pink salt and freshly ground pepper"
        ],
        "prep_time_minutes": 20,
        "macros": {
            "calories": 460,
            "protein_g": 42,
            "carbs_g": 11,
            "fat_g": 28,
            "sugar_g": 2
        },
        "tags": ["zero-added-sugar", "omega-3", "balanced", "keto-friendly", "dinner"]
    },
    {
        "id": "cucumber-hummus-flax-bites",
        "name": "Spiced Cucumber & Roasted Garlic Hummus Bites",
        "meal_type": "snack",
        "description": "Thick Persian cucumber rounds topped with savory roasted garlic hummus, roasted chickpeas, and ground flaxseeds.",
        "ingredients": [
            "1 large English or Persian cucumber, cut into thick discs",
            "3 tbsp traditional roasted garlic hummus (unsweetened)",
            "2 tbsp spiced crunchy roasted chickpeas",
            "1 tsp whole golden flaxseeds"
        ],
        "prep_time_minutes": 5,
        "macros": {
            "calories": 160,
            "protein_g": 7,
            "carbs_g": 16,
            "fat_g": 8,
            "sugar_g": 1
        },
        "tags": ["zero-added-sugar", "quick-snack", "fiber-rich", "plant-based", "snack"]
    },
    {
        "id": "turkey-zucchini-skillet",
        "name": "Savory Lean Turkey & Zucchini Herb Skillet",
        "meal_type": "dinner",
        "description": "Lean ground turkey sautéed with zucchini noodles, diced bell peppers, Italian herbs, and crushed walnuts.",
        "ingredients": [
            "160g 93% lean ground turkey",
            "2 medium zucchinis, spiralized or diced",
            "1/2 green bell pepper, diced",
            "1 tbsp extra virgin olive oil",
            "15g crushed walnuts",
            "1 tsp Italian seasoning blend",
            "Sea salt and black pepper"
        ],
        "prep_time_minutes": 15,
        "macros": {
            "calories": 390,
            "protein_g": 36,
            "carbs_g": 10,
            "fat_g": 23,
            "sugar_g": 3
        },
        "tags": ["zero-added-sugar", "balanced", "high-protein", "easy-prep", "dinner"]
    }
]


def seed_database():
    print(f"Connecting to Firestore with hardcoded project ID: {PROJECT_ID}...")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection("meals")

    print(f"Seeding {len(SAMPLE_MEALS)} items into 'meals' collection...")
    for meal in SAMPLE_MEALS:
        doc_id = meal["id"]
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(meal)
        print(f"  ✓ Seeded meal: {meal['name']} ({meal['meal_type']})")

    print("✅ Firestore seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
