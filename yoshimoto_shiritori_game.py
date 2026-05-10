#!/usr/bin/env python3
"""吉本興業芸人しりとりゲーム（CLI版）

Windowsのexe化は以下で可能:
  pyinstaller --onefile yoshimoto_shiritori_game.py
"""

from __future__ import annotations

import random

COMEDIANS = {
    "あいだみつを": "あいだみつを",
    "あいかわ": "あいかわ",
    "あきな": "あきな",
    "いけだ": "いけだ",
    "いまい": "いまい",
    "うーばーいーつ": "うーばーいーつ",
    "えはら": "えはら",
    "おかだ": "おかだ",
    "かまいたち": "かまいたち",
    "きんぐこんぐ": "きんぐこんぐ",
    "くまだまさし": "くまだまさし",
    "けんどーこばやし": "けんどーこばやし",
    "こっとん": "こっとん",
    "さばんな": "さばんな",
    "しずる": "しずる",
    "すーぱーまりお": "すーぱーまりお",
    "せかいのなべあつ": "せかいのなべあつ",
    "そいつどいつ": "そいつどいつ",
    "だいあん": "だいあん",
    "ちょこれーとぷらねっと": "ちょこれーとぷらねっと",
    "つーとらいぶ": "つーとらいぶ",
    "てんじくねずみ": "てんじくねずみ",
    "とっと": "とっと",
    "なだる": "なだる",
    "にしきごい": "にしきごい",
    "ぬまんづ": "ぬまんづ",
    "ねこにすず": "ねこにすず",
    "のんすたいる": "のんすたいる",
    "はいひーる": "はいひーる",
    "びすけっとぶらざーず": "びすけっとぶらざーず",
    "ふっとぼーるあわー": "ふっとぼーるあわー",
    "へんじがない": "へんじがない",
    "ほんこん": "ほんこん",
    "まぢらぶ": "まぢらぶ",
    "みるくぼーい": "みるくぼーい",
    "むらかみしょーじ": "むらかみしょーじ",
    "めっせんじゃー": "めっせんじゃー",
    "もんすたーえんじん": "もんすたーえんじん",
    "やすとも": "やすとも",
    "ゆにばーす": "ゆにばーす",
    "よしもとしんきげき": "よしもとしんきげき",
    "らんじゃたい": "らんじゃたい",
    "りあるきっず": "りあるきっず",
    "るしふぁーよしおか": "るしふぁーよしおか",
    "れいざーらもん": "れいざーらもん",
    "ろざん": "ろざん",
    "わらいめし": "わらいめし",
}

SMALL_TO_LARGE = str.maketrans({
    "ぁ": "あ", "ぃ": "い", "ぅ": "う", "ぇ": "え", "ぉ": "お",
    "ゃ": "や", "ゅ": "ゆ", "ょ": "よ", "っ": "つ",
    "ゎ": "わ",
})

KATAKANA_TO_HIRAGANA_START = ord("ァ")
KATAKANA_TO_HIRAGANA_END = ord("ヶ")


def normalize(text: str) -> str:
    text = text.strip().lower().replace(" ", "").replace("　", "")
    out = []
    for ch in text:
        code = ord(ch)
        if KATAKANA_TO_HIRAGANA_START <= code <= KATAKANA_TO_HIRAGANA_END:
            out.append(chr(code - 0x60))
        else:
            out.append(ch)
    return "".join(out).translate(SMALL_TO_LARGE)


def tail_char(word: str) -> str:
    if not word:
        return ""
    w = word
    while w and w[-1] in "ー-〜":
        w = w[:-1]
    if not w:
        return ""
    return normalize(w[-1])


def cpu_pick(start: str, used: set[str]) -> str | None:
    choices = [name for name in COMEDIANS if name[0] == start and name not in used and tail_char(name) != "ん"]
    return random.choice(choices) if choices else None


def main() -> None:
    print("=== 吉本興業 芸人しりとり ===")
    print("ひらがな/カタカナで入力してください。終了は quit")
    used: set[str] = set()
    current = random.choice([n for n in COMEDIANS if tail_char(n) != "ん"])
    used.add(current)
    print(f"CPU: {current}")

    while True:
        required = tail_char(current)
        user_raw = input(f"『{required}』ではじまる芸人名 > ")
        user = normalize(user_raw)

        if user in {"quit", "exit", "おわり"}:
            print("ゲーム終了！")
            return
        if not user:
            print("入力が空です。")
            continue
        if user[0] != required:
            print(f"先頭が違います。『{required}』から始めてください。")
            continue
        if user not in COMEDIANS:
            print("登録されていない芸人名です（このゲーム内辞書）。")
            continue
        if user in used:
            print("その芸人はすでに使われています。")
            continue
        if tail_char(user) == "ん":
            print("『ん』で終わったのであなたの負け！")
            return

        used.add(user)
        print(f"あなた: {user}")

        next_start = tail_char(user)
        cpu = cpu_pick(next_start, used)
        if cpu is None:
            print("CPUが答えられません。あなたの勝ち！")
            return
        used.add(cpu)
        current = cpu
        print(f"CPU: {cpu}")


if __name__ == "__main__":
    main()
