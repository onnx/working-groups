let swap (idx: (int) list) : (int) list =
  match idx with
  | i :: (j :: ([])) -> j :: i :: [] 
  | _ -> assert false (* absurd *)

let get : type a. (a Tensor__Tensor.tensor) -> (int) -> (int) ->  a =
  fun t i j -> t.Tensor__Tensor.value (i :: j :: [] )

let cols : type a. (a Tensor__Tensor.tensor) ->  (int) =
  fun a -> Sequence__Seq.mixfix_lbrb a.Tensor__Tensor.shape 0

let rows : type a. (a Tensor__Tensor.tensor) ->  (int) =
  fun a -> Sequence__Seq.mixfix_lbrb a.Tensor__Tensor.shape 1

let transpose :
  type a. (a Tensor__Tensor.tensor) ->  (a Tensor__Tensor.tensor) =
  fun a -> let value (idx: (int) list) : a =
             if Sequence__Seq.length idx = 2
             then a.Tensor__Tensor.value (swap idx)
             else a.Tensor__Tensor.value idx in
           { Tensor__Tensor.shape = swap a.Tensor__Tensor.shape;
             Tensor__Tensor.value = value }

