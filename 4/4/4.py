from pathlib import Path
from typing import Tuple, List, Optional

def get_card(card: str) -> str:
    return card.split(": ")[1]

def split_winning(card: str) -> Tuple[str, str]:
    return (card.split("|")[0], card.split("|")[1])

def get_card_numbers(numbers: Tuple[str, str]) -> Tuple[List[int], List[int]]:
    winning_numbers = parse_numbers(numbers[0])
    card_numbers = parse_numbers(numbers[1])
    return (winning_numbers, card_numbers)

def parse_numbers(numbers: str) -> List[int]:
    return [int(x.strip()) for x in numbers.split(" ") if len(x) > 0]

def check_matches(numbers: Tuple[List[int], List[int]]) -> int:
    matched = 0
    for number in numbers[1]:
        if number in numbers[0]:
            matched += 1

    return matched

def calculate_score(number_count: int) -> int:
    if number_count == 0 or number_count == 1:
        return number_count
        
    result = 1
    for _ in range(1, number_count):
        result *= 2

    return result

def get_indexes(index: int, score: int) -> Optional[List[int]]:
    if score == 0:
        return None
    
    return [x for x in range(index + 1, index + score + 1)]

def process_card(index: int, score: int, scores: List[int]) -> int:
    indexes = get_indexes(index, score)
    if indexes is None:
        return 1

    counts = sum([process_card(x, scores[x], scores) for x in indexes])
    return counts + 1

def main():
    p = Path(__file__).with_name('cards.txt')
    with p.open('r') as file:
        lines = file.readlines()

    cards = [get_card(x) for x in lines]
    split_cards = [split_winning(x) for x in cards]
    card_numbers = [get_card_numbers(x) for x in split_cards]
    match_counts = [check_matches(x) for x in card_numbers]
    match_scores = [calculate_score(x) for x in match_counts]

    card_count = 0
    for index, score in enumerate(match_counts):
        card_result = process_card(index, score, match_counts)
        if card_result is not None:
            card_count += card_result

    print("Part one: " + str(sum(match_scores)))
    print("Part two: " + str(card_count))


if __name__ == "__main__":
    main()