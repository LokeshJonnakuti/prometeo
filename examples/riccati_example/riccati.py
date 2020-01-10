from prometeo import *

sizes: dimv = [[2,2], [2,2], [2,2], [2,2], [2,2]]
nx: dims  = 2
nxu: dims = 4
nu: dims  = 2
N:  dims  = 5

def function1() -> None:
    # M: pmat = pmat(nxu, nxu)
    function2()
    return            
                        
def function2() -> None:
    function1()
    return

class qp_data:
    A: List = plist(pmat, sizes)
    B: List = plist(pmat, sizes)
    Q: List = plist(pmat, sizes)
    R: List = plist(pmat, sizes)
    P: List = plist(pmat, sizes)

    fact: List = plist(pmat, sizes)

    def factorize(self) -> None:
        M: pmat = pmat(nxu, nxu)
        Mu: pmat = pmat(nu, nu)
        Mxut: pmat = pmat(nu, nxu)
        Mxx: pmat = pmat(nx, nx)
        Mxu: pmat = pmat(nxu, nu)
        Lu: pmat = pmat(nu, nu)
        Q: pmat = pmat(nx, nx)
        R: pmat = pmat(nu, nu)
        BA: pmat = pmat(nx, nxu)
        BAtP: pmat = pmat(nxu, nx)
        pmat_copy(self.Q[N-1], self.P[N-1])

        for i in range(1, N):
            pmat_hcat(self.B[N-i], self.A[N-i], BA)
            pmt_gemm_tn(BA, self.P[N-i], BAtP, BAtP)

            pmat_copy(self.Q[N-i], Q)
            pmat_copy(self.R[N-i], R)
            M[0:nu,0:nu] = R
            M[nu:nu+nx,nu:nu+nx] = Q

            pmt_gemm_nn(BAtP, BA, M, M)
            Mu[0:nu, 0:nu] = M[0:nu, 0:nu]
            pmt_potrf(Mu, Lu)

            Mxut[0:nx, 0:nx] = M[0:nx, nu:nu+nx]
            Mxu[0:nx, 0:nu] = M[nu:nu+nx, 0:nu]

            pmt_potrsm(Lu, Mxut)
            pmt_gemm_nn(Mxu, Mxut, self.P[N-i-1], Mxx)
            pmt_gead(-1.0, self.P[N-i-1], Mxx)
            pmat_copy(Mxx, self.P[N-i-1])
            pmat_print(self.P[N-i-1])

        return

def main() -> int:
# def main() -> None:

    A: pmat = pmat(nx, nx)
    A[0,0] = 0.8
    A[0,1] = 0.1
    A[1,0] = 0.3
    A[1,1] = 0.8

    B: pmat = pmat(nx, nu)
    B[0,0] = 1.0  
    B[0,1] = 0.0
    B[1,0] = 0.0
    B[1,1] = 1.0

    Q: pmat = pmat(nx, nx)
    Q[0,0] = 1.0  
    Q[0,1] = 0.0
    Q[1,0] = 0.0
    Q[1,1] = 1.0

    R: pmat = pmat(nu, nu)
    R[0,0] = 1.0  
    R[0,1] = 0.0
    R[1,0] = 0.0
    R[1,1] = 1.0

    qp : qp_data = qp_data() 

    for i in range(N):
        qp.A[i] = A

    for i in range(N):
        qp.B[i] = B

    for i in range(N):
        qp.Q[i] = Q

    for i in range(N):
        qp.R[i] = R

    qp.factorize()
    
    return 0
