let pp_real fmt v = Format.fprintf fmt "%3.2f" v
let pp_bool fmt v = Format.fprintf fmt "%c" (if v then 'T' else 'F')

let c = Tensor.vector [true;true;false;true;false]
let a = Tensor.vector [1.0;2.0;3.0;4.0;5.0]
let b = Tensor.vector [0.1;0.2;0.3;0.4;0.5]
let w = Tensor.where c a b

let () =
  begin
    Format.printf "C: %a@." (Tensor.pretty pp_bool) c ;
    Format.printf "A: %a@." (Tensor.pretty pp_real) a ;
    Format.printf "B: %a@." (Tensor.pretty pp_real) b ;
    Format.printf "W: %a@." (Tensor.pretty pp_real) w ;
   end
