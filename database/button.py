from tkinter import ttk


class CustomButton(ttk.Button):
    def __init__(self, parent, text="", command=None, style_type="primary", **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.style_type = style_type
        self.configure_style()

    def configure_style(self):
        style = ttk.Style()
        # Định nghĩa các loại nút bấm
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'), foreground='#2980b9')
        style.configure('Success.TButton', font=('Arial', 10, 'bold'), foreground='#27ae60')
        style.configure('Danger.TButton', font=('Arial', 10, 'bold'), foreground='#c0392b')
        style.configure('Warning.TButton', font=('Arial', 10, 'bold'), foreground='#e67e22')
        style.configure('Info.TButton', font=('Arial', 10, 'bold'), foreground='#3498db')
        style.configure('Secondary.TButton', font=('Arial', 10), foreground='#7f8c8d')

        self.configure(style=f'{self.style_type.capitalize()}.TButton')