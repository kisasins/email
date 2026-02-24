import tkinter as tk
from tkinter import ttk, messagebox
import os
import re

TEMPLATES_DIR = "templates"

TEMPLATE_MAP = {
    "Германия": "Germany_template.txt",
    "Италия": "Italy_template.txt",
    "Китай": "China_template.txt",
    "Азия": "Asia_template.txt",
    "Сборки": "Sborki_template.txt",
    "СНГ": "Rus_template.txt",
    "ЦЕ": "Europe_template.txt",
    "Турция": "Turkey_template.txt"
}

TRANSIT_DAYS = {
    "Китай": "40дн.",
    "Германия": "7дн.",
    "Италия": "7дн.",
    "ЦЕ": "7дн.",
    "Турция": "14дн.",
    "СНГ": "7дн.",
    "Азия": "20дн.",
    "Сборки": "12дн."
}

CURRENCY_RATES = {
    "USD": 1.0,
    "BYN": 0.39,
    "RUB": 0.013,
    "CNY": 0.14,
    "EUR": 1.08
}


def load_template(filename):
    path = os.path.join(TEMPLATES_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_company_mapping():
    path = os.path.join(TEMPLATES_DIR, "company.txt")
    mapping = {}
    if not os.path.exists(path):
        return mapping
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                company_type, companies = line.split(":", 1)
                mapping[company_type.strip()] = companies.strip().rstrip(".")
    return mapping


class EmailConstructorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Email Constructor")
        self.root.geometry("850x1000")
        self.root.resizable(False, False)

        self.company_mapping = load_company_mapping()
        self.create_widgets()

    def create_widgets(self):
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Имя ЛПР:").pack(anchor="w")
        self.name_entry = ttk.Entry(main, width=60)
        self.name_entry.pack(anchor="w", pady=5)

        ttk.Label(main, text="Направление:").pack(anchor="w")
        self.direction_combo = ttk.Combobox(main, values=list(TEMPLATE_MAP.keys()), state="readonly")
        self.direction_combo.pack(anchor="w", pady=5)

        ttk.Label(main, text="Тип компании:").pack(anchor="w")
        self.company_type_combo = ttk.Combobox(
            main,
            values=[
                "Фарма", "Пищевые добавки", "Кондитерка",
                "Кофе/чай/какао", "Оборудование",
                "Сантехника", "Алкоголь", "Корма"
            ],
            state="readonly"
        )
        self.company_type_combo.pack(anchor="w", pady=5)

        ttk.Label(main, text="Доп. сервис:").pack(anchor="w")
        self.service_combo = ttk.Combobox(main, values=["Нет", "Маркировка"], state="readonly")
        self.service_combo.current(0)
        self.service_combo.pack(anchor="w", pady=5)

        ttk.Label(main, text="Есть ставка?").pack(anchor="w")
        self.rate_var = tk.StringVar(value="Нет")
        rate_combo = ttk.Combobox(main, textvariable=self.rate_var, values=["Да", "Нет"], state="readonly")
        rate_combo.pack(anchor="w", pady=5)
        rate_combo.bind("<<ComboboxSelected>>", self.toggle_rate_fields)

        self.rate_frame = ttk.Frame(main)
        self.rate_frame.pack(fill="x", pady=10)

        ttk.Label(self.rate_frame, text="Тип ТС:").pack(anchor="w")
        self.vehicle_combo = ttk.Combobox(self.rate_frame, values=["40HC", "20фут", "тент", "реф"], state="readonly")
        self.vehicle_combo.pack(anchor="w", pady=3)

        ttk.Label(self.rate_frame, text="Условия (FCA/EXW/FOB):").pack(anchor="w")
        self.conditions_entry = ttk.Entry(self.rate_frame, width=60)
        self.conditions_entry.pack(anchor="w", pady=3)

        ttk.Label(self.rate_frame, text="Город загрузки:").pack(anchor="w")
        self.load_city_entry = ttk.Entry(self.rate_frame, width=60)
        self.load_city_entry.pack(anchor="w", pady=3)

        ttk.Label(self.rate_frame, text="Город выгрузки:").pack(anchor="w")
        self.unload_city_entry = ttk.Entry(self.rate_frame, width=60)
        self.unload_city_entry.pack(anchor="w", pady=3)

        ttk.Label(self.rate_frame, text="Ставка (пример 5000USD):").pack(anchor="w")
        self.rate_entry = ttk.Entry(self.rate_frame, width=60)
        self.rate_entry.pack(anchor="w", pady=3)

        ttk.Label(self.rate_frame, text="Морской фрахт:").pack(anchor="w")
        self.seaprice_entry = ttk.Entry(self.rate_frame, width=60)
        self.seaprice_entry.pack(anchor="w", pady=3)

        ttk.Label(self.rate_frame, text="ЖД фрахт:").pack(anchor="w")
        self.rwprice_entry = ttk.Entry(self.rate_frame, width=60)
        self.rwprice_entry.pack(anchor="w", pady=3)

        ttk.Label(self.rate_frame, text="Автовывоз:").pack(anchor="w")
        self.avdelivery_entry = ttk.Entry(self.rate_frame, width=60)
        self.avdelivery_entry.pack(anchor="w", pady=3)

        ttk.Label(self.rate_frame, text="Планируемые даты выхода:").pack(anchor="w")
        self.date_entry = ttk.Entry(self.rate_frame, width=60)
        self.date_entry.pack(anchor="w", pady=3)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Сгенерировать", command=self.generate_email).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Скопировать", command=self.copy_text).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Очистить", command=lambda: self.output_text.delete("1.0", tk.END)).pack(side="left", padx=5)

        self.output_text = tk.Text(main, height=25, wrap="word")
        self.output_text.pack(fill="both", expand=True)

        self.toggle_rate_fields()

    def toggle_rate_fields(self, event=None):
        state = "normal" if self.rate_var.get() == "Да" else "disabled"
        for child in self.rate_frame.winfo_children():
            try:
                child.configure(state=state)
            except:
                pass

    def build_route(self):
        load = self.load_city_entry.get().strip()
        unload = self.unload_city_entry.get().strip()
        if load and unload:
            return f"{load} - {unload}"
        return load or unload or ""

    def parse_currency(self, value):
        match = re.match(r"([0-9.]+)\s*([A-Z]+)", value.strip())
        if match:
            amount, currency = match.groups()
            return float(amount) * CURRENCY_RATES.get(currency.upper(), 1)
        return 0.0

    def calculate_allin(self):
        return (
            self.parse_currency(self.seaprice_entry.get()) +
            self.parse_currency(self.rwprice_entry.get()) +
            self.parse_currency(self.avdelivery_entry.get())
        )

    def generate_email(self):
        name = self.name_entry.get().strip() or "Коллеги"
        direction = self.direction_combo.get()
        company_type = self.company_type_combo.get()

        template_file = TEMPLATE_MAP.get(direction)
        text = load_template(template_file)

        text = text.replace("{company}", self.company_mapping.get(company_type, ""))

        transit_route = self.build_route()
        text = text.replace("{transit}", transit_route)

        if self.rate_var.get() == "Да":
            if direction == "Китай":
                price_block = (
                    f"{self.conditions_entry.get()} {transit_route}, {self.vehicle_combo.get()} - {self.rate_entry.get()}\n"
                    f"Морской фрахт: {self.seaprice_entry.get()}\n"
                    f"ЖД фрахт: {self.rwprice_entry.get()}\n"
                    f"Автовывоз: {self.avdelivery_entry.get()}\n"
                    f"Планируемые даты выхода: {self.date_entry.get()}\n"
                    f"Транзитный срок: {TRANSIT_DAYS.get(direction, 'уточняется')}"
                )
            else:
                price_block = (
                    f"{self.conditions_entry.get()} {transit_route}, {self.vehicle_combo.get()} - {self.rate_entry.get()}\n"
                    f"Транзитный срок: {TRANSIT_DAYS.get(direction, 'уточняется')}"
                )
            text = text.replace("{price}", price_block)
        else:
            text = text.replace("{price}", "")

        if "{sale}" in text:
            if self.rate_var.get() == "Да" and transit_route:
                text = text.replace("{sale}", f"Хочу предложить для Вас наши условия и тарифы по маршруту {transit_route}.")
            else:
                text = text.replace("{sale}", "")

        if "{marking}" in text:
            if self.service_combo.get() == "Маркировка":
                text = text.replace("{marking}", load_template("marking_template.txt"))
            else:
                text = text.replace("{marking}", "")

        if direction == "Китай" and self.rate_var.get() == "Да":
            text += f"\n\nALL-IN (USD): {self.calculate_allin():.2f}"

        final_text = f"{name}, Добрый день!\n\n" + text

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, final_text)

    def copy_text(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get("1.0", tk.END))
        messagebox.showinfo("Скопировано", "Текст скопирован в буфер обмена")


if __name__ == "__main__":
    if not os.path.exists(TEMPLATES_DIR):
        os.makedirs(TEMPLATES_DIR)

    root = tk.Tk()
    app = EmailConstructorApp(root)
    root.mainloop()
