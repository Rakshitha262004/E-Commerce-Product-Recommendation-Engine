# src/data_loader.py
# Loads JSON data into HashMaps (dictionaries) for O(1) lookup

import json
from src.product import Product
from src.user import User


def load_products(filepath):
    """
    Load products.json and return a HashMap: product_id → Product object
    Also returns a category map: category → [product_ids]
    """
    with open(filepath, 'r') as f:
        data = json.load(f)

    product_map = {}        # HashMap: O(1) product lookup
    category_map = {}       # HashMap: category → list of product IDs

    for item in data:
        p = Product(
            pid=item['id'],
            name=item['name'],
            category=item['category'],
            price=item['price'],
            rating=item['rating'],
            tags=item['tags']
        )
        product_map[p.id] = p

        # Build category index
        if p.category not in category_map:
            category_map[p.category] = []
        category_map[p.category].append(p.id)

    return product_map, category_map


def load_users(user_filepath, interaction_filepath):
    """
    Load users.json and interactions.json
    Returns a HashMap: user_id → User object
    """
    with open(user_filepath, 'r') as f:
        user_data = json.load(f)

    with open(interaction_filepath, 'r') as f:
        interaction_data = json.load(f)

    user_map = {}

    for item in user_data:
        u = User(
            uid=item['id'],
            name=item['name'],
            age=item['age'],
            interests=item['interests']
        )
        u.load_interactions(interaction_data)
        user_map[u.id] = u

    return user_map