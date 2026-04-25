# AI Problem Solving — GitHub Submission

> **Course:** Artificial Intelligence | **Team Size:** 2 members
> **Implemented Problems:** Problem — Map Coloring (CSP)
> **Language:** Python 3 | **Framework:** Streamlit

---

## Live Demo

| Problem            | Live Link                          |
| ------------------ | ---------------------------------- |
| Map Coloring (CSP) | https://mapcoloring.streamlit.app/ |

---

## Repository Structure

```
AI_ProblemSolving/
├── map_coloring_csp/
│   ├── app.py               # Streamlit app
│   ├── requirements.txt
│   └── README.md
└── README.md
```

---

## Problem — Map Coloring using CSP

### Case Study

The Map Coloring Problem assigns colors to regions such that no two adjacent regions share the same color. It is a classic **Constraint Satisfaction Problem (CSP)** used in AI for decision-making and optimization.

---

## Algorithm Used

### Backtracking (CSP)

* Assign colors to regions one by one
* Check constraints before assigning
* If conflict occurs, backtrack and try another color
* Ensures all constraints are satisfied

**Time Complexity:** Exponential (depends on number of regions and colors)

---

## How to Run Locally

```bash
cd MapColoring_CSP
pip install -r requirements.txt
streamlit run app.py
```

---

## Sample Input

```
Regions: A, B, C, D
A → B, C
B → A, C, D
C → A, B, D
D → B, C

Colors: Red, Green, Blue
```

---

## Sample Output

```
A → Red
B → Green
C → Blue
D → Red
```

---

## Features

* User input for regions, neighbors, and colors
* Ensures no adjacent regions share same color
* Streamlit-based interactive UI
* Displays valid color assignment
* Handles invalid input and no-solution cases

---

## Execution Steps

### Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/AI_ProblemSolving_RA2411026050174.git
cd AI_ProblemSolving_RA2411026050174/MapColoring_CSP
pip install -r requirements.txt
streamlit run app.py
```

---

### Streamlit Cloud Deployment

1. Push project to GitHub (public repo)
2. Go to https://share.streamlit.io
3. Click **New App**
4. Select repository
5. Set main file: `map_coloring_CSP/app.py`
6. Click Deploy

---

## Team Members

| Name     | Register Number |
| -------- | --------------- |
| Deepak B | RA2411026050174 |

---

*Submitted for AI Problem Solving Assignment — April 2026*
