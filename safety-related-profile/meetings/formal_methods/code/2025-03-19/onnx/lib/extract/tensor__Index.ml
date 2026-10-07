type index = (int) list

let valid (idx: (int) list) (s: Tensor__Shape.shape) : bool =
  let rec inrange (ks: (int) list) (ds: (int) list) : bool =
    match (ks, ds) with
    | ([], []) -> true
    | (k :: ksr, d :: dsr) -> (0 <= k && k < d) && inrange ksr dsr
    | _ -> false in
  inrange idx s

