let where :
  type a. ((bool) Tensor__Tensor.tensor) -> (a Tensor__Tensor.tensor) ->
          (a Tensor__Tensor.tensor) ->  (a Tensor__Tensor.tensor) =
  fun cond a b -> { Tensor__Tensor.shape = cond.Tensor__Tensor.shape;
                    Tensor__Tensor.value =
                    (fun (i: (Z.t) list) ->
                       if Map__Map.mixfix_lbrb cond.Tensor__Tensor.value i
                       then Map__Map.mixfix_lbrb a.Tensor__Tensor.value i
                       else Map__Map.mixfix_lbrb b.Tensor__Tensor.value i) }

