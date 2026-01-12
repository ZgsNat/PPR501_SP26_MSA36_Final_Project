import pytest
from src.usecases.student.create_student import CreateStudentUseCase
from src.domain.entities.student import Student
from src.domain.exceptions.student import StudentAlreadyExistsError, InvalidStudentDataError


def test_create_student_success(mock_uow):
    """Test trường hợp tạo sinh viên thành công"""
    # --- ARRANGE (Chuẩn bị) ---
    # Giả lập: Không tìm thấy sinh viên nào trùng ID (trả về None)
    mock_uow.students.get_by_student_id.return_value = None
    
    # Giả lập: Khi gọi create, trả về đúng object student đó
    # (Side_effect là hành động phụ, ở đây ta chỉ cần nó nhận vào cái gì trả ra cái đó để giả vờ đã lưu)
    def fake_create(student):
        return student
    mock_uow.students.create.side_effect = fake_create

    # Dữ liệu đầu vào
    input_data = {
        "student_id": "SV_TEST_01",
        "full_name": "Nguyen Van Test",
        "email": "test@example.com",
        "phone": "0909000111",
        "birth_date": "01/01/2000",
        "home_town": "Hanoi",
        "math_score": 9.0,
        "literature_score": 8.0,
        "english_score": 7.5
    }

    # --- ACT (Hành động) ---
    use_case = CreateStudentUseCase(mock_uow)
    result = use_case.execute(input_data)

    # --- ASSERT (Kiểm tra kết quả) ---
    # 1. Kiểm tra kết quả trả về có đúng là Student entity không
    assert isinstance(result, Student)
    assert result.student_id == "SV_TEST_01"
    assert result.math_score == 9.0

    # 2. Quan trọng: Kiểm tra xem Use Case có GỌI Repository đúng cách không?
    # "Này mock_uow, mày có thấy hàm get_by_student_id được gọi với tham số 'SV_TEST_01' không?"
    mock_uow.students.get_by_student_id.assert_called_once_with("SV_TEST_01")
    
    # "Này mock_uow, mày có thấy hàm create được gọi 1 lần không?"
    mock_uow.students.create.assert_called_once()

def test_create_student_already_exists(mock_uow):
    """Test trường hợp tạo sinh viên thất bại do trùng student_id"""
    # --- ARRANGE (Chuẩn bị) ---
    # Giả lập: Tìm thấy sinh viên trùng ID (trả về một Student object)
    existing_student = Student(
        student_id="SV_TEST_01",
        full_name="Existing Student",
        email="existing@example.com",
        phone="0909000222",
        birth_date="02/02/2000", 
        home_town="Hanoi",
        math_score=7.0,
        literature_score=6.5,
        english_score=8.0
    )
    mock_uow.students.get_by_student_id.return_value = existing_student
    # Dữ liệu đầu vào
    input_data = {
        "student_id": "SV_TEST_01",
        "full_name": "Nguyen Van Test",
        "email": "test@example.com",
        "phone": "0909000111",
        "birth_date": "01/01/2000",
        "home_town": "Hanoi",
        "math_score": 9.0,
        "literature_score": 8.0,
        "english_score": 7.5
    }
    # --- ACT & ASSERT (Hành động & Kiểm tra kết quả) ---
    use_case = CreateStudentUseCase(mock_uow)
    with pytest.raises(StudentAlreadyExistsError) as exc_info:
        use_case.execute(input_data)
    assert str(exc_info.value) == "Student with ID SV_TEST_01 already exists"
    # Kiểm tra xem get_by_student_id có được gọi đúng không
    mock_uow.students.get_by_student_id.assert_called_once_with("SV_TEST_01")
    # Kiểm tra xem create KHÔNG được gọi
    mock_uow.students.create.assert_not_called()

def test_create_student_with_invalid_data(mock_uow):
    """ Test khởi tạo lỗi sinh viên vì trường thông tin lỗi"""
    mock_uow.students.get_by_student_id.return_value = None

    def fake_create(student):
        return student
    mock_uow.students.create.side_effect = fake_create
    input_data = {
        "student_id": "SV_TEST_02",
        "full_name": "Le Thi Test",
        "email": "<EMAIL>",
        "phone": "0909000333",
        "birth_date": "31-12-2000",  # Định dạng sai
        "home_town": "HCM",
        "math_score": 8.0,
        "literature_score": 7.5,
        "english_score": 9.0
    }
    use_case = CreateStudentUseCase(mock_uow)
    with pytest.raises(InvalidStudentDataError) as exc_info:
        use_case.execute(input_data)
    assert str(exc_info.value) == "Invalid Data! Date must be in dd/mm/yyyy format. Got: 31-12-2000"
    mock_uow.students.get_by_student_id.assert_called_once_with("SV_TEST_02")
    mock_uow.students.create.assert_not_called()

