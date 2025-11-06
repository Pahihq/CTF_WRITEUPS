## Overview

Чтобы получить флаг, нужно успеть собрать весь пазл за 1 минуту.  
Количество пазлов: 16 шт
Чтобы получить флаг, нужно успеть собрать весь пазл за 1 минуту.  
Количество пазлов: 64 шт
Чтобы получить флаг, нужно успеть собрать весь пазл за 1 минуту.  
Количество пазлов: 256 шт

---
## Что отдаёт бэкенд

Фронт делает:
`GET /api/new-game`
и получает примерно такое:
`{   "success": true,   "puzzle": [ ...64 элементов... ],   "originalImage": "data:image/jpeg;base64,...",   "gridSize": 8,   "pieceSize": 70 }`

Где:

- `originalImage` — исходная, целая картинка;
- `puzzle` — массив из 64 кусочков;
- `gridSize = 8` → поле 8×8;
- `pieceSize = 70` → каждый кусок 70×70.

Отдельный эндпоинт проверки:
`POST /api/check-solution Content-Type: application/json  {   "solution": ["id1", "id2", ..., "id64"] }`

То есть серверу вообще всё равно на DOM и перетаскивания — он ждёт **просто массив id в правильном порядке**.

Важно: у элементов в `puzzle` всего 4 поля:
`{ "id": "uuid", "image": "data:image/jpeg;base64,...", "width": 70, "height": 70 }`

---
## Идея решения

Раз сервер отдаёт **и целую картинку**, и **все нарезанные куски по отдельности**, то порядок можно восстановить прямо в браузере:
1. нарисовать оригинал в `<canvas>`;
2. разрезать его по сетке 8×8 (с шагом 70 пикселей);
3. для каждой такой ячейки подобрать из присланных кусков тот, который визуально ближе всего;
4. из подобранных id собрать массив слева направо, сверху вниз;
5. отправить этот массив на `/api/check-solution`.

То есть мы эмулируем «обратную нарезку»: сравниваем то, что было до разрезания, с тем, что прислали.

---
## Проблема точного сравнения

Оригинал и кусочки приходят как JPEG (base64). JPEG — с потерями, поэтому пиксель-в-пиксель совпадения не будет. Поэтому пришлось делать **сравнение с допуском**: не полное побитовое сравнение, а “насколько две картинки похожи” (считаем суммарную разницу по RGB с шагом).

---
## Скрипт для консоли

Рабочий вариант, который:
- забирает новый пазл;
- рисует оригинал;
- загружает все кусочки;
- по каждой клетке оригинала находит самый похожий кусок;
- шлёт решение на сервер.

```java
(async () => {
  // загрузка картинки
  const loadImage = (src) => new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });

  // получение ImageData из <img>
  const getImageDataFromImg = (img, w, h) => {
    const c = document.createElement('canvas');
    const ctx = c.getContext('2d', { willReadFrequently: true });
    c.width = w;
    c.height = h;
    ctx.drawImage(img, 0, 0, w, h);
    return ctx.getImageData(0, 0, w, h);
  };

  // метрика похожести (чем меньше score, тем больше похожи)
  const diffScore = (a, b, step = 4) => {
    let score = 0;
    const aw = a.width, ah = a.height;
    const ad = a.data, bd = b.data;
    for (let y = 0; y < ah; y += step) {
      for (let x = 0; x < aw; x += step) {
        const idx = (y * aw + x) * 4;
        const dr = ad[idx]   - bd[idx];
        const dg = ad[idx+1] - bd[idx+1];
        const db = ad[idx+2] - bd[idx+2];
        score += dr*dr + dg*dg + db*db;
      }
    }
    return score;
  };

  try {
    // 1. забираем пазл
    const resp = await fetch('/api/new-game');
    const data = await resp.json();
    const { originalImage, puzzle, gridSize, pieceSize } = data;

    // 2. рисуем оригинал
    const origImg = await loadImage(originalImage);
    const origCanvas = document.createElement('canvas');
    origCanvas.width = pieceSize * gridSize;
    origCanvas.height = pieceSize * gridSize;
    const origCtx = origCanvas.getContext('2d', { willReadFrequently: true });
    origCtx.drawImage(origImg, 0, 0, origCanvas.width, origCanvas.height);

    // 3. загружаем все кусочки и превращаем их в ImageData
    const pieces = [];
    for (const p of puzzle) {
      const img = await loadImage(p.image);
      const imgData = getImageDataFromImg(img, pieceSize, pieceSize);
      pieces.push({ id: p.id, imgData, used: false });
    }

    const solutionIds = [];

    // 4. проходим по оригиналу — сверху вниз, слева направо
    for (let row = 0; row < gridSize; row++) {
      for (let col = 0; col < gridSize; col++) {
        const x = col * pieceSize;
        const y = row * pieceSize;
        const origPieceData = origCtx.getImageData(x, y, pieceSize, pieceSize);

        let bestId = null;
        let bestScore = Infinity;
        let bestIdx = -1;

        // ищем наиболее похожий ещё не использованный кусок
        for (let i = 0; i < pieces.length; i++) {
          const pc = pieces[i];
          if (pc.used) continue;
          const score = diffScore(origPieceData, pc.imgData, 4);
          if (score < bestScore) {
            bestScore = score;
            bestId = pc.id;
            bestIdx = i;
          }
        }

        if (bestIdx >= 0) {
          pieces[bestIdx].used = true;
        }

        solutionIds.push(bestId);
      }
    }

    console.log('Собранный порядок:', solutionIds);

    // 5. отправляем решение
    const checkResp = await fetch('/api/check-solution', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ solution: solutionIds })
    });

    console.log('Ответ сервера:', await checkResp.json());
  } catch (e) {
    console.error(e);
  }
})();

```

![Puzzel 1](Puzzel-1.png)
![Puzzel 2](Puzzel-2.png)
![Puzzel 3](Puzzel-3.png)

