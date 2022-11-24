# 家具クラス
class Furniture ():
    def __init__(self, material=None, size=0): # self : インスタンス
        print("家具クラスです。")
        self.material = material # プロパティに受け取った引数を代入しているよ
        self.size = size

    def show_material(self):
        print(f'素材は{self.material}です。')

# テーブルクラス
class Table (Furniture): # 家具クラスを継承しているよ
    print("テーブルクラスです。")

    def __init__(self, material, size, leg_num): # 家具としての共通分を引き継ぐ + 脚の本数
        super().__init__(material, size) # 家具クラスのコンストラクタを呼ぶ
        self.leg_num = leg_num

    def show_leg_num(self):
        print(f'脚の本数は{self.leg_num}です。')

# --------メイン関数--------
def main():
        table = Table("木", 160, 4) # インスタンスを作るよ。このとき同時にコンストラクタを呼び出している!
        table.show_material()   
        table.show_leg_num()

if __name__ == "__main__":
    main()