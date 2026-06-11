# CAPRI — TODO

## 1. Remove Old Imperfections

- [ ] Fix issues related to party/night mode and similar legacy edge cases.

## 2. Alternative Algorithms for the Main Pipeline

### General Replacements

- [ ] Replace MST + 2-opt with the **Christofides algorithm**.
- [ ] Replace constrained k-means with **multi-day VRP**.

### Detailed Requirements & Proposals

- [ ] Add algorithm selection options to the **clickable menu** in the UI.
- [ ] **Day grouping** (currently *constrained k-means*): Evaluate DBSCAN / HDBSCAN or *hierarchical clustering* as alternatives.
- [ ] **Dynamic time windows** — implement as an option suitable for night-owl users.

### Summary — Key Alternatives to Implement
>
> Christofides · Multi-day VRP · Metaheuristics (GA / ACO)

## 3. Feature Extensions

- [ ] **Travel modes**: implement Night / Luxury / Budget modes.
- [ ] **Intelligent Time Configuration (Dynamic Scheduling)**: implement "Owl" mode (late riser) and "Lark" mode (early bird).
- [ ] **Anti-Repetition Mechanism** (intra-day diversity): introduce a *Diversity Constraint* parameter in algorithms (e.g. max 2 POIs of the same sub-category per day) — the current system can suggest 5 parks or 3 casinos in a single day.
- [ ] **"Human Touch" Calibration**: develop objective-function weights that let the user choose what matters more — shortest route (math) vs. attractiveness/atmosphere (*human touch*).
- [ ] **"City Identity" (Must-Have vs. Profile)**: implement a *City Landmark Score* parameter that forces the inclusion of key landmarks in the plan (e.g. the Eiffel Tower).
- [ ] **Metrics**: implement tracking and calculation of various quality metrics — **METRICS ARE IMPORTANT**.

## 4. LLM as Planner

- [ ] Implement LLM-based planning as discussed (verbal agreements — details to be formalised).
