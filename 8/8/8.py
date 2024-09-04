from pathlib import Path
from enum import Enum
from typing import List, Dict, Tuple

class Direction(Enum):
    Left = 0
    Right = 1

def process_input(input: str) -> Tuple[str, str, str]:
    key = input.split("=")[0].strip()
    leftright = input.split("=")[-1].strip().strip("(").strip(")").split(",")
    left = leftright[0].strip()
    right = leftright[1].strip()
    return (key, left, right)

def process_instruction(instruction: Direction, node: Tuple[str, str], nodes: Dict[str, Tuple[str, str]]) -> Tuple[str, Tuple[str, str]]:
    next_node_id = node[instruction.value]
    return (next_node_id, nodes[next_node_id])

def get_direction(input: str) -> Direction:
    if input == "L":
        return Direction.Left
    elif input == "R":
        return Direction.Right
    
def repeat_instructions(instructions: List[Direction]):
    index = 0
    while True:
        yield instructions[index]   
        index = index + 1 if index < len(instructions) - 1 else 0

def main():
    p = Path(__file__).with_name('input.txt')
    with p.open('r') as file:
        lines = file.readlines()

    instructions = [get_direction(x) for x in lines[0].strip()]
    nodes_parsed = [process_input(x) for x in lines[2:]]
    nodes = dict([(x[0], (x[1], x[2])) for x in nodes_parsed])

    count: int = 0
    if "AAA" in nodes:
        node: Tuple[str, Tuple[str, str]] = ("AAA", nodes["AAA"])
        for instruction in repeat_instructions(instructions):
            count += 1
            node = process_instruction(instruction, node[1], nodes)
            if node[0] == "ZZZ":
                break

    ghost_nodes = [(key, value) for key, value in nodes.items() if key.endswith("A")]
    ghost_count: int = 0
    for instruction in repeat_instructions(instructions):
        ghost_count += 1
        ghost_nodes = [process_instruction(instruction, node[1], nodes) for node in ghost_nodes]
        if all([node[0].endswith("Z") for node in ghost_nodes]):
            break

    print("Part 1: " + str(count))
    print("Part 2: " + str(ghost_count))

if __name__ == '__main__':
    main()