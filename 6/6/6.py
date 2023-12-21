from pathlib import Path
from typing import List, Tuple
import math

def get_values(input: str) -> List[int]:
    return [int(x.strip()) for x in input.split(":")[1].split(" ") if len(x) > 0]

def calculate_time(input: int, total: int) -> int:
    travel_time: int = total - input
    return travel_time * input

def get_winning_count(input: Tuple[int, int]) -> int:
    win_count = 0
    for i in range(0, input[0] + 1):
        distance = calculate_time(i, input[0])
        if distance > input[1]:
            win_count += 1

    return win_count

def main():
    p = Path(__file__).with_name('races.txt')
    with p.open('r') as file:
        lines = file.readlines()

    times = get_values(lines[0])
    distances = get_values(lines[1])
    races = list(zip(times, distances))
    win_counts = [get_winning_count(x) for x in races if x != 0]

    time = int("".join([str(time) for time in times]))
    distance = int("".join([str(distance) for distance in distances]))
    win_count = get_winning_count((time, distance))

    print("Part 1: " + str(math.prod(win_counts)))
    print("Part 2: " + str(win_count))

if __name__ == "__main__":
    main()