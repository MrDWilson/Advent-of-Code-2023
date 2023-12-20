from pathlib import Path
from typing import List, Tuple

def split_input(input: List[str]) -> Tuple[List[int], List[List[List[int]]]]:
    seeds: List[int] = []
    maps: List[List[List[int]]] = []

    current_map: List[List[int]] = []
    for index, line in enumerate(input):
        if index == 0:
            seeds = [int(x.strip()) for x in line.split(":")[1].split(" ") if len(x) > 0]
            continue

        if len(line.strip()) == 0:
            if len(current_map) > 0:
                maps.append(current_map)
                current_map = []
                continue
            else:
                continue

        if ":" in line:
            continue

        current_map.append([int(x.strip()) for x in line.split(" ") if len(x) > 0])

    if len(current_map) > 0:
        maps.append(current_map)

    return seeds, maps

def convert_map_row(row: List[int]) -> Tuple[List[int], List[int]]:
    source_range = range(row[1], row[1] + row[2])
    dest_range = range(row[0], row[0] + row[2])
    return (source_range, dest_range)

def convert_map(map: List[List[int]]) -> List[List[Tuple[int, int]]]:
    return [convert_map_row(x) for x in map]

def get_next_map_match(input: int, maps: List[Tuple[List[int], List[int]]]) -> int:
    for map in maps:
        if input in map[0]:
            index = map[0].index(input)
            destination = map[1][index]
            return destination
        
    return input

def get_end_number(input: int, all_maps: List[List[Tuple[List[int], List[int]]]]) -> int:
    current_match = input
    for maps in all_maps:
        print(current_match)
        current_match = get_next_map_match(current_match, maps)

    return current_match

def main():
    p = Path(__file__).with_name('test.txt')
    with p.open('r') as file:
        lines = file.readlines()

    seeds, maps = split_input(lines)
    map_ranges = [convert_map(map) for map in maps]

    for seed in seeds:
        print("Seed " + str(seed) + ": " + str(get_end_number(seed, map_ranges)))

if __name__ == "__main__":
    main()