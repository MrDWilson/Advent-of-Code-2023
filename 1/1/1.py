from pathlib import Path
import re
from itertools import chain

def get_indexes(input: str, check_text: bool):
    numbers = {}
    
    values = { "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine" }
    if check_text:
        for key, value in values.items():
            indexes = [match.start() for match in re.finditer(value, input)]
            if indexes:
                numbers[key] = indexes

    for key in values.keys():
        indexes = [match.start() for match in re.finditer(key, input)]
        if indexes:
            if key in numbers:
                existing = numbers[key]
                numbers[key] = existing + indexes
            else:
                numbers[key] = indexes

    return numbers

def calculate_line(line: str, check_text: bool = False) -> int:
    indexes = get_indexes(line, check_text)

    min_str = min(chain(*indexes.values()))
    max_str = max(chain(*indexes.values()))

    min_digit = [x[0] for x in indexes.items() if min_str in x[1]]
    max_digit = [x[0] for x in indexes.items() if max_str in x[1]]
    number = min_digit[0] + max_digit[0]
    return int(number)

def main():
    p = Path(__file__).with_name('codes.txt')
    with p.open('r') as file:
        lines = file.readlines()

        numbers = []
        for line in lines:
            numbers.append(calculate_line(line))

        print("Part one: " + str(sum(numbers)))

        numbers = []
        for line in lines:
            numbers.append(calculate_line(line, True))

        print("Part two: " + str(sum(numbers)))

if __name__ == "__main__":
    main()