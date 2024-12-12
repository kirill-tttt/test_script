import matplotlib.pyplot as plt

# Исходные данные
total_users = 100000
percentage_dissatisfied = 0.20  # 20%
average_orders_dissatisfied = 3.2
average_order_value = 1500  # рублей
average_delivery_cost = 100  # рублей (X)
average_commission_rate = 0.10  # 10%
average_delay_days = 5  # U
average_commission = 150  # рублей (Z)


# Функция для расчета средней скидки
def calculate_discount(U, X, Z):
    discount = (U - 3) * 0.1 * X
    discount = min(discount, 0.6 * X, 0.5 * Z)
    return discount


# Расчет средней скидки
average_discount = calculate_discount(average_delay_days, average_delivery_cost, average_commission)
print(f"Средняя скидка: {average_discount} рублей")

# Расчет текущих потерь (утраченные комиссии)
current_lost_users = total_users * percentage_dissatisfied  # 20,000
current_lost_orders = current_lost_users * average_orders_dissatisfied  # 64,000
current_lost_commissions = current_lost_orders * average_order_value * average_commission_rate  # 64,000 * 1500 * 0.10 = 9,600,000 рублей

print(f"Текущие утраченные комиссии: {current_lost_commissions:,.0f} рублей")

# Определение сценариев
scenarios = {
    'Негативный': 0.20,  # 20% увеличение удержания
    'Нейтральный': 0.50,  # 50% увеличение удержания
    'Позитивный': 0.80  # 80% увеличение удержания
}

# Расчеты для сценариев
final_losses = {}
percentage_change = {}
profit_increase = {}

for scenario, retention_factor in scenarios.items():
    # Количество удержанных пользователей
    retained_users = current_lost_users * retention_factor
    # Количество удержанных заказов
    retained_orders = retained_users * average_orders_dissatisfied
    # Комиссия с удержанных заказов (10% от (1,500 - скидка))
    retained_commissions = retained_orders * average_commission_rate * (average_order_value - average_discount)
    # Общие расходы на скидки (одна скидка на пользователя)
    total_discounts = retained_users * average_discount
    # Увеличение прибыли: удержанные комиссии минус расходы на скидки
    profit_increase_scenario = retained_commissions - total_discounts
    # Итоговые потери после внедрения фичи
    final_loss = current_lost_commissions - profit_increase_scenario
    # Процентное изменение потерь
    change = ((final_loss - current_lost_commissions) / current_lost_commissions) * 100

    # Сохранение результатов
    final_losses[scenario] = final_loss
    percentage_change[scenario] = change
    profit_increase[scenario] = profit_increase_scenario

    # Вывод результатов для сценария
    print(f"\nСценарий: {scenario}")
    print(f"Удержанные пользователи: {retained_users:.0f} человек")
    print(f"Удержанные заказы: {retained_orders:.0f} заказов")
    print(f"Комиссия с удержанных заказов: {retained_commissions:,.0f} рублей")
    print(f"Расходы на скидки: {total_discounts:,.0f} рублей")
    print(f"Увеличение прибыли: {profit_increase_scenario:,.0f} рублей")
    print(f"Итоговые потери: {final_loss:,.0f} рублей")
    print(f"Изменение утраченных комиссий: {change:.2f}%")

# Визуализация результатов потерь
labels = list(scenarios.keys()) + ['Текущее состояние']
loss_values = list(final_losses.values()) + [current_lost_commissions]
colors = ['orange', 'blue', 'green', 'red']

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, loss_values, color=colors)
ax.set_ylabel('Утраченные комиссии (рубли)')
ax.set_title('Сравнение утраченных комиссий по различным сценариям')
ax.bar_label(bars, fmt='{:,.0f}')
plt.show()

# Визуализация увеличения прибыли
labels_profit = list(scenarios.keys())
profits = list(profit_increase.values())

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels_profit, profits, color=['orange', 'blue', 'green'])
ax.set_ylabel('Увеличение прибыли (рубли)')
ax.set_title('Увеличение прибыли по различным сценариям')
ax.bar_label(bars, fmt='{:,.0f}')
plt.show()

# Визуализация процентного изменения потерь
labels_change = list(scenarios.keys())
changes = list(percentage_change.values())

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels_change, changes, color=['orange', 'blue', 'green'])
ax.set_ylabel('Изменение утраченных комиссий (%)')
ax.set_title('Процентное изменение утраченных комиссий по сценариям')
ax.bar_label(bars, fmt='{:0.2f}%')
plt.show()
