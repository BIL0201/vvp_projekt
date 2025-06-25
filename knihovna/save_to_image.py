import numpy as np
import os
import matplotlib.pyplot as plt


def solved_maze_to_image(
    maze_map: np.ndarray,
    path_map: np.ndarray,
    n: int,
    nazev: str
) -> None:
    """
    Uloží vyřešené bludiště jako obrázek PNG s vyznačenou cestou.

    Funkce vytvoří RGB obrázek, kde:
    - černá barva značí zdi,
    - bílá barva značí průchozí cesty,
    - červená barva značí nalezenou cestu (podle path_map).

    Výsledný obrázek se uloží do složky 'solved_mazes'.

    Args:
        maze_map (np.ndarray): Logická matice bludiště (True = průchozí).
        path_map (np.ndarray): Logická matice s cestou (True = buňka na cestě).
        n (int): Rozměr matice (n x n).
        nazev (str): Název výstupního souboru (bez přípony).
    """
    # Vytvoření RGB obrázku z logické matice
    # Začneme maticí s nulami (černé pozadí)
    maze_image = np.zeros(
        (n, n, 3),
        dtype=np.uint8)
    # Bílé pozadí pro průchozí cesty
    maze_image[maze_map] = [255, 255, 255]  # white

    # Překreslení cesty na červeno tam, kde je True v path_map
    maze_image[path_map] = [255, 0, 0]  # red

    # Výběr výstupní složky a jména
    output_dir = os.path.join(os.path.dirname(__file__), "..", "solved_mazes")
    output_filename = f"{nazev}.png"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    # Uložení obrázku
    plt.imsave(output_path, maze_image)
    print(f"Obrázek bludiště uložen jako '{output_path}'.")


def generated_maze_to_image(
    maze_map: np.ndarray,
    n: int,
    nazev: str
) -> None:
    """
    Uloží vygenerované bludiště jako obrázek PNG bez vyznačené cesty.

    Funkce vytvoří RGB obrázek, kde:
    - černá barva značí zdi,
    - bílá barva značí průchozí cesty.

    Výsledný obrázek se uloží do složky 'generated_mazes'.

    Args:
        maze_map (np.ndarray): Logická matice bludiště (True = průchozí).
        n (int): Rozměr matice (n x n).
        nazev (str): Název výstupního souboru (bez přípony).
    """
    # Vytvoření RGB obrázku z logické matice
    # Začneme maticí s nulami (černé pozadí)
    maze_image = np.zeros(
        (n, n, 3),
        dtype=np.uint8)
    # Bílé pozadí pro průchozí cesty
    maze_image[maze_map] = [255, 255, 255]  # white

    # Výběr výstupní složky a jména
    output_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "generated_mazes"
    )
    output_filename = f"{nazev}.png"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    # Uložení obrázku
    plt.imsave(output_path, maze_image)
    print(f"Obrázek bludiště uložen jako '{output_path}'.")
