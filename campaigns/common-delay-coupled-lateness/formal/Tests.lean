import Challenge
open CommonDelayCoupledLateness
example : targetWitness ⟨1, [(0,2)]⟩ [0] = true := by native_decide
example : targetWitness ⟨1, [(0,1)]⟩ [0] = false := by native_decide
example : targetWitness ⟨1, [(1,3),(1,3)]⟩ [0,0] = false := by native_decide
