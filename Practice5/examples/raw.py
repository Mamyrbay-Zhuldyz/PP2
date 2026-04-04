import re

def quick_parse():
    """Полный парсинг чека из предоставленного текста"""
    
    try:
        with open('raw.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print("Ошибка: Файл raw.txt не найден!")
        return

    print("=" * 50)
    print("ИНФОРМАЦИЯ ИЗ ЧЕКА")
    print("=" * 50)

    # 1. Магазин
    store_match = re.search(r'Филиал\s+(.+)', text)
    if store_match:
        print(f"Магазин: {store_match.group(1).strip()}")

    # 2. БИН
    bin_match = re.search(r'БИН\s+(\d+)', text)
    if bin_match:
        print(f"БИН: {bin_match.group(1)}")

    # 3. Дата и время
    datetime_match = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})', text)
    if datetime_match:
        print(f"Дата/время: {datetime_match.group(1)}")

    # 4. Товары
    print("\n" + "-" * 50)
    print(f"{'№':<3} | {'Наименование':<35} | {'Итог':>10}")
    print("-" * 50)

    item_pattern = r'(\d+)\.\s+(.*?)\s+(\d+[.,]\d+)\s*[xх]\s*([\d\s]+[.,]\d+)\s+([\d\s]+[.,]\d+)\s+Стоимость'
    
    items = re.findall(item_pattern, text, re.DOTALL)
    
    total_calculated = 0.0
    for num, name, qty, price, total in items:
        clean_name = re.sub(r'\s+', ' ', name.strip())
        
        def clean_float(s):
            return float(s.replace(' ', '').replace(',', '.'))

        price_val = clean_float(price)
        total_val = clean_float(total)
        total_calculated += total_val
        
        print(f"{num:<3} | {clean_name[:35]:<35} | {total_val:>10.2f}")
        if len(clean_name) > 35:
            print(f"{'':<3} | {clean_name[35:70]:<35} |")

    # 5. Итоговые данные
    print("-" * 50)
    
    total_match = re.search(r'ИТОГО:\s*([\d\s]+[.,]\d+)', text)
    if total_match:
        actual_total = total_match.group(1).replace(' ', '').replace(',', '.')
        print(f"ИТОГО (по чеку):  {actual_total:>28}")
    
    print(f"ИТОГО (расчет):  {total_calculated:>29.2f}")

    address_match = re.search(r'(г\.\s*[^А-Я]+)', text)
    if address_match:
        print(f"\nАдрес: {address_match.group(1).strip().replace(chr(10), ' ')}")

if __name__ == "__main__":
    quick_parse()