#!/usr/bin/env python3
import struct
import zlib
import sys
from pathlib import Path

PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SOI = b"\xFF\xD8"

# SOF-маркеры, в которых у JPEG лежат размеры
SOF_MARKERS = {
    0xC0, 0xC1, 0xC2, 0xC3,
    0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB,
    0xCD, 0xCE, 0xCF,
}


def ask_dim(name: str, old_value: int) -> int:
    """
    Спрашивает у пользователя новое значение размера.
    Пустой ввод — оставить старое значение.
    """
    s = input(f"Новая {name} (Enter, чтобы оставить {old_value}): ").strip()
    if s == "":
        return old_value
    try:
        v = int(s)
        if v <= 0:
            print("Размер должен быть > 0, оставляю старое значение.")
            return old_value
        return v
    except ValueError:
        print("Некорректное число, оставляю старое значение.")
        return old_value


def patch_png_file(in_path: Path):
    data = bytearray(in_path.read_bytes())

    if data[:8] != PNG_SIG:
        raise ValueError("Это не PNG (сигнатура не совпадает)")

    # Первый чанк после сигнатуры — IHDR:
    # [len(4)][type(4)][data(len)][crc(4)]
    off = 8
    length = struct.unpack(">I", data[off:off+4])[0]
    chunk_type = data[off+4:off+8]

    if chunk_type != b"IHDR":
        raise ValueError("Первый чанк не IHDR, странный PNG")

    if length != 13:
        raise ValueError(f"Неожиданная длина IHDR: {length}")

    ihdr_start = off + 8
    ihdr_end = ihdr_start + length
    ihdr = bytearray(data[ihdr_start:ihdr_end])

    old_w, old_h = struct.unpack(">II", ihdr[0:8])
    print(f"[PNG] Текущий размер: {old_w} x {old_h}")

    new_w = ask_dim("ширина", old_w)
    new_h = ask_dim("высота", old_h)

    ihdr[0:4] = struct.pack(">I", new_w)
    ihdr[4:8] = struct.pack(">I", new_h)

    # Пересчёт CRC для IHDR: crc32(type + data)
    new_crc = zlib.crc32(chunk_type + ihdr) & 0xFFFFFFFF

    # Записываем изменённый IHDR и новый CRC обратно
    data[ihdr_start:ihdr_end] = ihdr
    crc_pos = ihdr_end
    data[crc_pos:crc_pos+4] = struct.pack(">I", new_crc)

    out_path = in_path.with_name(f"{in_path.stem}_{new_w}x{new_h}{in_path.suffix}")
    out_path.write_bytes(data)

    print(f"[PNG] Новый размер: {new_w} x {new_h}")
    print(f"[PNG] Файл записан: {out_path}")


def patch_jpeg_file(in_path: Path):
    data = bytearray(in_path.read_bytes())

    if data[:2] != JPEG_SOI:
        raise ValueError("Это не JPEG (нет SOI 0xFFD8)")

    i = 2  # после SOI
    found = False

    while i < len(data):
        # ищем байт маркера 0xFF
        if data[i] != 0xFF:
            i += 1
            continue

        # пропускаем возможные fill-байты 0xFF
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break

        marker = data[i]
        i += 1

        # маркеры без длины (RST, SOI, EOI, TEM)
        if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
            continue

        if i + 2 > len(data):
            break

        seg_len = struct.unpack(">H", data[i:i+2])[0]

        # SOF-сегменты содержат размеры
        if marker in SOF_MARKERS:
            if seg_len < 7:
                raise ValueError("SOF-сегмент слишком короткий")

            # структура: [len_hi len_lo] [precision] [h_hi h_lo] [w_hi w_lo] ...
            p = i + 2
            precision = data[p]
            old_h = struct.unpack(">H", data[p+1:p+3])[0]
            old_w = struct.unpack(">H", data[p+3:p+5])[0]

            print(f"[JPEG] Найден SOF 0xFF{marker:02X}, precision = {precision}")
            print(f"[JPEG] Текущий размер: {old_w} x {old_h}")

            new_w = ask_dim("ширина", old_w)
            new_h = ask_dim("высота", old_h)

            # для JPEG размеры должны влезать в 16 бит
            if new_w > 65535 or new_h > 65535:
                print("Внимание: JPEG хранит размер в 16 бит, "
                      "значения > 65535 будут обрезаны.")
                new_w &= 0xFFFF
                new_h &= 0xFFFF

            data[p+1:p+3] = struct.pack(">H", new_h)
            data[p+3:p+5] = struct.pack(">H", new_w)

            out_path = in_path.with_name(f"{in_path.stem}_{new_w}x{new_h}{in_path.suffix}")
            out_path.write_bytes(data)

            print(f"[JPEG] Новый размер: {new_w} x {new_h}")
            print(f"[JPEG] Файл записан: {out_path}")

            found = True
            break

        # пропускаем сегмент целиком (длина включает сами 2 байта длины)
        i += seg_len

    if not found:
        raise ValueError("SOF-сегмент с размерами не найден (нестандартный JPEG?)")


def main():
    if len(sys.argv) < 2:
        print(f"Использование: {sys.argv[0]} image.(png|jpg|jpeg)")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    if not in_path.is_file():
        print("Файл не найден:", in_path)
        sys.exit(1)

    # читаем пару первых байт, чтобы понять формат
    head = in_path.read_bytes()[:10]

    try:
        if head.startswith(PNG_SIG):
            patch_png_file(in_path)
        elif head.startswith(JPEG_SOI):
            patch_jpeg_file(in_path)
        else:
            print("Неподдерживаемый формат (только PNG и JPEG)")
    except Exception as e:
        print("Ошибка:", e)


if __name__ == "__main__":
    main()
