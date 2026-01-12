import pytest
from src.usecases.student.update_student import UpdateStudentUseCase
from src.domain.entities.student import Student
from src.domain.exceptions.student import StudentNotFoundError, InvalidStudentDataError


def test_update_student_success(mock_uow):
    """Test trường hợp update sinh viên thành công"""

    # --- ARRANGE ---
    existing_student = Student(
        student_id="SV_TEST_01",
        full_name="Nguyen Van A",
        email="old@example.com",
        phone="0909000000",
        birth_date="01/01/2000",
        home_town="Hanoi",
        math_score=7.0,
        literature_score=7.0,
        english_score=7.0
    )

    # Giả lập tìm thấy sinh viên
    mock_uow.students.get_by_student_id.return_value = existing_student

    # Giả lập update: merge dữ liệu mới vào object cũ
    def fake_update(student_id, update_data):
        for k,_toggle in update_data.items():
            setattr(existing_student, k, _toggle)
        return existing_student

    mock_uow.students.update.side_effect = fake_update

    update_data = {
        "full_name": "Nguyen Van Updated",
        "math_score": 9.5
    }

    # --- ACT ---
    use_case = UpdateStudentUseCase(mock_uow)
    result = use_case.execute("SV_TEST_01", update_data)

    # --- ASSERT ---
    assert isinstance(result, Student)
    assert result.full_name == "Nguyen Van Updated"
    assert result.math_score == 9.5

    mock_uow.students.get_by_student_id.assert_called_once_with("SV_TEST_01")
    mock_uow.students.update.assert_called_once_with(
        "SV_TEST_01",
        {"full_name": "Nguyen Van Updated", "math_score": 9.5}
    )

def test_update_student_success_with_missing_fields(mock_uow):
    """Test update thành công khi chỉ cung cấp một số field"""

    # --- ARRANGE ---
    existing_student = Student(
        student_id="SV_TEST_01",
        full_name="Nguyen Van A",
        email="old@example.com",
        phone="0909000000",
        birth_date="01/01/2000",
        home_town="Hanoi",
        math_score=7.0,
        literature_score=7.0,
        english_score=7.0
    )
    mock_uow.students.get_by_student_id.return_value = existing_student
    def fake_update(student_id, update_data):
        for k, v in update_data.items():
            setattr(existing_student, k, v)
        return existing_student
    mock_uow.students.update.side_effect = fake_update
    update_data = {
        "email": "new@example.com"
    }
    # --- ACT ---
    use_case = UpdateStudentUseCase(mock_uow)
    result = use_case.execute("SV_TEST_01", update_data)
    # --- ASSERT ---
    assert isinstance(result, Student)
    assert result.email == "new@example.com"
    assert result.full_name == "Nguyen Van A"  # không đổi
    mock_uow.students.get_by_student_id.assert_called_once_with("SV_TEST_01")
    mock_uow.students.update.assert_called_once_with(
        "SV_TEST_01",
        {"email": "new@example.com"}
    )

def test_update_student_not_found(mock_uow):
    """Test update thất bại do không tìm thấy sinh viên"""

    # --- ARRANGE ---
    mock_uow.students.get_by_student_id.return_value = None

    update_data = {
        "full_name": "New Name"
    }

    # --- ACT & ASSERT ---
    use_case = UpdateStudentUseCase(mock_uow)
    with pytest.raises(StudentNotFoundError) as exc_info:
        use_case.execute("SV_NOT_EXIST", update_data)

    assert str(exc_info.value) == "Student with ID SV_NOT_EXIST not found"

    mock_uow.students.get_by_student_id.assert_called_once_with("SV_NOT_EXIST")
    mock_uow.students.update.assert_not_called()

def test_update_student_no_fields_provided(mock_uow):
    """Test update thất bại vì không có field nào để update"""

    # --- ARRANGE ---
    existing_student = Student(
        student_id="SV_TEST_01",
        full_name="Nguyen Van A",
        email="a@example.com",
        phone="0909",
        birth_date="01/01/2000",
        home_town="Hanoi",
        math_score=7.0,
        literature_score=7.0,
        english_score=7.0
    )
    mock_uow.students.get_by_student_id.return_value = existing_student

    update_data = {}

    # --- ACT & ASSERT ---
    use_case = UpdateStudentUseCase(mock_uow)
    with pytest.raises(InvalidStudentDataError) as exc_info:
        use_case.execute("SV_TEST_01", update_data)

    assert str(exc_info.value) == "Invalid Data! No fields provided to update"

    mock_uow.students.get_by_student_id.assert_called_once_with("SV_TEST_01")
    mock_uow.students.update.assert_not_called()

def test_update_student_ignore_student_id(mock_uow):
    """Test update bỏ qua student_id trong update_data"""

    # --- ARRANGE ---
    existing_student = Student(
        student_id="SV_TEST_01",
        full_name="Old Name",
        email="old@example.com",
        phone="0909",
        birth_date="01/01/2000",
        home_town="Hanoi",
        math_score=7.0,
        literature_score=7.0,
        english_score=7.0
    )
    mock_uow.students.get_by_student_id.return_value = existing_student

    def fake_update(student_id, update_data):
        for k, v in update_data.items():
            setattr(existing_student, k, v)
        return existing_student

    mock_uow.students.update.side_effect = fake_update

    update_data = {
        "student_id": "HACKED_ID",
        "full_name": "New Name"
    }

    # --- ACT ---
    use_case = UpdateStudentUseCase(mock_uow)
    result = use_case.execute("SV_TEST_01", update_data)

    # --- ASSERT ---
    assert result.student_id == "SV_TEST_01"   # không đổi
    assert result.full_name == "New Name"

    mock_uow.students.update.assert_called_once_with(
        "SV_TEST_01",
        {"full_name": "New Name"}
    )
