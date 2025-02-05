import Lean

import Foo.Export

open Lean

def main (args : List String) : IO Unit := do
  -- Initialize the Lean environment
  initSearchPath (← findSysroot)

  -- Process arguments
  let (imports, constants) := args.span (· != "--")
  let imports := imports.toArray.map fun mod => { module := Syntax.decodeNameLit ("`" ++ mod) |>.get! }
  let env ← importModules imports {}
  let constants := match constants.tail? with
    | some cs => cs.map fun c => Syntax.decodeNameLit ("`" ++ c) |>.get!
    | none    => env.constants.toList.map Prod.fst |>.filter (!·.isInternal)

  -- Open the output file and redirect stdout
  let filePath := "Export.txt"
  IO.FS.withFile filePath IO.FS.Mode.write fun handle => do
    let stream := IO.FS.Stream.ofHandle handle
    IO.withStdout stream do
      -- Run the M monad to process constants
      let _ ← M.run env do
        for c in constants do
          let _ ← dumpConstant c
  return ()
