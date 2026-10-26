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

"""Public API tools for searching global culinary recipes via TheMealDB."""

import json
import os
import urllib.parse
import urllib.request
from typing import Any, Dict, List


def search_online_recipes(query: str) -> str:
    """Searches a public recipe database (TheMealDB) for real culinary recipes and ingredients.

    Args:
        query: Ingredient or meal name to search for (e.g. 'salmon', 'chicken', 'broccoli').

    Returns:
        JSON string containing up to 3 matching recipes with their ingredients and instructions.
    """
    # Uses THEMEALDB_API_KEY if configured in environment, otherwise falls back to free public test tier '1'
    api_key = os.environ.get("THEMEALDB_API_KEY", "1")
    encoded_query = urllib.parse.quote(query.strip())
    url = f"https://www.themealdb.com/api/json/v1/{api_key}/search.php?s={encoded_query}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SavoryBalanceAgent/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        meals = data.get("meals")
        if not meals:
            return json.dumps({"status": "empty", "message": f"No online recipes found matching '{query}'."})

        results = []
        for meal in meals[:3]:  # Return top 3 matches to keep context compact
            ingredients = []
            for i in range(1, 21):
                ing = meal.get(f"strIngredient{i}")
                measure = meal.get(f"strMeasure{i}")
                if ing and ing.strip():
                    item = f"{measure.strip()} {ing.strip()}" if measure and measure.strip() else ing.strip()
                    ingredients.append(item)

            instructions = meal.get("strInstructions", "").strip()
            # Truncate very long instructions if needed
            if len(instructions) > 400:
                instructions = instructions[:397] + "..."

            results.append({
                "meal_name": meal.get("strMeal"),
                "category": meal.get("strCategory"),
                "cuisine": meal.get("strArea"),
                "ingredients": ingredients,
                "instructions": instructions,
                "thumbnail_url": meal.get("strMealThumb"),
            })

        return json.dumps({"status": "success", "count": len(results), "recipes": results}, indent=2)

    except Exception as e:
        return json.dumps({"status": "error", "message": f"Failed to fetch recipes: {str(e)}"})
