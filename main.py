import csv
import sys
import base

"""
This is the I/O module.
It reads a .txt file of declaration commands, builds a dictionary of vertices for fast lookup,
computes the directed edges among declarations (annotated with dependency kinds),
optionally filters out vertices (and related edges) that either lack additional information
or whose labels contain no letters,
and writes the resulting graph to a CSV file.
"""

def parse_declaration_commands(file_path):
    """
    Parses a .txt file where each line contains a declaration command.
    
    Parameters:
        file_path (str): The path to the .txt file containing declaration commands.
    
    Returns:
        list: A list of declaration command strings.
    """
    declaration_commands = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                command = line.strip()
                if command:
                    declaration_commands.append(command)
    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    return declaration_commands

def main():
    """
    Main function: reads the input file, precomputes a dictionary of vertices (with additional
    naming information), computes the edge list among declaration commands (including dependency kinds),
    optionally filters out vertices that either lack additional information or whose labels
    contain no letters (and edges involving them),
    and writes the output graph to a CSV file.
    
    In the CSV file the source and target of each edge are named solely by the vertex label.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <InputFilePath>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    declaration_commands = parse_declaration_commands(file_path)
    
    # Precompute vertices in a dictionary for efficient lookup.
    # Each vertex is computed from a declaration command via base.compute_identity.
    # The key is (group, unique_id) and the value is the vertex tuple (group, unique_id, label).
    vertices_dict = {}
    for command in declaration_commands:
        vertex = base.compute_identity(command)
        key = (vertex[0], vertex[1])
        vertices_dict[key] = vertex
    
    # Compute the edge list.
    edge_list = []
    for command in declaration_commands:
        edges = base.compute_edge_list(command, vertices_dict)
        for edge in edges:
            edge_list.append(edge)
    
    
    # Write the edge list to a CSV file.
    # The CSV will have three columns: source, target, and dependency_kind.
    # The source and target are output using only the vertex label.
    with open('graph.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['source', 'target', 'dependency_kind'])
        for edge in edge_list:
            source_label = edge[0][2]
            target_label = edge[1][2]
            dep_kind = edge[2]
            writer.writerow([source_label, target_label, dep_kind])
    
if __name__ == "__main__":
    main()
