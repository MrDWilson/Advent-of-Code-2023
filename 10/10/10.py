from enum import Enum
from pathlib import Path
from typing import List, Tuple, Dict
import numpy as np

class Pipe(Enum):
    VERTICAL = 1
    HORIZONTAL = 2
    NORTHEAST = 3
    NORTHWEST = 4
    SOUTHWEST = 5
    SOUTHEAST = 6
    GROUND = 7
    ANIMAL = 8

def parse_item(item: str) -> Pipe:
    options = {
        "|": Pipe.VERTICAL,
        "-": Pipe.HORIZONTAL,
        "L": Pipe.NORTHEAST,
        "J": Pipe.NORTHWEST,
        "7": Pipe.SOUTHWEST,
        "F": Pipe.SOUTHEAST,
        ".": Pipe.GROUND,
        "S": Pipe.ANIMAL
    }

    return options.get(item)

def parse_line(line: str) -> List[Pipe]:
    return [parse_item(x) for x in list(line.strip()) if len(x) > 0]

def get_connected(matrix, position) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    num_rows, num_cols = matrix.shape
    row, col = position
    current = matrix[row, col]

    matches: List[Tuple[int, int]] = []
    if col > 0 and current == Pipe.ANIMAL or current == Pipe.HORIZONTAL or current == Pipe.NORTHWEST or current == Pipe.SOUTHWEST:
        left = matrix[row, col - 1]
        if left == Pipe.HORIZONTAL or left == Pipe.NORTHEAST or left == Pipe.SOUTHEAST or left == Pipe.ANIMAL:
            matches.append((row, col - 1))

    if row < num_rows - 1 and current == Pipe.ANIMAL or current == Pipe.VERTICAL or current == Pipe.SOUTHEAST or current == Pipe.SOUTHWEST:
        bottom = matrix[row + 1, col]
        if bottom == Pipe.VERTICAL or bottom == Pipe.NORTHEAST or bottom == Pipe.NORTHWEST or bottom == Pipe.ANIMAL:
            matches.append((row + 1, col))

    if row > 0 and current == Pipe.ANIMAL or current == Pipe.VERTICAL or current == Pipe.NORTHEAST or current == Pipe.NORTHWEST:
        top = matrix[row - 1, col]
        if top == Pipe.VERTICAL or top == Pipe.SOUTHEAST or top == Pipe.SOUTHWEST or top == Pipe.ANIMAL:
            matches.append((row - 1, col))

    if col < num_cols - 1 and current == Pipe.ANIMAL or current == Pipe.HORIZONTAL or current == Pipe.NORTHEAST or current == Pipe.SOUTHEAST:
        right = matrix[row, col + 1]
        if right == Pipe.HORIZONTAL or right == Pipe.NORTHWEST or right == Pipe.SOUTHWEST or right == Pipe.ANIMAL:
            matches.append((row, col + 1))

    return (matches[0], matches[1])

def main():
    p = Path(__file__).with_name('input.txt')
    with p.open('r') as file:
        lines = file.readlines()

    matrix = np.array([parse_line(x) for x in lines])
    starting_point = np.where(matrix == Pipe.ANIMAL)
    start_position = starting_point[0][0], starting_point[1][0]
    initial_connections = get_connected(matrix, start_position)

    
    distances: Dict[Tuple[int, int], List[int]] = {}

    # Follow both ways and count steps
    current_step = initial_connections[0]
    previous_connection = start_position

    distance = 1
    distances[current_step] = [distance]
    while current_step != start_position:
        connectors = get_connected(matrix, current_step)
        next_step = connectors[0] if connectors[0] != previous_connection else connectors[1]
        previous_connection = current_step
        current_step = next_step
        distance += 1
        distances[current_step] = [distance]

    # Trace back in the other direction
    current_step = initial_connections[1]
    previous_connection = start_position

    distance = 1
    distances[current_step].append(distance)
    while current_step != start_position:
        connectors = get_connected(matrix, current_step)
        next_step = connectors[0] if connectors[0] != previous_connection else connectors[1]
        previous_connection = current_step
        current_step = next_step
        distance += 1
        distances[current_step].append(distance)

    del distances[start_position]

    for key, value in distances.items():
        distances[key] = [min(value)]

    max_distance = max([value[0] for key, value in distances.items()])

    print("Part 1: " + str(max_distance))


if __name__ == '__main__':
    main()