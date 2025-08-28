import tkinter as tk
from tkinter import ttk, messagebox
import math
import sys
import os

class SpO2Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("SpO₂ Calculator")
        self.root.geometry("350x560")
        self.root.resizable(False, False)

        # Цветовая схема
        self.bg_color = "#f8f9fa"
        self.frame_bg = "#ffffff"
        self.accent_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.text_color = "#212121"
        self.border_color = "#dee2e6"

        self.root.configure(bg=self.bg_color)

        # Создание интерфейса
        self.create_widgets()

    def create_context_menu(self, entry_widget):
        """Создание контекстного меню для полей ввода"""
        menu = tk.Menu(self.root, tearoff=0, font=('Segoe UI', 9))

        is_readonly = entry_widget.cget('state') == 'readonly'

        if not is_readonly:
            menu.add_command(label="✂ Вырезать",
                           command=lambda: self.cut_text(entry_widget))

        menu.add_command(label="📋 Копировать",
                       command=lambda: self.copy_text(entry_widget))

        if not is_readonly:
            menu.add_command(label="📄 Вставить",
                           command=lambda: self.paste_text(entry_widget))
            menu.add_separator()
            menu.add_command(label="🗑 Очистить",
                           command=lambda: entry_widget.delete(0, tk.END))

        menu.add_separator()
        menu.add_command(label="🔍 Выделить все",
                       command=lambda: entry_widget.select_range(0, tk.END))

        def show_menu(event):
            entry_widget.focus_set()
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

        entry_widget.bind("<Button-3>", show_menu)

    def cut_text(self, widget):
        """Вырезать текст"""
        try:
            text = widget.selection_get()
            widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except:
            pass

    def copy_text(self, widget):
        """Копировать текст"""
        try:
            if widget.selection_present():
                text = widget.selection_get()
            else:
                text = widget.get()
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except:
            pass

    def paste_text(self, widget):
        """Вставить текст"""
        try:
            text = self.root.clipboard_get()
            if widget.selection_present():
                widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
            widget.insert(widget.index(tk.INSERT), text)
        except:
            pass

    def create_widgets(self):
        """Создание всех виджетов интерфейса"""

        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill='both', expand=True, padx=12, pady=12)

        # Заголовок
        header_frame = tk.Frame(main_container, bg=self.accent_color, height=40)
        header_frame.pack(fill='x', pady=(0, 12))
        header_frame.pack_propagate(False)

        header_label = tk.Label(header_frame,
                               text="🩺 SpO₂ Calculator",
                               bg=self.accent_color,
                               fg='white',
                               font=('Segoe UI', 13, 'bold'))
        header_label.pack(expand=True)

        # Фрейм для ввода данных
        input_frame = tk.Frame(main_container, bg=self.frame_bg, relief='flat', bd=1)
        input_frame.pack(fill='x', pady=(0, 10), anchor='w')

        # Заголовок секции
        input_header = tk.Frame(input_frame, bg='#e8f4f8', height=32)
        input_header.pack(fill='x')
        input_header.pack_propagate(False)

        tk.Label(input_header, text="📊 Входные данные",
                bg='#e8f4f8', fg=self.text_color,
                font=('Segoe UI', 10, 'bold')).pack(side='left', padx=10, pady=6)

        # Таблица ввода
        table_frame = tk.Frame(input_frame, bg=self.frame_bg)
        table_frame.pack(fill='x', padx=10, pady=10, anchor='w')

        # Заголовки колонок
        headers = ['λ (нм)', 'Id', 'Is']
        widths = [8, 12, 12]
        for col, (header, width) in enumerate(zip(headers, widths)):
            label = tk.Label(table_frame, text=header,
                           bg=self.frame_bg, fg='#495057',
                           font=('Segoe UI', 9, 'bold'), width=width, anchor='w')
            label.grid(row=0, column=col, padx=5, pady=(0, 5), sticky='w')

        # Создание полей ввода
        self.entries = {}
        wavelengths = [660, 805, 880, 940]

        for row, wavelength in enumerate(wavelengths, start=1):
            # Метка длины волны с цветовой индикацией
            colors = ['#ff6b6b', '#ffa726', '#66bb6a', '#ab47bc']
            wave_label = tk.Label(table_frame, text=f"● {wavelength}",
                                bg=self.frame_bg, fg=colors[row-1],
                                font=('Segoe UI', 9, 'bold'), width=8, anchor='w')
            wave_label.grid(row=row, column=0, padx=5, pady=3, sticky='w')

            # Поле для Id
            id_entry = tk.Entry(table_frame, width=12, font=('Segoe UI', 9),
                              relief='solid', bd=1, highlightthickness=0)
            id_entry.grid(row=row, column=1, padx=5, pady=3, sticky='w')
            self.entries[f'id_{wavelength}'] = id_entry
            self.create_context_menu(id_entry)

            # Поле для Is
            is_entry = tk.Entry(table_frame, width=12, font=('Segoe UI', 9),
                              relief='solid', bd=1, highlightthickness=0)
            is_entry.grid(row=row, column=2, padx=5, pady=3, sticky='w')
            self.entries[f'is_{wavelength}'] = is_entry
            self.create_context_menu(is_entry)

        # Фрейм для промежуточных результатов R
        r_frame = tk.Frame(main_container, bg=self.frame_bg, relief='flat', bd=1)
        r_frame.pack(fill='x', pady=(0, 10), anchor='w')

        # Заголовок секции
        r_header = tk.Frame(r_frame, bg='#fff3e0', height=32)
        r_header.pack(fill='x')
        r_header.pack_propagate(False)

        tk.Label(r_header, text="🔢 Промежуточные расчеты",
                bg='#fff3e0', fg=self.text_color,
                font=('Segoe UI', 10, 'bold')).pack(side='left', padx=10, pady=6)

        # Контейнер для значений R
        r_values_frame = tk.Frame(r_frame, bg=self.frame_bg)
        r_values_frame.pack(fill='x', padx=10, pady=10, anchor='w')

        self.r_labels = {}
        colors = ['#ff6b6b', '#ffa726', '#66bb6a', '#ab47bc']
        for i in range(1, 5):
            row = (i-1) // 2
            col = (i-1) % 2

            r_container = tk.Frame(r_values_frame, bg=self.frame_bg)
            r_container.grid(row=row, column=col, padx=5, pady=3, sticky='w')

            r_name = tk.Label(r_container, text=f"R{i} =",
                            bg=self.frame_bg, fg=colors[i-1],
                            font=('Segoe UI', 9, 'bold'), width=4, anchor='w')
            r_name.pack(side='left')

            r_value_entry = tk.Entry(r_container, width=14,
                                    font=('Segoe UI', 9),
                                    relief='solid', bd=1,
                                    state='readonly',
                                    readonlybackground='#f8f9fa')
            r_value_entry.pack(side='left', padx=(2, 0))
            self.r_labels[f'R{i}'] = r_value_entry
            self.create_context_menu(r_value_entry)

        # Фрейм для результата
        result_frame = tk.Frame(main_container, bg=self.frame_bg, relief='flat', bd=1)
        result_frame.pack(fill='x', pady=(0, 10))

        # Заголовок секции
        result_header = tk.Frame(result_frame, bg='#e8f5e9', height=32)
        result_header.pack(fill='x')
        result_header.pack_propagate(False)

        tk.Label(result_header, text="✅ Результат",
                bg='#e8f5e9', fg=self.text_color,
                font=('Segoe UI', 10, 'bold')).pack(side='left', padx=10, pady=6)

        # Контейнер для результатов
        result_container = tk.Frame(result_frame, bg=self.frame_bg)
        result_container.pack(fill='x', padx=10, pady=10)

        # SpO2 как доля
        fraction_container = tk.Frame(result_container, bg=self.frame_bg)
        fraction_container.pack(fill='x', pady=3)

        tk.Label(fraction_container, text="SpO₂ =",
                font=('Segoe UI', 10),
                bg=self.frame_bg, fg=self.text_color, width=10, anchor='w').pack(side='left')

        self.result_fraction_entry = tk.Entry(fraction_container,
                                             font=('Segoe UI', 10, 'bold'),
                                             width=15,
                                             state='readonly',
                                             relief='solid', bd=1,
                                             readonlybackground='#e8f5e9',
                                             fg=self.success_color)
        self.result_fraction_entry.pack(side='left', padx=(0, 8))
        self.create_context_menu(self.result_fraction_entry)

        self.copy_fraction_button = tk.Button(fraction_container, text="📋 Копировать",
                                             command=lambda: self.copy_result(self.result_fraction_entry),
                                             state='disabled',
                                             bg=self.success_color, fg='white',
                                             font=('Segoe UI', 9),
                                             relief='flat', bd=0,
                                             padx=12, pady=3,
                                             cursor='hand2')
        self.copy_fraction_button.pack(side='left')

        # SpO2 в процентах
        percent_container = tk.Frame(result_container, bg=self.frame_bg)
        percent_container.pack(fill='x', pady=3)

        tk.Label(percent_container, text="SpO₂ (%) =",
                font=('Segoe UI', 10),
                bg=self.frame_bg, fg=self.text_color, width=10, anchor='w').pack(side='left')

        self.result_percent_entry = tk.Entry(percent_container,
                                            font=('Segoe UI', 10, 'bold'),
                                            width=15,
                                            state='readonly',
                                            relief='solid', bd=1,
                                            readonlybackground='#e8f5e9',
                                            fg=self.success_color)
        self.result_percent_entry.pack(side='left', padx=(0, 8))
        self.create_context_menu(self.result_percent_entry)

        self.copy_percent_button = tk.Button(percent_container, text="📋 Копировать",
                                            command=lambda: self.copy_result(self.result_percent_entry),
                                            state='disabled',
                                            bg=self.success_color, fg='white',
                                            font=('Segoe UI', 9),
                                            relief='flat', bd=0,
                                            padx=12, pady=3,
                                            cursor='hand2')
        self.copy_percent_button.pack(side='left')

        # Фрейм для кнопок управления
        button_frame = tk.Frame(main_container, bg=self.bg_color)
        button_frame.pack(fill='x', pady=(5, 0))

        button_container = tk.Frame(button_frame, bg=self.bg_color)
        button_container.pack()

        # Кнопка расчета
        calc_button = tk.Button(button_container, text="🧮 Рассчитать",
                              command=self.calculate,
                              bg=self.accent_color, fg='white',
                              font=('Segoe UI', 11, 'bold'),
                              relief='flat', bd=0,
                              padx=25, pady=10,
                              cursor='hand2',
                              activebackground='#1976D2')
        calc_button.pack(side='left', padx=5)

        # Эффект при наведении
        calc_button.bind("<Enter>", lambda e: calc_button.config(bg='#1976D2'))
        calc_button.bind("<Leave>", lambda e: calc_button.config(bg=self.accent_color))

        # Кнопка очистки
        clear_button = tk.Button(button_container, text="🗑 Очистить",
                               command=self.clear_all,
                               bg='#6c757d', fg='white',
                               font=('Segoe UI', 10),
                               relief='flat', bd=0,
                               padx=20, pady=10,
                               cursor='hand2',
                               activebackground='#5a6268')
        clear_button.pack(side='left', padx=5)

        # Эффект при наведении
        clear_button.bind("<Enter>", lambda e: clear_button.config(bg='#5a6268'))
        clear_button.bind("<Leave>", lambda e: clear_button.config(bg='#6c757d'))

    def parse_number(self, value_str):
        """Парсинг числа с поддержкой точки и запятой"""
        if not value_str.strip():
            raise ValueError("Пустое значение")

        # Замена запятой на точку
        value_str = value_str.replace(',', '.')

        try:
            value = float(value_str)
            if value <= 0:
                raise ValueError("Значение должно быть положительным")
            return value
        except ValueError:
            raise ValueError(f"Некорректное число: {value_str}")

    def calculate(self):
        """Расчет SpO2"""
        try:
            wavelengths = [660, 805, 880, 940]
            r_values = []

            # Расчет R для каждой длины волны
            for i, wavelength in enumerate(wavelengths, start=1):
                id_str = self.entries[f'id_{wavelength}'].get()
                is_str = self.entries[f'is_{wavelength}'].get()

                # Парсинг значений
                try:
                    id_val = self.parse_number(id_str)
                    is_val = self.parse_number(is_str)
                except ValueError as e:
                    raise ValueError(f"Ошибка в данных для {wavelength} нм: {e}")

                if is_val >= id_val:
                    raise ValueError(f"Is должно быть меньше Id для {wavelength} нм")

                # Расчет R
                r = math.log(id_val / is_val)
                r_values.append(r)

                # Отображение R
                self.r_labels[f'R{i}'].config(state='normal')
                self.r_labels[f'R{i}'].delete(0, tk.END)
                self.r_labels[f'R{i}'].insert(0, f"{r:.6f}")
                self.r_labels[f'R{i}'].config(state='readonly')

            # Расчет SpO2 по формуле
            r1, r2, r3, r4 = r_values

            numerator = 1.587 * r1 - 5.348 * r2 - 4.009 * r3 + 3.426 * r4
            denominator = 5.43 * r1 - 140.05 * r2 + 168.532 * r3 - 73.191 * r4

            if abs(denominator) < 1e-10:
                raise ValueError("Деление на ноль при расчете SpO₂")

            spo2_fraction = numerator / denominator
            spo2_percent = spo2_fraction * 100

            # Отображение результата как доли
            self.result_fraction_entry.config(state='normal')
            self.result_fraction_entry.delete(0, tk.END)
            self.result_fraction_entry.insert(0, f"{spo2_fraction:.4f}")
            self.result_fraction_entry.config(state='readonly')

            # Отображение результата в процентах
            self.result_percent_entry.config(state='normal')
            self.result_percent_entry.delete(0, tk.END)
            self.result_percent_entry.insert(0, f"{spo2_percent:.2f}")
            self.result_percent_entry.config(state='readonly')

            # Активация кнопок копирования
            self.copy_fraction_button.config(state='normal')
            self.copy_percent_button.config(state='normal')

        except ValueError as e:
            messagebox.showerror("❌ Ошибка ввода", str(e))
            self.clear_result()
        except Exception as e:
            messagebox.showerror("❌ Ошибка расчета", f"Произошла ошибка: {str(e)}")
            self.clear_result()

    def clear_all(self):
        """Очистка всех полей"""
        wavelengths = [660, 805, 880, 940]
        for wavelength in wavelengths:
            self.entries[f'id_{wavelength}'].delete(0, tk.END)
            self.entries[f'is_{wavelength}'].delete(0, tk.END)

        for i in range(1, 5):
            self.r_labels[f'R{i}'].config(state='normal')
            self.r_labels[f'R{i}'].delete(0, tk.END)
            self.r_labels[f'R{i}'].config(state='readonly')

        self.clear_result()

    def clear_result(self):
        """Очистка результата"""
        self.result_fraction_entry.config(state='normal')
        self.result_fraction_entry.delete(0, tk.END)
        self.result_fraction_entry.config(state='readonly')

        self.result_percent_entry.config(state='normal')
        self.result_percent_entry.delete(0, tk.END)
        self.result_percent_entry.config(state='readonly')

        self.copy_fraction_button.config(state='disabled')
        self.copy_percent_button.config(state='disabled')

    def copy_result(self, entry_widget):
        """Копирование результата в буфер обмена"""
        result = entry_widget.get()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            # Визуальная обратная связь
            original_bg = entry_widget.cget('readonlybackground')
            entry_widget.config(readonlybackground='#c8e6c9')
            self.root.after(300, lambda: entry_widget.config(readonlybackground=original_bg))

def main():
    """Главная функция"""
    try:
        root = tk.Tk()
        app = SpO2Calculator(root)

        # Центрирование окна
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Произошла критическая ошибка:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
