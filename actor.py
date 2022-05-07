# actor.py - アクタクラス
#


# 参照
#
import pyxel
from abc import ABC, abstractmethod


# アクタクラス
#
class Actor(ABC):

    # フレーム毎の更新を行う
    @abstractmethod
    def update(self):
        pass

    # フレーム毎の描画を行う
    @abstractmethod
    def draw(self):
        pass
    
