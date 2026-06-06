# 🛒 E-Commerce Product Recommendation Engine

> A **Data Structures & Algorithms** project implementing a product recommendation system  
> using **HashMap, Priority Queue, Jaccard Similarity, and Sorting** — with a Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![DSA](https://img.shields.io/badge/DSA-HashMap%20%7C%20Heap%20%7C%20Sets-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 Problem Statement

Online platforms like Amazon and Flipkart generate billions in revenue through personalized
recommendations. This project builds the **algorithmic core** of such a system using fundamental
DSA concepts — no ML libraries, no black boxes.

---

## 🧠 DSA Concepts Used

| Concept | Where Used | Complexity |
|---|---|---|
| **HashMap / Dictionary** | Product & user lookup, category index | O(1) |
| **Set** | Filter purchased products, tag intersection | O(1) membership |
| **Jaccard Similarity** | Content-based product similarity | O(min(A,B)) |
| **Priority Queue (heapq)** | Top-N recommendation extraction | O(n log k) |
| **Sorting** | Ranking by affinity score | O(n log n) |
| **Weighted Scoring** | Multi-signal affinity (purchase/cart/search) | O(interactions) |

---

## ⚙️ Algorithm Explanation

### Jaccard Similarity (Tag-based)
```
Jaccard(A, B) = |tags_A ∩ tags_B| / |tags_A ∪ tags_B|
```

### Affinity Score (Per product per user)
```
score = Σ [ jaccard(product, interacted) × weight ]
      + category_interest_bonus (2)
      + product_rating × 0.5

Weights: purchase=3 | cart=2 | search=1 | rating=actual value
```

### Top-N via Min-Heap
```
For each non-purchased product:
    compute affinity_score
    heappush(heap, (score, pid, product))
    if len(heap) > N: heappop()   ← discard lowest
Return heap sorted descending
```

---

## ✨ Features

- 🎯 Personalized top-N product recommendations per user  
- 📂 Category-wise recommendations based on user interests  
- 🔍 Similar product finder via Jaccard similarity  
- ⚡ HashSet filtering of already-purchased products  
- 📊 Live affinity score bar chart  
- 📄 One-click JSON report download  
- 🌙 Dark-mode Streamlit dashboard  

---

## 📁 Folder Structure

```
E-Commerce-Product-Recommendation-Engine/
├── data/
│   ├── products.json          ← 20 product catalog
│   ├── users.json             ← 4 user profiles
│   └── interactions.json      ← purchase / cart / search / rating data
├── src/
│   ├── product.py             ← Product class
│   ├── user.py                ← User class
│   ├── data_loader.py         ← HashMap-based JSON loader
│   ├── similarity.py          ← Jaccard similarity
│   ├── recommender.py         ← Core engine (heap + scoring)
│   └── report.py              ← Report generator
├── outputs/                   ← Saved JSON reports
├── images/                    ← Screenshots
├── app.py                     ← Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Rakshitha262004/E-Commerce-Product-Recommendation-Engine.git
cd E-Commerce-Product-Recommendation-Engine

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit dashboard
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📸 Screenshots

| Dashboard | Category Picks |
|---|---|
| ![main](images/dashboard.png) | ![cat](images/category_recs.png) |

---

## 🎓 Learning Outcomes

- Implementing **HashMaps** for O(1) lookup in real-world scenarios  
- Using **heapq** to solve top-K problems efficiently  
- Applying **set theory (Jaccard)** as a similarity metric  
- Understanding **content-based filtering** from scratch  
- Building a modular, production-style Python project  
- Deploying a data app with **Streamlit**  

---

## 👤 Author

**Rakshitha A S** | USN: 1AH23CY042  
B.E. Cybersecurity · ACS College of Engineering, Bengaluru · VTU  
GitHub: [github.com/Rakshitha262004](https://github.com/Rakshitha262004)

---

## 🙏 Acknowledgements

Special thanks to **Umesh Yadav** (mentor) for guidance on project structuring and GitHub documentation.
