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

    def add_user(self, user: User): # почему user_id? Как добавить пользователя, зная только его айди?
        UserStorage().storage['FaceNet'] = user

    def get_user(self, user_id: int) -> User:
        for model, user in UserStorage().storage.items():
            if model == FaceVerification.model:
                if user.id == user_id:
                    return user

    def update_user(self, user: User) -> User:
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
        vector = DeepFace.represent(img_path=img_path)
        return self.check_user(user_id, vector)

    def check_user(self, user_id: int, vector: list[float]) -> bool:
        user = self.user_storage.get_user(user_id)
        if user:
            if user.vector == vector:
                verified = True
            else:
                updated_user = User(user_id, True, vector)
                self.user_storage.update_user(updated_user)
                verified = True
        else:
            new_user = User(user_id, True, vector)
            self.user_storage.add_user(new_user)
            verified = True
        return verified


