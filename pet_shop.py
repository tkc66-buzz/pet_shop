import csv
import textwrap
from collections import defaultdict

import pet

PET_CSV_PATH = './pet_num.csv'


class PetShop(object):
    """
    ペットショップ。ペットの在庫を管理し、ペットの追加、販売、在庫の表示などをする。
    """

    def __init__(self):
        # 在庫のペットを保持する辞書。{種別名:ペットのリスト}の構造。
        self.pet_dict = None

    def run(self):
        """
        ペットショップを起動する。
        """

        # CSVファイルからペットごとの数を読み込む
        self.pet_dict = self.load_pet_num_csv(PET_CSV_PATH)

        # 終了がユーザから指示されるまで、メニューを繰り返し出す。
        while True:
            quit_app = self.select_menu()
            if quit_app:
                break

        # CSVに結果を書きこむ。
        self.save_pet_num_csv(PET_CSV_PATH, self.pet_dict)

    def load_pet_num_csv(self, file_path):
        """
        ペットの在庫をCSVファイルから読み込む。CSVは "種別, 数" の形式である。
        Args:
            file_path: CSVファイルのパス

        Returns:{種別名:ペットのリスト}の辞書
        """

        pet_dict = defaultdict(list)

        # CSVファイルを開く。
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)

            # CSVの行ごとに、種別と数を取得する。
            for pet_type, pet_num_text in reader:
                pet_num = int(pet_num_text)

                # 種別に対応したインスタンスを、数の分だけ生成して在庫に追加する。
                for n in range(pet_num):
                    pet_instance = pet.create_instance(pet_type)

                    pet_dict[pet_type].append(pet_instance)

        return pet_dict

    def save_pet_num_csv(self, file_path, pet_dict):
        """
        ペットの在庫をCSVファイルへ書き込む。形式はload_pet_csv()に同じ。

        Args:
            file_path: CSVファイルのパス
            pet_dict: {種別名:ペットのリスト}の辞書
        """
        # CSVファイルを開く。
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)

            # 在庫の種別と数を1行ずつ書き込む。
            for pet_type, pet_list in pet_dict.items():
                writer.writerow([pet_type, len(pet_list)])

    def select_menu(self):
        """
        メニューを番号で選択させ、実行する。
        Returns:メニューで終了を指定された場合のみTrue
        """
        quit_app = False

        print('=====================')

        menu_text = textwrap.dedent('''\
            番号を入力してください。
            1.ペットの声を聴く
            2.ペットの数を表示
            3.ペットを追加
            4.ペットを売る
            5.終了
            ''')

        selected_num = self.require_num_input(menu_text, 5)

        # ペットの声を聴く
        if selected_num == 1:
            self.let_pet_cry()
        # ペットの数を表示
        elif selected_num == 2:
            self.display_pet_num()
        # ペットを追加
        elif selected_num == 3:
            # ペットの種別をユーザに選択させる。
            selected_pet_type = self.select_pet_type()

            self.add_pet(selected_pet_type)
        # ペットを売る
        elif selected_num == 4:
            # ペットの種別をユーザに選択させる。
            selected_pet_type = self.select_pet_type()

            self.sell_pet(selected_pet_type)
        # 終了
        elif selected_num == 5:
            print('終了します。')
            quit_app = True

        return quit_app

    def let_pet_cry(self):
        """
        ペットに鳴かせる。
        """
        for pet_type, pet_list in self.pet_dict.items():
            for p in pet_list:
                p.cry()

    def display_pet_num(self):
        """
        ペットの数を表示
        """
        for pet_type, pet_list in self.pet_dict.items():
            print('  {0:5s}: {1}匹'.format(pet_type, len(pet_list)))

    def add_pet(self, pet_type):
        """
        引数の種別のペットを1匹追加する。
        Args:
            pet_type: ペットの種別
        """

        # 選択された種別のペットを生成し、在庫に追加する。
        new_pet = pet.create_instance(pet_type)
        self.pet_dict[pet_type].append(new_pet)

        # 結果を表示する。
        print('{}を追加しました。{}匹になりました。'.format(pet_type, len(self.pet_dict[pet_type])))

    def sell_pet(self, pet_type):
        """
        引数の種別のペットを1匹売る。
        Args:
            pet_type: ペットの種別
        Returns:売られたペット
        """
        # 指定された種別のペットの在庫数を確認。0であればエラー表示して終了。
        current_num = len(self.pet_dict[pet_type])

        if current_num <= 0:
            print('{}は現在0匹です。お売りできません。'.format(pet_type))
            return None

        # 1匹、在庫から取り出して返す。
        sold_pet = self.pet_dict[pet_type].pop()
        print('{}をお買い上げいただきました。{}匹になりました。'.format(pet_type, len(self.pet_dict[pet_type])))
        return sold_pet

    def select_pet_type(self):
        """
        ペットの種別をユーザに選択させ、返す。
        Returns:種別の文字列

        """
        message = 'ペットの種別を選択してください。\n'

        # メッセージに、「番号: ペットの種別」の文字列を種別の分、足す。
        pet_type_list = pet.get_pet_type_list()
        for i, pet_type in enumerate(pet_type_list, 1):
            message += '{}. {}\n'.format(i, pet_type)

        # ユーザにメッセージを見せ、番号を選ばせる。
        type_num = self.require_num_input(message, len(pet_type_list))

        # 番号に応じたペットの種別を返す。
        selected_pet_type = pet_type_list[type_num - 1]
        return selected_pet_type

    @staticmethod
    def require_num_input(message, max_num, min_num=1):
        """
        メッセージ付きで数値入力を促し、入力内容を返す。引数の最大値を超えた値や数値以外が入力された場合は
        再度プロンプトを出す。
        Args:
            message: 表示メッセージ
            max_num: 最大値
            min_num: 最小値
        Returns:入力された値
        """
        # メッセージを表示。
        print(message)

        # 数値入力させる。引数の最大値を超えた値や数値以外が入力された場合は再入力させる。
        while True:
            try:
                input_text = input('>>>')

                input_num = int(input_text)

                if input_num > max_num:
                    print('{}以下で入力してください。'.format(max_num))
                    continue

                if input_num < min_num:
                    print('{}以上で入力してください。'.format(min_num))
                    continue

                return input_num
            except ValueError:
                print('半角数字で入力してください。')


if __name__ == '__main__':
    pet_shop = PetShop()
    pet_shop.run()
