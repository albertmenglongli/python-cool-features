#!/usr/bin/env python3
# Path: deck_of_cards.py
# Based on python 3.12
"""
This is an implementation of a deck of cards. It is a standard 52 card deck, with 4 suits, and 13 cards in each suit.
The cards should be able to be shuffled, and drawn from the deck.

The following codes show many python new features introduced from python 3.6 to 3.12:
1. PEP 634: Structural Pattern Matching: match case
2. PEP 572: Assignment Expressions: walrus operator
3. New annotations, such as: str | int, list[str] | None, etc.
4. PEP 616: String methods to remove prefixes and suffixes: str.removeprefix(), str.removesuffix()
5. f-string: f"{variable=}" to print variable name and value,
    f"{variable!r}" to print variable name and repr(variable),
    f"{variable:<8}" to align left, f"{variable:>8}" to align right, f"{variable:^8}" to align center
6. dataclasses: dataclass, field, ClassVar, __post_init__
7. str.center(width, fill_char)
8. dict new features
etc.
"""
import sys

if sys.version_info < (3, 12):
    raise RuntimeError("This script requires Python 3.12+")

import itertools
import random
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, override, Self


class SUITS(str, Enum):
    """
    ♢ ♣ ♡ ♠ Alternating colours
    Diamonds, followed by clubs, hearts, and spades
    """
    DIAMONDS = '♢'
    CLUBS = '♣'
    HEARTS = '♡'
    SPADES = '♠'

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def get_all(cls):
        """
        return: ['♢', '♣', '♡', '♠']
        """
        return [str(suit) for suit in SUITS]


@dataclass(order=True, frozen=True)
class Card:
    sort_index: int = field(init=False, repr=False)

    rank: str | int = field(default_factory=lambda: random.choices(Card.ALL_RANKS)[0])
    suit: str | SUITS = field(default_factory=lambda: random.choices(Card.ALL_SUITS)[0])

    ALL_RANKS: ClassVar[list[str]] = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
    ALL_SUITS: ClassVar[list[str]] = SUITS.get_all()

    def __post_init__(self):
        # check suit is valid or not
        match self.suit:
            case str():
                if self.suit not in self.ALL_SUITS:
                    raise ValueError(f'Invalid suit: {self.suit}')
            case SUITS():
                # convert enum to str
                setattr(self, 'suit', str(self.suit))
            case _:
                raise ValueError(f'Invalid suit: {self.suit}')

        # check rank is valid or not
        match self.rank:
            case int() as rank if rank == 1:
                object.__setattr__(self, 'rank', self.ALL_RANKS[-1])
            case int() as rank if 2 <= rank <= len(self.ALL_RANKS):
                object.__setattr__(self, 'rank', self.ALL_RANKS[rank - 2])
            case int() as rank if rank <= 0 or rank > len(self.ALL_RANKS):
                raise ValueError(f'Invalid rank: {self.rank}')
            case str() as rank if rank in self.ALL_RANKS:
                # ignore, everything is fine
                pass
            case str() as rank if rank == '1':
                # '1' -> 'A'
                object.__setattr__(self, 'rank', self.ALL_RANKS[-1])
            case str() as rank if (upper_case_rank := rank.upper()) in self.ALL_RANKS:
                # 'a' -> 'A', 'j' -> 'J', 'q' -> 'Q', 'k' -> 'K'
                object.__setattr__(self, 'rank', upper_case_rank)
            case _:
                raise ValueError(f'Invalid rank: {self.rank}')

        # sort_index should be within 0 ~ 51
        # '2♢' < '2♣' < '2♡' < '2♠' < ...< 'K♢' < 'K♣' < 'K♡' < 'K♠' < 'A♢' < 'A♣' < 'A♡' < 'A♠'
        if (sort_index := self.ALL_RANKS.index(self.rank) * len(self.ALL_SUITS) + self.ALL_SUITS.index(
                self.suit)) < 0 or sort_index > 51:
            raise ValueError(f'Invalid sort_index: {sort_index}')
        object.__setattr__(self, 'sort_index', sort_index)

    @property
    def shape(self) -> str:
        """
        :return: string looks like the following
        ┌─────────┐
        │ A       │
        │ ♠       │
        │         │
        │       ♠ │
        │       A │
        └─────────┘
        """
        card_width = 11
        # print a card shape, which is consisted of rank and suit

        return (f"┌{"─" * 9}┐\n"  # Python3.12
                f"│ {self.rank:<8}│\n"  # align left
                f"│ {self.suit:<8}│\n"
                f"│{' ':{card_width - 2}}│\n"  # {i:{align}{padding}} with variable in f-string
                f"│{self.suit:>8} │\n"  # align right
                f"│{self.rank:>8} │\n"  # align right
                f"└{''.center(9, '─')}┘")  # use str.center(width, fill_char)

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.sort_index == other.sort_index

    def __hash__(self):
        return hash((self.sort_index,))

    def __bool__(self):
        return True

    def __repr__(self):
        """
         Actually will be automatically generated by dataclass
        """
        rank = self.rank
        suit = self.suit
        return f'{__class__.__name__}({rank=}, {suit=})'

    def __str__(self):
        return f'{__class__.__name__}({self.rank!r}, {self.suit!r})'


