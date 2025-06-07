from ete3 import Tree, TreeStyle, NodeStyle, TextFace

def create_tree_style():
    """
    Create a custom TreeStyle
    """
    ts = TreeStyle()
    
    # Basic tree layout
    ts.show_leaf_name = False
    ts.show_branch_length = True
    ts.show_branch_support = False
    ts.show_scale = False
    
    # Layout customization
    ts.branch_vertical_margin = 0
    ts.scale = 0
    ts.margin_left = 10
    ts.margin_right = 10
    ts.margin_top = 10
    ts.margin_bottom = 10
    
    # custom layout function for branch length text
    def layout(node):
        if node.dist != 0:
            # add horizontal space by adjusting column position
            node.add_face(TextFace(f"{node.dist:.5f}" + "     ", fsize=2), column=0, position="branch-top")
    
    ts.layout_fn = layout
    ts.show_branch_length = False
    
    ts.rotation = 0
    
    return ts

def style_nodes(tree):
    """
    Apply custom styles to tree nodes
    """
    # Default node style
    nstyle = NodeStyle()
    nstyle["size"] = 0
    nstyle["vt_line_width"] = 1
    nstyle["hz_line_width"] = 1
    nstyle["vt_line_type"] = 0
    nstyle["hz_line_type"] = 0
    
    # Apply style to all nodes
    for n in tree.traverse():
        n.set_style(nstyle)
        
        # Add small font leaf names
        if n.is_leaf():
            n.add_face(TextFace(n.name, fsize=3), column=0)
        
        # Optional: Color nodes based on support values
        if hasattr(n, "support"):
            if n.support >= 90:
                n.set_style(NodeStyle({"size": 5, "fgcolor": "#2ecc71"}))
            elif n.support >= 70:
                n.set_style(NodeStyle({"size": 5, "fgcolor": "#f1c40f"}))
            elif n.support >= 50:
                n.set_style(NodeStyle({"size": 5, "fgcolor": "#e74c3c"}))

if __name__ == "__main__":
    # Load the tree file
    tree_path = "/Users/torben.sanders/Desktop/PhD/Corinna_project/phylo_tree/all_bacteria.nw"
    output_path = "/Users/torben.sanders/Desktop/PhD/Corinna_project/phylo_tree/all_bacteria.svg"
    
    try:
        tree = Tree(tree_path)
        
        # Apply styling
        ts = create_tree_style()
        style_nodes(tree)
        
        # Render the tree
        tree.render(output_path,
                   tree_style=ts,
                   w=80,  # Width in mm
                   h=80,  # Height in mm
                   units="mm",
                   dpi=100)
        
        print(f"Tree successfully rendered to {output_path}")
        
    except Exception as e:
        print(f"Error processing tree: {str(e)}")
