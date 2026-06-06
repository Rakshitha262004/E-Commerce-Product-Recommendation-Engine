# src/similarity.py
# Jaccard Similarity between two products based on their tag sets
# Jaccard(A, B) = |A ∩ B| / |A ∪ B|

def jaccard_similarity(tags_a, tags_b):
    """
    Calculate Jaccard similarity between two tag sets.
    Returns a float between 0.0 (no similarity) and 1.0 (identical).
    
    DSA concept: Set operations — intersection and union
    Time complexity: O(min(|A|, |B|)) for set intersection
    """
    if not tags_a or not tags_b:
        return 0.0

    intersection = tags_a & tags_b          # Set intersection
    union = tags_a | tags_b                 # Set union
    return len(intersection) / len(union)


def get_similar_products(target_product, product_map, top_n=5):
    """
    Find top-N products most similar to target_product using Jaccard.
    Uses a list + sort approach — demonstrates sorting on custom key.
    
    DSA: Sorting by computed score, O(n log n)
    """
    scores = []

    for pid, product in product_map.items():
        if pid == target_product.id:
            continue    # Skip self

        score = jaccard_similarity(target_product.tags, product.tags)
        if score > 0:
            scores.append((score, product))

    # Sort descending by similarity score
    scores.sort(key=lambda x: (-x[0], -x[1].rating))

    return scores[:top_n]