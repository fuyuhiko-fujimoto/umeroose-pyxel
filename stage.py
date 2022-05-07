# stage.py - ステージ
#


# 参照
#
import pyxel
from actor import Actor
from block import Block


# ステージクラス
#
class Stage(Actor):

    # 床
    __FLOOR_NULL    = 0
    __FLOOR_BLOCK   = 1
    __FLOOR_LENGTH  = 32
    __FLOOR_HEAD    = 24
    __FLOOR_TAIL    = 27
    __FLOOR_LIMIT   = 10
    __FLOOR_X       = 0
    __FLOOR_Y       = 160

    # 天井
    __CEIL_X    = 0
    __CEIL_Y    = 0
    
    # イメージ
    __IMAGE_BANK    = 0
    __IMAGE_U       = 0
    __IMAGE_V       = 0
    __IMAGE_W       = 8
    __IMAGE_H       = 8

    # コンストラクタ
    def __init__(self, level):

        # 処理の初期化
        self.__state = 0

        # 床の初期化
        self.__floor = [Stage.__FLOOR_BLOCK] * Stage.__FLOOR_LENGTH

        # ブロックの初期化
        self.__block = Block(level)

        # 停止の初期化
        self.__pause = True

        # ステージの作成
        self.build(level)

    # フレーム毎の更新を行う
    def update(self):

        # 初期化
        if self.__state == 0:

            # 初期化の完了
            self.__state = self.__state + 1

        # ブロックの更新
        if not self.__pause:
            self.__block.update()
            self.dig(self.__block.get_dig())

    # フレーム毎の描画を行う
    def draw(self):

        # 床の描画
        for i in range(Stage.__FLOOR_LENGTH):
            b = 0b000
            if self.__floor[i] == Stage.__FLOOR_BLOCK:
                b = 0b100
                if i == 0 or self.__floor[i - 1] == Stage.__FLOOR_BLOCK:
                    b = b | 0b001
                if i == Stage.__FLOOR_LENGTH - 1 or self.__floor[i + 1] == Stage.__FLOOR_BLOCK:
                    b = b | 0b010
            pyxel.blt(Stage.__FLOOR_X + i * Stage.__IMAGE_W, Stage.__FLOOR_Y, Stage.__IMAGE_BANK, Stage.__IMAGE_U + b * Stage.__IMAGE_W, Stage.__IMAGE_V, Stage.__IMAGE_W, Stage.__IMAGE_H)

        # ブロックの描画
        self.__block.draw()

        # 天井の描画
        for i in range(Stage.__FLOOR_LENGTH):
            pyxel.blt(Stage.__CEIL_X + i * Stage.__IMAGE_W, Stage.__CEIL_Y, Stage.__IMAGE_BANK, Stage.__IMAGE_U + 0b001 * Stage.__IMAGE_W, Stage.__IMAGE_V, Stage.__IMAGE_W, Stage.__IMAGE_H)

    # ステージを作成する
    def build(self, level):

        # 床の作成
        head = max(Stage.__FLOOR_HEAD - (level), Stage.__FLOOR_LIMIT)
        for i in range(head, Stage.__FLOOR_TAIL + 1):
            self.__floor[i] = Stage.__FLOOR_NULL

    # ステージの操作を開始する
    def begin(self):

        # 停止の更新
        self.__pause = False

    # ステージの操作を停止する
    def pause(self):

        # 停止の更新
        self.__pause = True

    # 穴を掘る
    def dig(self, position):

        # 床の更新
        if 0 <= position and position <= Stage.__FLOOR_LENGTH - 4:
            self.__floor[position + 0] = Stage.__FLOOR_BLOCK
            self.__floor[position + 1] = Stage.__FLOOR_NULL
            self.__floor[position + 2] = Stage.__FLOOR_NULL
            self.__floor[position + 3] = Stage.__FLOOR_BLOCK

    # 穴を埋める
    def fill(self, position):

        # 床の更新
        if 0 <= position and position < Stage.__FLOOR_LENGTH:
            self.__floor[position] = Stage.__FLOOR_BLOCK

    # 落下するかどうか
    def is_fall(self, rect):

        # 床との判定
        return self.__floor[int(rect[0])] == Stage.__FLOOR_NULL and self.__floor[int(rect[2])] == Stage.__FLOOR_NULL

    # ブロックにぶつかったかどうか
    def is_hit(self, rect):

        # ブロックとの判定
        return (self.__block is not None) and self.__block.is_hit(rect)


