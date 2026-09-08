import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import numpy as np


    def stiffness_matrix_spring_1d(k: float):
        return k * np.asarray([[1, -1], [-1, 1]])

    return np, stiffness_matrix_spring_1d


@app.cell
def _(np):
    conn = np.array([[0, 1, 2, 3], [1, 2, 3, 4]])
    conn
    return (conn,)


@app.cell
def _():
    k = 200
    return (k,)


@app.cell
def _(conn, k, np, stiffness_matrix_spring_1d):
    K = np.zeros((5, 5))

    for i in range(4):
        j = conn[:, i][0]
        m = conn[:, i][1]
        K[[j, j, m, m], [j, m, j, m]] = (
            K[[j, j, m, m], [j, m, j, m]] + stiffness_matrix_spring_1d(k).ravel()
        )

    K
    return (K,)


@app.cell
def _(K, np):
    F = np.array([[0], [0], [0]])
    F = F - K[1:4][:, [4]] * 0.02
    F
    return (F,)


@app.cell
def _(F, K, np):
    d = np.vstack((0, np.linalg.solve(K[1:4][:, 1:4], F), 0.02))
    return (d,)


@app.cell
def _(d):
    d
    return


if __name__ == "__main__":
    app.run()
