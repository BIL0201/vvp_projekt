import numpy as np
import random


# n - velikost matice (n x n)
def create_simple_tem(n: int) -> np.ndarray:
    """
    Vytvoří jednoduchou šablonu bludiště.

    Cesta vede:
    - dolů po levém okraji do středu,
    - vodorovně přes střed,
    - dolů po pravém okraji do cíle.

    Args:
        n (int): Rozměr matice (n x n).

    Returns:
        np.ndarray: Matice s hodnotami 0 (cesta) a 1 (zdi).
    """
    template = np.ones((n, n), dtype=int)

    mid = n // 2  # prostřední řádek

    for i in range(mid + 1):
        template[i, 0] = 0  # cesta dolů doprostřed v levém sloupci

    for j in range(n):
        template[mid, j] = 0  # cesta doprava

    for i in range(mid + 1, n):
        template[i, n - 1] = 0  # cesta dolů v pravém sloupci

    return template


# z - velikost "zigzag" úseček
def create_zigzag_tem(n: int, z: int) -> np.ndarray:
    """
    Vytvoří šablonu bludiště ve tvaru "zigzag".

    Cesta vede střídavě dolů a doprava v blocích délky `z`,
    dokud se nedostane k pravému dolnímu rohu.

    Args:
        n (int): Rozměr matice (n x n).
        z (int): Délka jednotlivých segmentů zigzagu.

    Returns:
        np.ndarray: Matice s hodnotami 0 (cesta) a 1 (zdi).
    """
    template = np.ones((n, n), dtype=int)

    i = 0
    j = 0

    # hlavní zigzag část
    while i + z < n and j + z < n:
        # svislý úsek dolů
        for k in range(z):
            template[i + k, j] = 0
        i += z - 1  # končíme dole

        # vodorovně doprava
        for k in range(1, z):
            template[i, j + k] = 0
        j += z - 1  # končíme vpravo

        # příprava na další "zig zag"
    template[i, j] = 0
    # dokončení do pravého dolního rohu
    while (i, j) != (n - 1, n - 1):
        if i < n - 1:
            i += 1
        template[i, j] = 0
        if j < n - 1:
            j += 1
        template[i, j] = 0
    return template


# f - fraction - určuje, do jakého zlomu bude matice rozdělena
def create_best_tem(n: int, f: int) -> np.ndarray:
    """
    Vytvoří šablonu bludiště s klikatou cestou a mírným ohybem.

    Cesta:
    - začíná v levém horním rohu,
    - kličkuje skrz několik zlomů,
    - končí v pravém dolním rohu.

    Zlomy cesty jsou určeny parametrem `f`.

    Args:
        n (int): Rozměr matice (n x n).
        f (int): Míra členění cesty (větší = jemnější rozdělení).

    Returns:
        np.ndarray: Matice s hodnotami 0 (cesta) a 1 (zdi).
    """
    template = np.ones((n, n), dtype=int)

    mid = n // 2
    fraction = n // f

    # 1. Dolů po levém okraji
    for i in range(mid + 1):
        template[i, 0] = 0

    # 2. Doprava ve středu
    for j in range(mid + 1):
        template[mid, j] = 0

    # 3. Nahoru do zlomu ve sloupci mid
    for i in range(mid - 1, fraction - 1, -1):
        template[i, mid] = 0

    # 4. Doprava z mid na n - fraction v řádku fraction
    for j in range(mid + 1, n - fraction):
        template[fraction, j] = 0

    # 5. Dolů vpravo – sloupec n - fraction
    for i in range(fraction + 1, n - fraction):
        template[i, n - fraction - 1] = 0

    # 6. Doleva – v řádku n - fraction
    for j in range(n - fraction - 2, mid - 1, -1):
        template[n - fraction - 1, j] = 0

    # 7. Dolů středem ke spodnímu řádku
    for i in range(n - fraction, n):
        template[i, mid] = 0

    # 8. Doprava do pravého dolního rohu9
    for j in range(mid + 1, n):
        template[n - 1, j] = 0

    return template


