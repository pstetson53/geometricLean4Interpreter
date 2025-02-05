import Lake
open Lake DSL

package foo where
  version := v!"0.1.0"

lean_lib Foo where
  -- Ensure the Export module is included
  roots := #[`Foo.Export, `Foo.Test, `Foo.LeanDojo]

@[default_target]
lean_exe foo where
  root := `Main

require mathlib from git "https://github.com/leanprover-community/mathlib4.git"

--@ "8f68ff90bd32731c9297588d885fcfab67cee14a"
