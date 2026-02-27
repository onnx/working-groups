type 'a tensor = {
  shape: Tensor__Shape.shape;
  value: (int) list -> 'a;
  }

let dim : type a. (a tensor) ->  (int) =
  fun t -> Sequence__Seq.length t.shape

exception Invalid_index

let mem : type a. ((int) list) -> (a tensor) ->  (bool) =
  fun idx t -> Tensor__Index.valid idx t.shape

let get : type a. ((int) list) -> (a tensor) ->  a =
  fun idx t -> if Tensor__Index.valid idx t.shape
               then t.value idx
               else raise Invalid_index

