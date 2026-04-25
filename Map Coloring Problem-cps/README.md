# Map Coloring Solver

## What is this project?
Imagine you have a blank map of different states or countries. Your goal is to color every region using a few crayons like Red, Green, and Blue. But there is one strict rule: Two regions that touch each other cannot be the same color, otherwise they would blend together.

This project is a Python application that solves this puzzle automatically. It acts like an AI that figures out the perfect colors for any map you give it, now featuring a beautiful web-based interface powered by **Streamlit**!

## How does the AI work?
We used a concept in Artificial Intelligence called a **Constraint Satisfaction Problem (CSP)**.
- **Regions** are the areas we need to color.
- **Colors** are our available options.
- **Adjacencies** are the rule that touching regions cannot share a color.

To find the solution, the program uses the **Backtracking Algorithm**. Think of it as a smart guessing game where it colors a region, checks if it breaks any rules, and moves to the next. If it hits a dead end where it has no colors left to use without breaking a rule, it undoes its last move and tries a different color until the whole map is successfully colored.

## Cool Features Included
- **Web Interface:** Easy-to-use modern UI built with Streamlit.
- **Graph Visualization:** You can literally see the map drawn on your screen with circles and connecting lines automatically painted with the correct colors.
- **Step-by-Step Backtracking:** Expand the log to see exactly how the AI thought through the problem step by step.
- **Smart Error Handling:** If you give it an impossible puzzle (like trying to color highly connected regions with only 2 colors) it will not crash. It will politely tell you that a solution is not possible.
- **Performance Stats:** It shows you exactly how many steps the computer took and how fast it solved it.

## How to Run It Locally

**1. Install Required Libraries**
Before running, you need to install the required libraries. Open your terminal or command prompt and run:
```bash
pip install -r requirements.txt
```

**2. Run the App**
Open this project folder in Visual Studio Code. Open your terminal and run the Streamlit app:
```bash
streamlit run app.py
```

**3. Play with it**
Once the browser window opens, click the "Load Basic Sample" or "Load Complex Sample" buttons to automatically fill in test data. Click "Solve Problem" to see the magic happen!

## How to Deploy on Streamlit Cloud
1. Push this project to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click on **New app**.
4. Select your repository, branch, and specify `app.py` as the Main file path.
5. Click **Deploy!** Streamlit will automatically install dependencies from `requirements.txt` and launch your app. No Tkinter errors!

## Sample Input and Output

**If you input this:**
- **Regions:** A, B, C, D
- **Colors:** Red, Green, Blue
- **Adjacencies:**
  ```text
  A: B, C
  B: A, C, D
  C: A, B, D
  D: B, C
  ```

**The Output will correctly be:**
- A → Red
- B → Green
- C → Blue
- D → Red

*The computer figured out that A and D can share the color Red because they do not touch each other.*
