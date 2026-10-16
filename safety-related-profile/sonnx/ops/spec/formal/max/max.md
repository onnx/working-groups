The purpose of this file is to keep trace of some mathematical concepts usefull for future formal specification

#### Properties
From the mathematical definition of the maximum we have two properties:

The maximum corresponding shall be larger or equal than each of 

$\forall n \in [1, N], \forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... ~~~~ y_{i,j,k,l...} \geq z^n_{i,j,k,l...}$

$\forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... \exists n \in [1, N] ~~| ~~~~ y_{i,j,k,l...} = z^n_{i,j,k,l...}$

The same properties written in function of unboardcasted inputs are:

$\forall n \in [1, N], \forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... ~~~~ y_{i,j,k,l...} \geq x^n_{f(i,I_n,\max_{m \in [1, N] } I_m),f(j,J_n,\max_{m \in [1, N] } J_m),f(k,K_n,\max_{m \in [1, N] } K_m),f(l,L_n,\max_{m \in [1, N] } L_m)...}$

$\forall i \in [1, I], \forall j \in [1, J], \forall k \in [1, K], \forall l \in [1, L]... \exists n \in [1, N] ~~| ~~~~ y_{i,j,k,l...} = x^n_{f(i,I_n,\max_{m \in [1, N] } I_m),f(j,J_n,\max_{m \in [1, N] } J_m),f(k,K_n,\max_{m \in [1, N] } K_m),f(l,L_n,\max_{m \in [1, N] } L_m)...}$