class Deck:
    type Cards = list[Card]  # Python3.12

    def __init__(self, cards: Cards | None = None):
        cards = cards or self.generate_default_cards()
        self._cards: deque = deque(list(cards))

    @classmethod
    def generate_default_cards(cls) -> Cards:
        return []

    @property
    def cards(self):
        return self._cards

    def gen_shape(self, *cards: Card, space_width: int = -8, show_all: bool = False) -> str:
        cards = cards or self._cards
        if isinstance(cards, Card):
            cards = [cards]
        cards = list(cards)
        # the minimum interval width is -8
        space_width = max(space_width, -8)

        # combine cards shape with interval width
        card_lines: list[list[str]] = list(zip(*[card.shape.split('\n') for card in cards]))
        result = ''
        if space_width > 0:
            space = ' ' * space_width
        else:
            space = ''

        for line_num, _card_lines in enumerate(card_lines):
            if space_width < 0:
                # remove space_width spaces in each card line after second card
                _card_lines = [line if idx == 0 else line[abs(space_width):] for idx, line in enumerate(_card_lines)]
            if show_all is False and len(cards) > 6:
                match line_num:
                    case 3:
                        # replace from 4th to last 4th cards with three dots
                        _card_lines[3:-3] = ['...']
                    case 4 | 5:
                        _card_lines[3:-3] = (len(_card_lines[3]) - 1) * ' ' + '│'
                    case _:
                        _card_lines[3:-3] = _card_lines[3]
            result += space.join(_card_lines) + '\n'

        return result.strip('\n')

    def shuffle(self) -> Self:
        random.shuffle(self._cards)
        return self

    def sort(self, reverse=False) -> Self:
        self._cards = sorted(self._cards, reverse=reverse)
        return self

    def make_hand(self, num_cards: int = 5) -> Cards:
        # if not enough cards, return all the remaining cards
        if num_cards > (remaining_length := len(self._cards)):
            num_cards = remaining_length
        return [self.popleft() for _ in range(num_cards)]

    def __iter__(self):
        return iter(self._cards)

    def __len__(self):
        return len(self._cards)

    def __contains__(self, item):
        return item in self._cards

    def __getitem__(self, item: int | slice) -> Card | Cards | None:
        res = None
        match item:
            case int():
                res = self._cards[item]
            case slice():
                res = list(itertools.islice(self._cards, item.start, item.stop, item.step))
            case _:
                raise ValueError(f'Invalid item: {item}')
        return res

    def popleft(self) -> Card:
        try:
            card = self._cards.popleft()
        except IndexError:
            raise IndexError('No more cards in the deck')
        return card

    def pop(self) -> Card:
        try:
            card = self._cards.pop()
        except IndexError:
            raise IndexError('No more cards in the deck')
        return card

    def append(self, card: Card):
        if not isinstance(card, Card):
            raise ValueError(f'Invalid card: {card}')
        self._cards.append(card)

    def appendleft(self, card: Card):
        if not isinstance(card, Card):
            raise ValueError(f'Invalid card: {card}')
        self._cards.appendleft(card)

    def is_empty(self):
        return len(self._cards) == 0

    def __bool__(self):
        return len(self._cards) > 0


class FrenchDeck(Deck):
    @classmethod
    @override  # Python3.12
    def generate_default_cards(cls) -> Deck.Cards:
        return [Card(rank, suit) for rank, suit in itertools.product(Card.ALL_RANKS, Card.ALL_SUITS)]


def strip_shape(shape_content: str) -> str:
    # remove the leading spaces of each line
    res = '\n'.join(line.lstrip() for line in shape_content.split('\n'))
    # remove the leading and trailing '\n' of final result
    res = res.removeprefix('\n').removesuffix('\n')
    return res


