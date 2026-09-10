import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook 1 - Solving 1D Bar Finite Element Problems
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Imports
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



    Suppose a user has a 1D bar finite element problem they want to solve that has $n$ elements (for 1D problems, that necessarily means $n + 1$ nodes). Solving this problem through the finite element method requires that the following be defined:


    | Variable                          | Variable Name    | Description                                                                                                                                                |
    | --------------------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | Array of node coordinates         | `node_coords`    | An array where each array element is a coordinate tuple. The array index of each coordinate tuple corresponds with the numbering of a particular node.     |
    | Connectivity matrix               | `conn_matrix`    | A matrix where each column represents the nodes that make up a particular finite element. The number of columns is equal to the number of finite elements. |
    | Young's modulus array             | `E_array`        | An array where each array element                                                                                                                          |
    | Displacement boundary conditions  | `bc_dict`        | A dictionary containing known nodal displacements, where the key is the node number and the value is that node's displacement.                             |
    | Applied force boundary conditions | `f_applied_dict` | A dictionary containing known applied (i.e. external) nodal forces, where the key is the node number and the value is the node's applied force             |

    From *A First Course in the Finite Element Method* by Logan
    """)
    return


@app.cell
def _(np):
    conn_matrix = np.array([[0, 1], [1, 2]])
    ke = np.float64(21e9*4e-4/2)
    bc_dict = {
        0: 0,
        2: 25/1000 
    }
    f_applied_list = {
        1: -10000
    }
    return (conn_matrix,)


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
    return


if __name__ == "__main__":
    app.run()
