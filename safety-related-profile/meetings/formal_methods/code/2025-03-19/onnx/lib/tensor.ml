(* ONNX Tensor API *)

module S = Tensor__Shape
module T = Tensor__Tensor

type 'a tensor = 'a T.tensor
let dim = T.dim
let shape t = t.T.shape

let scalar v =
  T.{
    shape = [] ;
    value = fun _ -> v ;
  }

exception Invalid_index

let vector vs =
  let m = Array.of_list vs in
  T.{
    shape = [ Array.length m ] ;
    value = (function [ k ] -> m.(k) | _ -> raise Invalid_index) ;
  }

let matrix vs =
  let m = Array.map Array.of_list @@ Array.of_list vs in
  T.{
    shape = [ Array.length m ; Array.length m.(0) ] ;
    value = (function [ i ; j ] -> m.(i).(j) | _ -> raise Invalid_index) ;
  }

let pretty pp fmt (t : 'a tensor) =
  match t.shape with
  | [] -> pp fmt @@ t.value []
  | [n] ->
      begin
        Format.fprintf fmt "[" ;
        for i = 0 to n-1 do
          Format.fprintf fmt " %a" pp @@ t.value [i]
        done ;
        Format.fprintf fmt " ]" ;
      end
  | [n;m] ->
      begin
        Format.fprintf fmt "@[<hv 0>" ;
        for i = 0 to n-1 do
          Format.fprintf fmt "[" ;
          for j = 0 to m-1 do
            Format.fprintf fmt " %a" pp @@ t.value [i;j]
          done ;
          Format.fprintf fmt " ]@," ;
        done ;
        Format.fprintf fmt "@]" ;
      end
  | _ -> invalid_arg "Tensor.pretty"

let where = Opwhere__Where.where
