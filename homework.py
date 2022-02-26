from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:.3f} ч.; '
               'Дистанция: {distance:.3f} км; '
               'Ср. скорость: {speed:.3f} км/ч; '
               'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
    hour_in_min = 60
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return Training.get_distance(self) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass
        # При использовании raise NotImplementedError()
        # не получется пройти автопроверку

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           Training.get_distance(self),
                           self.__class__.get_mean_speed(self),
                           self.__class__.get_spent_calories(self)
                           )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        duration_in_min = self.duration * self.hour_in_min
        return ((self.coeff_calorie_1 * Running.get_mean_speed(self)
                 - self.coeff_calorie_2) * self.weight
                / self.M_IN_KM * duration_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 2
    coeff_calorie_3 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        duration_in_min = self.duration * self.hour_in_min
        return ((self.coeff_calorie_1 * self.weight
                + (SportsWalking.get_mean_speed(self)
                 ** self.coeff_calorie_2 // self.height)
                * self.coeff_calorie_3 * self.weight)
                * duration_in_min)


class Swimming(Training):
    LEN_STEP = 1.38
    coeff_calorie_1 = 1.1
    coeff_calorie_2 = 2
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self):

        return ((Swimming.get_mean_speed(self)
                + self.coeff_calorie_1) * self.coeff_calorie_2
                * self.weight)

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    package_dict = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}

    try:
        return package_dict[workout_type](*data)
    except KeyError:
        print('Неверный ключ')


def main(training: Training) -> None:
    """Главная функция."""
    print(Training.show_training_info(training).get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
