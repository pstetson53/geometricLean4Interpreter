# Nat.gcd_self 

This proof takes approximately 12,000 declarations to state.

Representative code: https://github.com/leanprover/lean4/blob/baa4b68a71926a722b77d4ec2cba34bfc76cc5aa/src/Init/Data/Nat/Gcd.lean#L38-L39

With the code in *~/Foo/Test.lean* reading only "import Init.Data.Nat.Div" the command 

    user@pc %   lake exe foo Foo.Test -- Nat.gcd_self

will yield the file *Nat.gcd_self.txt* (renamed as *Export.txt*). 

The resulting *graph.csv* from the Python.main function is *Nat.gcd_self.csv*.