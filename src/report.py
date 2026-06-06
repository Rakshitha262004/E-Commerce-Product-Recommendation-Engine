# src/report.py
# Generates and saves the recommendation report as JSON

import json
import os
from datetime import datetime


def generate_report(user, recommendations, category_recommendations, similar_products_map):
    """
    Build a structured report dictionary.
    """
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": {
            "id": user.id,
            "name": user.name,
            "interests": user.interests,
            "total_purchases": len(user.purchased),
            "cart_items": len(user.cart),
            "search_history_count": len(user.searched)
        },
        "top_recommendations": [
            {
                "rank": i + 1,
                "product_id": p.id,
                "name": p.name,
                "category": p.category,
                "price": p.price,
                "rating": p.rating,
                "affinity_score": score
            }
            for i, (p, score) in enumerate(recommendations)
        ],
        "category_recommendations": {
            cat: [
                {"product_id": p.id, "name": p.name, "score": score}
                for score, p in recs
            ]
            for cat, recs in category_recommendations.items()
        },
        "similar_products": {
            pid: [
                {"product_id": sp.id, "name": sp.name, "similarity": round(sim, 4)}
                for sim, sp in sims
            ]
            for pid, sims in similar_products_map.items()
        }
    }
    return report


def save_report(report, output_dir="outputs"):
    """Save report to JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/recommendation_report_{report['user']['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Report saved to: {filename}")
    return filename