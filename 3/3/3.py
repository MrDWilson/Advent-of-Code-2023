from pathlib import Path
from typing import List, Tuple, Optional, Dict
from functools import reduce

class CellResult:
    def __init__(self, match: bool, end_index: int, value: Optional[int] = None, gear_number: Optional[List[str]] = None):
        self.match = match
        self.end_index = end_index
        self.value = value
        self.gear_number = gear_number

def check_cell(items: List[str]) -> bool:
    for item in items:
        if not item.isdigit() and item != ".":
            return True
    
    return False

def get_full_number(row, start_column: int) -> Tuple[int, int]:
    column = start_column
    full_value = []
    while column < len(row) and row[column].isdigit():
        full_value.append(row[column])
        column += 1

    return (int("".join(full_value)), column)

def get_cell(grid, row, index) -> ((int, int), str):
    if index < 0 or index >= len(grid[row]):
        return None
    else:
        return ((row, index), grid[row][index])

def get_keys(grid, row: int, start_index: int, end_index: int) -> List[Tuple[Tuple[int, int], str]]:
    result = []
    
    above_row = row - 1
    below_row = row + 1

    start_index = start_index - 1 if start_index > 0 else 0
    end_index = end_index if end_index < len(grid[row]) - 1 else len(grid[row]) - 1

    if above_row in range(0, len(grid)):
        result.extend(get_cell(grid, above_row, index) for index, _ in enumerate(grid[above_row]) if index in range(start_index, end_index + 1))

    result.extend(get_cell(grid, row, index) for index, _ in enumerate(grid[row]) if index in range(start_index, end_index + 1))

    if below_row in range(0, len(grid)):
        result.extend(get_cell(grid, below_row, index) for index, _ in enumerate(grid[below_row]) if index in range(start_index, end_index + 1))

    return result

def get_gear(grid, row: int, column: int) -> str:
    above_row = row - 1
    below_row = row + 1

    start_index = column
    end_index = column
    start_index = start_index - 1 if start_index > 0 else 0
    end_index = end_index + 1 if end_index < len(grid[row]) - 1 else len(grid[row]) - 1

    number_count = 0
    if above_row in range(0, len(grid)):
        if grid[above_row][start_index].isdigit() \
            and grid[above_row][end_index].isdigit() \
            and not grid[above_row][column].isdigit():
            number_count += 2
        elif any(x.isdigit() for x in grid[above_row][start_index:end_index + 1]):
            number_count += 1

    if grid[row][start_index].isdigit():
        number_count += 1

    if grid[row][end_index].isdigit():
        number_count += 1

    if below_row in range(0, len(grid)):
        if grid[below_row][start_index].isdigit() \
            and grid[below_row][end_index].isdigit() \
            and not grid[below_row][column].isdigit():
            number_count += 2
        elif any(x.isdigit() for x in grid[below_row][start_index:end_index + 1]):
            number_count += 1

    if number_count == 2:
        return str(row) + "-" + str(column)
    else:
        return None

def process_next(grid, row: int, column: int) -> CellResult:
    if grid[row][column].isdigit():
        (number, end_index) = get_full_number(grid[row], column)
        keys = get_keys(grid, row, column, end_index)

        gear_keys = [x for x in keys if x[1] == "*"]
        gears = []
        if len(gear_keys):
            for gear_key in gear_keys:
                gear_number = get_gear(grid, gear_key[0][0], gear_key[0][1])
                if gear_number is not None:
                    gears.append(gear_number)

        match = check_cell([x[1] for x in keys])

        if match:
            return CellResult(True, end_index, number, gears)

        return CellResult(False, end_index)
    else:
        return CellResult(False, column)
    
def process_row(grid, row: int) -> List[int]:
    numbers = []
    column = 0
    while column < len(grid[row]):
        cell_result = process_next(grid, row, column)
        if cell_result.match:
            numbers.append(cell_result.value)

        column = cell_result.end_index + 1

    return numbers

def process_gears(grid, row: int) -> Dict[int, List[int]]:
    numbers: Dict[int, List[int]] = {}
    column = 0
    while column < len(grid[row]):
        cell_result = process_next(grid, row, column)
        if cell_result.match and len(cell_result.gear_number):
            for gear_number in cell_result.gear_number:
                if gear_number not in numbers:
                    numbers[gear_number] = []
                numbers[gear_number].append(cell_result.value)

        column = cell_result.end_index + 1

    return numbers
    
def process_grid(grid) -> (List[int], Dict[int, int]):
    numbers: List[int] = []
    for row in range(0, len(grid)):
        numbers.extend(process_row(grid, row))

    gears: Dict[int, List[int]] = {}
    for row in range(0, len(grid)):
        row_gears = process_gears(grid, row)
        for key, items in row_gears.items():
            if key not in gears:
                gears[key] = []

            gears[key].extend(items)

    return (numbers, gears)

def main():
    p = Path(__file__).with_name('numbers.txt')
    with p.open('r') as file:
        lines = file.readlines()
        grid = [[char for char in line] for line in lines]

    (numbers, gears) = process_grid(grid)
    print("Part one: " + str(sum(numbers)))

    gears = sum(reduce(lambda x, y: x * y, items) for _, items in gears.items())
    print("Part two: " + str(gears))

if __name__ == "__main__":
    main()