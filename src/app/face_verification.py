from deepface import DeepFace
from dataclasses import dataclass, field


@dataclass
class User:
    """Класс создание пользователя."""

    id: int
    verified: bool = False
    vector: list[float] = field(default_factory=list[float])


class UserStorage:
    """Класс хранилища с пользователями."""

    storage: dict[str, User] = {}

    def add_user(self, user: User):
        """Добавление пользователя в базу."""
        UserStorage().storage['FaceNet'] = user

    def get_user(self, user_id: int) -> User:
        """Получение пользователя по айди."""
        for model, user in UserStorage().storage.items():
            if model == FaceVerification.model:
                if user.id == user_id:
                    return user

    def update_user(self, user: User) -> User:
        """Обновление существующего пользователя."""
        for model, current_user in UserStorage().storage.items():
            if model == FaceVerification.model:
                if current_user.id == user.id:
                    current_user = user
                    return current_user


class FaceVerification:
    """Класс обработки фотографии."""

    user_storage: UserStorage = UserStorage()
    model: str = 'FaceNet'

    def verify(self, user_id: int, img_path: str) -> bool:
        """Верификация пользователя."""
        vector = DeepFace.represent(img_path=img_path)
        return self.check_user(user_id, vector)

    def check_user(self, user_id: int, vector: list[float]) -> bool:
        """Проверка наличия пользователя в базе."""
        verified = False
        user = self.user_storage.get_user(user_id)
        if user:
            if user.vector == vector:
                verified = True
            else:
                verified = True
                updated_user = User(user_id, verified, vector)
                self.user_storage.update_user(updated_user)
        else:
            verified = True
            new_user = User(user_id, verified, vector)
            self.user_storage.add_user(new_user)
        return verified
