# title.py - タイトル
#


# 参照
#
import pyxel
from const import Const
from actor import Actor


# タイトルクラス
#
class Title(Actor):

    # コンストラクタ
    def __init__(self):

        # 処理の初期化
        self.__process = self.idle
        self.__state = 0

        # 更新の初期化
        self.__updates= []

        # 描画の初期化
        self.__draws = []

        # フレームの初期化
        self.__frame = 0
        
        # 点滅の初期化
        self.__blink = 0

        # 結果の初期化
        self.__result = None

    # フレーム毎の更新を行う
    def update(self):

        # 処理の実行
        if self.__process is not None:
            self.__process()

        # 終了
        return self.__result

    # フレーム毎の描画を行う
    def draw(self):

        # 画面のクリア
        pyxel.cls(pyxel.COLOR_BLACK)

        # 描画の実行
        self.execute_draws()

    # 処理を設定する
    def set_process(self, process):

        # 処理の設定
        self.__process = process
        self.__state = 0

    # 更新を実行する
    def execute_updates(self):

        # 更新の実行
        for method in self.__updates:
            method()

    # 描画を実行する
    def execute_draws(self):

        # 描画の実行
        for method in self.__draws:
            method()

    # 待機する
    def idle(self):

        # 初期化
        if self.__state == 0:

            # 更新の設定
            self.__updates.clear()

            # 描画の設定
            self.__draws.clear()
            self.__draws.append(self.print_title)
            self.__draws.append(self.print_hit_space_bar)

            # 初期化の完了
            self.__state = self.__state + 1

        # 更新の実行
        self.execute_updates()

        # SPACE キーの入力
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD_1_A):

            # 処理の更新
            self.set_process(self.start)

        # 点滅の更新
        self.__blink = self.__blink + 1

    # ゲームを開始する
    def start(self):

        # 初期化
        if self.__state == 0:

            # フレームの設定
            self.__frame = 0

            # サウンドの再生
            pyxel.play(3, Const.SOUND_BOOT)

            # 更新の設定
            self.__updates.clear()

            # 描画の設定
            self.__draws.clear()
            self.__draws.append(self.print_title)
            self.__draws.append(self.print_hit_space_bar)

            # 初期化の完了
            self.__state = self.__state + 1

        # 更新の実行
        self.execute_updates()

        # フレームの更新
        self.__frame = self.__frame + 1
        if self.__frame > 90:

            # シーンの遷移
            self.__result = Const.SCENE_GAME

        # 点滅の更新
        self.__blink = self.__blink + 8

    # タイトルを描画する
    def print_title(self):

        # タイトルの描画
        s = "UMEROOSE"
        pyxel.text((pyxel.width - len(s) * pyxel.FONT_WIDTH) / 2, pyxel.height * 1 / 3 - pyxel.FONT_HEIGHT, s, pyxel.COLOR_WHITE)

    # HIT SPACE BAR を描画する
    def print_hit_space_bar(self):

        # HIT SPACE BAR の描画
        if (self.__blink & 0x20) == 0:
            s = "HIT SPACE BAR"
            pyxel.text((pyxel.width - len(s) * pyxel.FONT_WIDTH) / 2, pyxel.height * 2 / 3 - pyxel.FONT_HEIGHT, s, pyxel.COLOR_WHITE)
