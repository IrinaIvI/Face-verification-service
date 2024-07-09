from deepface import DeepFace


class FaceVerification:
    """Класс обработки фотографии."""

    def embeddings_vec(self, file_name: str) -> list:
        """Генерация вектора на основе фотографии."""
        return DeepFace.represent(img_path=file_name)
