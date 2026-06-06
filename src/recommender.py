# src/recommender.py

import heapq
from src.similarity import jaccard_similarity


def compute_affinity_score(product, user, product_map):
    score = 0.0

    all_interactions = {
        **{pid: 3 for pid in user.purchased},
        **{pid: 2 for pid in user.cart},
        **{pid: 1 for pid in user.searched},
    }

    for interacted_pid, weight in all_interactions.items():
        if interacted_pid not in product_map:
            continue
        sim = jaccard_similarity(product.tags, product_map[interacted_pid].tags)
        score += sim * weight

    for rated_pid, rating in user.ratings.items():
        if rated_pid in product_map:
            sim = jaccard_similarity(product.tags, product_map[rated_pid].tags)
            score += sim * rating

    if product.category in user.interests:
        score += 2

    score += product.rating * 0.5
    return round(score, 4)


def get_recommendations(user, product_map, top_n=5):
    purchased_set = set(user.purchased)
    heap = []

    for pid, product in product_map.items():
        if pid in purchased_set:
            continue
        score = compute_affinity_score(product, user, product_map)
        heapq.heappush(heap, (score, pid, product))
        if len(heap) > top_n:
            heapq.heappop(heap)

    results = sorted(heap, key=lambda x: -x[0])
    return [(product, score) for score, pid, product in results]


def get_category_recommendations(user, product_map, category_map, top_n=3):
    category_recommendations = {}
    purchased_set = set(user.purchased)

    for category in user.interests:
        if category not in category_map:
            continue
        candidates = []
        for pid in category_map[category]:
            if pid in purchased_set:
                continue
            product = product_map[pid]
            score = compute_affinity_score(product, user, product_map)
            candidates.append((score, product))

        candidates.sort(key=lambda x: -x[0])
        category_recommendations[category] = candidates[:top_n]

    return category_recommendations


def get_all_scores(user, product_map):
    purchased_set = set(user.purchased)
    scores = {}
    for pid, product in product_map.items():
        if pid in purchased_set:
            scores[product.name] = None
        else:
            scores[product.name] = compute_affinity_score(product, user, product_map)
    return scores