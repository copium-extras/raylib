import ctypes
import os
import platform
import time

# --- 1. Load the Raylib DLL ---

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# *** MODIFIED PART ***
# Construct the path to the DLL inside the 'zig_out/bin' subdirectory
dll_path = os.path.join(script_dir, "zig-out", "bin", "raylib.dll")

# Check if the DLL exists before trying to load it
if not os.path.exists(dll_path):
    raise FileNotFoundError(f"raylib.dll not found at the expected path: {dll_path}")

# Load the library
try:
    raylib = ctypes.CDLL(dll_path)
except OSError as e:
    print(f"Error loading raylib.dll: {e}")
    # On some systems, you might need to ensure all dependencies of
    # raylib.dll (like system libraries) are available.
    exit(1)

print(f"Successfully loaded raylib.dll from: {dll_path}")

# --- 2. Define Raylib Data Structures (as ctypes Structures) ---

class Vector2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]

class Color(ctypes.Structure):
    _fields_ = [("r", ctypes.c_ubyte),
                ("g", ctypes.c_ubyte),
                ("b", ctypes.c_ubyte),
                ("a", ctypes.c_ubyte)]

# --- 3. Define Raylib Function Prototypes ---
# It's crucial to define argtypes and restype for functions
# to ensure ctypes calls them correctly.

# void InitWindow(int width, int height, const char *title)
raylib.InitWindow.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
raylib.InitWindow.restype = None

# bool WindowShouldClose(void)
raylib.WindowShouldClose.argtypes = []
raylib.WindowShouldClose.restype = ctypes.c_bool

# void CloseWindow(void)
raylib.CloseWindow.argtypes = []
raylib.CloseWindow.restype = None

# void BeginDrawing(void)
raylib.BeginDrawing.argtypes = []
raylib.BeginDrawing.restype = None

# void EndDrawing(void)
raylib.EndDrawing.argtypes = []
raylib.EndDrawing.restype = None

# void ClearBackground(Color color)
raylib.ClearBackground.argtypes = [Color]
raylib.ClearBackground.restype = None

# void DrawText(const char *text, int posX, int posY, int fontSize, Color color)
raylib.DrawText.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, Color]
raylib.DrawText.restype = None

# void DrawCircleV(Vector2 center, float radius, Color color)
raylib.DrawCircleV.argtypes = [Vector2, ctypes.c_float, Color]
raylib.DrawCircleV.restype = None

# void SetTargetFPS(int fps)
raylib.SetTargetFPS.argtypes = [ctypes.c_int]
raylib.SetTargetFPS.restype = None

# --- 4. Main Test Logic ---

def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Initialize the window
    # Note: We need to encode the string to a byte string for C
    window_title = "Raylib DLL Test from Python".encode('utf-8')
    raylib.InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, window_title)

    # Set our game to run at 60 frames-per-second
    raylib.SetTargetFPS(60)

    # Circle position
    circle_pos = Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)
    circle_velocity = Vector2(3.0, 3.0) # pixels per frame
    
    print("Window initialized. Press ESC to close.")

    # Main game loop
    # Loop continues until the user presses ESC or closes the window
    while not raylib.WindowShouldClose():
        # --- Update ---
        circle_pos.x += circle_velocity.x
        circle_pos.y += circle_velocity.y

        # Bounce off screen edges
        if circle_pos.x > SCREEN_WIDTH or circle_pos.x < 0:
            circle_velocity.x *= -1
        if circle_pos.y > SCREEN_HEIGHT or circle_pos.y < 0:
            circle_velocity.y *= -1

        # --- Draw ---
        raylib.BeginDrawing()

        # Clear the background to a light gray
        raylib.ClearBackground(Color(245, 245, 245, 255)) # RAYWHITE

        # Draw some static text
        raylib.DrawText(
            "Success! raylib is running from Python.".encode('utf-8'),
            190,
            200,
            20,
            Color(130, 130, 130, 255) # GRAY
        )

        # Draw the moving circle
        raylib.DrawCircleV(circle_pos, 50, Color(255, 0, 0, 255)) # RED

        raylib.EndDrawing()

    # --- De-Initialization ---
    raylib.CloseWindow()
    print("Window closed. Test finished.")

if __name__ == '__main__':
    main()