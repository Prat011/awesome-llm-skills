#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Прогон регулярных выражений из references/chatbot-artifacts.md
по проверочным образцам из references/test-fixtures.md.

Каждое выражение проходит три уровня:
  1. Прямой образец  — выражение обязано сработать.
  2. Отрицательный   — похожий, но не машинный текст; срабатывать не должно.
  3. Граничный       — пустая строка и многократные совпадения; без падений.

Только стандартная библиотека. Запуск:  python3 scripts/check_markers.py
Код возврата 0 — все проверки пройдены, 1 — есть провалы.

При добавлении нового выражения в chatbot-artifacts.md сюда добавляется
блок с образцами, а парные образцы — в references/test-fixtures.md.
Ни одно работающее правило не удаляется (см. принцип в test-fixtures.md).
"""

import re
import sys

# name: (выражение, прямые образцы, отрицательные образцы, [многократный образец, ожидаемое число])
CASES = {
    # --- A.1. Метки внутреннего цитирования OpenAI ---
    "contentReference": (
        r":contentReference\[oaicite:\d+\]\{index=\d+\}",
        ["Согласно отчёту :contentReference[oaicite:0]{index=0}, рынок вырос на 12%.",
         ":contentReference[oaicite:42]{index=42}"],
        ["Это просто ссылка на oaicite (упоминание термина в статье об ИИ).",
         "Документация: содержит [oaicite:N] как пример формата."],
        (":contentReference[oaicite:0]{index=0} и :contentReference[oaicite:1]{index=1} и :contentReference[oaicite:2]{index=2}", 3),
    ),
    "oai_citation": (
        r"oai_citation:\d+‡",
        ["Источник oai_citation:5‡Wikipedia говорит, что…", "oai_citation:0‡"],
        ["oai_citation без числа после двоеточия"],
        None,
    ),
    "oaicite_short": (
        r"oaicite:\d+",
        ["усечённая ссылка oaicite:7"],
        ["oaicite без двоеточия и числа"],
        None,
    ),
    # --- A.2. Метки веб-поиска OpenAI ---
    "turn_search": (
        r"turn\d+search\d+",
        ["Согласно turn0search0, тема актуальна.", "turn3search12 в середине предложения"],
        ["turn left and search again", "turnaround search"],
        ("turn0search0 turn1search1 turn2search2", 3),
    ),
    "turn_fetch": (
        r"turn\d+fetch\d+",
        ["[turn0fetch0] в скобках"],
        ["turn fetch the file"],
        None,
    ),
    "turn_file": (
        r"turn\d+file\d+",
        ["Вывод обрывается метками fileciteturn0file2turn0file6 в конце.",
         "одиночная метка turn0file11 после цитаты"],
        ["turn the file over", "return file 5 to the archive"],
        ("fileciteturn0file2turn0file6", 2),
    ),
    # --- A.3. Метки UTM от чат-ботов ---
    "utm_chatgpt": (
        r"[?&]utm_source=chatgpt\.com",
        ["https://example.com/article?utm_source=chatgpt.com",
         "https://example.com/?id=5&utm_source=chatgpt.com",
         "?utm_source=chatgpt.com&other=1"],
        ["utm_source=chatgpt.com упомянут в статье об отслеживании",
         "https://example.com/?utm_source=other.com"],
        None,
    ),
    "utm_openai": (
        r"[?&]utm_source=openai",
        ["https://docs.example.com/?utm_source=openai"],
        ["OpenAI utm_source без знака ? или &"],
        None,
    ),
    "utm_copilot": (
        r"[?&]utm_source=copilot\.com",
        ["https://example.com/?utm_source=copilot.com",
         "https://example.com/?id=7&utm_source=copilot.com"],
        ["utm_source=copilot.com упомянут в статье об отслеживании",
         "https://example.com/?utm_source=chatgpt.com"],
        None,
    ),
    "grok_referrer": (
        r"[?&]referrer=grok\.com",
        ["https://x.com/post?referrer=grok.com",
         "https://example.com/?id=1&referrer=grok.com"],
        ["referrer=grok.com упомянут без URL-параметра",
         "https://example.com/?referrer=other.com"],
        None,
    ),
    # --- A.4. Метки прикрепления и карточек ---
    "attached_file": (
        r"attached_file:\/\/",
        ["См. attached_file:///tmp/upload.pdf"],
        ["Файл прикреплён, см. attached file (по-русски)"],
        None,
    ),
    "grok_card": (
        r"grok_card:\/\/",
        ["grok_card://1234567890"],
        ["карточка Grok без специфичной разметки"],
        None,
    ),
    "grok_render_json": (
        r"grok_render_citation_card_json",
        ['[](grok_render_citation_card_json={"cardIds":["3bb883"]})'],
        ["grok render citation card json обсуждают в документации"],
        ('[](grok_render_citation_card_json={"cardIds":["1"]}) [](grok_render_citation_card_json={"cardIds":["2"]})', 2),
    ),
    "vertexaisearch": (
        r"vertexaisearch\.cloud\.google\.com/grounding-api-redirect",
        ["https://vertexaisearch.cloud.google.com/grounding-api-redirect/AbCdEf"],
        ["vertexaisearch.cloud.google.com без пути",
         "https://cloud.google.com/vertex-ai-search"],
        None,
    ),
    # --- A.5. Прочие маркеры разметки ---
    "attributableIndex": (
        r"\battributableIndex\b",
        ['{"attributableIndex": 0}'],
        ["слово attributable в обычном тексте о праве и атрибуции",
         "attributableIndexes (с окончанием)"],
        None,
    ),
    "citation_n": (
        r"\[citation:\d+\]",
        ["Согласно исследованию [citation:3], результаты неоднозначны."],
        ["[citation needed] (Википедийный шаблон)"],
        None,
    ),
    # --- A.6. Маркеры новых платформ (v2.5) ---
    "copilot_caret": (
        r"\[\^\d+\^\]",
        ["Рынок вырос на 12%[^1^] по данным отчёта.", "[^10^]"],
        ["Обычная сноска Markdown[^1] определена ниже."],
        ("[^1^][^2^][^10^]", 3),
    ),
    "assistants_source": (
        r"【\d+(?::\d+)?†source】",
        ["Согласно политике【1†source】, доступ разрешён.", "【4:2†source】"],
        ["Декоративные уголки 【примечание】 без кинжала."],
        None,
    ),
    "cite_turn": (
        r"citeturn\d+[a-z]+\d+",
        ["Текст citeturn0file0 со ссылкой.", "citeturn2search5 в середине строки"],
        ["Прошу процитировать, затем turn to page 5."],
        ("citeturn0file0 citeturn2search5", 2),
    ),
    "sandbox_link": (
        r"\]\(sandbox:/mnt/data/",
        ["[Скачать отчёт](sandbox:/mnt/data/report.xlsx)"],
        ["Развернули окружение sandbox на /mnt/data сервера."],
        ("[A](sandbox:/mnt/data/a.csv) [B](sandbox:/mnt/data/b.csv)", 2),
    ),
    # --- A.7. Невидимые и служебные символы (v2.6) ---
    "openai_pua": (
        "[\ue200-\ue204]",
        ["Amazon Nova даёт ряд возможностей \ue200cite\ue202turn0search3\ue201.",
         "скрытый блок \ue203служебная пометка\ue204 в тексте"],
        ["Обычный текст без служебных символов.",
         "Символ иконки \ue000 из шрифтового набора (другая часть PUA)"],
        ("\ue200cite\ue202turn0search3\ue201", 3),
    ),
    # Короткая форма сноски ChatGPT: одиночная цифра, ограждённая U+EA01/U+EA02 (v3.2)
    "openai_pua_short": (
        "[\uea01\uea02]",
        ["известная по ролям в сериале.\uea012\uea02",
         "высокий рейтинг на агрегаторе.\uea015\uea02 Следующее предложение."],
        ["Обычный текст без служебных символов с цифрой 2 в конце.",
         "Символ иконки \ue000 из шрифтового набора (другая часть PUA)",
         "Служебный разделитель \ue200 из длинной формы (своё выражение openai_pua)"],
        ("Первое.\uea012\uea02 Второе.\uea013\uea02", 4),
    ),
    "think_tag": (
        r"</?think>",
        ["<think>Сначала разберу условия задачи…</think> Ответ: 42.",
         "хвост рассуждения…</think> Итоговый ответ ниже."],
        ["Я думаю (think), что это норма.",
         "Тег <thinking> другого формата здесь не считается."],
        ("<think>а</think>", 2),
    ),
    # --- A.8. Сцепки «Источник+цифра» (v2.7) ---
    "source_plus_chain": (
        r"[A-Za-zА-Яа-яЁё)]\+\d+[A-ZА-ЯЁ]",
        ["Стандарт создан комитетом ISO. IT Governance+3ISO+3ISO+3. Он входит в семейство…",
         "адаптирован к облачным средам. Microsoft Learn+3Google Cloud+3."],
        ["стандарт C++11 и C++14 поддерживаются",
         "формула x+1 в каждой строке",
         "оценка 5+ за контрольную",
         "Wikipedia+1."],
        ("Wikipedia+1Реестр+2Архив+3", 2),
    ),
    # --- A.9. Метки цитирования Gemini (v2.9) ---
    "gemini_cite_start": (
        r"\[cite_start\]",
        ["[cite_start]Компания основана в 1994 году и с тех пор…",
         "Вывод содержит [cite_start] в середине строки."],
        ["функция cite_start() в коде без скобок вокруг",
         "[cite start] с пробелом вместо подчёркивания"],
        ("[cite_start]Первое. [cite_start]Второе.", 2),
    ),
    "gemini_cite_n": (
        r"\[[Cc]ite:\s?\d+(?:,\s?\d+)*\]",
        ["Выручка выросла на 12% [cite: 8] по итогам года.",
         "Согласно отчёту [Cite: 12], план выполнен.",
         "Работала с клиентами в медицине и недвижимости [cite: 19, 20, 21]."],
        ["[citation needed] (Википедийный шаблон)",
         "[citation:3] — метка DeepSeek, у неё своё выражение",
         "команда \\cite{ivanov2024} в LaTeX"],
        ("[cite: 1][cite: 2][Cite: 3]", 3),
    ),
    # --- A.10. Символы нулевой ширины (v2.9) ---
    "zero_width": (
        "[\u200b-\u200d\u2060\ufeff]",
        ["Слово\u200bразорвано пробелом нулевой ширины.",
         "Невидимый соединитель\u2060внутри текста.",
         "Метка\ufeffпосреди строки."],
        ["Обычный текст с обычными пробелами.",
         "Узкий неразрывный пробел\u202fне входит в выражение (ручная проверка)."],
        ("а\u200bб\u200cв\u200dг", 3),
    ),
    # --- A.11. Блоки «writing» ChatGPT (v3.0) ---
    "writing_block": (
        r":::\w+\{variant",
        [':::writing{variant="document" id="68427"}',
         'Черновик письма ниже. :::writing{variant="email" id="51724"}',
         ':::écriture{variante="document" id="28471"}'],
        [":::note — директива Docusaurus без атрибута variant",
         ':::tip{title="Совет"} — атрибут другой',
         "обычное троеточие в конце фразы..."],
        (':::writing{variant="email" id="11111"} текст ::: :::writing{variant="chat_message" id="22222"}', 2),
    ),
    # --- A.12. DeepSeek/derivative line references (v3.1) ---
    "deepseek_line_ref": (
        r"【\d+†L\d+(?:-L?\d+)?】",
        ["В 2024 году кампания выросла【85†L261-269】.",
         "Альбом вышел【854†L119-123】 в 2024 году.",
         "【854†L119-L123】 — форма с L после дефиса."],
        ["OpenAI Assistants метка 【1†source】 ловится другим выражением.",
         "Декоративные уголки 【примечание】 без строк.",
         "Обычная сноска [1] не должна срабатывать."],
        ("【29†L582-589】【32†L142-149】", 2),
    ),
    # --- A.4 доп. Grok XML-тег (v3.1) ---
    "grok_card_tag": (
        r"<grok-card\b[^>]*\bcitation_card\b",
        ['<grok-card data-id="e8ff4f" data-type="citation_card">',
         '\u0422\u0435\u043a\u0441\u0442...<grok-card data-id="abc" data-type="citation_card">'],
        ["<grok-card> \u0431\u0435\u0437 \u0430\u0442\u0440\u0438\u0431\u0443\u0442\u0430 citation_card",
         "\u043e\u0431\u044b\u0447\u043d\u044b\u0439 XML-\u0442\u0435\u0433 <div>"],
        None,
    ),
    # --- A.2 доп. turn image/news/video/ref (v3.1) ---
    "turn_other": (
        r"turn\d+(?:image|news|video|ref)\d+",
        ["\u0424\u043e\u0442\u043e turn0image0 \u0432 \u0442\u0435\u043a\u0441\u0442\u0435.", "turn0news0 \u0432 \u0441\u0435\u0440\u0435\u0434\u0438\u043d\u0435", "turn0video0", "turn0ref0"],
        ["turn left and image again", "turnaround news"],
        ("turn0image0 turn0news0 turn0video0", 3),
    ),
    # --- A.5 доп. скобочная форма ссылок инструментов (v3.1) ---
    "attached_web_bracket": (
        r"\[(?:attached_file|web):\d+\]",
        ["\u0421\u043c. [attached_file:1] \u0432 \u043e\u0442\u0432\u0435\u0442\u0435.", "\u0426\u0438\u0442\u0430\u0442\u0430 [web:3] \u0438\u0437 \u043f\u043e\u0438\u0441\u043a\u0430."],
        ["[attach:1] \u0434\u0440\u0443\u0433\u043e\u0439 \u0444\u043e\u0440\u043c\u0430\u0442", "\u043e\u0431\u044b\u0447\u043d\u0430\u044f \u0441\u043d\u043e\u0441\u043a\u0430 [1]"],
        ("[attached_file:1][web:2][web:3]", 3),
    ),
    # --- A.6 доп. generated-reference-identifier (v3.1) ---
    "generated_ref_id": (
        r"citegenerated-reference-identifier",
        ["\u0422\u0435\u043a\u0441\u0442 citegenerated-reference-identifier \u0432 \u0432\u044b\u0432\u043e\u0434\u0435."],
        ["generated reference identifier \u0447\u0435\u0440\u0435\u0437 \u043f\u0440\u043e\u0431\u0435\u043b"],
        None,
    ),
    # --- A.5 доп. placeholder URLs (v3.1) ---
    "placeholder_url": (
        r"\b(?:INSERT_SOURCE_URL(?:_\d+)?|URL_HERE|PASTE_\w+_URL_HERE)\b",
        ["\u0412\u0441\u0442\u0430\u0432\u044c\u0442\u0435 INSERT_SOURCE_URL_30 \u0441\u044e\u0434\u0430.", "\u0421\u043c. URL_HERE \u0432 \u0448\u0430\u0431\u043b\u043e\u043d\u0435.", "PASTE_SPOTIFY_TRACK_URL_HERE"],
        ["insert source url \u0432 \u043e\u0431\u044b\u0447\u043d\u043e\u0439 \u0444\u0440\u0430\u0437\u0435", "\u0432\u0441\u0442\u0430\u0432\u044c\u0442\u0435 URL \u0441\u044e\u0434\u0430"],
        ("INSERT_SOURCE_URL URL_HERE PASTE_TRACK_URL_HERE", 3),
    ),
    # --- A.5 доп. placeholder-даты (v3.1) ---
    "placeholder_date": (
        r"\b\d{4}-(?:\d{2}|[Xx]{2})-[Xx]{2}\b",
        ["дата обращения: 2025-XX-XX.",
         "|date=2022-11-XX |publisher=…",
         "access-date=2025-xx-xx"],
        ["обычная дата 2025-11-30 не срабатывает",
         "артикул 2025-XX-XXL не срабатывает",
         "диапазон 2024-2025 без дня"],
        ("2025-XX-XX и 2022-11-XX в одном списке литературы", 2),
    ),
}


def _inside_backticks(line: str, start: int, end: int) -> bool:
    """Совпадение внутри `обратных кавычек` — это документация, не артефакт."""
    return line[:start].count("`") % 2 == 1 and line[end:].count("`") >= 1


def scan(paths: list) -> int:
    """Прогон всех выражений по произвольным файлам.

    Запуск:  python3 scripts/check_markers.py --scan файл1 [файл2 …]
    Печатает каждое совпадение в формате «файл:строка [имя] фрагмент».
    Совпадения внутри обратных кавычек пропускаются (документация выражений).
    Код возврата 0 — чисто, 1 — найдены маркеры.
    """
    compiled = {name: re.compile(case[0]) for name, case in CASES.items()}
    found = 0
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except OSError as exc:
            print(f"Не удалось прочитать {path}: {exc}", file=sys.stderr)
            return 2
        for lineno, line in enumerate(lines, 1):
            for name, rx in compiled.items():
                for m in rx.finditer(line):
                    if _inside_backticks(line, m.start(), m.end()):
                        continue
                    found += 1
                    fragment = line.strip()[:90]
                    print(f"{path}:{lineno} [{name}] {fragment}")
    if found:
        print(f"\nНайдено маркеров: {found}.")
        return 1
    print("Маркеров не найдено.")
    return 0


def main() -> int:
    fails = 0
    for name, (pattern, positives, negatives, multi) in CASES.items():
        rx = re.compile(pattern)
        for s in positives:
            if not rx.search(s):
                print(f"ПРОВАЛ {name}: прямой образец не пойман: {s!r}")
                fails += 1
        for s in negatives:
            if rx.search(s):
                print(f"ПРОВАЛ {name}: ложное срабатывание на: {s!r}")
                fails += 1
        if rx.search(""):
            print(f"ПРОВАЛ {name}: срабатывание на пустой строке")
            fails += 1
        if multi is not None:
            text, expected = multi
            got = len(rx.findall(text))
            if got != expected:
                print(f"ПРОВАЛ {name}: многократный образец — ожидалось {expected}, найдено {got}")
                fails += 1

    total = len(CASES)
    if fails:
        print(f"\nИтог: {total} выражений, провалов: {fails}.")
        return 1
    print(f"Итог: {total} из {total} выражений проходят все проверки.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--scan":
        sys.exit(scan(sys.argv[2:]))
    sys.exit(main())
