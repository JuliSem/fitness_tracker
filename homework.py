class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,  # Тип тренировки
                 duration: float,  # Продолжительность в ч
                 distance: float,  # Дистанция в км
                 speed: float,  # Скорость км/ч
                 calories: float  # Потраченные ккал
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        msg: str = (f'Тип тренировки: {self.training_type}; '
                    f'Длительность: {self.duration:.3f} ч.; '
                    f'Дистанция: {self.distance:.3f} км ; '
                    f'Ср. скорость: {self.speed:.3f} км/ч; '
                    f'Потрачено ккал: {self.calories:.3f}.')
        return msg


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Длина шага в метрах
    M_IN_KM: int = 1000  # Метров в километре
    MIN_IN_H: int = 60  # Минут в часе
    CM_IN_M: int = 100  # Сантиметров в метре

    def __init__(self,
                 action: int,  # Действие
                 duration: float,  # Продолжительность
                 weight: float  # Вес
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Расчёт калорий при беге."""
        spent_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                 * self.get_mean_speed()
                                 + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.weight / self.M_IN_KM
                                 * self.duration * self.MIN_IN_H)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100
    MIN_IN_H = 60
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчёт калорий при спортивной ходьбе."""
        spent_calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                                 * self.weight + ((self.get_mean_speed()
                                  * self.KMH_IN_MSEC)**2 / (self.height
                                  / self.CM_IN_M))
                                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                 * self.weight) * self.duration
                                 * self.MIN_IN_H)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: float = 2.0
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Расчёт калорий при плавании."""
        spent_calories: float = ((self.get_mean_speed()
                                 + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.CALORIES_WEIGHT_MULTIPLIER
                                 * self.weight * self.duration)
        return spent_calories

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости при плавании."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes: dict = {'SWM': Swimming,
                             'RUN': Running,
                             'WLK': SportsWalking
                             }
    if workout_type not in workout_classes:
        return 'There is no such training'
    return workout_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
