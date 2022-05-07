# application.py - アプリケーション
#


# 参照
#
import pyxel
from const import Const
from title import Title
from game import Game

# アプリケーションクラス
#
class Application:

    # コンストラクタ
    def __init__(self):

        # Pyxel の初期化
        pyxel.init(256, 168, caption = "Umeroose", scale = 2, fps = 60)

        # シーンの初期化
        self.__scene = None
        self.__trans = Const.SCENE_TITLE

        # リソースの読み込み
        filename = "assets/resource.pyxres"
        pyxel.load(filename)

        # Pyxel の実行
        pyxel.run(self.update, self.draw)

    # フレーム毎の更新を行う
    def update(self):

        # シーンの作成
        if self.__trans is not None:
            if self.__scene is not None:
                del self.__scene
                self.__scene = None
            if self.__trans == Const.SCENE_TITLE:
                self.__scene = Title()
            elif self.__trans == Const.SCENE_GAME:
                self.__scene = Game()
            self.__trans = None

        # シーンの更新
        if self.__scene is not None:
            self.__trans = self.__scene.update()
        
    # フレーム毎の描画を行う
    def draw(self):

        # シーンの描画
        if self.__scene is not None:
            self.__scene.draw()


# アプリケーションのエントリポイント
#
Application()

