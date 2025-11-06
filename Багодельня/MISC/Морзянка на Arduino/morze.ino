// Определение длительности сигналов
const int DOT_DURATION = 200;      // длительность точки (мс)
const int DASH_DURATION = 600;     // длительность тире (3 точки)
const int SYMBOL_PAUSE = 200;      // пауза между символами (1 точка)
const int LETTER_PAUSE = 600;      // пауза между буквами (3 точки)
const int WORD_PAUSE = 1000;       // пауза между словами (7 точек)

const int LED_PIN = 13;            // пин светодиода

// Карта символов Морзе
const char* morseMap[] = {
    ".-",    // A
    "-...",  // B
    "-.-.",  // C
    "-..",   // D
    ".",     // E
    "..-.",  // F
    "--.",   // G
    "....",  // H
    "..",    // I
    ".---",  // J
    "-.-",   // K
    ".-..",  // L
    "--",    // M
    "-.",    // N
    "---",   // O
    ".--.",  // P
    "--.-",  // Q
    ".-.",   // R
    "...",   // S
    "-",     // T
    "..-",   // U
    "...-",  // V
    ".--",   // W
    "-..-",  // X
    "-.--",  // Y
    "--..",  // Z
    "-----", // 0
    ".----", // 1
    "..---", // 2
    "...--", // 3
    "....-", // 4
    ".....", // 5
    "-....", // 6
    "--...", // 7
    "---..", // 8
    "----.", // 9
    "..--.-",// _
    "-.--.", // {
    "-.--.-",// }
};

// Функция для отправки символа Морзе
void sendMorseChar(char c) {
    if (c == ' ') {
        delay(WORD_PAUSE);
        return;
    }
    
    int index;
    if (c >= 'A' && c <= 'Z') {
        index = c - 'A';
    } else if (c >= 'a' && c <= 'z') {
        index = c - 'a';
    } else if (c >= '0' && c <= '9') {
        index = c - '0' + 26;
    } else {
        switch (c) {
            
            case '_': index = 36; break;
            case '{': index = 37; break;
            case '}': index = 38; break;
            default: return;
        }
    }
    
    const char* morseCode = morseMap[index];
    
    for (int i = 0; morseCode[i] != '\0'; i++) {
        if (morseCode[i] == '.') {
            digitalWrite(LED_PIN, HIGH);
            delay(DOT_DURATION);
            digitalWrite(LED_PIN, LOW);
        } else if (morseCode[i] == '-') {
            digitalWrite(LED_PIN, HIGH);
            delay(DASH_DURATION);
            digitalWrite(LED_PIN, LOW);
        }
        
        if (morseCode[i + 1] != '\0') {
            delay(SYMBOL_PAUSE);
        }
    }
    
    delay(LETTER_PAUSE - SYMBOL_PAUSE);
}

// Функция для отправки текста Морзе
void sendMorseText(const char* text) {
    for (int i = 0; text[i] != '\0'; i++) {
        sendMorseChar(text[i]);
    }
}

void setup() {
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    delay(3000);
    const char* message = "BUGCTF{TEST_FLAG}";
    sendMorseText(message);
}

void loop() {
    
}