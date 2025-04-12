# SigWatcher

**SigWatcher** — это утилита для анализа флагов SIGHASH и типов подписей в транзакциях Bitcoin.

## Что такое SIGHASH?

SIGHASH-флаг указывает, какие части транзакции подписаны:
- `ALL` — по умолчанию (вся транзакция)
- `NONE` — только входы
- `SINGLE` — один выход
- `ANYONECANPAY` — позволяет другим добавлять входы

## Возможности

- Распознаёт флаги SIGHASH (включая комбинации)
- Поддерживает анализ SegWit и Legacy-подписей
- Выявляет нестандартные схемы подписей

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python sigwatcher.py <txid>
```

Пример:

```bash
python sigwatcher.py e2b6...
```

## Лицензия

MIT License
