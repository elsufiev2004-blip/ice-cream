import pandas as pd
import matplotlib.pyplot as plt
import sys

def load_data(filepath):
    """Загружает данные из CSV файла."""
    try:
        df = pd.read_csv(filepath)
        print(f"Данные успешно загружены. Строк: {len(df)}")
        return df
    except FileNotFoundError:
        print(f"Ошибка: файл '{filepath}' не найден. Положите его в папку с программой.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)

def clean_data(df):
    """Очищает данные и подготавливает их к анализу."""
    # Проверяем, что нужные колонки есть
    required_cols = ['date', 'product', 'quantity', 'price']
    if not all(col in df.columns for col in required_cols):
        print(f"Ошибка: в файле должны быть колонки: {required_cols}")
        sys.exit(1)

    # Удаляем пустые строки
    initial_len = len(df)
    df = df.dropna()
    print(f"Удалено пустых строк: {initial_len - len(df)}")

    # Преобразуем даты
    try:
        df['date'] = pd.to_datetime(df['date'])
    except Exception as e:
        print(f"Ошибка формата даты: {e}")
        sys.exit(1)

    # Создаем колонку с номером месяца
    df['month'] = df['date'].dt.month
    return df

def analyze_sales(df):
    """Считает выручку по месяцам."""
    # Выручка = количество * цена
    df['revenue'] = df['quantity'] * df['price']
    # Группировка по месяцам
    monthly_sales = df.groupby('month')['revenue'].sum().reset_index()
    return monthly_sales

def plot_seasonality(monthly_sales):
    """Строит график сезонности и выводит текстовый вывод."""
    month_names = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 
                   'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
    
    # Настройка графика
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales['month'], monthly_sales['revenue'], 
             marker='o', color='#1f77b4', linewidth=2, markersize=8)
    
    plt.title('Сезонность спроса на мороженое\n(Сумма продаж по месяцам)', fontsize=14)
    plt.xlabel('Месяц', fontsize=12)
    plt.ylabel('Выручка (руб.)', fontsize=12)
    
    # Красивые подписи месяцев
    plt.xticks(monthly_sales['month'], [month_names[int(m)-1] for m in monthly_sales['month']])
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Находим пик и минимум
    peak_month = monthly_sales.loc[monthly_sales['revenue'].idxmax()]
    low_month = monthly_sales.loc[monthly_sales['revenue'].idxmin()]
    
    print("\n--- РЕЗУЛЬТАТЫ АНАЛИЗА ---")
    print(f"Пик продаж: {month_names[int(peak_month['month'])-1]} (Выручка: {peak_month['revenue']:.2f} руб.)")
    print(f"Спад продаж: {month_names[int(low_month['month'])-1]} (Выручка: {low_month['revenue']:.2f} руб.)")
    print("--------------------------")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Запуск анализа продаж мороженого...")
    filepath = 'sales.csv'
    
    data = load_data(filepath)
    clean_df = clean_data(data)
    monthly = analyze_sales(clean_df)
    plot_seasonality(monthly)