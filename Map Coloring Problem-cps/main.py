import tkinter as tk
from tkinter import messagebox, font
import time

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False


class MapColoringCSP:
    def __init__(self, variables, domains, neighbors):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.step_count = 0
        self.execution_log = []

    def is_consistent(self, variable, value, assignment):
        for neighbor in self.neighbors.get(variable, []):
            if neighbor in assignment and assignment[neighbor] == value:
                self.execution_log.append(f"Assign {variable} \u2192 {value} (Conflict with {neighbor})")
                return False
        return True

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]
        first = unassigned[0]

        for value in self.domains[first]:
            self.step_count += 1
            if self.is_consistent(first, value, assignment):
                self.execution_log.append(f"Assign {first} \u2192 {value} (Valid)")
                assignment[first] = value
                
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                    
                self.execution_log.append(f"Backtrack: Remove {value} from {first} (No colors worked)")
                del assignment[first]
                
        return None

class MapColoringGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Coloring Problem using CSP")
        self.root.geometry("650x800")
        self.root.configure(padx=20, pady=20)
        
        self.latest_csp = None
        self.latest_solution = None
        self.execution_time = 0
        
        custom_font = font.Font(family="Helvetica", size=11)
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        
        tk.Label(root, text="Map Coloring Solver (CSP)", font=title_font).pack(pady=(0, 10))
        
        if not VISUALIZATION_AVAILABLE:
            tk.Label(root, text="Install networkx and matplotlib to enable Graph Visualization.", fg="red").pack()
        
        tk.Label(root, text="Regions (comma-separated, e.g., A, B, C, D):", font=custom_font).pack(anchor="w")
        self.regions_var = tk.StringVar()
        tk.Entry(root, textvariable=self.regions_var, font=custom_font, width=70).pack(pady=(0, 10))
        
        tk.Label(root, text="Available Colors (comma-separated, e.g., Red, Green, Blue):", font=custom_font).pack(anchor="w")
        self.colors_var = tk.StringVar()
        tk.Entry(root, textvariable=self.colors_var, font=custom_font, width=70).pack(pady=(0, 10))
        
        tk.Label(root, text="Adjacencies (e.g., 'A: B, C' or 'A-B' per line):", font=custom_font).pack(anchor="w")
        self.adj_text = tk.Text(root, height=7, width=70, font=custom_font)
        self.adj_text.pack(pady=(0, 10))
        
        btn_frame1 = tk.Frame(root)
        btn_frame1.pack(pady=5)
        tk.Button(btn_frame1, text="Basic Sample", font=custom_font, command=self.load_example, bg="#e0e0e0").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame1, text="Complex Sample", font=custom_font, command=self.load_complex_example, bg="#e0e0e0").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame1, text="Clear", font=custom_font, command=self.clear_inputs, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame1, text="Solve Problem", font=custom_font, command=self.solve, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)

        self.btn_frame2 = tk.Frame(root)
        self.btn_frame2.pack(pady=5)
        self.btn_steps = tk.Button(self.btn_frame2, text="Show Steps", font=custom_font, command=self.show_steps, state=tk.DISABLED)
        self.btn_steps.pack(side=tk.LEFT, padx=5)
        self.btn_viz = tk.Button(self.btn_frame2, text="Visualize Graph", font=custom_font, command=self.visualize_graph, state=tk.DISABLED)
        self.btn_viz.pack(side=tk.LEFT, padx=5)
        
        self.perf_var = tk.StringVar()
        tk.Label(root, textvariable=self.perf_var, font=("Helvetica", 10, "italic"), fg="#555").pack(pady=5)
        
        tk.Label(root, text="Result:", font=custom_font).pack(anchor="w")
        self.result_text = tk.Text(root, height=10, width=70, font=custom_font, state=tk.DISABLED, bg="#f9f9f9")
        self.result_text.pack(pady=(0, 10))

    def load_example(self):
        self.clear_inputs()
        self.regions_var.set("A, B, C, D")
        self.colors_var.set("Red, Green, Blue")
        example_adj = "A: B, C\nB: A, C, D\nC: A, B, D\nD: B, C"
        self.adj_text.insert(tk.END, example_adj)

    def load_complex_example(self):
        self.clear_inputs()
        self.regions_var.set("WA, NT, SA, Q, NSW, V, T")
        self.colors_var.set("Red, Green, Blue")
        example_adj = "WA-NT\nWA-SA\nNT-SA\nNT-Q\nSA-Q\nSA-NSW\nSA-V\nQ-NSW\nNSW-V"
        self.adj_text.insert(tk.END, example_adj)

    def clear_inputs(self):
        self.regions_var.set("")
        self.colors_var.set("")
        self.adj_text.delete("1.0", tk.END)
        self.set_result("")
        self.perf_var.set("")
        self.latest_csp = None
        self.latest_solution = None
        self.btn_steps.config(state=tk.DISABLED)
        self.btn_viz.config(state=tk.DISABLED)

    def set_result(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)

    def solve(self):
        regions_str = self.regions_var.get().strip()
        colors_str = self.colors_var.get().strip()
        adj_str = self.adj_text.get("1.0", tk.END).strip()
        
        if not regions_str or not colors_str:
            messagebox.showerror("Input Error", "Regions and Colors cannot be empty!")
            return
            
        regions = [r.strip() for r in regions_str.split(',') if r.strip()]
        colors = [c.strip() for c in colors_str.split(',') if c.strip()]
        
        if len(regions) != len(set(regions)):
            messagebox.showerror("Input Error", "Duplicate regions detected! Ensure all regions are unique.")
            return
            
        domains = {r: colors[:] for r in regions}
        neighbors = {r: [] for r in regions}
        
        if adj_str:
            lines = adj_str.split('\n')
            for line in lines:
                line = line.strip()
                if not line: continue
                
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) != 2: continue
                    node, adj_nodes = parts
                    node = node.strip()
                    
                    if node not in neighbors:
                        messagebox.showwarning("Adjacency Warning", f"Region '{node}' is not in the Regions list. Ignoring.")
                        continue
                        
                    adj_list = [n.strip() for n in adj_nodes.split(',') if n.strip()]
                    for adj in adj_list:
                        if adj not in neighbors:
                            messagebox.showwarning("Adjacency Warning", f"Region '{adj}' is not in the Regions list. Ignoring.")
                            continue
                        if adj not in neighbors[node]: neighbors[node].append(adj)
                        if node not in neighbors[adj]: neighbors[adj].append(node)
                            
                elif '-' in line:
                    parts = line.split('-')
                    if len(parts) == 2:
                        u, v = parts[0].strip(), parts[1].strip()
                        if u not in neighbors or v not in neighbors:
                            messagebox.showwarning("Adjacency Warning", f"Regions '{u}' or '{v}' not in the Regions list. Ignoring.")
                            continue
                        if v not in neighbors[u]: neighbors[u].append(v)
                        if u not in neighbors[v]: neighbors[v].append(u)

        csp = MapColoringCSP(regions, domains, neighbors)
        self.latest_csp = csp
        
        start_time = time.time()
        solution = csp.backtrack({})
        end_time = time.time()
        self.execution_time = (end_time - start_time) * 1000
        
        self.latest_solution = solution
        
        self.perf_var.set(f"Performance: {csp.step_count} steps taken | Execution Time: {self.execution_time:.2f} ms")
        
        self.btn_steps.config(state=tk.NORMAL)
        if solution and VISUALIZATION_AVAILABLE:
            self.btn_viz.config(state=tk.NORMAL)
        else:
            self.btn_viz.config(state=tk.DISABLED)
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        if solution:
            self.result_text.insert(tk.END, "Solution Found:\n")
            for r in regions:
                color_val = solution[r]
                self.result_text.insert(tk.END, f"{r} \u2192 ")
                
                tag_name = f"color_{color_val}"
                try:
                    self.result_text.tag_config(tag_name, foreground=color_val.lower(), font=("Helvetica", 11, "bold"))
                    self.result_text.insert(tk.END, f"{color_val}\n", tag_name)
                except tk.TclError:
                    self.result_text.insert(tk.END, f"{color_val}\n")
        else:
            self.result_text.insert(tk.END, "Solution not possible with given colors. Please add more colors or reduce constraints.")
        self.result_text.config(state=tk.DISABLED)

    def show_steps(self):
        if not self.latest_csp: return
            
        steps_win = tk.Toplevel(self.root)
        steps_win.title("Backtracking Execution Steps")
        steps_win.geometry("450x550")
        
        tk.Label(steps_win, text="Step-by-Step Backtracking Log:", font=("Helvetica", 12, "bold")).pack(pady=5)
        
        frame = tk.Frame(steps_win)
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_area = tk.Text(frame, font=("Helvetica", 10), yscrollcommand=scrollbar.set)
        text_area.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.config(command=text_area.yview)
        
        log_text = "\n".join(self.latest_csp.execution_log)
        if not log_text:
            log_text = "No steps recorded."
            
        text_area.insert(tk.END, log_text)
        text_area.config(state=tk.DISABLED)

    def visualize_graph(self):
        if not VISUALIZATION_AVAILABLE:
            messagebox.showerror("Dependency Error", "Please install networkx and matplotlib: pip install networkx matplotlib")
            return
            
        if not self.latest_solution:
            return
            
        G = nx.Graph()
        G.add_nodes_from(self.latest_csp.variables)
        
        for node, adjacencies in self.latest_csp.neighbors.items():
            for neighbor in adjacencies:
                G.add_edge(node, neighbor)
                
        standard_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white', 'orange', 'purple', 'pink', 'brown', 'gray']
        
        color_map = []
        for node in G.nodes():
            color_name = self.latest_solution.get(node, "gray").lower()
            if color_name not in standard_colors:
                color_name = "lightblue"
            color_map.append(color_name)
            
        plt.figure(figsize=(7, 6))
        plt.title("Map Coloring Solution Visualization")
        
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color=color_map, 
                node_size=2500, font_color="white", font_weight="bold", 
                edge_color="gray", width=2)
                
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = MapColoringGUI(root)
    root.mainloop()
