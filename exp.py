'''
    経験値取得ロジック　二種類の取得方法がある。
        ・アクティブ化時　※初回起動除く
            (ログアウト時間(秒) - ログイン時間(秒)) // 経験値取得間隔(秒) * ステージ平均経験値
        ・起動中
            戦闘勝利判定が発生したタイミングで経験値を取得する

        ※アクティブ化とは、ログイン、もしくはウィンドウを開いた状態にすることを指す。

    実現に必要だと思われる機能
        ・関数　セーブ機能（辞書：セーブデータ)
            以下を記録してテキストファイルに出力
            ー　ログアウト時間
            ー　プレイヤー経験値

        ・関数　ロード機能（文字：ファイルパス）　→　辞書
            以下をテキストファイルから取得する
            ー　ログアウト時間
            ー　プレイヤー経験値

        ・関数：アクティブ中の経験値取得（）　→　数値
            現在時刻　％　経験値取得タイミング　＝　0　なら
            プレイヤー経験値を増やす
            例：9:00:15 間隔10秒だと増やさない
            例：9:00:15 間隔15秒だと増やす

        ・関数：アクティブ化時の経験値取得（ログアウト時間　ログイン時間　経験値取得間隔　平均経験値）→　数値
            (ログアウト時間(秒) - ログイン時間(秒)) // 経験値取得間隔(秒) * ステージ平均経験値
            で計算し、経験値を返す

        ・関数：ログアウト・非アクティブ判定（）
            ログアウトしたか、非アクティブになった場合、
            セーブ機能を働かせる。

        ・変数：プレイヤー経験値
        ・変数：経験値取得間隔
        ・変数：現在の時間
        ・変数：ファイルパス

'''

import time
import os

FILEPATH = './savedata.txt'


def save(player_exp: int):
    # プレイヤーの経験値を保存します
    with open(FILEPATH, mode='w') as f:
        f.write(str(player_exp))
        print('player exp saved')


def load():
    # プレイヤーの経験値をロードします
    # ファイルが無かったら新しく作ります。
    if not os.path.exists(FILEPATH):
        with open(FILEPATH, mode='w') as f:
            f.write(str(0))

    with open(FILEPATH, mode='r') as f:
        data = int(f.read())
    return data


if __name__ == "__main__":
    player_exp = load()
    intarbal_get_exp = 1  # 秒
    try:
        while(True):
            player_exp += 1
            print('player exp is {}'.format(player_exp))
            time.sleep(intarbal_get_exp)
    finally:
        save(player_exp)
