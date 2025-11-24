import zipfile
from pathlib import Path
import io

def read_nested_zip_chars(path, inner_name="boom.zip", max_depth=5000):
    data = Path(path).read_bytes()
    chars = []
    depth = 0

    while True:
        # открываем текущий zip из памяти
        zf = zipfile.ZipFile(io.BytesIO(data), "r")
        names = zf.namelist()

        # берём "не boom.zip" — там как раз имя-символ: ".Z", ".i", ". "
        non_boom = [n for n in names if n != inner_name]
        if non_boom:
            name = non_boom[0]
            # у тебя они начинаются с точки, типа ".Z"
            ch = name[1:] if name.startswith(".") else name
            chars.append(ch)

        # если есть следующий boom.zip — идём дальше
        if inner_name in names and depth < max_depth:
            data = zf.read(inner_name)
            depth += 1
        else:
            break

    return "".join(chars)

if __name__ == "__main__":
    text = read_nested_zip_chars("bomb")  # или путь к твоему файлу
    print(text)
