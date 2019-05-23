class Pet:
    """
    ペット
    """

    def __init__(self):
        pass

    def cry(self):
        """
        ペットに鳴かせる
        """
        pass

    @classmethod
    def get_pet_type(cls):
        """
        種別名を返す
        Returns:種別名
        """
        return cls.__name__


class Cat(Pet):
    """
    猫
    """

    def cry(self):
        print('にゃー')


class Dog(Pet):
    """
    犬
    """

    def cry(self):
        print('ワン')


class Snake(Pet):
    """
    蛇
    """

    def cry(self):
        print('シャー')


# 扱うペットのクラスリスト
pet_class_list = [Cat, Dog, Snake]
# 扱うペットの種別名リスト
pet_type_name_list = [c.get_pet_type() for c in pet_class_list]
# ペットの種別名とクラスの辞書
type_class_dict = {c.get_pet_type(): c for c in pet_class_list}


def get_pet_type_list():
    """
    ペットの名前のリストを返す。
    Returns:ペットの名前のリスト
    """
    return pet_type_name_list


def create_instance(pet_type):
    """
    引数のペット種別に応じたインスタンスを生成して返す。
    Args:
        pet_type: 種別の文字列
    Returns:インスタンス
    """
    pet_class = type_class_dict[pet_type]
    return pet_class()
