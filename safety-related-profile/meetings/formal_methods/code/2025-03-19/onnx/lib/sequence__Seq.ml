type 'a seq = 'a list

let length : type a. (a list) ->  (int) = fun u -> ((List.length u))

let rec mixfix_lbrb : type a. (a list) -> (int) ->  a =
  fun u k -> match u with
    | x :: w -> if k = 0 then x else mixfix_lbrb w (k - 1)
    | _ -> assert false (* absurd *)

let rec equal :
  type a. (a -> (a -> (bool))) -> (a list) -> (a list) ->  (bool) =
  fun eq u v -> match (u, v) with
    | (x :: u', y :: v') -> eq x y && equal eq u' v'
    | ([], []) -> true
    | _ -> false

let empty : type a.  (a list) = [] 

let elt : type a. a ->  (a list) = fun e -> e :: [] 

let hd : type a. (a list) ->  a =
  fun s -> match s with
    | x :: _ -> x
    | _ -> assert false (* absurd *)

let tl : type a. (a list) ->  a = fun s -> mixfix_lbrb s (length s - 1)

let rec create : type a. a -> (int) ->  (a list) =
  fun e n -> if n > 0 then e :: create e (n - 1) else [] 

let reset : type a b. a -> (b list) ->  (a list) =
  fun e s -> create e (length s)

let rec init : type a. ((int) -> a) -> (int) -> (int) ->  (a list) =
  fun f a b -> if a < b then f a :: init f (a + 1) b else [] 

let rec map : type a b. (a -> b) -> (a list) ->  (b list) =
  fun f s -> match s with
    | [] -> [] 
    | x :: xs -> f x :: map f xs

let rec infix_plpl : type a. (a list) -> (a list) ->  (a list) =
  fun u v -> match u with
    | [] -> v
    | x :: w -> x :: infix_plpl w v

let rec mixfix_lbdtdtrb : type a. (a list) -> (int) -> (int) ->  (a list) =
  fun u i j -> match u with
    | [] -> [] 
    | x :: w ->
      if 0 < i
      then mixfix_lbdtdtrb w (i - 1) (j - 1)
      else begin if 0 < j then x :: mixfix_lbdtdtrb w 0 (j - 1) else []  end

let mixfix_lbdtdt_rb : type a. (a list) -> (int) ->  (a list) =
  fun u i -> mixfix_lbdtdtrb u 0 i

let mixfix_lb_dtdtrb : type a. (a list) -> (int) ->  (a list) =
  fun u i -> mixfix_lbdtdtrb u i (length u)

let infix_pldt : type a. (a list) -> a ->  (a list) =
  fun s e -> infix_plpl s (elt e)

let infix_dtpl : type a. a -> (a list) ->  (a list) =
  fun e s -> infix_plpl (elt e) s

let rec mixfix_lblsmnrb : type a. (a list) -> (int) -> a ->  (a list) =
  fun u i x -> match u with
    | x0 :: w -> if i = 0 then x :: w else x0 :: mixfix_lblsmnrb w (i - 1) x
    | _ -> assert false (* absurd *)

let memcpy :
  type a. (a list) -> (int) -> (a list) -> (int) -> (int) ->  (a list) =
  fun u i v j n -> infix_plpl (infix_plpl (mixfix_lbdtdt_rb u i)
                               (mixfix_lbdtdtrb v j (j + n)))
                   (mixfix_lb_dtdtrb u (i + n))

