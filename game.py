# game.py - ゲーム
#


# 参照
#
import pyxel
from const import Const
from actor import Actor
from stage import Stage
from player import Player


# ゲームクラス
#
class Game(Actor):

    # コンストラクタ
    def __init__(self):

        # 処理の初期化
        self.__process = self.start
        self.__state = 0

        # 更新の初期化
        self.__updates = []

        # 描画の初期化
        self.__draws = []

        # ワールドの初期化
        self.__world = 0

        # スコアの初期化
        self.__score = 0

        # ステージの初期化
        self.__stage = None

        # プレイヤの初期化
        self.__player = None

        # フレームの初期化
        self.__frame = 0
        
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

    # ゲームを開始する
    def start(self):

        # 初期化
        if self.__state == 0:

            # ワールドの更新
            self.__world = self.__world + 1

            # レベルの取得
            level = self.__world - 1

            # ステージの作成
            self.__stage = Stage(level)

            # プレイヤの作成
            self.__player = Player()

            # フレームの設定
            self.__frame = 75

            # 更新の設定
            self.__updates.clear()
            self.__updates.append(self.__stage.update)
            self.__updates.append(self.__player.update)

            # 描画の設定
            self.__draws.clear()
            self.__draws.append(self.__stage.draw)
            self.__draws.append(self.__player.draw)
            self.__draws.append(self.print_start)

            # ミュージックの再生
            pyxel.playm(Const.MUSIC_START)

            # 初期化の完了
            self.__state = self.__state + 1
        
        # 更新の実行
        self.execute_updates()

        # フレームの更新
        self.__frame = self.__frame - 1
        if self.__frame <= 0:

            # 処理の更新
            self.set_process(self.play)

    # ゲームをプレイする
    def play(self):

        # 初期化
        if self.__state == 0:

            # 操作の開始
            self.__stage.begin()
            self.__player.begin_play()

            # 更新の設定
            self.__updates.clear()
            self.__updates.append(self.__stage.update)
            self.__updates.append(self.__player.update)

            # 描画の設定
            self.__draws.clear()
            self.__draws.append(self.__stage.draw)
            self.__draws.append(self.__player.draw)

            # 初期化の完了
            self.__state = self.__state + 1

        # 更新の実行
        self.execute_updates()

        # 穴を埋める
        self.__stage.fill(self.__player.get_fill())

        # ゴールしたかどうか
        if self.__player.is_goal():

            # 処理の更新
            self.set_process(self.goal)

        # 落下したかどうか
        elif self.__stage.is_fall(self.__player.get_fall_rect()):

            # プレイヤの落下
            self.__player.begin_fall()

            # 処理の更新
            self.set_process(self.over)

        # ブロックにぶつかったかどうか
        elif self.__stage.is_hit(self.__player.get_hit_rect()):

            # プレイヤの死亡
            self.__player.begin_dead()

            # 処理の更新
            self.set_process(self.over)

    # ゴールする
    def goal(self):

        # 初期化
        if self.__state == 0:

            # フレームの設定
            self.__frame = 360

            # 操作の停止
            self.__stage.pause()

            # 更新の設定
            self.__updates.clear()
            self.__updates.append(self.__stage.update)
            self.__updates.append(self.__player.update)

            # 描画の設定
            self.__draws.clear()
            self.__draws.append(self.__stage.draw)
            self.__draws.append(self.__player.draw)
            self.__draws.append(self.print_goal)

            # ミュージックの再生
            pyxel.playm(Const.MUSIC_GOAL)

            # 初期化の完了
            self.__state = self.__state + 1

        # 更新の実行
        self.execute_updates()

        # フレームの更新
        self.__frame = self.__frame - 1
        if self.__frame <= 0:

            # ステージの破棄
            del self.__stage
            self.__stage = None

            # プレイヤの破棄
            del self.__player
            self.__player = None

            # 描画のクリア
            self.__draws.clear()

            # 処理の更新
            self.set_process(self.start)

    # ゲームオーバーになる
    def over(self):

        # 初期化
        if self.__state == 0:

            # スコアの設定
            self.__score = max((self.__world - 1) * 10, 0)

            # 操作の停止
            self.__stage.pause()

            # 更新の設定
            self.__updates.clear()
            self.__updates.append(self.__stage.update)
            self.__updates.append(self.__player.update)

            # 描画の設定
            self.__draws.clear()
            self.__draws.append(self.__stage.draw)
            self.__draws.append(self.__player.draw)

            # ミュージックの再生
            pyxel.playm(Const.MUSIC_OVER)

            # 初期化の完了
            self.__state = self.__state + 1

        # 更新の実行
        self.execute_updates()

        # プレイヤの完了
        if self.__player.is_idle():

            # ゲームオーバーの描画
            if not self.print_over in self.__draws:
                self.__draws.append(self.print_over)

            # SPACE キーの入力
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD_1_A):

                # 描画のクリア
                self.__draws.clear()

                # サウンドの再生
                # pyxel.play(3, Const.SOUND_CLICK)

                # シーンの遷移
                self.__result = Const.SCENE_TITLE

    # ゲームの開始を描画する
    def print_start(self):

        # テキストの描画
        self.print_text((pyxel.height - pyxel.FONT_HEIGHT) / 2, "WORLD {0}".format(self.__world))

    # ゴールを描画する
    def print_goal(self):

        # テキストの描画
        self.print_text((pyxel.height - pyxel.FONT_HEIGHT) / 2, "YOU ARE GOOD!")

    # ゲームオーバーを描画する
    def print_over(self):

        # テキストの描画
        self.print_text((pyxel.height - pyxel.FONT_HEIGHT) * 2 / 5, "GAME OVER!!")
        self.print_text((pyxel.height - pyxel.FONT_HEIGHT) * 3 / 5, "SCORE {0}".format(self.__score))

    # テキストを描画する
    def print_text(self, y, s):

        # テキストの描画
        w = len(s) * pyxel.FONT_WIDTH
        h = pyxel.FONT_HEIGHT
        x = (pyxel.width - w) / 2
        pyxel.rect(x - 1, y - 1, w + 2, h + 2, pyxel.COLOR_BLACK)
        pyxel.text(x, y, s, pyxel.COLOR_WHITE)

