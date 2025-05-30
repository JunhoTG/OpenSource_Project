def get_group_size() -> int:
    print("식사 인원 수를 입력하세요 (예: 1, 3, 5):")
    while True:
        try:
            size = int(input(">>> "))
            if size <= 0:
                print("인원 수는 1명 이상이어야 합니다. 다시 입력하세요.")
            else:
                return size
        except ValueError:
            print("유효한 숫자를 입력해주세요.")
