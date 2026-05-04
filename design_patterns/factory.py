"""
Design Patterns: Factory Method
"""

from abc import ABC, abstractmethod


# Product interface
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_click(self, handler) -> None:
        pass


# Concrete products
class WindowsButton(Button):
    def render(self) -> str:
        return "Rendering Windows-style button"

    def on_click(self, handler):
        print("Windows click event")


class MacButton(Button):
    def render(self) -> str:
        return "Rendering Mac-style button"

    def on_click(self, handler):
        print("Mac click event")


# Creator
class Dialog(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        """Factory method - subclasses decide what to create."""
        pass

    def render(self) -> None:
        button = self.create_button()
        print(button.render())

    def click(self) -> None:
        button = self.create_button()
        button.on_click(lambda: print("Button clicked!"))


# Concrete creators
class WindowsDialog(Dialog):
    def create_button(self) -> Button:
        return WindowsButton()


class MacDialog(Dialog):
    def create_button(self) -> Button:
        return MacButton()


# Client code
def create_ui(dialog: Dialog):
    dialog.render()
    dialog.click()


# Usage
print("=== Windows UI ===")
create_ui(WindowsDialog())

print("\n=== Mac UI ===")
create_ui(MacDialog())