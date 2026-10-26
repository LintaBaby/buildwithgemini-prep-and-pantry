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

"""Firestore tools for reading and saving healthy, sugar-free meals and meal plans."""

import json
from typing import Any, Dict, List, Optional
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-18d3e33b1a42"

_db_client: Optional[firestore.Client] = None


def get_firestore_client() -> firestore.Client:
    """Returns a singleton Firestore client with the hardcoded GCP project ID."""
    global _db_client
    if _db_client is None:
        _db_client = firestore.Client(project=PROJECT_ID)
    return _db_client


def list_meals(meal_type: Optional[str] = None) -> str:
    """Retrieves healthy, balanced sugar-free meals from Firestore.

    Args:
        meal_type: Optional filter by type: 'breakfast', 'lunch', 'dinner', or 'snack'.

    Returns:
        JSON string containing the list of matching meals.
    """
    db = get_firestore_client()
    query = db.collection("meals")

    if meal_type:
        clean_type = meal_type.strip().lower()
        query = query.where("meal_type", "==", clean_type)

    docs = query.stream()
    results = []
    for doc in docs:
        meal_data = doc.to_dict()
        results.append(meal_data)

    if not results:
        msg = f"No meals found for category '{meal_type}'." if meal_type else "No meals found in database."
        return json.dumps({"status": "empty", "message": msg, "meals": []})

    return json.dumps({"status": "success", "count": len(results), "meals": results}, indent=2)


def get_meal_details(meal_id: str) -> str:
    """Fetches full recipe, ingredients, and nutrition macros for a specific meal.

    Args:
        meal_id: Unique ID of the meal document (e.g. 'avocado-poached-egg-bowl').

    Returns:
        JSON string with meal details or error if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection("meals").document(meal_id.strip())
    doc = doc_ref.get()

    if not doc.exists:
        return json.dumps({"status": "not_found", "message": f"Meal with ID '{meal_id}' does not exist."})

    return json.dumps({"status": "success", "meal": doc.to_dict()}, indent=2)


def add_custom_meal(
    meal_id: str,
    name: str,
    meal_type: str,
    description: str,
    ingredients: List[str],
    prep_time_minutes: int,
    calories: int,
    protein_g: int,
    carbs_g: int,
    fat_g: int,
    sugar_g: int = 0
) -> str:
    """Adds a new custom healthy, sugar-free meal or recipe to Firestore.

    Args:
        meal_id: Unique slug/identifier for the meal (e.g., 'tofu-sesame-stir-fry').
        name: Display name of the dish.
        meal_type: Type of meal ('breakfast', 'lunch', 'dinner', 'snack').
        description: Brief description of flavor and balance.
        ingredients: List of ingredients.
        prep_time_minutes: Preparation/cooking time in minutes.
        calories: Estimated total calories.
        protein_g: Grams of protein.
        carbs_g: Grams of carbohydrates.
        fat_g: Grams of healthy fats.
        sugar_g: Grams of sugar (should be minimal/zero added sugar).

    Returns:
        JSON confirmation string.
    """
    db = get_firestore_client()
    meal_data = {
        "id": meal_id.strip().lower(),
        "name": name,
        "meal_type": meal_type.strip().lower(),
        "description": description,
        "ingredients": ingredients,
        "prep_time_minutes": prep_time_minutes,
        "macros": {
            "calories": calories,
            "protein_g": protein_g,
            "carbs_g": carbs_g,
            "fat_g": fat_g,
            "sugar_g": sugar_g
        },
        "tags": ["custom", "zero-added-sugar", meal_type.strip().lower()]
    }

    db.collection("meals").document(meal_data["id"]).set(meal_data)
    return json.dumps({"status": "created", "meal_id": meal_data["id"], "name": name})


def generate_grocery_shopping_list(meal_ids: List[str]) -> str:
    """Generates a consolidated, deduplicated grocery shopping list from selected meal IDs.

    Args:
        meal_ids: List of meal IDs to aggregate ingredients for (e.g. ['avocado-poached-egg-bowl', 'wild-salmon-roasted-broccoli']).

    Returns:
        JSON string containing the items and meals included.
    """
    db = get_firestore_client()
    included_meals = []
    all_ingredients = set()

    for meal_id in meal_ids:
        doc = db.collection("meals").document(meal_id.strip()).get()
        if doc.exists:
            data = doc.to_dict()
            included_meals.append(data.get("name", meal_id))
            for ing in data.get("ingredients", []):
                all_ingredients.add(ing.strip())

    if not included_meals:
        return json.dumps({"status": "not_found", "message": "None of the specified meals were found."})

    return json.dumps({
        "status": "success",
        "meals_count": len(included_meals),
        "meals": included_meals,
        "shopping_list": sorted(list(all_ingredients))
    }, indent=2)

