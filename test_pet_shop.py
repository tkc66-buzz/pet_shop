import unittest

import pet
from pet_shop import PetShop


class TestPetShop(unittest.TestCase):
    longMessage = True
    maxDiff = 1000

    def setUp(self):
        self.pet_shop = PetShop()
        self.pet_shop.pet_dict = self.pet_shop.load_pet_num_csv('./test_pet_num.csv')

    def tearDown(self):
        pass

    def test_load_csv_file(self):
        """
        CSVファイルから読み込む。ペットごとの数がファイル内容通りになるか？
        """
        pet_dict = self.pet_shop.load_pet_num_csv('./test_pet_num.csv')

        self.assertSetEqual(set(pet_dict.keys()), set(['Cat', 'Dog', 'Snake']), '種別キー')

        self.assertEqual(len(pet_dict['Cat']), 3, '猫の数')
        self.assertEqual(len(pet_dict['Dog']), 5, '犬の数')
        self.assertEqual(len(pet_dict['Snake']), 1, '蛇の数')

    def test_save_csv_file(self):
        """
        CSVファイルに書き込む。書き込まれたペットごとの数が書き込んだ元の物と一致するか？
        """
        # 初期内容から猫を増やし蛇を減らす
        self.pet_shop.add_pet('Cat')
        self.pet_shop.sell_pet('Snake')
        pet_dict = self.pet_shop.pet_dict

        # 数を保存
        self.pet_shop.save_pet_num_csv('test_pet_num2.csv', pet_dict)

        # 保存した内容を取得し、書き込み前と同じ数が得られるか確認
        saved_dict = self.pet_shop.load_pet_num_csv('test_pet_num2.csv')

        self.assertEqual(len(pet_dict['Cat']), len(saved_dict['Cat']), '猫の数')
        self.assertEqual(len(pet_dict['Dog']), len(saved_dict['Dog']), '犬の数')
        self.assertEqual(len(pet_dict['Snake']), len(saved_dict['Snake']), '蛇の数')


    def test_add_pet(self):
        """
        猫を追加する。猫が1増え、他は元の数のままになるか？
        """
        pet_dict = self.pet_shop.load_pet_num_csv('./test_pet_num.csv')
        self.pet_shop.add_pet('Cat')

        pet_dict = self.pet_shop.pet_dict
        self.assertEqual(len(pet_dict['Cat']), 4, '猫の数')
        self.assertEqual(len(pet_dict['Dog']), 5, '犬の数')
        self.assertEqual(len(pet_dict['Snake']), 1, '蛇の数')

    def test_sell_pet_normal(self):
        """
        猫を売る。猫が1減り、他は元の数のままか？
        """
        sold_pet = self.pet_shop.sell_pet('Cat')

        pet_dict = self.pet_shop.pet_dict
        self.assertEqual(len(pet_dict['Cat']), 2, '猫の数')
        self.assertEqual(len(pet_dict['Dog']), 5, '犬の数')
        self.assertEqual(len(pet_dict['Snake']), 1, '蛇の数')

        self.assertIsInstance(sold_pet, pet.Cat, '猫が売れているか？')

    def test_sell_pet_zero(self):
        """
        1匹だった蛇を売る。0匹になるか？
        """
        sold_pet = self.pet_shop.sell_pet('Snake')

        pet_dict = self.pet_shop.pet_dict
        self.assertEqual(len(pet_dict['Cat']), 3, '猫の数')
        self.assertEqual(len(pet_dict['Dog']), 5, '犬の数')
        self.assertEqual(len(pet_dict['Snake']), 0, '蛇の数')

        self.assertIsInstance(sold_pet, pet.Snake, '蛇が売れているか？')

    def test_sell_pet_minus(self):
        """
        蛇を0匹にし、さらに売る。0のまま維持されるか？
        """
        sold_pet1 = self.pet_shop.sell_pet('Snake')
        sold_pet2 = self.pet_shop.sell_pet('Snake')

        pet_dict = self.pet_shop.pet_dict
        self.assertEqual(len(pet_dict['Cat']), 3, '猫の数')
        self.assertEqual(len(pet_dict['Dog']), 5, '犬の数')
        self.assertEqual(len(pet_dict['Snake']), 0, '蛇の数')

        self.assertIsInstance(sold_pet1, pet.Snake, '蛇が売れているか？')
        self.assertIsNone(sold_pet2, '在庫0で売れないようになっているか？')
