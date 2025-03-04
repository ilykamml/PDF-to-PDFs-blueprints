import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from pdf_processor import process_pdf

class PDFProcessorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Processor")
        # self.geometry("600x500")
        self.create_widgets()
        self.grid_columnconfigure(0, weight=1)
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())
        self.resizable(False, False)
        print(self.winfo_width())

    def create_widgets(self):
        # Поле для выбора исходного файла
        tk.Label(self, text="Исходный PDF-файл:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Выбрать...", command=self.select_input_file).grid(row=0, column=2, padx=10, pady=5)

        # Поле для выбора папки сохранения
        tk.Label(self, text="Папка для сохранения:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.output_entry = tk.Entry(self, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Button(self, text="Выбрать...", command=self.select_output_folder).grid(row=1, column=2, padx=10, pady=5)

        # Кнопка запуска обработки
        self.start_button = tk.Button(self, text="Начать обработку", command=self.start_processing)
        self.start_button.grid(row=2, column=0, columnspan=3, padx=200, pady=10, sticky='ew')

        # Шкала загрузки
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate")
        self.progress.grid(row=3, column=0, columnspan=3, sticky='ew', padx=10, pady=10)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите исходный PDF-файл",
            filetypes=[("PDF files", "*.pdf")]
        )
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory(title="Выберите папку для сохранения результатов")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, folder_path)

    def start_processing(self):
        input_file = self.input_entry.get()
        output_dir = self.output_entry.get()

        if not input_file or not output_dir:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл и папку.")
            return

        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.run_processing, args=(input_file, output_dir)).start()

    def run_processing(self, input_file, output_dir):
        try:
            process_pdf(input_file, output_dir, self.update_progress)
            self.show_completion_message(output_dir)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.start_button.config(state=tk.NORMAL)

    def update_progress(self, value):
        self.progress['value'] = value
        self.update_idletasks()

    def show_completion_message(self, output_dir):
        def open_folder():
            os.startfile(output_dir)
            completion_window.destroy()

        completion_window = tk.Toplevel(self)
        completion_window.title("Обработка завершена")
        tk.Label(completion_window, text="Обработка завершена!").pack(pady=10)
        tk.Button(completion_window, text="ОК", command=completion_window.destroy).pack(side="left", padx=10, pady=10)
        tk.Button(completion_window, text="Открыть папку", command=open_folder).pack(side="right", padx=10, pady=10)

if __name__ == "__main__":
    app = PDFProcessorGUI()
    app.mainloop()
