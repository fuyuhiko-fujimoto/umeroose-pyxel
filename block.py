# block.py - ブロック
#


# 参照
#
import pyxel
import random
from actor import Actor


# ブロッククラス
#
class Block(Actor):

    # 位置
    __POSITION_X_MIN    = 5
    __POSITION_X_MAX    = 25
    __POSITION_Y_MIN    = 0
    __POSITION_Y_MAX    = 20

    # 速度
    __SPEED_MIN = 1 / 8
    __SPEED_MAX = 4 / 8

    # イメージ
    __IMAGE_BANK    = 0
    __IMAGE_U       = 16
    __IMAGE_V       = 0
    __IMAGE_W       = 8
    __IMAGE_H       = 8

    # コンストラクタ
    def __init__(self, level):

        # 処理の初期化
        self.__state = 0

        # 位置の初期化
        self.__position_x = 0
        self.__position_y = 0

        # 速度の初期化
        self.__speed = min(Block.__SPEED_MIN + level * (Block.__SPEED_MAX - Block.__SPEED_MIN) / 30, Block.__SPEED_MAX)

        # 掘る位置の初期化
        self.__dig = -1

    # フレーム毎の更新を行う
    def update(self):

        # 初期化
        if self.__state == 0:

            # 位置の設定
            self.__position_x = random.randint(Block.__POSITION_X_MIN, Block.__POSITION_X_MAX)
            self.__position_y = Block.__POSITION_Y_MIN

            # 初期化の完了
            self.__state = self.__state + 1

        # 位置の更新
        self.__position_y = min(self.__position_y + self.__speed, Block.__POSITION_Y_MAX)

        # 掘る位置のクリア
        self.__dig = -1

        # 落下の完了
        if self.__position_y >= Block.__POSITION_Y_MAX:

            # 穴を掘る
            self.__dig = self.__position_x

            # 処理の更新
            self.__state = 0

    # フレーム毎の描画を行う
    def draw(self):

        # ブロックの描画
        if self.__state != 0:
            pyxel.blt((self.__position_x + 0) * Block.__IMAGE_W, self.__position_y * Block.__IMAGE_H, Block.__IMAGE_BANK, Block.__IMAGE_U, Block.__IMAGE_V, Block.__IMAGE_W, Block.__IMAGE_H)
            pyxel.blt((self.__position_x + 3) * Block.__IMAGE_W, self.__position_y * Block.__IMAGE_H, Block.__IMAGE_BANK, Block.__IMAGE_U, Block.__IMAGE_V, Block.__IMAGE_W, Block.__IMAGE_H)

    # 穴を掘る位置を取得する
    def get_dig(self):

        # 位置の取得
        return self.__dig

    # ヒット判定を行う
    def is_hit(self, rect):

        # 左のブロックとの判定
        left = True
        if rect[2] < self.__position_x or self.__position_x + 1 <= rect[0] or rect[3] < self.__position_y or self.__position_y + 1 <= rect[1]:
            left = False
        
        # 右のブロックとの判定
        right = True
        if rect[2] < self.__position_x + 3 or self.__position_x + 4 <= rect[0] or rect[3] < self.__position_y or self.__position_y + 1 <= rect[1]:
            right = False
        
        # 判定の完了
        return left or right
