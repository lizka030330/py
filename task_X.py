import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

class CocktailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конструктор коктейлів")
        
        # Список напоїв
        self.drinks = [
            {"name": "Віскі", "alcohol": 43, "color": "#C49258"},
            {"name": "Текіла", "alcohol": 40, "color": "#C6A15A"},
            {"name": "Вино", "alcohol": 12, "color": "#B24A2E"},
            {"name": "Пиво", "alcohol": 8, "color": "#F4D03F"},
            {"name": "Сок", "alcohol": 0, "color": "#FFA500"}
        ]
        
        self.ingredients = []
        self.total_volume = 0
        self.alcohol_content = 0
        self.color = "#FFFFFF"
        self.saved_recipes = []

        # Інтерфейс
        self.drink_buttons_frame = tk.Frame(root)
        self.drink_buttons_frame.grid(row=0, column=0, padx=10, pady=10)

        self.create_drink_buttons()

        self.ingredients_label = tk.Label(root, text="Інгредієнти коктейлю:")
        self.ingredients_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.ingredients_listbox = tk.Listbox(root, width=50, height=10)
        self.ingredients_listbox.grid(row=2, column=0, padx=10, pady=10)

        self.alcohol_label = tk.Label(root, text="Вміст алкоголю: 0%")
        self.alcohol_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.color_label = tk.Label(root, text="Колір коктейлю:")
        self.color_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.color_display = tk.Canvas(root, width=200, height=50, bg=self.color)
        self.color_display.grid(row=5, column=0, padx=10, pady=10)

        self.clear_button = tk.Button(root, text="Очистити коктейль", command=self.clear_cocktail)
        self.clear_button.grid(row=6, column=0, padx=10, pady=10)

        self.save_button = tk.Button(root, text="Зберегти рецепт", command=self.save_recipe)
        self.save_button.grid(row=7, column=0, padx=10, pady=10)

        self.show_recipes_button = tk.Button(root, text="Переглянути рецепти", command=self.show_saved_recipes)
        self.show_recipes_button.grid(row=8, column=0, padx=10, pady=10)

    def create_drink_buttons(self):
        for drink in self.drinks:
            button = tk.Button(self.drink_buttons_frame, text=f"{drink['name']} ({drink['alcohol']}%)", 
                               command=lambda d=drink: self.add_ingredient(d))
            button.pack(side="left", padx=5)

    def add_ingredient(self, drink):
        volume = tk.simpledialog.askinteger("Введіть об'єм", f"Введіть об'єм {drink['name']} (мл):")
        if volume is None or volume <= 0:
            return

        self.ingredients.append({"name": drink['name'], "alcohol": drink['alcohol'], 
                                 "color": drink['color'], "volume": volume})
        self.total_volume += volume
        self.update_cocktail()

    def update_cocktail(self):
        # Розрахунок вмісту алкоголю
        total_alcohol = sum(item["volume"] * item["alcohol"] for item in self.ingredients)
        self.alcohol_content = (total_alcohol / self.total_volume) if self.total_volume else 0
        self.alcohol_label.config(text=f"Вміст алкоголю: {self.alcohol_content:.2f}%")

        # Розрахунок кольору коктейлю
        avg_color = self.calculate_average_color()
        self.color = avg_color
        self.color_display.config(bg=self.color)

        # Оновлення списку інгредієнтів
        self.ingredients_listbox.delete(0, tk.END)
        for item in self.ingredients:
            self.ingredients_listbox.insert(tk.END, f"{item['name']} - {item['volume']} мл")

    def calculate_average_color(self):
        r, g, b = 0, 0, 0
        for ingredient in self.ingredients:
            hex_color = ingredient['color']
            r_ig, g_ig, b_ig = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
            r += r_ig
            g += g_ig
            b += b_ig
        n = len(self.ingredients)
        if n > 0:
            r //= n
            g //= n
            b //= n
        return f"#{r:02x}{g:02x}{b:02x}"

    def clear_cocktail(self):
        self.ingredients.clear()
        self.total_volume = 0
        self.alcohol_content = 0
        self.color = "#FFFFFF"
        self.update_cocktail()

    def save_recipe(self):
        name = tk.simpledialog.askstring("Назва коктейлю", "Введіть назву коктейлю:")
        if not name:
            return
        self.saved_recipes.append({
            "name": name,
            "alcohol_content": self.alcohol_content,
            "color": self.color
        })
        messagebox.showinfo("Коктейль збережено", "Ваш коктейль було успішно збережено.")

    def show_saved_recipes(self):
        if not self.saved_recipes:
            messagebox.showinfo("Немає збережених коктейлів", "У вас ще немає збережених коктейлів.")
            return
        recipes_window = tk.Toplevel(self.root)
        recipes_window.title("Збережені рецепти")
        for recipe in self.saved_recipes:
            recipe_label = tk.Label(recipes_window, text=f"{recipe['name']} - {recipe['alcohol_content']:.2f}% - {recipe['color']}")
            recipe_label.pack(padx=10, pady=5)

if __name__ == "__main__":
    import tkinter.simpledialog
    root = tk.Tk()
    app = CocktailApp(root)
    root.mainloop()
