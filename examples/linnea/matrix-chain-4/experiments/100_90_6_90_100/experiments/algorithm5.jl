using LinearAlgebra.BLAS
using LinearAlgebra

"""
    algorithm5(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2})

Compute
Y = (A B C D).

Requires at least Julia v1.0.

# Arguments
- `ml0::Array{Float64,2}`: Matrix A of size 90 x 100 with property FullRank.
- `ml1::Array{Float64,2}`: Matrix B of size 100 x 6 with property FullRank.
- `ml2::Array{Float64,2}`: Matrix C of size 6 x 90 with property FullRank.
- `ml3::Array{Float64,2}`: Matrix D of size 90 x 100 with property FullRank.
"""                    
function algorithm5(ml0::Array{Float64,2}, ml1::Array{Float64,2}, ml2::Array{Float64,2}, ml3::Array{Float64,2})
    # cost: 3.71e+06 FLOPs
    # A: ml0, full, B: ml1, full, C: ml2, full, D: ml3, full
    ml4 = Array{Float64}(undef, 100, 90)
    # tmp2 = (B C)
    stime0= time()
    gemm!('N', 'N', 1.0, ml1, ml2, 0.0, ml4)

    # A: ml0, full, D: ml3, full, tmp2: ml4, full
    ml5 = Array{Float64}(undef, 100, 100)
    # tmp5 = (tmp2 D)
    stime1= time()
    gemm!('N', 'N', 1.0, ml4, ml3, 0.0, ml5)

    # A: ml0, full, tmp5: ml5, full
    ml6 = Array{Float64}(undef, 90, 100)
    # tmp6 = (A tmp5)
    stime2= time()
    gemm!('N', 'N', 1.0, ml0, ml5, 0.0, ml6)

    # tmp6: ml6, full
    # Y = tmp6
    stime3= time()
    return (ml6) ,(stime0,stime1,stime2,stime3,)
end

function write_algorithm5_to_eventlog(io, id, stamps)
    write( io, string(id, ";", "gemm_1.08e+05;", "1.08e+05;", "tmp2 = (B C);", "gemm!('N', 'N', 1.0, ml1, ml2, 0.0, ml4);", string(stamps[1]), ";", string(stamps[2]), '
'  ))
    write( io, string(id, ";", "gemm_1.8e+06;", "1.8e+06;", "tmp5 = (tmp2 D);", "gemm!('N', 'N', 1.0, ml4, ml3, 0.0, ml5);", string(stamps[2]), ";", string(stamps[3]), '
'  ))
    write( io, string(id, ";", "gemm_1.8e+06;", "1.8e+06;", "tmp6 = (A tmp5);", "gemm!('N', 'N', 1.0, ml0, ml5, 0.0, ml6);", string(stamps[3]), ";", string(stamps[4]), '
'  ))
end