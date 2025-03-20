type index = (int) list

type 'a tensor = {
  shape: Tensor__Shape.shape;
  value: (int) list -> 'a;
  }

let dim : type a. (a tensor) ->  (int) =
  fun t -> Sequence__Seq.length t.shape

