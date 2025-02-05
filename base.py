"""
Table of contents, in order of weak dependence. 

    compute_identity
    parse_declaration
    compute_edge_list
"""

def compute_identity(command):
    """
    Computes the identity of a declaration command.
    
    Returns a tuple (group, unique_id, label) where:
       - group is one of "A", "B", "C", "D", "E", or "G"
       - unique_id is the integer identifier computed from the command
       - label is a string that incorporates additional information (if available)
    
    The label is constructed to include extra details from the command so that
    vertices in the output graph are more descriptively named.
    """
    parts = command.split()
    kind = next((part for part in parts if part.startswith("#")), None)
    if kind is None:
        raise ValueError("No valid kind marker found in the declaration command.")
    
    # Initialize extra information as empty.
    extra = ""
    
    if kind == "#NS":
        # About the meaning:
        # Group A (Hierarchical name, kind NS):
        #   Format: n' ⨆ #NS ⨆ n0 ⨆ s
        #   n' is the unique identifier for the name,
        #   n0 (slot "n0") is a unique integer for a Group A declaration,
        #   s is an extra string.
        group = "A"
        unique_id = int(parts[0])
        extra = parts[3] if len(parts) >= 4 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#NI":
        # About the meaning:
        # Group A (Hierarchical name, kind NI):
        #   Format: n' ⨆ #NI ⨆ n0 ⨆ z
        #   z is an integer providing additional info.
        group = "A"
        unique_id = int(parts[0])
        extra = parts[3] if len(parts) >= 4 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#US":
        # About the meaning:
        # Group B (Universe, kind US):
        #   Format: n' ⨆ #US ⨆ n0
        group = "B"
        unique_id = int(parts[0])
        label = f"{group}_{unique_id}"
    elif kind == "#UM":
        # About the meaning:
        # Group B (Universe, kind UM):
        #   Format: n' ⨆ #UM ⨆ n0 ⨆ n1
        group = "B"
        unique_id = int(parts[0])
        if len(parts) >= 4:
            label = f"{group}_{unique_id}_{parts[2]}_{parts[3]}"
        else:
            label = f"{group}_{unique_id}"
    elif kind == "#UIM":
        # About the meaning:
        # Group B (Universe, kind UIM):
        #   Format: n' ⨆ #UIM ⨆ n0 ⨆ n1
        group = "B"
        unique_id = int(parts[0])
        if len(parts) >= 4:
            label = f"{group}_{unique_id}_{parts[2]}_{parts[3]}"
        else:
            label = f"{group}_{unique_id}"
    elif kind == "#UP":
        # About the meaning:
        # Group B (Universe, kind UP):
        #   Format: n' ⨆ #UP ⨆ n0
        #   Note: The dependent is actually in Group A.
        group = "B"
        unique_id = int(parts[0])
        label = f"{group}_{unique_id}_{parts[2]}" if len(parts) >= 3 else f"{group}_{unique_id}"
    elif kind == "#EV":
        # About the meaning:
        # Group C (Expression, kind EV):
        #   Format: n' ⨆ #EV ⨆ z
        #   z is an integer providing extra info.
        group = "C"
        unique_id = int(parts[0])
        extra = parts[2] if len(parts) >= 3 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#ES":
        # About the meaning:
        # Group C (Expression, kind ES):
        #   Format: n' ⨆ #ES ⨆ n0,
        #   where n0 is from Group B.
        group = "C"
        unique_id = int(parts[0])
        label = f"{group}_{unique_id}_{parts[2]}" if len(parts) >= 3 else f"{group}_{unique_id}"
    elif kind == "#EC":
        # About the meaning:
        # Group C (Expression, kind EC):
        #   Format: n' ⨆ #EC ⨆ n0 ⨆ overline{n0}
        #   The first dependency (slot "n0") is from Group A;
        #   the remainder (if any) come from Group B.
        group = "C"
        unique_id = int(parts[0])
        extra = "_".join(parts[2:]) if len(parts) > 2 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#EA":
        # About the meaning:
        # Group C (Expression, kind EA):
        #   Format: n' ⨆ #EA ⨆ n0 ⨆ n1
        #   Both dependencies are in Group C.
        group = "C"
        unique_id = int(parts[0])
        extra = f"{parts[2]}_{parts[3]}" if len(parts) >= 4 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#EL":
        # About the meaning:
        # Group C (Expression, kind EL):
        #   Format: n' ⨆ #EL ⨆ s ⨆ n0 ⨆ n1 ⨆ n2
        #   s (slot "s") is extra info; dependency n0 is from Group A and n1,n2 from Group C.
        group = "C"
        unique_id = int(parts[0])
        extra = parts[2] if len(parts) >= 3 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#EP":
        # About the meaning:
        # Group C (Expression, kind EP):
        #   Format: n' ⨆ #EP ⨆ s ⨆ n0 ⨆ n1 ⨆ n2
        group = "C"
        unique_id = int(parts[0])
        extra = parts[2] if len(parts) >= 3 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#DEF":
        # About the meaning:
        # Group D (Definition, kind DEF):
        #   Format: #DEF ⨆ n' ⨆ n0 ⨆ n1 ⨆ overline{n0}
        group = "D"
        unique_id = int(parts[1])
        label = f"{group}_{unique_id}"
    elif kind == "#AX":
        # About the meaning:
        # Group D (Axiom, kind AX):
        #   Format: #AX ⨆ n' ⨆ n0 ⨆ overline{n0}
        group = "D"
        unique_id = int(parts[1])
        label = f"{group}_{unique_id}"
    elif kind == "#IND":
        # About the meaning:
        # Group E (Inductive definition, kind IND):
        #   Format: #IND ⨆ n0 ⨆ n' ⨆ n1 ⨆ n2 ⨆ overline{n0} ⨆ overline{n1}
        #   We choose n' (the third token) as the unique id for naming.
        group = "E"
        unique_id = int(parts[2])
        label = f"{group}_{unique_id}"
    elif kind == "#EJ":
        # About the meaning:
        # Group G (Format extension, kind EJ):
        #   Format: n' ⨆ #EJ ⨆ n0 ⨆ z ⨆ n1
        group = "G"
        unique_id = int(parts[0])
        extra = parts[3] if len(parts) >= 5 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#ELN":
        # About the meaning:
        # Group G (Format extension, kind ELN):
        #   Format: n' ⨆ #ELN ⨆ z
        group = "G"
        unique_id = int(parts[0])
        extra = parts[2] if len(parts) >= 3 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#ELS":
        # About the meaning:
        # Group G (Format extension, kind ELS):
        #   Format: n' ⨆ #ELS ⨆ overline{h}
        group = "G"
        unique_id = int(parts[0])
        extra = "_".join(parts[2:]) if len(parts) > 2 else ""
        label = f"{group}_{unique_id}_{extra}"
    elif kind == "#EZ":
        # About the meaning:
        # Group G (Format extension, kind EZ):
        #   Format: n' ⨆ #EZ ⨆ n0 ⨆ n1 ⨆ n2 ⨆ n3
        group = "G"
        unique_id = int(parts[0])
        label = f"{group}_{unique_id}"
    else:
        raise ValueError("Invalid kind marker for declaration command.")
    
    return (group, unique_id, label)


