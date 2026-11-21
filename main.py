from src.core.campus_manager import CampusSystemManager


def main():
    manager = CampusSystemManager("config/settings.json")
    manager.setup_default_gates()

    student = manager.register_student("ST-101", "Олена Ковальчук", "kovalchuk@student.edu", "ІТ", 2)
    prof = manager.register_professor("PR-501", "Іван Петренко", "petrenko@campus.edu", "Кібербезпека")

    manager.create_access_group("Команда хакатону", [student, prof])

    print("\n--- Симуляція проходу через турнікети ---")
    manager.process_student_entry("ST-101", "G-01")    # Успіх (рівень 1 >= 1)
    manager.process_student_entry("ST-101", "G-02")    # Відмова (рівень 1 < 3)
    manager.process_professor_entry("PR-501", "G-02")  # Успіх (рівень 3 >= 3)

    print("\n--- Підсумок ---")
    print(manager.generate_summary_report())


if __name__ == "__main__":
    main()