from gui import App
from config import Settings
from bot import Bot


class MainApp:
    """Brings all the programs together."""
    def __init__(self):
        """Creates whole structure."""
        self.settings = Settings()
        self.bot = Bot(self.settings)
        self.app = App(self.settings, self.bot)

    def run(self):
        """Shows the GUI."""
        self.app.mainloop()


if __name__ == "__main__":
    main = MainApp()
    main.run()
