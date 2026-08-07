# Converting Why3 Specifications to C Code

This document outlines how to extract C code from Why3 (`.mlw`) specifications using the Why3 extraction mechanism and a C driver. It includes an example, supported features, and key constraints.

## Compiling Why3 to C language
### Example

This example defines a function `locate_max` that returns the index of the maximum element in an array `a` of size `n`.

```whyml
use int.Int
use map.Map as Map
use mach.c.C
use mach.int.Int32
use mach.int.Int64

function ([]) (a: ptr 'a) (i: int): 'a = Map.get a.data.Array.elts (a.offset + i)

let locate_max (a: ptr int64) (n: int32): int32
  requires { 0 < n }
  requires { valid a n }
  ensures  { 0 <= result < n }
  ensures  { forall i. 0 <= i < n -> a[i] <= a[result] }
= let ref idx = 0 in
  for j = 1 to n - 1 do
    invariant { 0 <= idx < n }
    invariant { forall i. 0 <= i < j -> a[i] <= a[idx] }
    if get_ofs a idx < get_ofs a j then idx <- j
  done;
  idx
  ```

### Extraction Command
```bash
why3 extract -D c locate_max.mlw
```
With debug details:
```bash
why3 extract -D c --debug-all locate_max.mlw -o locate_max.c
```
### Output C code
```c
#include <stdint.h>

int32_t locate_max(int64_t * a, int32_t n) {
  int32_t idx;
  int32_t j, o;
  idx = 0;
  o = n - 1;
  if (1 <= o) {
    for (j = 1; ; ++j) {
      if (a[idx] < a[j]) {
        idx = j;
      }
      if (j == o) break;
    }
  }
  return idx;
}
```

## Supporte Features and Rules
### Basic Types

| WhyML Type           | Description                        | C Equivalent           |
|----------------------|------------------------------------|------------------------|
| `int32`, `uint64`, etc. | From `mach.int`                  | `int32_t`, `uint64_t`, etc. |
| `bool`               | Translated from `bool.Bool`        | `int`                  |
| `char`, `string`     | Partial support via `mach.c.String`| `char`, `char *`       |
| `int` (mathematical) | ❌ Not supported                   | —                      |
| `float`              | ❌ Not supported                   | —                      |
---

### Compound Types
#### Immutable Records

**WhyML:**
```whyml
type r = { x : int32; y : int32 }
let swap (a : r) : r = { x = a.y ; y = a.x }
```
**C:**
```c
struct r {
  int32_t x;
  int32_t y;
};

struct r swap(struct r a) {
  struct r r;
  r.x = a.y;
  r.y = a.x;
  return r;
}
```

#### Mutable Records
**WhyML:**
```whyml
type r = { mutable x : int32; mutable y : int32 }
let swap (a : r) : unit =
   let tmp = a.y in a.y <- a.x; a.x <- tmp
```
**C:**
```c
struct r {
  int32_t x;
  int32_t y;
};

void swap(struct r * a) {
  int32_t tmp;
  tmp = a->y;
  a->y = a->x;
  a->x = tmp;
}
```
## Unsupported Features
- WhyML arrays

- Algebraic data types (including enumerations)

- Pattern matching

- Exception raising and catching

- Floating-point types

## Control Stuctures

| Feature                    | Support |
|----------------------------|---------|
| `if` / `else`              | ✅       |
| `while` loops              | ✅       |
| `for` loops                | ✅       |
| Sequence (`;`)             | ✅       |
| `break`, `continue`, `return` | ✅    |
| Pattern matching           | ❌       |
| Exceptions                 | ❌       |

## Notes
- **Example of driver file used for C extraction**: [`c.drv`](https://gitlab.inria.fr/why3/why3/-/blob/master/drivers/c.drv)
- This driver defines how WhyML types and functions are translated into equivalent C constructs.

## References

- [Why3 Documentation](https://why3.lri.fr/doc/)
- [Why3 GitLab Repository](https://gitlab.inria.fr/why3/why3)




