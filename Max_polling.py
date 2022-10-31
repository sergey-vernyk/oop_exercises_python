import numpy as np


class MaxPooling:
    def __init__(self, step=(2, 2), size=(2, 2)):  # step - stride size; size - pool size
        self.step = step
        self.size = size

    def __call__(self, mtx, **kwargs):
        if not all(len(row) == len(mtx[0]) for row in mtx): # если матрица не прямоугольная
            raise ValueError("Неверный формат для первого параметра matrix.")
        for row in mtx:
            if not isinstance(row, list):
                raise ValueError("Неверный формат для первого параметра matrix.")
            for element in row:
                if not isinstance(element, (int, float)):
                    raise ValueError("Неверный формат для первого параметра matrix.")

        pools = self.get_pools(mtx, self.size, self.step)
        return self.max_pooling(pools)

    @staticmethod
    def max_pooling(array_pools: list) -> list:
        """Метод для создания результирующей матрицы
        с максимальными значениями в окнах размера size"""
        result = []
        i = 0  # переменная для размера выходной матрицы
        for pool in array_pools:
            result.append(np.max(pool))
            i += 1

        res_array = np.array(result).reshape((int(i ** 0.5), int(i ** 0.5)))  # результирующая матрица
        return res_array.tolist()  # преобразование из объекта numpy в обычный список перед возвратом

    @staticmethod
    def get_pools(array: list, size: tuple, step: tuple) -> list:
         """Метод для получения матриц из окна, размером size * size, 
         с шагом step"""
        conv_output = np.array(array)  # преобразование в объект матриц numpy
        pools = []
        for i in np.arange(conv_output.shape[0], step=step[0]):
            for j in np.arange(conv_output.shape[0], step=step[1]):
                matrix = conv_output[i:i + size[0], j:j + size[1]]
                if matrix.shape == (size[0], size[1]):  # если матрица нужного размера
                    pools.append(matrix)

        return pools
