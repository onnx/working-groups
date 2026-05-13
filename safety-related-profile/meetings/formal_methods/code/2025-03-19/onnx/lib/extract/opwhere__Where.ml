let where :
  type a. ((bool) Tensor__Tensor.tensor) -> (a Tensor__Tensor.tensor) ->
          (a Tensor__Tensor.tensor) ->  (a Tensor__Tensor.tensor) =
  fun cond a b -> { Tensor__Tensor.shape =
                    ((ignore ((ignore (b.Tensor__Tensor.shape) ; (a.Tensor__Tensor.shape))) ; 
                    (cond.Tensor__Tensor.shape))); Tensor__Tensor.value =
                    (fun (i: (int) list) ->
                       if ((cond.Tensor__Tensor.value) i)
                       then ((a.Tensor__Tensor.value) i)
                       else ((b.Tensor__Tensor.value) i)) }

