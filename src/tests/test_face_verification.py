from app.face_verification import FaceVerification
import pytest
from pytest_mock import MockerFixture


@pytest.mark.parametrize('file_name', [
    pytest.param('img_path.jpg', id='is correct'),
    pytest.param('', id='is not correct', marks=pytest.mark.xfail()),
    pytest.param('img', id='is not correct', marks=pytest.mark.xfail())
])
def test_embeddings_vec(file_name, mocker: MockerFixture):
    vector = mocker.patch('app.face_verification.DeepFace.represent', return_value = [1,2,3,4,5,6])
    assert FaceVerification().embeddings_vec(file_name) == [1,2,3,4,5,6]
    vector.assert_called_once()
