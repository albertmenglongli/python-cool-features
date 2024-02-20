# python-cool-features

[中文说明](README.zh.md)

This project is an implementation of a deck of cards in Python. It is a standard 52 card deck, with 4 suits, and 13 cards in each suit. The cards can be shuffled, and drawn from the deck.

## Features

The project demonstrates many Python features introduced from Python 3.6 to 3.12:

1. PEP 634: Structural Pattern Matching: match case
2. PEP 572: Assignment Expressions: walrus operator
3. New annotations, such as: str | int, list[str] | None, etc.
4. PEP 616: String methods to remove prefixes and suffixes: str.removeprefix(), str.removesuffix()
5. f-string: f"{variable=}" to print variable name and value, f"{variable!r}" to print variable name and repr(variable), f"{variable:<8}" to align left, f"{variable:>8}" to align right, f"{variable:^8}" to align center
6. dataclasses: dataclass, field, ClassVar, \__post_init\__
7. str.center(width, fill_char)
8. dict new features
9. etc.

## Classes

The project includes the following classes:

- `SUIT`: An enumeration representing the four suits of a deck of cards.
- `Card`: A class representing a playing card, with a rank and a suit.
- `Deck`: A class representing a deck of cards.
- `FrenchDeck`: A subclass of `Deck` that generates a standard 52 card deck.

## Usage

To use the deck of cards, create an instance of `FrenchDeck`, shuffle it, and draw cards:

```python
deck = FrenchDeck()
deck.shuffle()
hand: list[Card] = deck.make_hand(num_cards=5)
```

```
┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐
│ 7       ││ 8       ││ J       ││ Q       ││ K       │
│ ♣       ││ ♣       ││ ♠       ││ ♠       ││ ♣       │
│         ││         ││         ││         ││         │
│       ♣ ││       ♣ ││       ♠ ││       ♠ ││       ♣ │
│       7 ││       8 ││       J ││       Q ││       K │
└─────────┘└─────────┘└─────────┘└─────────┘└─────────┘
```


## Requirements

This script requires Python 3.12 or later.