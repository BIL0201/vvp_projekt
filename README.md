# Generátor a řešič bludišť (Projekt do předmětu)

Tento repozitář obsahuje projekt vytvořený jako součást předmětu Vědecké výpočty v pythonu.
Cílem bylo vytvořit knihovnu, která umožňuje:

- generování bludišť dle různých šablon,
- přidávání falešných cest pro zvýšení obtížnosti,
- automatizované řešení bludiště,
- vizualizaci a testování příkladů v Jupyter notebooku.

---

## Funkcionality knihovny

### 1. **Generování bludišť**
Bludiště lze generovat pomocí různých šablon:

- `create_simple_tem` – základní jednoduchá struktura,
- `create_zigzag_tem` – klikatá struktura (zigzag),
- `create_best_tem` – optimalizované bludiště se složitější cestou,
- `create_turbo_tem` – velmi náročné bludiště (může selhat),
- `create_tem_with_fake_paths` – bludiště s falešnými (mrtvými) cestami.

Funkce `create_maze(n, t)` umožňuje zvolit velikost a typ šablony (`t ∈ {1, 2, 3, 4, 5}`)
a vytvoří plně funkční bludiště s hlavní i falešnou cestou.

### 2. **Řešení bludišť**
Pomocí funkce `solve` lze najít cestu bludištěm
od levého horního rohu do pravého dolního. Výsledkem je:

- booleanová mapa cesty (`path_map`),
- souřadnice řešení (`steps`),
- případně počet kroků.

### 3. **Náhodné rozšíření cest**
Funkce `create_maze` také umožňuje přidávat falešné cesty do bludiště,
čímž ztíží jeho řešení a zvýší komplexitu.

---

## Struktura repozitáře

- `knihovna/` – v této složce se nachází všechny funkce potřebné k tomuto projektu.
- `data/` – složka obsahuje bludiště, které jsou řešeny později v `examples/`.
- `solved_mazes/` – do této složky budou přesunuty obrázky, které vzniknou po použití funkce solve v `examples/`.
- `generated_mazes/` – do této složky budou přesunuty bludiště, která vzniknou po použití funkce create_maze v `examples/`.
- `examples/` – příklady použití v Jupyter notebooku (`.ipynb`), vizualizace a testování.
- `README.md` – tento soubor.

projekt_vpp/
│
├── knihovna/
│   ├── __init__.py
│   ├── maze_generator.py
│   ├── maze_template.py
│   ├── save_to_image.py
│   └── solve_maze.py
│
├── data/
│   ├── maze_1.csv
│   ├── maze_2.csv
│   ├── maze_3.csv
│   ├── maze_4.csv
│   └── maze_5.csv
│
├── solved_mazes/
│   ├── ...
│
├── generated_mazes/
│   ├── ...
│
├── examples.ipynb
│
└── README.md
---

## Příklady (Jupyter Notebook)

Ve složce `examples/` naleznete interaktivní Jupyter notebook, který demonstruje:

- generování různých typů bludišť,
- vizualizaci řešené cesty,
- ladění složitosti bludiště,
- práci s výstupy funkcí.

---

## Požadavky

Projekt využívá následující knihovny:

- `numpy`
- `random`
- `matplotlib` 


