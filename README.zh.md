# python-cool-features

[English README](README.md)

这个项目是用Python实现的一副扑克牌。它是一副标准的52张牌，有4种花色，每种花色有13张牌。这些牌可以被洗牌，并从牌堆中抽出。

## 特性

该项目展示了从Python 3.6到3.12引入的许多Python特性：

1. PEP 634：结构模式匹配：匹配案例
2. PEP 572：赋值表达式：海象运算符
3. 新的注释，例如：str | int, list[str] | None等
4. PEP 616：删除前缀和后缀的字符串方法：str.removeprefix(), str.removesuffix()
5. f-string：f"{variable=}"打印变量名和值，f"{variable!r}"打印变量名和repr(variable)，f"{variable:<8}"左对齐，f"{variable:>8}"右对齐，f"{variable:^8}"居中对齐
6. 数据类：dataclass, field, ClassVar, \__post_init\__
7. str.center(width, fill_char)
8. 字典的新特性
9. 等等。

## 类

该项目包括以下类：

- `SUIT`：表示一副牌的四种花色的枚举。
- `Card`：表示一张扑克牌，有一个等级和一个花色。
- `Deck`：表示一副牌的类。
- `FrenchDeck`：`Deck`的子类，生成一副标准的52张牌。

## 使用

要使用这副牌，创建一个`FrenchDeck`的实例，洗牌，然后抽牌：

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


## 要求

这个脚本需要Python 3.12或更高版本。