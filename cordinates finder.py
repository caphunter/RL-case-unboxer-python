import pyautogui
import time


def wait_for_stationary_mouse(delay=5):
    """Waits until the mouse stays still for `delay` seconds, then prints its position."""
    last_position = pyautogui.position()
    start_time = time.time()

    while True:
        current_position = pyautogui.position()

        if current_position == last_position:
            elapsed_time = time.time() - start_time
            if elapsed_time >= delay:
                print(f"Mouse stationary for {delay} seconds at: {current_position}")
                return current_position  # Return the position after waiting
        else:
            start_time = time.time()  # Reset timer if the mouse moves
            last_position = current_position

        time.sleep(0.1)  # Small delay to prevent high CPU usage


# Run the function
wait_for_stationary_mouse()
