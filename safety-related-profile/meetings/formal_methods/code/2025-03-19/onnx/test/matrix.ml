let pp_int fmt = Format.fprintf fmt "%2d"
let pp_matrix = Tensor.pretty pp_int

let a = Tensor.matrix [
  [ 1; 2; 3 ];
  [ 4; 5; 6 ];
]

let () = Format.printf " A = %a@." pp_matrix a
let () = Format.printf "tA = %a@." pp_matrix (Tensor.transpose a)
