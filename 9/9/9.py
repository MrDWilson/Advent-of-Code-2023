from pathlib import Path
from typing import List

def parse_line(input: str) -> List[str]:
    return [int(x.strip()) for x in input.split(" ") if len(x) > 0]

def generate_next_seq(input: List[int]) -> List[int]:
    zipped = [(a, b) for a, b in zip(input, input[1:])]
    return [y - x for (x, y) in zipped]

def generate_history(input: List[int]) -> List[List[int]]:
    history: List[List[int]] = [input]
    next_history: List[int] = []
    while True: 
        next_history = generate_next_seq(history[-1])
        history.append(next_history)

        if all([x == 0 for x in next_history]):
            break

    return history

def find_next_value(input: List[List[int]], backwards: bool = False) -> int:
    next_difference: int = 0
    for history_row in reversed(input):
        if all([x == 0 for x in history_row]):
            continue
        
        if backwards:
            next_difference = history_row[0] - next_difference
        else:
            next_difference = history_row[-1] + next_difference

    return next_difference

def main():
    p = Path(__file__).with_name('input.txt')
    with p.open('r') as file:
        lines = file.readlines()

    histories = [parse_line(x) for x in lines]
    evaluated_histories = [generate_history(x) for x in histories]
    next_values = [find_next_value(x) for x in evaluated_histories]
    previous_values = [find_next_value(x ,True) for x in evaluated_histories]

    print("Part 1: " + str(sum(next_values)))
    print("Part 2: " + (str(sum(previous_values))))


if __name__ == '__main__':
    main()