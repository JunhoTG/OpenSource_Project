def get_free_time() -> int:
    print("공강 시간을 분 단위로 입력하세요 (예: 30, 60, 120):")
    while True:
        try:
            free_time = int(input(">>> "))
            if free_time <= 0:
                print("공강 시간은 0분 이상이어야 합니다. 다시 입력하세요.")
            else:
                return free_time
        except ValueError:
            print("유효한 숫자를 입력해주세요.")
