from collections import deque
import numpy as np
from typing import Optional, Tuple, List

"""
Zvolil jsem průchod BFS (Breadth-First Search) pro hledání cesty v bludišti,
protože BFS je vhodný pro hledání nejkratší cesty
v neorientovaných grafech a mřížkách.
Zároveň jsme BFS implementovali v předmětu Algoritmy 1
a vím o něm více než o Dijkstrově algoritmu...
"""


def get_neighbors(i: int, j: int, n: int) -> List[Tuple[int, int]]:
    """
    Vrací seznam sousedních buněk v matici NxN pro danou buňku (i, j).

    Sousedé jsou definováni jako buňky nahoře, dole, vlevo a vpravo,
    pokud zůstávají uvnitř hranic matice.

    Args:
        i (int): Řádek aktuální buňky.
        j (int): Sloupec aktuální buňky.
        n (int): Velikost matice (n x n).

    Returns:
        List[Tuple[int, int]]: Seznam souřadnic sousedních buněk.
    """
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # nahoru, dolů, vlevo, vpravo

    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n:
            # zkontrolujeme, jestli je potenciální soused v rámci matice
            neighbors.append((ni, nj))
            # přidáme souseda jako dvojici (řádek, sloupec)

    return neighbors


def show_path(
    n: int,
    parent_map: np.ndarray,
    end: Tuple[int, int]
) -> Tuple[np.ndarray, int, List[Tuple[int, int]]]:
    """
    Zrekonstruuje cestu od počátku k cílové buňce pomocí mapy předků.

    Projde parent_map od cílové buňky zpět k začátku a vytvoří:
    - matici s vyznačenou cestou,
    - počet kroků,
    - seznam souřadnic buněk na cestě (od začátku do cíle).

    Args:
        n (int): Velikost matice (n x n).
        parent_map (np.ndarray): Pole s odkazy na předchozí buňky.
        end (Tuple[int, int]): Souřadnice cílové buňky.

    Returns:
        Tuple[np.ndarray, int, List[Tuple[int, int]]]:
            Mapa cesty (True pro buňky na cestě),
            počet buněk na cestě,
            seznam souřadnic buněk tvořících cestu.
    """
    path_map = np.full((n, n), False, dtype=bool)
    # vytvoříme matici pro zobrazení cesty,
    # kde True znamená, že buňka je součástí cesty
    path_steps: List[Tuple[int, int]] = []
    # list pro uchování souřadnic buněk, které jsou součástí cesty
    current: Optional[Tuple[int, int]] = end
    p = 0  # počet buněk, které jsou součástí cesty
    # (p má využití pří vytváření bludiště)
    while current is not None:
        p += 1
        path_map[current] = True
        path_steps.append(current)
        current = parent_map[current]

    return path_map, p, path_steps[::-1]
    # vrátíme matici cesty, počet buněk na cestě
    # a zpětně seznam souřadnic buněk, které jsou součástí cesty


def solve(
        matrix: np.ndarray
) -> Optional[Tuple[np.ndarray, int, List[Tuple[int, int]]]]:
    """
    Najde průchozí cestu z levého horního
    do pravého dolního rohu matice pomocí BFS.

    Algoritmus prohledává matici z buňky (0, 0) a hledá cestu
    do buňky (n-1, n-1) přes hodnoty True (průchozí buňky).
    Pokud cesta existuje, vrací její podobu.

    Args:
        matrix (np.ndarray): Čtvercová matice (n x n),
        kde True značí průchozí buňky.

    Returns:
        Optional[Tuple[np.ndarray, int, List[Tuple[int, int]]]]:
            Pokud cesta existuje:
                - Mapa cesty (True pro buňky na cestě),
                - počet buněk na cestě,
                - seznam souřadnic buněk na cestě (od začátku do cíle).
            Jinak: None.
    """
    n = matrix.shape[0]
    state_map = np.full(matrix.shape, "unknown", dtype=object)
    # počáteční stav všech buněk je "unknown",
    # v průběhu prohledávání se mění na "discovered" a "finished"
    parent_map = np.full(matrix.shape, None, dtype=object)
    # parent_map slouží k uchování "předků", abychom mohli sledovat cestu zpět.
    # pro konkrétní buňky bude obsahovat dvojice (i, j) pro jejich předka.
    # dtype=object -> NumPy musí vědět,
    # že ty položky jsou obecné Python objekty.
    # položky jsou buď dvojice (i, j)
    # nebo None (pro počáteční buňku) pro parent_map
    # a "unknown", "discovered", "finished" pro state_map
    queue = deque()

    state_map[0, 0] = "discovered"
    parent_map[0, 0] = None
    # počáteční buňka nemá žádného předka
    queue.append((0, 0))  # algoritmus vždy začneme v levém horním rohu

    while queue:
        # klasický bsf algoritmus
        i, j = queue.popleft()
        for ni, nj in get_neighbors(i, j, n):
            if (ni, nj) == (n-1, n-1):
                # pokud jsme dosáhli pravého dolního rohu, můžeme skončit
                parent_map[ni, nj] = (i, j)
                # p teď nepotřebujeme, proto _
                path_map, p, path_steps = show_path(n, parent_map, (n-1, n-1))
                return path_map, p, path_steps
            if state_map[ni, nj] == "unknown" and matrix[ni, nj]:
                # pokud je buňka neznámá a je průchozí (True),
                # přidáme ji do fronty
                state_map[ni, nj] = "discovered"
                parent_map[ni, nj] = (i, j)
                queue.append((ni, nj))
        state_map[i, j] = "finished"

    # Pokud se sem dostaneme, žádná cesta neexistuje
    print("Cesta nebyla nalezena.")
    return None
