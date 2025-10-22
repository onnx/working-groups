# `max` operator
### Contents
- `Maximum` operator for any type on which an order is defined.
## `Max`  `(type on which an order is defined)`

### Signature
`Y = max(X_1, ... , X_N)`
where

- `N`: 
- `X_1`: first input tensor
- ...
- `X_N`: last input tensor
- `Y`: output tensor

#### Restrictions
The following restrictions apply to the `max` operator for the SONNX profile:

| Restriction    | Statement | Origin |
| -------- | ------- | ------- |
| `R1` | `N` is an integer between 1 and 2147483647 | Transient |
| `R2` | Numpy boardcasting rules shall be applicable to `Y`, `X_1`, ... , `X_N` | https://numpy.org/doc/stable/user/basics.broadcasting.html |

 #### Informal specification

The result tensor `Y` is based on the boardcasted values of the input tensors `X_1^B`, ... , `X_N^B`.
