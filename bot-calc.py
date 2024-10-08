#a python calculator with ui using tklib entirely written by chatbots

import tkinter as tk
from typing import Callable, Dict, List, Union

class Calculator:
    def __init__(self):
        self.memory: float = 0
        self.error_showing = False
        self.start_new_number = False
        
        # Constants for layout
        self.BUTTON_WIDTH = 6
        self.BUTTON_HEIGHT = 2
        self.TOTAL_COLUMNS = 5
        self.TOTAL_ROWS = 5
        self.PADDING_X = 5
        self.PADDING_Y = 5
        
        self.setup_window()
        self.setup_display()
        self.create_buttons()
        
    def setup_window(self) -> None:
        self.window = tk.Tk()
        self.window.title("Calculator")
        
        # Calculate window dimensions more precisely
        button_pixel_width = 50  # Adjusted base button width
        button_pixel_height = 40  # Adjusted base button height
        
        # Calculate total width including all padding
        total_width = (button_pixel_width * self.TOTAL_COLUMNS) + (self.PADDING_X * (self.TOTAL_COLUMNS + 1))
        # Calculate total height including all padding and display
        total_height = (button_pixel_height * self.TOTAL_ROWS) + (self.PADDING_Y * (self.TOTAL_ROWS + 1)) + 40  # 40 for display
        
        # Set minimum size to prevent shrinking
        self.window.minsize(total_width, total_height)
        self.window.resizable(False, False)

    def setup_display(self) -> None:
        # Calculate display width based on button grid width
        display_width = self.BUTTON_WIDTH * self.TOTAL_COLUMNS
        
        self.display = tk.Entry(
            self.window,
            width=display_width,
            borderwidth=3,  # Slightly reduced border
            font=('Arial', 16),
            justify='right'
        )
        self.display.grid(
            row=0,
            column=0,
            columnspan=5,
            padx=self.PADDING_X,
            pady=self.PADDING_Y,
            sticky='ew'  # Stretch horizontally
        )

    def button_click(self, value: str) -> None:
        if self.error_showing:
            self.clear()
            self.error_showing = False

        current = self.display.get()
        
        if value in ['+', '-', '×', '÷']:
            self.start_new_number = False
        elif self.start_new_number:
            current = ''
            self.start_new_number = False
            
        if value == '.':
            if '.' in current or not current:
                return
            
        self.display.delete(0, tk.END)
        self.display.insert(0, current + str(value))

    def clear(self) -> None:
        self.display.delete(0, tk.END)
        self.error_showing = False
        self.start_new_number = False

    def evaluate(self) -> None:
        if self.error_showing:
            self.clear()
            return

        try:
            expression = self.display.get()
            
            if '/0' in expression.replace(' ', ''):
                raise ZeroDivisionError("Division by zero")
                
            expression = expression.replace('×', '*').replace('÷', '/')
            
            result = eval(expression)
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 8)
                    result = '{:.8f}'.format(result).rstrip('0').rstrip('.')
                    
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.start_new_number = True
            
        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")
        except Exception:
            self.show_error("Error")

    def show_error(self, message: str) -> None:
        self.display.delete(0, tk.END)
        self.display.insert(0, message)
        self.error_showing = True
        self.start_new_number = True

    def memory_clear(self) -> None:
        self.memory = 0
        if self.error_showing:
            self.clear()

    def memory_recall(self) -> None:
        if self.error_showing:
            self.clear()
        self.display.delete(0, tk.END)
        self.display.insert(0, str(self.memory))
        self.start_new_number = True

    def memory_operation(self, operation: Callable[[float, float], float]) -> None:
        if self.error_showing:
            self.clear()
            return
            
        try:
            current_value = float(self.display.get())
            self.memory = operation(self.memory, current_value)
            self.clear()
        except ValueError:
            self.show_error("Error")

    def toggle_sign(self) -> None:
        if self.error_showing:
            self.clear()
            return
            
        try:
            current = self.display.get()
            if current:
                value = float(current)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(-value))
        except ValueError:
            self.show_error("Error")

    def calculate_percentage(self) -> None:
        if self.error_showing:
            self.clear()
            return
            
        try:
            current = float(self.display.get())
            result = current / 100
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.start_new_number = True
        except ValueError:
            self.show_error("Error")

    def create_buttons(self) -> None:
        buttons_layout: List[List[str]] = [
            ['mc', 'mr', 'm-', 'm+', '÷'],
            ['%', '7', '8', '9', '×'],
            ['+/-', '4', '5', '6', '-'],
            ['C', '1', '2', '3', '+'],
            ['AC', '0', '.', '=', '']
        ]

        button_functions: Dict[str, Callable[[], None]] = {
            'mc': self.memory_clear,
            'mr': self.memory_recall,
            'm+': lambda: self.memory_operation(lambda x, y: x + y),
            'm-': lambda: self.memory_operation(lambda x, y: x - y),
            'C': self.clear,
            'AC': self.clear,
            '=': self.evaluate,
            '+/-': self.toggle_sign,
            '%': self.calculate_percentage
        }

        # Configure grid columns to be equal width
        for i in range(self.TOTAL_COLUMNS):
            self.window.grid_columnconfigure(i, weight=1)

        for i, row in enumerate(buttons_layout):
            for j, button_text in enumerate(row):
                if not button_text:
                    continue
                    
                command: Union[Callable[[], None], Callable[[str], None]]
                if button_text in button_functions:
                    command = button_functions[button_text]
                else:
                    command = lambda x=button_text: self.button_click(x)

                button = tk.Button(
                    self.window,
                    text=button_text,
                    width=self.BUTTON_WIDTH,
                    height=self.BUTTON_HEIGHT,
                    command=command
                )
                button.grid(
                    row=i+1,
                    column=j,
                    padx=self.PADDING_X,
                    pady=self.PADDING_Y,
                    sticky='nsew'  # Make buttons expand to fill their grid cell
                )

    def run(self) -> None:
        self.window.mainloop()

if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()