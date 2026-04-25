Map Coloring Solver

What is this project
Imagine you have a blank map of different states or countries. Your goal is to color every region using a few crayons like Red Green and Blue. But there is one strict rule. Two regions that touch each other cannot be the same color otherwise they would blend together.

This project is a Python application that solves this puzzle automatically. It acts like an AI that figures out the perfect colors for any map you give it.

How does the AI work
We used a concept in Artificial Intelligence called a Constraint Satisfaction Problem or CSP.
Regions are the areas we need to color.
Colors are our available options.
Adjacencies are the rule that touching regions cannot share a color.

To find the solution the program uses the Backtracking Algorithm. Think of it as a smart guessing game where it colors a region checks if it breaks any rules and moves to the next. If it hits a dead end where it has no colors left to use without breaking a rule it undoes its last move and tries a different color until the whole map is successfully colored.

Cool Features Included
Graph Visualization You can literally see the map drawn on your screen with circles and connecting lines automatically painted with the correct colors.
Step by Step Backtracking Click a button to see exactly how the AI thought through the problem step by step.
Smart Error Handling If you give it an impossible puzzle like trying to color highly connected regions with only 2 colors it will not crash. It will politely tell you that a solution is not possible.
Performance Stats It shows you exactly how many steps the computer took and how fast it solved it.

How to Run It on Your Computer

1 Install Required Libraries
Before running you need to install two standard Python tools used for drawing the visual graphs. Open your terminal or command prompt and type pip install networkx matplotlib

2 Run the App
Open this project folder in Visual Studio Code. Open your terminal and type python main.py

3 Play with it
Once the window opens click the Basic Sample or Complex Sample buttons to automatically fill in test data. Click Solve Problem and then try the Visualize Graph button to see the magic happen.

Sample Input and Output

If you input this
Regions A B C D
Colors Red Green Blue
Adjacencies Who touches who
A touches B
A touches C
B touches C
B touches D
C touches D

The Output will correctly be
A gets Red
B gets Green
C gets Blue
D gets Red

The computer figured out that A and D can share the color Red because they do not touch each other.
