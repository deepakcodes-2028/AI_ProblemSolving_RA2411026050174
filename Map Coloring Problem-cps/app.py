# cSpell:ignore figsize stcli
import streamlit as st
import time
import networkx as nx
import matplotlib.pyplot as plt

# --- CSP Solver Logic ---
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
                self.execution_log.append(f"Assign {variable} → {value} (Conflict with {neighbor})")
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
                self.execution_log.append(f"Assign {first} → {value} (Valid)")
                assignment[first] = value
                
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                    
                self.execution_log.append(f"Backtrack: Remove {value} from {first} (No colors worked)")
                del assignment[first]
                
        return None

# --- Streamlit App UI ---
st.set_page_config(page_title="Map Coloring Solver", layout="centered")

st.title("🗺️ Map Coloring Problem using CSP")
st.markdown("Solve the map coloring problem using **Constraint Satisfaction Problem (CSP)** with the **Backtracking Algorithm**.")

# Initialize session state for inputs
if 'regions_input' not in st.session_state:
    st.session_state.regions_input = ""
if 'colors_input' not in st.session_state:
    st.session_state.colors_input = ""
if 'adj_input' not in st.session_state:
    st.session_state.adj_input = ""

def load_basic_sample():
    st.session_state.regions_input = "A, B, C, D"
    st.session_state.colors_input = "Red, Green, Blue"
    st.session_state.adj_input = "A: B, C\nB: A, C, D\nC: A, B, D\nD: B, C"

def load_complex_sample():
    st.session_state.regions_input = "WA, NT, SA, Q, NSW, V, T"
    st.session_state.colors_input = "Red, Green, Blue"
    st.session_state.adj_input = "WA-NT\nWA-SA\nNT-SA\nNT-Q\nSA-Q\nSA-NSW\nSA-V\nQ-NSW\nNSW-V"

def clear_inputs():
    st.session_state.regions_input = ""
    st.session_state.colors_input = ""
    st.session_state.adj_input = ""

# Sample Buttons
st.write("### Load Sample Inputs")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("🟢 Load Basic Sample", on_click=load_basic_sample, use_container_width=True)
with col2:
    st.button("🔵 Load Complex Sample", on_click=load_complex_sample, use_container_width=True)
with col3:
    st.button("🔴 Clear Inputs", on_click=clear_inputs, use_container_width=True)

# Input Fields
st.write("### Problem Configuration")
regions_str = st.text_input("Regions (comma-separated, e.g., A, B, C, D):", key="regions_input")
colors_str = st.text_input("Available Colors (comma-separated, e.g., Red, Green, Blue):", key="colors_input")
adj_str = st.text_area("Adjacencies (e.g., 'A: B, C' or 'A-B' per line):", key="adj_input", height=150)

# Solve Button
if st.button("🚀 Solve Problem", type="primary", use_container_width=True):
    if not regions_str or not colors_str:
        st.error("Regions and Colors cannot be empty!")
    else:
        regions = [r.strip() for r in regions_str.split(',') if r.strip()]
        colors = [c.strip() for c in colors_str.split(',') if c.strip()]
        
        if len(regions) != len(set(regions)):
            st.error("Duplicate regions detected! Ensure all regions are unique.")
        else:
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
                            st.warning(f"Adjacency Warning: Region '{node}' is not in the Regions list. Ignoring.")
                            continue
                            
                        adj_list = [n.strip() for n in adj_nodes.split(',') if n.strip()]
                        for adj in adj_list:
                            if adj not in neighbors:
                                st.warning(f"Adjacency Warning: Region '{adj}' is not in the Regions list. Ignoring.")
                                continue
                            if adj not in neighbors[node]: neighbors[node].append(adj)
                            if node not in neighbors[adj]: neighbors[adj].append(node)
                                
                    elif '-' in line:
                        parts = line.split('-')
                        if len(parts) == 2:
                            u, v = parts[0].strip(), parts[1].strip()
                            if u not in neighbors or v not in neighbors:
                                st.warning(f"Adjacency Warning: Regions '{u}' or '{v}' not in the Regions list. Ignoring.")
                                continue
                            if v not in neighbors[u]: neighbors[u].append(v)
                            if u not in neighbors[v]: neighbors[v].append(u)

            csp = MapColoringCSP(regions, domains, neighbors)
            
            with st.spinner("Solving..."):
                start_time = time.time()
                solution = csp.backtrack({})
                end_time = time.time()
                execution_time = (end_time - start_time) * 1000
            
            st.divider()
            st.write("### Output")
            st.info(f"**Performance:** {csp.step_count} steps taken | **Execution Time:** {execution_time:.2f} ms")
            
            if solution:
                st.success("✅ Solution Found!")
                cols = st.columns(min(len(regions), 4)) # Display in columns
                for idx, r in enumerate(regions):
                    color_val = solution[r]
                    with cols[idx % min(len(regions), 4)]:
                        st.markdown(f"**{r}** → {color_val}")
                
                # Visualization
                st.write("### Graph Visualization")
                G = nx.Graph()
                G.add_nodes_from(csp.variables)
                
                for node, adjacencies in csp.neighbors.items():
                    for neighbor in adjacencies:
                        G.add_edge(node, neighbor)
                        
                standard_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white', 'orange', 'purple', 'pink', 'brown', 'gray']
                
                color_map = []
                for node in G.nodes():
                    color_name = solution.get(node, "gray").lower()
                    if color_name not in standard_colors:
                        color_name = "lightblue"
                    color_map.append(color_name)
                    
                fig, ax = plt.subplots(figsize=(7, 6))
                pos = nx.spring_layout(G, seed=42)
                nx.draw(G, pos, with_labels=True, node_color=color_map, 
                        node_size=2500, font_color="white", font_weight="bold", 
                        edge_color="gray", width=2, ax=ax)
                
                st.pyplot(fig)
                
                # Backtracking steps
                with st.expander("Show Backtracking Steps"):
                    for step in csp.execution_log:
                        st.text(step)
                        
            else:
                st.error("❌ Solution not possible with given colors. Please add more colors or reduce constraints.")

if __name__ == "__main__":
    import sys
    from streamlit.web import cli as stcli
    from streamlit import runtime
    if not runtime.exists():
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
