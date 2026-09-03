import UniversalSingularity.Challenge

namespace UniversalSingularity

theorem NS_Q_lt_one_stable {X : Type} [NavierStokesDomain X] (x : X) (h : Q_NS x < 1) : NSStable x :=
  h

theorem NS_Q_gt_one_unstable {X : Type} [NavierStokesDomain X] (x : X) (h : Q_NS x > 1) : ¬NSStable x :=
  intro h_stable
  have h₂ : Q_NS x < 1 := h_stable
  linarith

theorem YM_Q_lt_one_stable {X : Type} [YangMillsDomain X] (x : X) (h : Q_YM x < 1) : YMStable x :=
  h

theorem YM_Q_gt_one_unstable {X : Type} [YangMillsDomain X] (x : X) (h : Q_YM x > 1) : ¬YMStable x :=
  intro h_stable
  have h₂ : Q_YM x < 1 := h_stable
  linarith

theorem BS_Q_lt_one_stable {X : Type} [BSDomain X] (x : X) (h : Q_BS x < 1) : BSStable x :=
  h

theorem BS_Q_gt_one_unstable {X : Type} [BSDomain X] (x : X) (h : Q_BS x > 1) : ¬BSStable x :=
  intro h_stable
  have h₂ : Q_BS x < 1 := h_stable
  linarith

-- Poincaré Conjecture
theorem POC_Q_lt_one_stable {X : Type} [PoincareDomain X] (x : X) (h : Q_P x < 1) : POCStable x :=
  h

theorem POC_Q_ge_one_unstable {X : Type} [PoincareDomain X] (x : X) (h : Q_P x ≥ 1) : ¬POCStable x :=
  intro h_stable
  have h₂ : Q_P x < 1 := h_stable
  linarith

-- P versus NP
theorem SAT_Q_lt_one_stable {X : Type} [PvsNPDomain X] (x : X) (h : Q_SAT x < 1) : SATStable x :=
  h

theorem SAT_Q_ge_one_unstable {X : Type} [PvsNPDomain X] (x : X) (h : Q_SAT x ≥ 1) : ¬SATStable x :=
  intro h_stable
  have h₂ : Q_SAT x < 1 := h_stable
  linarith

-- Hodge Conjecture
theorem HODGE_Q_lt_one_stable {X : Type} [HodgeDomain X] (x : X) (h : Q_H x < 1) : HODGEStable x :=
  h

theorem HODGE_Q_ge_one_unstable {X : Type} [HodgeDomain X] (x : X) (h : Q_H x ≥ 1) : ¬HODGEStable x :=
  intro h_stable
  have h₂ : Q_H x < 1 := h_stable
  linarith

-- Riemann Hypothesis
theorem RH_Q_lt_one_stable {X : Type} [RiemannDomain X] (x : X) (h : Q_RH x < 1) : RHStable x :=
  h

theorem RH_Q_ge_one_unstable {X : Type} [RiemannDomain X] (x : X) (h : Q_RH x ≥ 1) : ¬RHStable x :=
  intro h_stable
  have h₂ : Q_RH x < 1 := h_stable
  linarith

end UniversalSingularity