def parse_declaration(command, vertices_dict):
    """
    Parses a declaration command and returns a list of dependent vertices along with
    the dependency kind (i.e. which slot in the command produced the dependency).
    
    This function uses a precomputed dictionary (vertices_dict) that maps keys of the form
       (group, unique_id)
    to vertex tuples (group, unique_id, label).
    
    Returns:
        List of tuples (vertex, dependency_kind) corresponding to the dependents.
    """
    parts = command.split()
    kind = next((part for part in parts if part.startswith("#")), None)
    if kind is None:
        raise ValueError("No valid kind marker found in the declaration command.")
    
    dependents = []
    
    if kind in {"#NS", "#NI"}:
        # About the meaning:
        # Group A declaration.
        # Format: n' ⨆ #NS/NI ⨆ n0 ⨆ s/z.
        # Dependency: slot "n0" (parts[2]) from Group A.
        linked_id = int(parts[2])
        key = ("A", linked_id)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
            
    elif kind in {"#US", "#UM", "#UIM", "#UP"}:
        # About the meaning:
        # Group B declarations.
        # For #US: Format: n' ⨆ #US ⨆ n0  → dependency slot "n0" from Group B.
        # For #UM/#UIM: Format: n' ⨆ #UM/#UIM ⨆ n0 ⨆ n1  → dependencies "n0" and "n1" from Group B.
        # For #UP: Format: n' ⨆ #UP ⨆ n0  → dependency "n0" but lookup in Group A.
        for i, part in enumerate(parts[2:]):
            try:
                linked_id = int(part)
                slot = f"n{i}"
                group_lookup = "A" if kind == "#UP" else "B"
                key = (group_lookup, linked_id)
                if key in vertices_dict:
                    dependents.append((vertices_dict[key], slot))
            except ValueError:
                continue
            
    elif kind == "#EV":
        # About the meaning:
        # Group C (Expression, kind EV) has no hierarchical dependencies.
        pass
    
    elif kind == "#ES":
        # About the meaning:
        # Group C (Expression, kind ES): Format: n' ⨆ #ES ⨆ n0,
        # where n0 (slot "n0") comes from Group B.
        linked_id = int(parts[2])
        key = ("B", linked_id)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
            
    elif kind == "#EC":
        # About the meaning:
        # Group C (Expression, kind EC): Format: n' ⨆ #EC ⨆ n0 ⨆ overline{n0}.
        # The first dependency (slot "n0") is from Group A;
        # subsequent dependencies (slots "n1", "n2", …) are from Group B.
        linked_id = int(parts[2])
        key = ("A", linked_id)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
        for i, part in enumerate(parts[3:]):
            try:
                linked_id = int(part)
                slot = f"n{i+1}"
                key = ("B", linked_id)
                if key in vertices_dict:
                    dependents.append((vertices_dict[key], slot))
            except ValueError:
                continue
            
    elif kind == "#EA":
        # About the meaning:
        # Group C (Expression, kind EA): Format: n' ⨆ #EA ⨆ n0 ⨆ n1.
        # Dependencies: slot "n0" and slot "n1", both from Group C.
        linked_id1 = int(parts[2])
        key = ("C", linked_id1)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
        linked_id2 = int(parts[3])
        key = ("C", linked_id2)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n1"))
            
    elif kind in {"#EL", "#EP"}:
        # About the meaning:
        # Group C (Expression, kinds EL/EP): Format: n' ⨆ #EL/EP ⨆ s ⨆ n0 ⨆ n1 ⨆ n2.
        # Dependency: slot "n0" (parts[3]) from Group A; slots "n1" and "n2" (parts[4] and [5]) from Group C.
        linked_id0 = int(parts[3])
        key = ("A", linked_id0)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
        linked_id1 = int(parts[4])
        key = ("C", linked_id1)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n1"))
        linked_id2 = int(parts[5])
        key = ("C", linked_id2)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n2"))
            
    elif kind == "#DEF":
        # About the meaning:
        # Group D (Definition, kind DEF): Format: #DEF ⨆ n' ⨆ n0 ⨆ n1 ⨆ overline{n0}.
        # Dependencies: slot "n0" (parts[2]) and "n1" (parts[3]) from Group C;
        # remaining parts (slots "n2", …) from Group A.
        linked_id1 = int(parts[2])
        key = ("C", linked_id1)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
        linked_id2 = int(parts[3])
        key = ("C", linked_id2)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n1"))
        for i, part in enumerate(parts[4:]):
            try:
                linked_id = int(part)
                slot = f"n{i+2}"
                key = ("A", linked_id)
                if key in vertices_dict:
                    dependents.append((vertices_dict[key], slot))
            except ValueError:
                continue
            
    elif kind == "#AX":
        # About the meaning:
        # Group D (Axiom, kind AX): Format: #AX ⨆ n' ⨆ n0 ⨆ overline{n0}.
        # Dependency: slot "n0" (parts[2]) from Group C; remaining parts (slots "n1", …) from Group A.
        linked_id0 = int(parts[2])
        key = ("C", linked_id0)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
        for i, part in enumerate(parts[3:]):
            try:
                linked_id = int(part)
                slot = f"n{i+1}"
                key = ("A", linked_id)
                if key in vertices_dict:
                    dependents.append((vertices_dict[key], slot))
            except ValueError:
                continue
            
    elif kind == "#IND":
        # About the meaning:
        # Group E (Inductive definition, kind IND):
        # Format: #IND ⨆ n0 ⨆ n' ⨆ n1 ⨆ n2 ⨆ overline{n0} ⨆ overline{n1}.
        # Here n0 (number of parameters) and n2 (number of intro rules) are counts.
        # The dependency: slot "n1" (parts[3]) from Group C.
        # Then overline{n0} yields pairs: each pair gives one dependency from Group A and one from Group C.
        # Finally, overline{n1} yields dependencies from Group A.
        linked_id1 = int(parts[3])
        key = ("C", linked_id1)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n1"))
        num_pairs = int(parts[4])
        for i in range(5, 5 + 2 * num_pairs, 2):
            try:
                linked_id_a = int(parts[i])
                key = ("A", linked_id_a)
                pair_index = (i - 5) // 2
                if key in vertices_dict:
                    dependents.append((vertices_dict[key], f"pair{pair_index}_A"))
                linked_id_c = int(parts[i + 1])
                key = ("C", linked_id_c)
                if key in vertices_dict:
                    dependents.append((vertices_dict[key], f"pair{pair_index}_C"))
            except ValueError:
                continue
        start = 5 + 2 * num_pairs
        for j, part in enumerate(parts[start:]):
            try:
                linked_id = int(part)
                slot = f"n_overline{j}"
                key = ("A", linked_id)
                if key in vertices_dict:
                    dependents.append((vertices_dict[key], slot))
            except ValueError:
                continue
            
    elif kind == "#EJ":
        # About the meaning:
        # Group G (Format extension, kind EJ):
        # Format: n' ⨆ #EJ ⨆ n0 ⨆ z ⨆ n1.
        # Dependencies: slot "n0" (parts[2]) from Group A; slot "n1" (parts[4]) from Group C.
        linked_id0 = int(parts[2])
        key = ("A", linked_id0)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
        linked_id1 = int(parts[4])
        key = ("C", linked_id1)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n1"))
            
    elif kind == "#ELN":
        # About the meaning:
        # Group G (Format extension, kind ELN):
        # Format: n' ⨆ #ELN ⨆ z.
        # No hierarchical dependencies.
        pass
        
    elif kind == "#ELS":
        # About the meaning:
        # Group G (Format extension, kind ELS):
        # Format: n' ⨆ #ELS ⨆ overline{h}.
        # No hierarchical dependencies.
        pass
        
    elif kind == "#EZ":
        # About the meaning:
        # Group G (Format extension, kind EZ):
        # Format: n' ⨆ #EZ ⨆ n0 ⨆ n1 ⨆ n2 ⨆ n3.
        # Dependency: slot "n0" (parts[2]) from Group A; slots "n1", "n2", and "n3" (parts[3]-[5]) from Group C.
        linked_id0 = int(parts[2])
        key = ("A", linked_id0)
        if key in vertices_dict:
            dependents.append((vertices_dict[key], "n0"))
        for i in range(3, 6):
            try:
                linked_id = int(parts[i])
                slot = f"n{i-2}"  # i=3 -> "n1", i=4 -> "n2", i=5 -> "n3"
                key = ("C", linked_id)
                if key in vertices_dict:
                    dependents.append((vertices_dict[key], slot))
            except ValueError:
                continue
    return dependents


def compute_edge_list(command, vertices_dict):
    """
    Computes the edge list for a given declaration command.
    
    Each edge is a tuple (source, target, dependency_kind), where:
      - source is the vertex (group, unique_id, label) computed from the command,
      - target is the dependent vertex,
      - dependency_kind is the slot label captured during parsing.
    
    This uses efficient lookups via vertices_dict.
    """
    source = compute_identity(command)
    deps = parse_declaration(command, vertices_dict)
    edge_list = []
    for target, dep_kind in deps:
        edge_list.append((source, target, dep_kind))
    return edge_list
