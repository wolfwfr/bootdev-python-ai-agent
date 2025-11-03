from subprocess import run
from functions import get_file_content
from functions.get_file_content import get_file_content
from functions.write import write_file
from functions.run_python_file import run_python_file


def test_get_files_info():
    res = get_files_info.get_files_info("calculator", ".")
    print("Result for current directory:")
    print(res)

    print()

    res = get_files_info.get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(res)

    print()

    res = get_files_info.get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(res)

    print()

    res = get_files_info.get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(res)


def test_get_file_content():
    # res = get_file_content.get_file_content("calculator", "lorem.txt")
    # print(res)

    res = get_file_content("calculator", "main.py")
    print("Results for main.py:")
    print(res)
    print()
    res = get_file_content("calculator", "pkg/calculator.py")
    print("Results for pkg/calculator.py:")
    print(res)
    print()
    res = get_file_content("calculator", "/bin/cat")
    print("Results for /bin/cat:")
    print(res)
    print()
    res = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Results for pkg/does_not_exist.py:")
    print(res)


def test_write_file():
    res = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print("Result for lorem.txt:")
    print(res)
    print()

    res = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print("Result for pkg/morelorem.txt")
    print(res)
    print()

    res = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print("Result for /tmp/temp.txt")
    print(res)
    print()


def test_run_python_file():
    res = run_python_file("calculator", "main.py")
    print("Result for main.py:")
    print(res)
    print()
    res = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for main.py with args:")
    print(res)
    print()
    res = run_python_file("calculator", "tests.py")
    print("Result for tests.py:")
    print(res)
    print()
    res = run_python_file("calculator", "../main.py")
    print("Result for ../main.py:")
    print(res)
    print()
    res = run_python_file("calculator", "nonexistent.py")
    print("Result for nonexistent.py:")
    print(res)
    print()
    res = run_python_file("calculator", "lorem.txt")
    print("Result for lorem.txt:")
    print(res)
    print()


# test_get_files_info()
# test_get_file_content()
# test_write_file()
test_run_python_file()
