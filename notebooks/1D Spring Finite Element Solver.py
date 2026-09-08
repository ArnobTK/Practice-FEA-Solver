import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1D Spring Finite Element Solver
    """)
    return


@app.cell
def _():
    import numpy as np
    from numpy.typing import NDArray

    return NDArray, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Problem Definition

    Suppose a user has a 1D finite element spring problem with $n$ nodes (for 1D problems, that means $n + 1$ elements).
    - `conn_matrix`: A

    From *A First Course in the Finite Element Method* by Logan
    """)
    return


@app.cell
def _(np):
    conn_matrix = np.array([[0, 2, 3], [2, 3, 1]])
    ke_list = np.array([1000, 2000, 3000])
    bc_dict = [(0, 0), (1, 0)]
    f_applied_list = [(3, 5000)]

    return conn_matrix, ke_list


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Solve Problem
    """)
    return


@app.cell
def _(NDArray, np):
    def local_stiffness_matrix_spring_1d(ke: float) -> NDArray:
        return ke * np.array([[1, -1], [-1, 1]])

    return (local_stiffness_matrix_spring_1d,)


@app.cell
def _(NDArray, local_stiffness_matrix_spring_1d, np):
    def assemble_global_stiffness_matrix_1d(ke_list: NDArray, conn_matrix: NDArray) -> NDArray: #TODO: Make a function that generalizes to any number of dimensions
        num_elems = len(ke_list)
        num_nodes = len(ke_list) + 1 
        K = np.zeros((num_nodes, num_nodes))

        # Main assembly loop
        for i in range(num_elems):
            j = conn_matrix[:, i][0]
            m = conn_matrix[:, i][1]
            K[[j, j, m, m], [j, m, j, m]] = (
                K[[j, j, m, m], [j, m, j, m]] + local_stiffness_matrix_spring_1d(ke_list[i]).ravel()
            )

        return K

    return (assemble_global_stiffness_matrix_1d,)


@app.cell
def _(NDArray, np):
    def apply_boundary_conditions_1d(K: NDArray, bc: list[tuple[int, int]], f_applied: list[tuple[int, int]]) -> tuple[NDArray, NDArray]:
        F = np.zeros((K.shape[0], 1))

        # Apply applied forces to global nodal force vector
        for i, f in f_applied:
            F[i] = f

        # For nonhomogenous boundary conditions
        for i, d in bc:
            if not np.isclose(d, 0): #TODO: Implement with Example 2.2
                pass            

        # for homogenous boundary conditions
        deletion_indices = [i for i, _ in bc]
        K = np.delete(K, deletion_indices, 0)
        K = np.delete(K, deletion_indices, 1)
        F = np.delete(F, deletion_indices, 0)
        return K, F

    return


@app.cell
def _(NDArray, np):
    def solve_problem(K: NDArray, F: NDArray):
        bc_indices = [0, 0] # TODO: Order bc such that np.insert() works properly with it
        bc_values = [0, 0]
        d = np.linalg.solve(K, F)
        d = np.array([np.insert(d, bc_indices, bc_values)]).T


    return


@app.cell
def _(assemble_global_stiffness_matrix_1d, conn_matrix, ke_list):
    K = assemble_global_stiffness_matrix_1d(ke_list=ke_list, conn_matrix=conn_matrix)

    return (K,)


@app.cell
def _(K, np):
    test = np.arange(100).reshape((10, 10))
    with np.printoptions(linewidth=100):
        print("\n", K)
    return


if __name__ == "__main__":
    app.run()
