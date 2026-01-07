# Reasoning Consistency Under Perturbation

This repository evaluates the **stability of LLM reasoning outcomes** under small, meaning-preserving
changes to the input (prompt perturbations). The goal is to measure whether a model’s **final answers**
remain consistent when the surface form of the prompt changes.


---

## What this repo measures

Given a base prompt, we generate multiple perturbed versions and query the model on each version.
We then compute:

- **Stability (majority)**: fraction of variants that match the most common answer
- **Stability (vs. key)**: fraction of variants that match the provided answer key (when available)
- **Accuracy over variants**: fraction of variants that are correct (best-effort evaluation)

---

## Perturbations included

- **Lexical**: small rewordings and punctuation shifts
- **Structural**: formatting changes and light instruction prefixing
- **Distractors**: irrelevant context added before/after the question


---