def test_cards():
    # test attributes
    assert Card('2', '♠') == Card(2, '♠') == Card(2, SUITS.SPADES)
    assert Card('1', '♠') == Card(1, '♠') == Card(1, SUITS.SPADES) == Card('A', '♠')
    assert (card := Card('A', '♠')) and card.rank == 'A' and card.suit == '♠'
    assert (card := Card('A', SUITS.SPADES)) and card.rank == 'A' and card.suit == '♠'

    # test comparing Cards in order
    assert Card('A', '♠') > Card('A', '♡') > Card('K', '♠')
    cards: list[Card] = sorted([Card('A', '♠'), Card('K', '♠'), Card('A', '♡')])
    assert cards == [Card('K', '♠'), Card('A', '♡'), Card('A', '♠')]
    all_aces = [Card('A', suit) for suit in Card.ALL_SUITS]
    # random a suit value if not specified
    assert Card('A') in all_aces
    # test string representation
    assert str(Card('A', '♠')) == "Card('A', '♠')"
    assert str(cards) == ("[Card(rank='K', suit='♠'),"
                          " Card(rank='A', suit='♡'),"
                          " Card(rank='A', suit='♠')]")
    # test equality
    assert Card('A', '♠') == Card(1, '♠')
    assert Card('2', '♢') == Card(2, '♢')
    assert Card('K', '♠') == Card(13, '♠')
    # test hash
    card_map: dict[Card, str] = {Card('A', '♠'): "Biggest card"}
    card_map |= {Card('2', '♢'): "Smallest card"}  # union update for dict
    assert card_map[Card('A', '♠')] == "Biggest card"
    assert card_map[Card('2', '♢')] == "Smallest card"
    # test shape
    expected_shape = strip_shape("""
        ┌─────────┐
        │ 10      │
        │ ♠       │
        │         │
        │       ♠ │
        │      10 │
        └─────────┘
    """)

    assert Card('10', '♠').shape == expected_shape


def test_deck():
    deck_of_aces: Deck = Deck(cards=[Card('A', suit) for suit in Card.ALL_SUITS])
    assert [Card('A', '♢'), Card('A', '♣'), Card('A', '♡'), Card('A', '♠')] == list(deck_of_aces)

    deck: Deck = FrenchDeck()

    # the deck contains 52 cards
    assert len(deck) == 52

    # random check if the deck contains a card
    assert Card() in deck

    # test getitem: the last card in the deck is A♠
    assert deck[-1] == Card('A', '♠')

    # test iterable unpacking
    first_card, second_card, *rest_cards = deck
    assert first_card == Card('2', '♢')
    assert second_card == Card('2', '♣')
    assert len(rest_cards) == 50

    # test slicing
    assert deck[0:2] == [Card('2', '♢'), Card('2', '♣')]

    # only keep 7 cards in the deck
    for _ in range(len(deck) - 7):
        deck.popleft()
    expected_shape = strip_shape("""
        ┌─────────┐──┐──┐──┐──┐──┐──┐
        │ K       │  │  │  │  │  │  │
        │ ♣       │  │  │  │  │  │  │
        │         │  │  │...  │  │  │
        │       ♣ │♡ │♠ │  │♣ │♡ │♠ │
        │       K │K │K │  │A │A │A │
        └─────────┘──┘──┘──┘──┘──┘──┘
    """)

    assert deck.gen_shape() == expected_shape

    expected_shape = strip_shape("""
        ┌─────────┐──┐──┐──┐──┐──┐──┐
        │ K       │  │  │  │  │  │  │
        │ ♣       │  │  │  │  │  │  │
        │         │  │  │  │  │  │  │
        │       ♣ │♡ │♠ │♢ │♣ │♡ │♠ │
        │       K │K │K │A │A │A │A │
        └─────────┘──┘──┘──┘──┘──┘──┘
    """)

    assert deck.gen_shape(show_all=True) == expected_shape

    # test user provided cards' shape
    expected_shape = strip_shape("""
        ┌─────────┐   ┌─────────┐   ┌─────────┐
        │ A       │   │ 2       │   │ 3       │
        │ ♠       │   │ ♠       │   │ ♠       │
        │         │   │         │   │         │
        │       ♠ │   │       ♠ │   │       ♠ │
        │       A │   │       2 │   │       3 │
        └─────────┘   └─────────┘   └─────────┘
    """)

    assert deck.gen_shape(Card('A', '♠'), Card('2', '♠'), Card('3', '♠'),
                          space_width=3, show_all=True) == expected_shape

    for _ in range(len(deck)):
        deck.pop()

    assert deck.is_empty()
    assert bool(deck) is False

    deck: Deck = FrenchDeck()
    deck.shuffle()

    num_cards_in_hand = 5
    hand_cards = deck.make_hand(num_cards=num_cards_in_hand)

    assert len(deck) == 52 - num_cards_in_hand
    assert hand_cards[0] not in deck


if __name__ == '__main__':
    # do some basic tests
    test_cards()
    test_deck()

    # do some integration tests here
    # make a deck of cards, shuffle it, and make a hand of 5 cards
    deck: Deck = FrenchDeck()
    print(deck.gen_shape())

    deck.shuffle()
    print(deck.gen_shape())

    hand_cards: list[Card] = deck.make_hand(num_cards=5)
    print(FrenchDeck(cards=hand_cards).sort().gen_shape(space_width=0, show_all=True))
