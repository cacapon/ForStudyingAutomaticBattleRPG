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

import datetime
import time
import os

FILEPATH = './savedata.txt'
INTARBAL_GET_EXP = 1  # 秒


def save(player_exp: int):
    # プレイヤーの経験値と現在の時間を保存します
    with open(FILEPATH, mode='w') as f:
        f.write('{},{}'.format(str(player_exp), datetime.datetime.now()))
        print('プレイヤーのデータをセーブしました')


def load() -> list:
    # プレイヤーの経験値とセーブした時間をロードします
    # ファイルが無かったら新しく作ります。

    if not os.path.exists(FILEPATH):
        print('新規でプレイヤーのデータを作成しました')
        save(0)

    with open(FILEPATH, mode='r') as f:
        data = f.read().split(',')
        data[0] = int(data[0])
        data[1] = datetime.datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S.%f')
        print('プレイヤーのデータをロードしました')

    assert type(data[0]) == int
    assert type(data[1]) == datetime.datetime

    return data


def update_exp_for_startup(exp: int, time) -> int:
    # 経過時間から現在の経験値を算出します。
    # exp += (time - 現在時刻) // INTARBAL_GET_EXP * 取得経験値
    dt_now = datetime.datetime.now()
    exp_during_inactive_periods = (dt_now - time).seconds // INTARBAL_GET_EXP * 1  # 1は後で変更する予定
    print('ログアウト期間中に{}の経験値を獲得'.format(exp_during_inactive_periods))
    return exp + exp_during_inactive_periods


if __name__ == "__main__":
    player_data = load()
    player_exp = update_exp_for_startup(player_data[0], player_data[1])

    try:
        while(True):
            player_exp += 1
            print('player exp is {}'.format(player_exp))
            time.sleep(INTARBAL_GET_EXP)
    finally:
        save(player_exp)
