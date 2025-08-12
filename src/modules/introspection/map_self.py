import os
import json
from datetime import datetime
from journal_entry.log_structure_read import log_structure_event

def map_self(root_dir="../../"):
    structure = {}
    for folder, subfolders, files in os.walk(root_dir):
        rel_folder = os.path.relpath(folder, root_dir)
        structure[rel_folder] = files
        depth = folder.replace(root_dir, '').count(os.sep)
        indent = '    ' * depth
        print(f"{indent}{os.path.basename(folder)}/")
        for f in files:
            print(f"{indent}    {f}")

    # Save structure to the tree's folder with a timestamped filename
    trees_dir = os.path.abspath(os.path.join(root_dir, "../tree's"))
    os.makedirs(trees_dir, exist_ok=True)
    tree_filename = f"structure_tree_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    tree_path = os.path.join(trees_dir, tree_filename)
    with open(tree_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "structure": structure
        }, f, indent=2)

    log_structure_event()  # Log only after successful reflection

if __name__ == "__main__":
    map_self()