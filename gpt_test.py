import g4f
import csv

def create_prompt(message: str) -> str:
    return (
        "Ты — нейросеть, которая выявляет сообщения, содержащие попытки обмена контактными данными "
        "(номер телефона, email, ссылка на мессенджер, соцсеть и т.п.).\n"
        "Проанализируй следующее сообщение и ответь строго 'True', если оно содержит попытку обмена контактами, "
        "иначе 'False'. Без дополнительного текста.\n\n"
        f"Сообщение: \"{message}\"\n"
    )

input_file = "messages.csv"
output_file = "results_with_model.csv"

count = 1
rows = []
with open(input_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

model_results = []
total = len(rows)

for row in rows:
    message = row["message"]
    prompt = create_prompt(message)

    response = g4f.ChatCompletion.create(
        model="o1-preview", messages=[{"role": "user", "content": prompt}], stream=False
    )

    answer = response.strip()
    print(f'{count}: {answer}')
    count += 1

    original_val = row["Содержит контакт"].strip()
    model_results.append({
        "ID": row["ID"],
        "message": message,
        "original": original_val,
        "model_prediction": answer
    })

# Подсчёт совпадений
matches = sum(1 for res in model_results if res["original"] == res["model_prediction"])
accuracy = matches / total if total > 0 else 0
for i in model_results:
    if i["original"] != i["model_prediction"]:
        print(i['ID'])

# Запись результатов
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "message", "original", "model_prediction"])
    for res in model_results:
        writer.writerow([res["ID"], res["message"], res["original"], res["model_prediction"]])

print(f"Совпадений: {matches} из {total}")
print(f"Точность: {accuracy * 100:.2f}%")
print(f"Результаты сохранены в {output_file}")
