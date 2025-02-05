# Preliminaries

This project is a prototype framework for extracting training data for machine-learning-based proof assistants. Specifically, it extracts maximally rich geometric data from constructive mathematical proofs written in Lean.

For additional context, refer to `main.pdf`.

## Getting Started

1. Clone this repository.
2. Initialize a Lean 4 project within the cloned repository and ensure Python is installed.
3. Modify your `lakefile` to include any required packages and Lean modules, ensuring they can be imported in `~/Foo/Test.lean`.

---

# Lean.foo

The module `Export.lean` was originally programmed by Mario Carneiro (see [Lean4Export](https://github.com/leanprover/lean4export) and [Lean3 Export Format](https://github.com/leanprover/lean3/blob/master/doc/export_format.md)).  

Minimal modifications were made to `Main.lean`, including an I/O operation at the end to write the output of Carneiro’s export process to a `.txt` file.

### How to Use

1. Write your Lean program (i.e., constructive mathematical theorem) in `~/Foo/Test.lean`, ensuring it compiles.
2. Alternatively, import all necessary Lean modules you'd like to export.
3. Execute the following command in a terminal within the same directory as `Main.lean`:

   ```sh
   lake exe foo Foo.Test -- <full name of your Lean program>
   ```

   This will export the fully elaborated Lean program to `Export.txt`.

4. To export all imported modules in `./Foo/Test.lean`, use:

   ```sh
   lake exe foo Foo.Test
   ```

This process allows exporting entire GitHub repositories, modules, etc.

---

# Python.main

This component processes Lean exports into structured data.

### How to Use

Once `Export.txt` has been generated using the `Lean.foo` process, run:

```sh
python main.py Export.txt
```

Upon successful execution, this Python script generates `graph.csv` in the same directory.

### Output Structure

- A set of declarations forming a directed acyclic graph (DAG).
- An edge `d → d'` exists if `d'` is referenced within `d`.
- Dependencies are labeled based on their position in the structure.

### Important Notes

1. **Computational Perspective**: The function computed by `main.py` is an **isomorphism**—it acts as an interpreter for Lean.
2. **Data Representation**: The exported data provides a compiler-invariant representation of fully elaborated Lean programs—constructive proofs of theorems. While the output format (`graph.csv`) represents labeled directed edges, alternative representations (e.g., sets of vertices and edges) can be derived using the functions in `base.py`.
3. **Machine Learning Relevance**: The exported data serves as the rawest form of positive training data for ML-based proof assistants.

---

# Visualization (Optional)

To visualize the exported digraph, use Cosmograph:

1. Upload `graph.csv` to [Cosmograph](https://cosmograph.app/run/).
2. The image `Nat.gcd_self.png` in this repo is an example visualization.

---

# Future Directions

A deeper understanding of the syntactic structure of each declaration will facilitate better insights into the exported digraph, enabling more effective transformations into training data.

This project leverages the **LeanDojo** ([LeanDojo GitHub](https://github.com/lean-dojo/LeanDojo)), **LeanCopilot** ([LeanCopilot GitHub](https://github.com/lean-dojo/LeanCopilot)), and **ReProver** ([ReProver GitHub](https://github.com/lean-dojo/ReProver)) frameworks.

The PDF `main.pdf` is a preprint of a paper I am writing on this project. Look there for specifics. 


## Summary

This framework provides an alternative approach to Lean data extraction by focusing on fully elaborated declarations and dependency structures. The extracted data can be directly utilized for machine learning applications, particularly in proof assistant research.