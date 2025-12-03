# Украденный флаг
## Overview

**Категория:** Forensic  
**Описание:** Злоумышленники нашли уязвимость в поисковой строке сайта и с помощью слепой sql-инъекции украли флаг из БД, а потом стерли его.  
Из логов есть только access-лог nginx. Попробуйте понять какой флаг был украден.
**Сложность:** Medium

---
## Анализ

### Разведка

Что было выдано:
- Архив: `bug-makers.ru-access.log.zip`
- Внутри: `bug-makers.ru-access.log`

Первичный осмотр первых строк лога:
- Много запросов к `/search?q=1 ...`
- User-Agent: `sqlmap/1.9.6#stable`
- Запросы с `SLEEP(5)`, `RANDOMBLOB`, `SELECT 0x...` — классическая time-based blind SQLi.

### Детальный анализ
1. **Наивный поиск флага**
    - Поиск по regex (`CTF{}`, `BugCTF{}`, `flag{}`) → ничего.
    - Значит, флаг не лежит «в лоб» в логе, его вытаскивали из БД.
2. **Шумящие 0x-константы**
    В логах много запросов вида:
    `/search?q=1'||(SELECT 0x53664b6a WHERE 5916=5916 AND (SELECT 4501 FROM (SELECT(SLEEP(5)))lqrP))||'`
    Раскодировка этих 0x-значений даёт строку, похожую на base64, но после декодирования — бинарный мусор без `CTF{}`. Оказалось, что это просто тестовые/служебные строки sqlmap, не сам флаг.
3. **Настоящая эксфильтрация флага**
    Более интересные запросы:
    `... SELECT HEX(COALESCE(CAST(flag AS TEXT),CHAR(32))) FROM flag LIMIT 0,1 ... ... SUBSTR(..., pos, 1) > CHAR(N) ... ... SUBSTR(..., pos, 1) != CHAR(N) ...`
    
    Это классическая схема sqlmap:
    - `HEX(flag)` → флаг в виде hex-строки
    - `SUBSTR(..., pos, 1)` → берём один hex-символ  
    - серия сравнений `> CHAR(x)` + финальное `!= CHAR(x)` → бинарный поиск по коду символа.

  Лог не содержит ответов сервера, но **последовательность запросов для каждой позиции** полностью кодирует значение символа.

---
## Решение

### Подход

Вместо того, чтобы пытаться расшифровать весь шум из `0x...`, мы:
1. Находим **только** запросы, где фигурирует `HEX(COALESCE(CAST(flag AS TEXT)... FROM flag LIMIT 0,1)`.
2. Парсим из них:
    - позицию символа `pos` (параметр `SUBSTR(..., pos, 1)`)
    - оператор (`>`, `!=`)
    - значение `CHAR(N)`
3. Для каждой позиции `pos` смотрим последнюю проверку вида `!= CHAR(N)` и берём это `N` как итоговый код символа в hex-строке.
4. Собираем по порядку все символы для `pos = 1..62`, получаем строку `hex(flag)`.  
5. Декодируем hex → ASCII → флаг.
### Эксплойт / Скрипт

```python
import re
from collections import defaultdict
from urllib.parse import unquote

log_path = "bug-makers.ru-access.log"

# собираем только запросы с HEX(flag)
flag_queries = []
with open(log_path, 'r', errors='ignore') as f:
    for line in f:
        if 'HEX%28COALESCE%28CAST%28flag' in line:
            m = re.search(r'"(?:GET|POST) ([^ ]+) HTTP', line)
            if not m:
                continue
            flag_queries.append(unquote(m.group(1)))

# парсим позицию, оператор и CHAR(...)
pattern = re.compile(
    r"SUBSTR\(\(SELECT HEX\(COALESCE\(CAST\(flag AS TEXT\),CHAR\(32\)\)\) FROM flag LIMIT 0,1\),(\d+),1\)\s*([!<>=]+)\s*CHAR\((\d+)\)"
)

by_pos = defaultdict(list)
for q in flag_queries:
    m = pattern.search(q)
    if m:
        pos = int(m.group(1))
        op  = m.group(2)
        val = int(m.group(3))
        by_pos[pos].append((op, val))

# для каждой позиции берём значение из '!='
final_vals = {}
for pos, ops in by_pos.items():
    neq = [v for op, v in ops if op == '!=']
    if len(neq) == 1:
        final_vals[pos] = neq[0]

# собираем hex-строку
max_pos = max(final_vals)
hex_str = ''.join(chr(final_vals[pos]) for pos in range(1, max_pos + 1))

flag = bytes.fromhex(hex_str).decode('ascii')
print(flag)

```

### Шаги выполнения 
1. Распаковать лог и убедиться, что атака шла через sqlmap.
2. Игнорировать `SELECT 0x...` — это шум.
3. Найти запросы с `HEX(COALESCE(CAST(flag AS TEXT)...`.
4. Спарсить `SUBSTR(..., pos, 1)` и `CHAR(N)` для каждого `pos`.
5. Для каждой позиции взять `N` из `!= CHAR(N)` как код символа.
6. Собрать hex-строку и декодировать её из hex → ASCII.
7. Получить флаг.