import random
from typing import Tuple, Optional
import numpy as np

from knihovna.solve_maze import (
    get_neighbors,
    solve,
)

from knihovna.maze_template import (
    create_simple_tem,
    create_zigzag_tem,
    create_best_tem,
    create_turbo_tem,
    create_tem_with_fake_paths,
    )


def rand_dir(i: int, j: int, n: int) -> Tuple[int, int]:
    """
    Vybere náhodného souseda buňky (i, j) v mřížce velikosti n x n.

    Args:
        i (int): Řádek aktuální buňky.
        j (int): Sloupec aktuální buňky.
        n (int): Velikost strany čtvercové mřížky.

    Returns:
        Tuple[int, int]: Souřadnice vybraného souseda.
    """
    neighbors = get_neighbors(i, j, n)
    cur_dir = random.choice(neighbors)
    return cur_dir


# t různých šablon pro generování bludiště

def create_maze(n: int, t: int) -> Optional[np.ndarray]:
    """
    Vygeneruje bludiště dle zvolené šablony a přidá falešné cesty.

    Args:
        n (int): Velikost bludiště (n x n), musí být v rozsahu 12–1000.
        t (int): Typ šablony (1–5).

    Returns:
        Optional[np.ndarray]: Matice bludiště,
        (kde True = průchozí, False = zeď)
        nebo None při chybě.
    """
    if n < 12 or n > 1000:
        print("Velikost matice musí být v rozmezí 12 až 1000.")
        return None

    # Zde zvolíme šablonu podle typu t
    if t == 1:
        maze = create_simple_tem(n)
    elif t == 2:
        maze = create_zigzag_tem(n, 3)
    elif t == 3:
        maze = create_best_tem(n, 5)
    elif t == 4:
        maze = create_turbo_tem(n)
    elif t == 5:
        maze = create_tem_with_fake_paths(n, 5)
    else:
        print("Neplatný typ šablony. Používám jednoduchou šablonu.")
        maze = create_simple_tem(n)
    # maze budeme teď už měnit dále, path_map se hodí k uložení cesty
    # teď potřebujeme maze dostat do formátu,
    # který bude použitelný pro funkci solve
    # path_map: 1 → False (není průchozí), 0 → True (průchozí)

    """
    protože varianta 4 (turbo) nemusí vždy fungovat,
    vytvoříme novou šablonu pro t = 3,
    pokud se nepodaří najít cestu pro t = 4,
    a použijeme ji pro další pokus o nalezení cesty.
    """

    converted_maze = (maze == 0)
    result = solve(converted_maze)
    if result is None:
        if t != 4:
            print("Cesta nebyla nalezena nebo má nesprávný formát.")
            return None
        else:
            maze = create_best_tem(n, 5)
            # pokud šablona turbo nevyšla,
            # vytvoříme novou šablonu
            converted_maze = (maze == 0)
            result = solve(converted_maze)
            if result is None:
                print("Cesta nebyla nalezena ani po vytvoření nové šablony.")
                return None
    # pokud je cesta nalezena, uložíme ji do proměnných
    path_map, _, win_steps = result

    # Přidáme náhodné falešné cesty do bludiště
    num_paths = n // 3
    # (podle mě) optimální počet falešných cest
    path_length = n - n // 3
    # (opět podle mě) optimální délka falešných cest
    opt_path_start = n - n // 4
    # chceme, aby falešné cesty prvních n // 3 buněk vedly dál od win_steps

    # path_map využijeme pro uložení všech možných cest (včetně falešných)
    # pomocí slice ořezáváme win_steps, aby se vyhnuly okrajům
    # a získali jsme pouze vnitřní buňky, kde můžeme přidávat falešné cesty
    opt_steps = win_steps[2:-2]
    paths = random.sample(opt_steps, num_paths)
    # z opt_steps náhodně vybereme optimální počet cest,
    # ze kterých povedou falešné cesty
    c = 0  # count pro počet kroků

    for (i, j) in paths:
        for _ in range(path_length):
            # pokud jsme na okraji, tak už nemůžeme pokračovat
            if (i, j) == (n - 1, n - 1):
                break
            if c == 0:
                maze[i, j] = 0  # nastavíme aktuální buňku jako průchozí
                path_map[i, j] = True  # nastavíme buňku jako součást cesty
            elif c <= opt_path_start:
                # nejprve zjistíme, kteří sousedi buňky jsou součástí win_steps
                neighbors = get_neighbors(i, j, n)
                for ni, nj in neighbors:
                    if (ni, nj) not in win_steps:
                        if path_map[ni, nj] is False:
                            # pokud není buňka součástí cesty
                            maze[ni, nj] = 0
                            path_map[ni, nj] = True
                            # nastavíme buňku jako součást cesty
                        # zjistíme, kterým směrem jsme se posunuli
                        # z aktuální buňky (i, j) do sousední buňky (ni, nj)
                        direction = None
                        di = ni - i
                        dj = nj - j

                        if di == -1 and dj == 0:
                            direction = (-1, 0)  # nahoru
                        elif di == 1 and dj == 0:
                            direction = (1, 0)  # dolů
                        elif di == 0 and dj == -1:
                            direction = (0, -1)  # doleva
                        elif di == 0 and dj == 1:
                            direction = (0, 1)  # doprava
                        if direction is not None:
                            # posuneme se z buňky (ni, nj) o daný směr
                            ni += direction[0]
                            nj += direction[1]
                        while (
                            c <= opt_path_start
                            and (0 <= ni < n and 0 <= nj < n)
                        ):
                            # pokud jsme v rámci matice,
                            # nastavíme buňku jako průchozí
                            maze[ni, nj] = 0
                            # posuneme se o daný směr
                            ni += direction[0]
                            nj += direction[1]
                            # zvýšíme počet kroků
                            c += 1
            # pokud už nejsme na začátku falešné cesty,
            # můžeme nový směr dát jako random
            # nastavíme aktuální buňku jako průchozí
            # náhodně zvolíme směr
            ni, nj = rand_dir(i, j, n)
            if maze[ni, nj] == 1:  # pokud je buňka volná
                maze[ni, nj] = 0  # vytvoříme falešnou cestu
            elif maze[ni, nj] == 0:  # pokud je buňka průchozí
                for _ in range(4):
                    # tři další pokusy o nalezení průchozí buňky
                    ni, nj = rand_dir(i, j, n)
                    if maze[ni, nj] == 1:
                        # nastavíme aktuální buňku jako průchozí
                        maze[ni, nj] = 0
                        break
            i, j = ni, nj
            # nakonec vytvoříme novou matici, která je nové bludiště,
    # kde 0 znamená průchozí buňku
    # a 1 znamená neprůchozí buňku
    # a uložíme ji do CSV souboru
    new_maze = (maze == 0)
    print("Bludiště bylo úspěšně vygenerováno.")
    return new_maze
