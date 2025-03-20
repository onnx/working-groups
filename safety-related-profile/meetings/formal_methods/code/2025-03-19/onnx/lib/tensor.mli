(** ONNX Tensor OCaml Interface *)

type 'a tensor

val dim : 'a tensor -> int
val shape : 'a tensor -> int list

val scalar : 'a -> 'a tensor
val vector : 'a list -> 'a tensor
val matrix : 'a list list -> 'a tensor

val pretty : (Format.formatter -> 'a -> unit) -> Format.formatter -> 'a tensor -> unit

val where : bool tensor -> 'a tensor -> 'a tensor -> 'a tensor
