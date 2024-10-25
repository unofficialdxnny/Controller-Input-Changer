import tkinter as tk
from tkinter import messagebox
import pygame
import vgamepad as vg

# Initialize Pygame for joystick detection
pygame.init()
pygame.joystick.init()


class ControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controller Input Switcher")

        self.gamepad = None

        # Create the main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Label for the detected controller
        self.controller_label = tk.Label(
            self.main_frame, text="Detecting controller..."
        )
        self.controller_label.pack(pady=5)

        # Button to detect the controller
        self.detect_button = tk.Button(
            self.main_frame, text="Detect Controller", command=self.detect_controller
        )
        self.detect_button.pack(pady=5)

        # Dropdown menu for input type selection with only Xbox 360 and DS4 options
        self.input_type_var = tk.StringVar(value="Select Input Type")
        self.input_type_menu = tk.OptionMenu(
            self.main_frame,
            self.input_type_var,
            "Xbox 360",
            "DS4",
        )
        self.input_type_menu.config(
            state="disabled"
        )  # Disabled until a controller is detected
        self.input_type_menu.pack(pady=5)

        # Button to apply the input type
        self.apply_button = tk.Button(
            self.main_frame, text="Apply Input Type", command=self.apply_input_type
        )
        self.apply_button.config(
            state="disabled"
        )  # Disabled until a controller is detected
        self.apply_button.pack(pady=5)

        # Detect controller on startup
        self.detect_controller()

    def detect_controller(self):
        """Detects the connected controller using pygame."""
        pygame.joystick.quit()
        pygame.joystick.init()

        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            controller_name = joystick.get_name()
            self.controller_label.config(text=f"Controller detected: {controller_name}")

            # Enable input selection and apply button
            self.input_type_menu.config(state="normal")
            self.apply_button.config(state="normal")
        else:
            self.controller_label.config(text="No controller connected.")
            messagebox.showerror(
                "Error", "No controller detected. Please connect a controller."
            )

    def apply_input_type(self):
        """Applies the selected input type to create a virtual controller."""
        input_type = self.input_type_var.get().lower().replace(" ", "_")
        if input_type not in ["xbox_360", "ds4"]:
            messagebox.showerror("Error", "Please select a valid input type.")
            return

        if self.gamepad:
            # Dispose of the previous gamepad if it exists
            del self.gamepad
            self.gamepad = None

        # Create a virtual controller based on the selected input type
        try:
            if input_type == "xbox_360":
                self.gamepad = vg.VX360Gamepad()
                self.controller_label.config(text="Xbox 360 Controller Emulated")
            elif input_type == "ds4":
                self.gamepad = vg.VDS4Gamepad()
                self.controller_label.config(text="DS4 Controller Emulated")

            messagebox.showinfo(
                "Success",
                f"Virtual {input_type.replace('_', ' ').capitalize()} controller created.",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create virtual controller: {e}")


# Create and run the Tkinter application
root = tk.Tk()
app = ControllerApp(root)
root.mainloop()
