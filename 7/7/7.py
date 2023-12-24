from pathlib import Path
from typing import List, Tuple
from enum import Enum
import itertools as it

class Hand(Enum):
    FiveOfKind = 1
    FourOfKind = 2
    FullHouse = 3
    ThreeKind = 4
    TwoPair = 5
    OnePair = 6
    HighCard = 7

def parse_input(input: str) -> Tuple[str, int]:
    return (input.split(" ")[0].strip(), int(input.split(" ")[1].strip()))

def summarise_cards(cards: List[str]) -> List[Tuple[str, int]]:
    card_summary = []
    cards_copy = cards.copy()
    while len(cards_copy) > 0:
        card = cards_copy[0]
        count = cards_copy.count(card)
        card_summary.append((card, count))
        cards_copy = [x for x in cards_copy if x != card]

    return card_summary

def calculate_hand(hand: str, joker_mode: bool = False) -> Hand:
    cards = [x for x in hand]
    card_summary = summarise_cards(cards)

    if len(card_summary) == 1:
        return Hand.FiveOfKind
    
    if len(card_summary) == 2 and any([x[1] == 4 for x in card_summary]):
        if joker_mode and any([x == "J" for x in cards]):
            return Hand.FiveOfKind

        return Hand.FourOfKind
    
    if len(card_summary) == 2 and any([x[1] == 3 for x in card_summary]):
        if joker_mode and any([x == "J" for x in cards]):
            return Hand.FiveOfKind

        return Hand.FullHouse
    
    if len(card_summary) == 3 and any([x[1] == 3 for x in card_summary]):
        if joker_mode and any([x == "J" for x in cards]):
            return Hand.FourOfKind

        return Hand.ThreeKind
    
    if len(card_summary) == 3 and any([x[1] == 2 for x in card_summary]):
        if joker_mode and any([x == "J" for x in cards]):
            if len([x for x in cards if x == "J"]) == 2:
                return Hand.FourOfKind
            else:
                return Hand.FullHouse

        return Hand.TwoPair
    
    if len(card_summary) == 4 and any([x[1] == 2 for x in card_summary]):
        if joker_mode and any([x == "J" for x in cards]):
            return Hand.ThreeKind

        return Hand.OnePair
    
    if joker_mode and any([x == "J" for x in cards]):
        return Hand.OnePair
    
    return Hand.HighCard
    
def get_card_ranks(hand: str, joker_mode: bool = False) -> List[int]:
    CARD_VALUES = "AKQJT98765432" if not joker_mode else "AKQT98765432J"
    return [CARD_VALUES.index(x) for x in hand]

def calculate_total_winnings(input: List[Tuple[Tuple[str, int], Hand]]) -> int:
    return sum([x[1] * x[0][0][1] for x in input])

def main():
    p = Path(__file__).with_name('cards.txt')
    with p.open('r') as file:
        lines = file.readlines()

    hands = [parse_input(line) for line in lines]

    hand_values = [(hand, calculate_hand(hand[0])) for hand in hands]
    joker_hand_values = [(hand, calculate_hand(hand[0], True)) for hand in hands]

    ranked_hands = sorted(hand_values, key=lambda x: (x[1].value, *get_card_ranks(x[0][0])))
    ranked_joker_hands = sorted(joker_hand_values, key=lambda x: (x[1].value, *get_card_ranks(x[0][0], True)))

    ranked_hands_with_score = list(zip(ranked_hands, range(len(ranked_hands), 0, -1)))
    total_winnings = calculate_total_winnings(ranked_hands_with_score)

    joker_ranked_hands_with_score = list(zip(ranked_joker_hands, range(len(ranked_joker_hands), 0, -1)))
    joker_total_winnings = calculate_total_winnings(joker_ranked_hands_with_score)

    print("Part one: " + str(total_winnings))
    print("Part two: " + str(joker_total_winnings))

if __name__ == '__main__':
    main()