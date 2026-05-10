#!/usr/bin/env python3
"""吉本興業 芸人しりとり GUI アプリ"""
from __future__ import annotations

import random
import tkinter as tk
from io import BytesIO
from tkinter import messagebox
from urllib.request import urlopen

COMEDIANS: dict[str, dict[str, str]] = {
    "かまいたち": {"display": "かまいたち", "image": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Kamaitachi_2018.jpg"},
    "ちょこれーとぷらねっと": {"display": "チョコレートプラネット", "image": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Chocolate_Planet_2019.jpg"},
    "のんすたいる": {"display": "NON STYLE", "image": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Nonstyle_2017.jpg"},
    "みるくぼーい": {"display": "ミルクボーイ", "image": "https://upload.wikimedia.org/wikipedia/commons/7/70/Milkboy_2019.jpg"},
    "ろざん": {"display": "ロザン", "image": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Rozan_2018.jpg"},
    "にしきごい": {"display": "錦鯉", "image": "https://upload.wikimedia.org/wikipedia/commons/d/dd/Nishikigoi_2022.jpg"},
    "だいあん": {"display": "ダイアン", "image": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Diane_2018.jpg"},
    "しずる": {"display": "しずる", "image": "https://upload.wikimedia.org/wikipedia/commons/8/88/Shizuru_2018.jpg"},
    "きんぐこんぐ": {"display": "キングコング", "image": "https://upload.wikimedia.org/wikipedia/commons/8/89/Kingkong_2016.jpg"},
    "わらいめし": {"display": "笑い飯", "image": "https://upload.wikimedia.org/wikipedia/commons/5/59/Waraimeshi_2018.jpg"},
}

SMALL_TO_LARGE = str.maketrans({"ぁ": "あ", "ぃ": "い", "ぅ": "う", "ぇ": "え", "ぉ": "お", "ゃ": "や", "ゅ": "ゆ", "ょ": "よ", "っ": "つ", "ゎ": "わ"})


def normalize(text: str) -> str:
    text = text.strip().lower().replace(" ", "").replace("　", "")
    chars = []
    for ch in text:
        o = ord(ch)
        if ord("ァ") <= o <= ord("ヶ"):
            chars.append(chr(o - 0x60))
        else:
            chars.append(ch)
    return "".join(chars).translate(SMALL_TO_LARGE)


def tail_char(word: str) -> str:
    w = word
    while w and w[-1] in "ー-〜":
        w = w[:-1]
    return normalize(w[-1]) if w else ""


class ShiritoriApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("吉本興業 芸人しりとり")
        root.geometry("580x520")

        self.used: set[str] = set()
        self.current = random.choice([k for k in COMEDIANS if tail_char(k) != "ん"])
        self.used.add(self.current)
        self.img_cache: dict[str, tk.PhotoImage] = {}

        self.status = tk.StringVar(value="CPUのターン")
        self.prompt = tk.StringVar()

        tk.Label(root, text="吉本興業 芸人しりとり", font=("Meiryo", 20, "bold")).pack(pady=8)
        tk.Label(root, textvariable=self.status, fg="#2a4").pack()

        self.image_label = tk.Label(root, width=500, height=280, bg="#eee")
        self.image_label.pack(padx=8, pady=8)

        self.name_label = tk.Label(root, font=("Meiryo", 14, "bold"))
        self.name_label.pack()

        tk.Label(root, textvariable=self.prompt, font=("Meiryo", 12)).pack(pady=10)

        self.entry = tk.Entry(root, font=("Meiryo", 14), width=22)
        self.entry.pack()
        self.entry.bind("<Return>", lambda _: self.submit())

        tk.Button(root, text="回答", command=self.submit).pack(pady=6)
        tk.Button(root, text="終了", command=root.destroy).pack()

        self.show_comedian(self.current, "CPU")

    def fetch_image(self, url: str) -> tk.PhotoImage | None:
        if url in self.img_cache:
            return self.img_cache[url]
        try:
            with urlopen(url, timeout=10) as r:
                data = r.read()
            img = tk.PhotoImage(data=BytesIO(data).getvalue())
            self.img_cache[url] = img
            return img
        except Exception:
            return None

    def show_comedian(self, key: str, who: str) -> None:
        meta = COMEDIANS[key]
        self.status.set(f"{who}: {meta['display']}")
        self.name_label.config(text=meta["display"])
        img = self.fetch_image(meta["image"])
        if img:
            self.image_label.configure(image=img, text="")
            self.image_label.image = img
        else:
            self.image_label.configure(image="", text="画像の読み込みに失敗しました", font=("Meiryo", 14), bg="#f9d")
        self.prompt.set(f"『{tail_char(key)}』ではじまる芸人名を入力")

    def submit(self) -> None:
        user = normalize(self.entry.get())
        self.entry.delete(0, tk.END)
        if not user:
            return

        required = tail_char(self.current)
        if user[0] != required:
            messagebox.showwarning("不正解", f"『{required}』から始めてください")
            return
        if user not in COMEDIANS:
            messagebox.showwarning("未登録", "このアプリの辞書にない芸人名です")
            return
        if user in self.used:
            messagebox.showwarning("使用済み", "その芸人名はすでに使われています")
            return
        if tail_char(user) == "ん":
            messagebox.showinfo("ゲーム終了", "語尾が『ん』なのであなたの負けです")
            self.root.destroy()
            return

        self.used.add(user)
        self.show_comedian(user, "あなた")

        start = tail_char(user)
        cpu_choices = [k for k in COMEDIANS if k not in self.used and k[0] == start and tail_char(k) != "ん"]
        if not cpu_choices:
            messagebox.showinfo("勝利", "CPUが答えられません。あなたの勝ち！")
            self.root.destroy()
            return

        self.current = random.choice(cpu_choices)
        self.used.add(self.current)
        self.show_comedian(self.current, "CPU")


def main() -> None:
    root = tk.Tk()
    ShiritoriApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