# tato turbo funkce není vždy úspěšná,
# ale snaží se vytvořit složitější bludiště
def create_turbo_tem(n: int) -> np.ndarray:
    """
    Pokusí se vytvořit komplikovanější šablonu bludiště s mnoha zatáčkami
    a falešnými cestami.

    Hlavní cesta kličkuje přes různé oblasti,
    přičemž je doplněna množstvím slepých uliček.
    Hodí se pro testování schopností algoritmu řešit složitější labyrinty.

    Poznámka:
        Generování není zaručeně úspěšné nebo optimální,
        protože výběr zlomů je náhodný.
        Náhodný je z důvodu,
        že chceme vytvořit různorodé šablony.

    Args:
        n (int): Rozměr matice (n x n).

    Returns:
        np.ndarray: Matice s hodnotami 0 (cesta) a 1 (zdi).
    """
    template = np.ones((n, n), dtype=int)
    mid = n // 2

    # výběr frakcí s dodatečnou podmínkou pro fraction3
    fraction1 = random.randint(3, 5)
    fraction2 = random.randint(6, 8)
    fraction3 = random.randint(fraction2 + 1, 12)
    # zajistí, že fraction3 - 1 > fraction2

    # 1. Dolů
    for i in range(fraction2 + 1):
        template[i, 0] = 0
    cur_i = i

    # 2. Doprava
    for j in range(fraction1 + 1):
        template[cur_i, j] = 0
    cur_j = j

    # 3. Nahoru
    for i in range(cur_i, fraction3 - 1, -1):
        template[i, cur_j] = 0
    cur_i = i

    # 4. Doprava
    for j in range(cur_j + 1, cur_j + fraction1):
        template[cur_i, j] = 0
    cur_j = j

    # 5. Dolů
    for i in range(cur_i + 1, cur_i + fraction2):
        template[i, cur_j] = 0
    cur_i = i

    # 6. Doleva
    for j in range(cur_j - 1, cur_j - fraction3, -1):
        template[cur_i, j] = 0
    cur_j = j

    # 7. Dolů
    for i in range(cur_i + 1, mid + 1):
        template[i, cur_j] = 0
    cur_i = i

    # 8. Doleva
    for j in range(cur_j - 1, fraction3, -1):
        template[cur_i, j] = 0
    cur_j = j

    # 9. Dolů
    for i in range(cur_i + 1, n - fraction2):
        template[i, cur_j] = 0
    cur_i = i

    # 10. Doprava
    for j in range(cur_j + 1, cur_j + fraction3):
        template[cur_i, j] = 0
    cur_j = j

    # 11. Nahoru
    for i in range(cur_i - 1, mid, -1):
        template[i, cur_j] = 0
    cur_i = i

    # 12. Doprava
    for j in range(cur_j + 1, n):
        template[cur_i, j] = 0
    cur_j = j

    # 13. Dolů
    for i in range(cur_i + 1, n - fraction3):
        template[i, cur_j] = 0
    cur_i = i

    # 14. Doleva
    for j in range(cur_j - 1, fraction2, -1):
        template[cur_i, j] = 0
    cur_j = j

    # 15. Dolů
    for i in range(cur_i + 1, n):
        template[i, cur_j] = 0

    # 16. Doprava do pravého dolního rohu
    for j in range(cur_j + 1, n):
        template[n - 1, j] = 0

    # A. Falešná cesta dolů
    for i in range(mid + 1, n - fraction1):
        template[i, 0] = 0

    # A.1 Falešná cesta doprava
    for j in range(1, mid + 1):
        template[mid // 2, j] = 0

    # B. Falešná cesta doprava
    for j in range(mid + 1, fraction2):
        template[mid, j] = 0

    # C. Falešná cesta dolů
    for i in range(mid + 1, fraction3):
        template[i, mid] = 0

    # D. Falešná cesta doprava z mid na n - fraction v řádku fraction
    for j in range(mid + 1, n - fraction1):
        template[fraction1, j] = 0

    # E. Falešná cesta dolů vpravo – sloupec n - fraction
    for i in range(fraction2 + 1, n - fraction2):
        template[i, n - fraction2 - 1] = 0

    # F. Falešná cesta doleva – v řádku n - fraction
    for j in range(n - fraction2 - 2, mid - 1, -1):
        template[n - fraction2 - 1, j] = 0

    # G. Falešná cesta dolů středem ke spodnímu řádku
    for i in range(n - fraction1, n):
        template[i, mid] = 0
    # H. Falešná cesta doleva
    for j in range(mid + 1, n):
        template[n - 1, j] = 0
    # I. Falešná cesta nahoru
    for i in range(n - 1, n - fraction1 - 1, -1):
        template[i, n - 1] = 0
    # J. Falešná cesta doleva
    for j in range(n - 2, mid - 1, -1):
        template[n - fraction1 - 1, j] = 0
    return template


# f - fraction - určuje, do jakého zlomu bude matice rozdělena
def create_tem_with_fake_paths(n: int, f: int) -> np.ndarray:
    """
    Vytvoří bludiště s hlavní cestou a několika falešnými odbočkami.

    Tato šablona imituje reálnější bludiště, kde kromě hlavní cesty
    existují i slepé uličky nebo falešné trasy.

    Args:
        n (int): Rozměr matice (n x n).
        f (int): Míra rozdělení a větvení cesty.

    Returns:
        np.ndarray: Matice s hodnotami 0 (cesta) a 1 (zdi).
    """
    template = np.ones((n, n), dtype=int)

    mid = n // 2
    fraction = n // f

    # 1. Dolů po levém okraji
    for i in range(mid + 1):
        template[i, 0] = 0

    # A. Falešná cesta dolů
    for i in range(mid + 1, n - fraction):
        template[i, 0] = 0

    # A.1 Falešná cesta doprava
    for j in range(1, mid + 1):
        template[mid // 2, j] = 0

    # 2. Doprava ve středu
    for j in range(mid + 1):
        template[mid, j] = 0

    # B. Falešná cesta doprava
    for j in range(mid + 1, fraction):
        template[mid, j] = 0

    # C. Falešná cesta dolů
    for i in range(mid + 1, fraction):
        template[i, mid] = 0

    # 3. Nahoru do zlomu ve sloupci mid
    for i in range(mid - 1, fraction - 1, -1):
        template[i, mid] = 0

    # D. Falešná cesta doprava z mid na n - fraction v řádku fraction
    for j in range(mid + 1, n - fraction):
        template[fraction, j] = 0

    # 4. Doprava z mid na n - fraction v řádku fraction
    for j in range(mid + 1, n - fraction):
        template[fraction, j] = 0

    # E. Falešná cesta dolů vpravo – sloupec n - fraction
    for i in range(fraction + 1, n - fraction):
        template[i, n - fraction - 1] = 0

    # 5. Dolů vpravo – sloupec n - fraction
    for i in range(fraction + 1, n - fraction):
        template[i, n - fraction - 1] = 0

    # F. Falešná cesta doleva – v řádku n - fraction
    for j in range(n - fraction - 2, mid - 1, -1):
        template[n - fraction - 1, j] = 0

    # 6. Doleva – v řádku n - fraction
    for j in range(n - fraction - 2, mid - 1, -1):
        template[n - fraction - 1, j] = 0

    # G. Falešná cesta dolů středem ke spodnímu řádku
    for i in range(n - fraction, n):
        template[i, mid] = 0

    # 7. Dolů středem ke spodnímu řádku
    for i in range(n - fraction, n):
        template[i, mid] = 0

    # H. Falešná cesta doleva
    for j in range(mid + 1, n):
        template[n - 1, j] = 0

    # 8. Doprava do pravého dolního rohu9
    for j in range(mid + 1, n):
        template[n - 1, j] = 0

    return template
