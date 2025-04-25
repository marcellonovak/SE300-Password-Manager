import unittest
from unittest.mock import patch
import tkinter as tk
import gui_main
from gui_main import PasswordManagerGUI

# Assumption that PIN is "1111" for test cases. If it was modified, ensure it returns to "1111" to run unit tests


class TesPasswordManager(unittest.TestCase):
    @patch("tkinter.simpledialog.askstring", return_value="0000")
    def test_wrong_pin(self, mock_ask):
        # Test Case 1
        root = tk.Tk()
        root.withdraw()
        gui = PasswordManagerGUI(root)
        result = gui.verify_pin()
        self.assertIsNone(result)
        root.destroy()

    @patch("tkinter.simpledialog.askstring", side_effect=["0000", "1234", "1111"])
    def test_multiple_wrong_pin(self, mock_ask):
        # Test Case 2
        root = tk.Tk()
        root.withdraw()
        gui = PasswordManagerGUI(root)

        for _ in range(3):
            result = gui.verify_pin()
            if result == "1111":
                break

        self.assertEqual(result, "1111")
        root.destroy()

    @patch("tkinter.simpledialog.askstring", side_effect=["6544", "123456234", "0987"])
    def test_all_wrong_pin(self, mock_ask):
        # Test Case 3
        root = tk.Tk()
        root.withdraw()
        gui = PasswordManagerGUI(root)

        for _ in range(3):
            result = gui.verify_pin()
            if result == "1111":
                break

        self.assertIsNone(result)
        root.destroy()

    @patch("tkinter.simpledialog.askstring", return_value="1111")
    def test_correct_pin(self, mock_ask):
        # Test Case 4
        root = tk.Tk()
        root.withdraw()
        gui = PasswordManagerGUI(root)
        result = gui.verify_pin()
        self.assertEqual(result, "1111")
        root.destroy()

    @patch(
        "tkinter.simpledialog.askstring",
        return_value="111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
    )
    def test_long_incorrect_pin(self, mock_ask):
        # Test Case 5
        root = tk.Tk()
        root.withdraw()
        gui = PasswordManagerGUI(root)
        result = gui.verify_pin()
        self.assertIsNone(result)
        root.destroy()


if __name__ == "__main__":
    unittest.main()
