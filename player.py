# player.py - プレイヤ
#


# 参照
#
import pyxel
from const import Const
from actor import Actor


# プレイヤクラス
#
class Player(Actor):

    # 位置
    __POSITION_X_MIN    = 0.5
    __POSITION_X_MAX    = 31.5
    __POSITION_Y_MIN    = 19.875
    __POSITION_Y_MAX    = 20.875
    __POSITION_ONE      = 8

    # 向き
    __DIRECTION_NULL    = 0
    __DIRECTION_LEFT    = 0
    __DIRECTION_RIGHT   = 0

    # 速度
    __SPEED = 0.25

    # 埋める
    __FILL_DISTANCE = 3

    # 落下
    __FALL          = 0.06125
    __FALL_LEFT     = -4 / 8
    __FALL_TOP      = -7 / 8
    __FALL_RIGHT    =  3 / 8
    __FALL_BOTTOM   =  0 / 8

    # ヒット
    __HIT_LEFT     = -2 / 8
    __HIT_TOP      = -7 / 8
    __HIT_RIGHT    =  1 / 8
    __HIT_BOTTOM   =  0 / 8

    # イメージ
    __IMAGE_BANK    = 0
    __IMAGE_U       = 0
    __IMAGE_V       = 8
    __IMAGE_W       = 8
    __IMAGE_H       = 8
    __IMAGE_LEFT    = -4
    __IMAGE_TOP     = -7
    __IMAGE_RIGHT   = 3
    __IMAGE_BOTTOM  = 0

    # パターン
    __PATTERN_STAY      = 0
    __PATTERN_LEFT      = 1
    __PATTERN_RIGHT     = 4
    __PATTERN_GOAL      = 7
    __PATTERN_FALL      = 7
    __PATTERN_DEAD      = 7

    # アニメーション
    __ANIMATION_WALK    = 3
    __ANIMATION_DEAD    = 5
    __ANIMATION_FRAME   = 4

    # コンストラクタ
    def __init__(self):

        # 処理の初期化
        self.__process = self.idle
        self.__state = 0

        # 位置の初期化
        self.__position_x = Player.__POSITION_X_MIN
        self.__position_y = Player.__POSITION_Y_MIN

        # 向きの初期化
        self.__direction = Player.__DIRECTION_NULL

        # 埋める位置の初期化
        self.__fill = -1

        # パターン
        self.__pattern = 0
        self.__animation = 0

    # フレーム毎の更新を行う
    def update(self):

        # 処理の実行
        if self.__process is not None:
            self.__process()

    # フレーム毎の描画を行う
    def draw(self):

        # プレイヤの描画
        pyxel.blt(self.__position_x * Player.__POSITION_ONE + Player.__IMAGE_LEFT, self.__position_y * Player.__POSITION_ONE + Player.__IMAGE_TOP, Player.__IMAGE_BANK, Player.__IMAGE_U + self.__pattern * Player.__IMAGE_W, Player.__IMAGE_V, Player.__IMAGE_W, Player.__IMAGE_H, pyxel.COLOR_BLACK)

    # 処理を設定する
    def set_process(self, proc):

        # 処理の設定
        self.__process = proc
        self.__state = 0

    # 待機する
    def idle(self):
        pass

    # プレイヤを操作する
    def play(self):

        # 初期化
        if self.__state == 0:

            # 初期化の完了
            self.__state = self.__state + 1

        # 埋める位置のクリア
        self.__fill = -1
        
        # ← キーの入力
        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD_1_LEFT):
            self.__fill = int(self.__position_x) + Player.__FILL_DISTANCE
            pyxel.play(3, Const.SOUND_FILL)

        # → キーの入力
        elif (not pyxel.btn(pyxel.KEY_LEFT) and not pyxel.btn(pyxel.KEY_A) and not pyxel.btn(pyxel.GAMEPAD_1_LEFT)) and (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT)):
            if self.__position_x < Player.__POSITION_X_MAX:
                self.__position_x = min(self.__position_x + Player.__SPEED, Player.__POSITION_X_MAX)
                self.__direction = Player.__DIRECTION_RIGHT
                self.__animation = self.__animation + 1
                if self.__animation >= Player.__ANIMATION_WALK * Player.__ANIMATION_FRAME:
                    self.__animation = 0
                self.__pattern = self.__animation // Player.__ANIMATION_FRAME + Player.__PATTERN_RIGHT
            else:
                self.__animation = 0
                self.__pattern = Player.__PATTERN_STAY

        # 入力なし
        else:
            if self.__position_x > Player.__POSITION_X_MIN:
                self.__position_x = max(self.__position_x - Player.__SPEED, Player.__POSITION_X_MIN)
                self.__direction = Player.__DIRECTION_LEFT
                self.__animation = self.__animation + 1
                if self.__animation >= Player.__ANIMATION_WALK * Player.__ANIMATION_FRAME:
                    self.__animation = 0
                self.__pattern = self.__animation // Player.__ANIMATION_FRAME + Player.__PATTERN_LEFT
            else:
                self.__animation = 0
                self.__pattern = Player.__PATTERN_STAY

        # ゴールの判定
        if self.__position_x >= Player.__POSITION_X_MAX:

            # 処理の更新
            self.set_process(self.goal)

    # プレイヤがゴールする
    def goal(self):

        # 初期化
        if self.__state == 0:

            # パターンの設定
            self.__pattern = Player.__PATTERN_GOAL

            # 初期化の完了
            self.__state = self.__state + 1

    # プレイヤが落下する
    def fall(self):

        # 初期化
        if self.__state == 0:

            # パターンの設定
            self.__pattern = Player.__PATTERN_FALL

            # 初期化の完了
            self.__state = self.__state + 1

        # 位置の更新
        self.__position_y = min(self.__position_y + Player.__FALL, Player.__POSITION_Y_MAX)

        # 落下の完了
        if self.__position_y >= Player.__POSITION_Y_MAX:

            # 処理の更新
            self.set_process(self.idle)

    # プレイヤが死亡する
    def dead(self):

        # 初期化
        if self.__state == 0:

            # アニメーションの設定
            self.__animation = 0

            # 初期化の完了
            self.__state = self.__state + 1

        # アニメーションの更新
        self.__animation = min(self.__animation + 1, Player.__ANIMATION_DEAD * Player.__ANIMATION_FRAME)
        self.__pattern = self.__animation // Player.__ANIMATION_FRAME + Player.__PATTERN_DEAD

        # 死亡の完了
        if self.__animation >= Player.__ANIMATION_DEAD * Player.__ANIMATION_FRAME:

            # 処理の更新
            self.set_process(self.idle)

    # プレイヤの操作を開始する
    def begin_play(self):

        # 処理の更新
        self.set_process(self.play)

    # プレイヤの落下を開始する
    def begin_fall(self):

        # 処理の更新
        self.set_process(self.fall)

    # プレイヤの死亡を開始する
    def begin_dead(self):

        # 処理の更新
        self.set_process(self.dead)

    # プレイヤが待機中かどうかを判定する
    def is_idle(self):

        # 待機の判定
        return self.__process == self.idle

    # プレイヤがゴールしたかどうかを判定する
    def is_goal(self):

        # 待機の判定
        return self.__process == self.goal

    # 穴を埋める位置を取得する
    def get_fill(self):

        # 位置の取得
        return self.__fill

    # 落下の矩形を取得する
    def get_fall_rect(self):

        # 矩形の取得
        return [self.__position_x + Player.__FALL_LEFT, self.__position_y + Player.__FALL_TOP, self.__position_x + Player.__FALL_RIGHT, self.__position_y + Player.__FALL_BOTTOM]

    # ヒットの矩形を取得する
    def get_hit_rect(self):

        # 矩形の取得
        return [self.__position_x + Player.__HIT_LEFT, self.__position_y + Player.__HIT_TOP, self.__position_x + Player.__HIT_RIGHT, self.__position_y + Player.__HIT_BOTTOM]
