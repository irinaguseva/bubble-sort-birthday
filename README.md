# Bubble Sort × Birthday Problem

Реализация и экспериментальная проверка результатов статьи:

> **Jichu Jiang**, *Relating bubble sort to birthday problem*, 2024.
> Beihang University.

## О чём это?

Статья устанавливает изоморфизм между двумя классическими задачами:
- **Задача о днях рождения** (теория вероятностей)
- **Сортировка пузырьком** (computer science)

**Главный результат:**
$$
\frac{n - P_n}{\sqrt{n}} \xrightarrow{d} \text{Ray}(1), \qquad
\frac{C_n - 1}{\sqrt{n}} \xrightarrow{d} \text{Ray}(1)
$$

где $P_n$ — число проходов bubble sort, $C_n$ — номер первого совпадения дней рождения.

## Установка

```bash
pip install -r requirements.txt