# 🔷 Model-Based Diagnosis with Conflict Sets & Minimal Hitting Sets

This project investigates model-based diagnosis using Reiter-style reasoning.  
We implement a **Hitting Set Tree (HS-Tree)** that enumerates all **subset-minimal diagnoses** from a set of minimal conflict sets.

The goal is to evaluate diagnostic completeness and search efficiency across circuits, and compare branching heuristics for systematic diagnosis.

---

## 🧠 Key Concepts

| Concept | Description |
|---|---|
| Conflict Set | A set of components that cannot all be healthy simultaneously |
| Diagnosis | A minimal set of faulty components explaining observations |
| Hitting Set Tree | A tree search that generates minimal diagnoses using systematic branching |
| Reiter's Algorithm | Classical model-based AI framework for diagnosis |

---

## 🛠 Implementation Features

- Constructing minimal **conflict sets** from circuit descriptions  
- Generating **minimal hitting sets** using **HS-Tree search**
- Two branching heuristics implemented & compared:
  - **Smallest-Conflict-First**
  - **Most-Frequent-Element**
- Enumeration of all minimal diagnoses
- Search metrics for evaluation

---

## 🧪 Experimental Setup & Findings

- Benchmarked on **seven digital circuits**
- Both heuristics produced **identical diagnosis sets → correctness satisfied**
- Efficiency measured via:
  - **Expanded search nodes**
  - **Wall-clock runtime**
- Effort patterns show room for:
  - Larger benchmarks
  - **Cost-based ranking**
  - Hybrid heuristic strategies

> Results confirm completeness, minimality, and predictable search behaviour across circuits.

---

