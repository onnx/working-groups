(** ONNX Tensor OCaml Interface *)

type 'a tensor

val dim : 'a tensor -> int
val shape : 'a tensor -> int list

val scalar : 'a -> 'a tensor
val vector : 'a list -> 'a tensor
val matrix : 'a list list -> 'a tensor

exception Invalid_index

val mem : int list -> 'a tensor -> bool
val get : int list -> 'a tensor -> 'a
val (.%[]) : 'a tensor -> int -> 'a
val (.%[;..]) : 'a tensor -> int array -> 'a

val pretty : (Format.formatter -> 'a -> unit) -> Format.formatter -> 'a tensor -> unit

val transpose : 'a tensor -> 'a tensor
val where : bool tensor -> 'a tensor -> 'a tensor -> 'a tensor
