(* ONNX Tensor API *)

module S = Tensor__Shape
module I = Tensor__Index
module T = Tensor__Tensor

type 'a tensor = 'a T.tensor
let dim = T.dim
let shape t = t.T.shape

let scalar v =
  T.{
    shape = [] ;
    value = fun _ -> v ;
  }

exception Invalid_index = T.Invalid_index
let mem = T.mem
let get = T.get

let (.%[]) t k = get [k] t
let (.%[;..]) t ks = get (Array.to_list ks) t

let vector vs =
  let d = Array.of_list vs in
  let n = Array.length d in
  if n = 0 then invalid_arg "Tensor.vector" ;
  T.{
    shape = [ n ] ;
    value = (function [ k ] -> d.(k) | _ -> raise Invalid_index) ;
  }

let matrix vs =
  let d = Array.map Array.of_list @@ Array.of_list vs in
  let n = Array.length d in
  if n = 0 then invalid_arg "Tensor.matrix" ;
  let m = Array.length d.(0) in
  if m = 0 then invalid_arg "Tensor.matrix" ;
  if Array.exists (fun r -> Array.length r <> m) d then
    invalid_arg "Tensor.matrix" ;
  T.{
    shape = [ n ; m ] ;
    value = (function [ i ; j ] -> d.(i).(j) | _ -> raise Invalid_index) ;
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

let transpose (t : 'a tensor) =
  if dim t <> 2 then invalid_arg "Tensor.transpose" ;
  Opmatrix__Matrix.transpose t

let where = Opwhere__Where.where
