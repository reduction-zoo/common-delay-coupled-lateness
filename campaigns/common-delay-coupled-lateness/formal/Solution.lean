module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace CommonDelayCoupledLateness

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

def legalSource (x : List Nat) : Bool := x.all (fun w => w > 0)

def sourceWitness (x : List Nat) (subset : List Nat) : Bool :=
  decide subset.Nodup && subset.all (fun i => i < x.length) &&
  2 * (subset.map (fun i => x[i]?.getD 0)).sum == x.sum

def encodeSource := encodeList encodeNat

def validSourceOutput := searchOutput legalSource sourceWitness

def encodeInt (z : Int) := [decide (z < 0)] ++ encodeNat z.natAbs
structure Instance where
  p : Nat
  jobs : List (Nat × Int)
  deriving Repr
def legalTarget (x : Instance) : Bool := x.p > 0
def separated (a b : Nat × Nat) : Bool :=
  a.2 == 0 || b.2 == 0 || a.1 + a.2 ≤ b.1 || b.1 + b.2 ≤ a.1
def targetWitness (x : Instance) (start : List Nat) : Bool :=
  start.length == x.jobs.length &&
  (x.jobs.zip start).all (fun (j,s) => (s + 2*x.p + j.1 : Nat) ≤ j.2) &&
  let ops := (x.jobs.zip start).flatMap (fun (j,s) => [(s,x.p),(s+2*x.p,j.1)])
  (List.range ops.length).all (fun i => (List.range ops.length).all (fun j =>
    i == j || separated (ops[i]?.getD (0,0)) (ops[j]?.getD (0,0))))
def encodeTarget (x : Instance) := encodeNat x.p ++
  encodeList (fun j => encodeNat j.1 ++ encodeInt j.2) x.jobs
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : (List Nat) → Instance)
    (recover : (List Nat) × Option (List Nat) → Option (List Nat)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2)
    (encodeOption (encodeList encodeNat)) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList encodeNat)) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))

def Goal : Prop :=
  ∃ (forward : (List Nat) → Instance)
    (recover : (List Nat) × Option (List Nat) → Option (List Nat)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end CommonDelayCoupledLateness
