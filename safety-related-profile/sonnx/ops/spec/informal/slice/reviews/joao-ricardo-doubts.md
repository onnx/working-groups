# SONNX Slice Operator Review

This document reviews key design considerations and potential issues related to the **slice** operator definition in the SONNX profile, highlighting areas that require clarification or decision-making.

---

## 1. Axis arrangement

### Current Issue

One of the core SONNX restrictions prohibits default values. Consequently, the input tensor **A** (axes) must explicitly list **all axes** of the input tensor **X**.

### Comparison: ONNX vs SONNX

| Framework | Behavior | Example (X.shape = (8, 3, 6, 3, 2)) |
|-----------|----------|--------------------------------------|
| **ONNX** | Missing axes use default values | `A = [3, 0, 4]` |
| **SONNX** | All axes must be specified | `A = [3, 0, 4, 1, 2]` |

### Proposed Simplification

Since all axes must be represented, using an **ordered representation** would be both clearer and easier to define:

```
A = [0, 1, 2, 3, 4]  // Sequential axis ordering
```

**Benefits:**
- Eliminates ambiguity in axis ordering
- Simplifies operator definition and verification
- Reduces potential for indexing errors
- Based on this structure:
    - axis attribute wouldn't even be needed as an argument
    - t axis wouldn't be needed to represent

---

## 2. Negative Indexing Support

### Current Behavior

The operator supports negative indexing for `A`, `S`, and `E` parameters, with preprocessing to normalize values:

**For tensor X with:**
- **X.shape = (8, 3, 6, 3, 2)** 

- **$r = \text{rank}(X) = 5$**

- **Axes range:** $A[i] \in [-r, r-1] = [-5, 4]$

- **Start range:** $S[i] \in [-d_j, d_j - 1]$ where $d_j$ is the dimension of axis $j$

- **End range:** $S[i], E[i] \in [-d_j - 1, d_j]$ where $d_j$ is the dimension of axis $j$

### Mathematical Normalization

The normalization process converts negative indices to positive equivalents:
```math
\text{normalized\_index\_axis} = \begin{cases} 
\text{index} & \text{if } \text{index} \geq 0 \\
\text{index} + \text{rank} & \text{if } \text{index} < 0
\end{cases}
```
```math
\text{normalized\_index\_start/end} = \begin{cases} 
\text{index} & \text{if } \text{index} \geq 0 \\
\text{index} + \text{dimension of the respective index} & \text{if } \text{index} < 0
\end{cases}
```

### Open Questions

1. **Should SONNX prohibit negative indexing entirely?** 
   - Would simplify specification and verification

   - Reduces preprocessing complexity

   - More readable/understandable

---

## 3. Mixed Positive/Negative Indexing

### Potential Ambiguity

The current specification allows mixing positive and negative indices within the same operation. 
However, based on this approach, we must guarantee that no index has multiple representations.

**Example:**
```
X = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  // length = 10

A = [-2, -1, 0, 3]  // equivalent to A = [8, 9, 0, 3] after normalization
```

### Concerns

- **Readability:** Mixed indexing can be confusing

- **Verification complexity:** Requires additional normalization logic in formal specifications

- **Error proneness:** Higher chance of off-by-one errors

### Recommendation

Consider restricting to **either** all positive **or** all negative indexing within a single operation.

---

## 4. Output Dimension Constraints

### Why3 Tensor Invariant

The Löic tensor files in Why3 enforce the following invariant:

> **Positive Dimensions:** All tensors must have positive dimensions.

### Mathematical Constraint

$$\forall i \in [0, \text{rank}(Y)-1] : \text{dim}(Y_i) > 0$$

### Implications

This constraint would **prohibit** tensors with zero-dimensional axes:

- **Valid:** `Y.shape = (5, 2, 3, 1)` 

- **Invalid:** `Y.shape = (5, 2, 0, 1)`  

### Impact on Slice Operations

Zero-dimensional outputs can legitimately occur when:
- Empty slicing ranges: $\text{end} = \text{start}$ 

- Mathematical edge cases in dimension calculations

---

### Decision Required

**Question:** Should SONNX slice operations be required to guarantee non-zero output dimensions?

**Options:**
1. **Enforce positive dimensions:** Add preconditions to prevent zero-dimensional outputs

2. **Allow zero dimensions:** Modify Why3 tensor invariants to permit empty dimensions

---

## Summary of Open Doubts

- Ordered axis representation or Axis attribute remotion 

- Negative indexing support

- Mixed indexing restrictions 

- Zero-dimensional output handling

---

## Operator status

We have already made the informal spec, hypothesis tests and the formal spec (real tensors) made without any of this "additional" restrictions. 

We identified those and we want to know if any of these should be in fact considered restrictions. 

If so we will adjust our work accordingly.
