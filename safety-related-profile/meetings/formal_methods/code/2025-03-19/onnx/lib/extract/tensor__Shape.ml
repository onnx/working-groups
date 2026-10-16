type shape = (int) list

let rec product (ds: (int) list) : int =
  match ds with
  | [] -> 1
  | d :: ds1 -> d * product ds1

let sizeof (s: shape) : int = product s

