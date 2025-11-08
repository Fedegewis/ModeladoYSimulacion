import numpy as np
from scipy.linalg import eig

# Definir todos los sistemas
sistemas = {
    1: {'eq': 'ẋ = x, ẏ = y', 'A': np.array([[1, 0], [0, 1]])},
    2: {'eq': 'ẋ = -y, ẏ = x', 'A': np.array([[0, -1], [1, 0]])},
    3: {'eq': 'ẋ = x, ẏ = -y', 'A': np.array([[1, 0], [0, -1]])},
    4: {'eq': 'ẋ = y - x, ẏ = -y - x', 'A': np.array([[-1, 1], [-1, -1]])},
    5: {'eq': 'ẋ = x + y, ẏ = x + y', 'A': np.array([[1, 1], [1, 1]])},
    6: {'eq': 'ẋ = -y, ẏ = x', 'A': np.array([[0, -1], [1, 0]])},
    7: {'eq': 'ẋ = 2y, ẏ = 2x', 'A': np.array([[0, 2], [2, 0]])},
    8: {'eq': 'ẋ = -y + x, ẏ = x + y', 'A': np.array([[1, -1], [1, 1]])},
    9: {'eq': 'ẋ = x - 2y, ẏ = -2x + y', 'A': np.array([[1, -2], [-2, 1]])},
    10: {'eq': 'ẋ = x + 2y, ẏ = 4x + 3y', 'A': np.array([[1, 2], [4, 3]])},
    11: {'eq': 'ẋ = x - 2y, ẏ = x + y', 'A': np.array([[1, -2], [1, 1]])},
    12: {'eq': 'ẋ = x - y, ẏ = 3x + 3y', 'A': np.array([[1, -1], [3, 3]])},
    13: {'eq': 'ẋ = -4x + 3y, ẏ = -6x + 5y', 'A': np.array([[-4, 3], [-6, 5]])},
    14: {'eq': 'ẋ = 6x - y, ẏ = 5x + 4y', 'A': np.array([[6, -1], [5, 4]])},
    15: {'eq': 'ẋ = x + 2y, ẏ = 2x - 4y', 'A': np.array([[1, 2], [2, -4]])},
    16: {'eq': 'ẋ = 2x - 5y, ẏ = 4x - 2y', 'A': np.array([[2, -5], [4, -2]])},
    17: {'eq': 'ẋ = -5x + 2y, ẏ = -10x + 3y', 'A': np.array([[-5, 2], [-10, 3]])},
    18: {'eq': 'ẋ = -2x + 3y, ẏ = -6x + 4y', 'A': np.array([[-2, 3], [-6, 4]])},
    19: {'eq': 'ẋ = 5x - 4y, ẏ = x + y', 'A': np.array([[5, -4], [1, 1]])},
    20: {'eq': 'ẋ = 3x + y, ẏ = x + 3y', 'A': np.array([[3, 1], [1, 3]])},
    21: {'eq': 'ẋ = y, ẏ = 6x + y', 'A': np.array([[0, 1], [6, 1]])},
    22: {'eq': 'ẋ = 2x - 2y, ẏ = 4x - 2y', 'A': np.array([[2, -2], [4, -2]])},
    23: {'eq': 'ẋ = x + 2y, ẏ = 2x + y', 'A': np.array([[1, 2], [2, 1]])},
    24: {'eq': 'ẋ = 2x + 3y, ẏ = 2x + y', 'A': np.array([[2, 3], [2, 1]])},
    25: {'eq': 'ẋ = -3x - 4y, ẏ = 2x + y', 'A': np.array([[-3, -4], [2, 1]])},
    26: {'eq': 'ẋ = 3x - y, ẏ = 9x - 3y', 'A': np.array([[3, -1], [9, -3]])},
    27: {'eq': 'ẋ = -2x + y, ẏ = x - 2y', 'A': np.array([[-2, 1], [1, -2]])},
    28: {'eq': 'ẋ = x + 3y, ẏ = x - y', 'A': np.array([[1, 3], [1, -1]])},
}

def clasificar_equilibrio(eigenvalues):
    """Clasificar el punto de equilibrio según los autovalores"""
    lambda1, lambda2 = eigenvalues
    
    if np.iscomplex(lambda1) or np.iscomplex(lambda2):
        parte_real = np.real(lambda1)
        if abs(parte_real) < 1e-10:
            return "Centro"
        elif parte_real > 0:
            return "Espiral inestable"
        else:
            return "Espiral estable"
    
    lambda1, lambda2 = np.real(lambda1), np.real(lambda2)
    
    if abs(lambda1) < 1e-10 or abs(lambda2) < 1e-10:
        return "Línea de equilibrios"
    elif lambda1 * lambda2 < 0:
        return "Punto silla"
    elif lambda1 > 0 and lambda2 > 0:
        return "Nodo inestable"
    else:
        return "Nodo estable"

print("=" * 90)
print("SOLUCIONES GENERALES DE LOS SISTEMAS DINÁMICOS".center(90))
print("=" * 90)

for num in range(1, 29):
    sistema = sistemas[num]
    A = sistema['A']
    eigenvalues, eigenvectors = eig(A)
    tipo = clasificar_equilibrio(eigenvalues)
    
    print(f"\n【Sistema {num}】 {sistema['eq']}")
    print(f"Tipo: {tipo}")
    
    if np.iscomplex(eigenvalues[0]):
        alpha = np.real(eigenvalues[0])
        beta = np.imag(eigenvalues[0])
        print(f"λ = {alpha:.3f} ± {beta:.3f}i")
        print(f"x(t) = e^({alpha:.3f}t)[c₁cos({beta:.3f}t) + c₂sin({beta:.3f}t)]")
        print(f"y(t) = e^({alpha:.3f}t)[c₃cos({beta:.3f}t) + c₄sin({beta:.3f}t)]")
    else:
        l1, l2 = np.real(eigenvalues[0]), np.real(eigenvalues[1])
        v1, v2 = np.real(eigenvectors[:, 0]), np.real(eigenvectors[:, 1])
        print(f"λ₁ = {l1:.3f}, λ₂ = {l2:.3f}")
        print(f"x(t) = c₁·e^({l1:.3f}t)·({v1[0]:.3f}) + c₂·e^({l2:.3f}t)·({v2[0]:.3f})")
        print(f"y(t) = c₁·e^({l1:.3f}t)·({v1[1]:.3f}) + c₂·e^({l2:.3f}t)·({v2[1]:.3f})")

print("\n" + "=" * 90)