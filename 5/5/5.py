from pathlib import Path
from typing import List, Tuple, Optional
import itertools as it

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
            return map[1][index]
        
    return input

def get_end_number(input: int, all_maps: List[List[Tuple[List[int], List[int]]]]) -> int:
    current_match = input
    for maps in all_maps:
        current_match = get_next_map_match(current_match, maps)

    return current_match

def chunked_range(start, end, chunk_size=10000000):
    current = start
    while current < end:
        next_chunk_end = min(current + chunk_size, end)
        yield range(current, next_chunk_end)
        current = next_chunk_end

def main():
    p = Path(__file__).with_name('maps.txt')
    with p.open('r') as file:
        lines = file.readlines()

    seeds, maps = split_input(lines)
    map_ranges = [convert_map(map) for map in maps]
    seed_locations = [get_end_number(x, map_ranges) for x in seeds]
    lowest_seed = min(seed_locations)

    current_min_seed: Optional[int] = None
    for seed, index in it.batched(seeds, 2):
        for chunk in chunked_range(seed, seed + index):
            for x in [get_end_number(x, map_ranges) for x in chunk]:
                if current_min_seed == None:
                    current_min_seed = x
                elif x < current_min_seed:
                    current_min_seed = x
        
    print("Part 1: " + str(lowest_seed))
    print("Part 2: " + str(current_min_seed))

if __name__ == "__main__":
    main()