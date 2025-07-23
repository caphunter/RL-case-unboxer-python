import pygetwindow as gw
import pyautogui
import time
import os
import sys

# Paths to the screenshots of UI elements
reward_items_image = "reward_items_screenshot.png"
open_drop_image = "open_drop_button.png"
open_drop_not_possible_image = "open_drop_button_not_possible.png"
confirm_button_image = "confirm_button.png"
ok_button_image = "ok.png"
back_button_image = "back.png"

# Position of the "Start Unbox" button
start_unbox = (140, 370)

# Delay Variables
unbox_delay = 10
home_delay = 2

# Max runtime in seconds (e.g., 5 minutes)
MAX_RUNTIME = 300

# Check if all required images exist
required_images = [
    reward_items_image,
    open_drop_image,
    confirm_button_image,
    ok_button_image,
    back_button_image
]

missing_images = [img for img in required_images if not os.path.exists(img)]
if missing_images:
    print(f"[ERROR] Missing image files: {', '.join(missing_images)}")
    sys.exit(1)

# Function to locate and click the button if found
def find_and_click_button(image_path, timeout=2):
    try:
        print(f"[INFO] Searching for '{image_path}'...")
        button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8, minSearchTime=timeout)
        if button_location:
            print(f"[SUCCESS] Found and clicked: {image_path} at {button_location}")
            pyautogui.click(button_location)
            return True
        else:
            print(f"[WARNING] '{image_path}' not found.")
            return False
    except Exception as e:
        print(f"[ERROR] Error in find_and_click_button: {e}")
        return False

# Function to check if we are on the home screen
def check_home_screen():
    return find_and_click_button(reward_items_image)

# Main execution loop
unboxing_in_progress = False
start_time = time.time()

print("[START] Beginning automation loop. Press Ctrl+C to stop.")

try:
    while True:
        elapsed = time.time() - start_time
        if elapsed > MAX_RUNTIME:
            print("[INFO] Maximum runtime exceeded. Exiting.")
            break

        if not unboxing_in_progress:
            if check_home_screen():
                print("[INFO] Home screen detected. Waiting 5 seconds before starting unbox...")
                time.sleep(5)

                pyautogui.click(start_unbox)
                print("[ACTION] Clicked 'Start Unbox'.")
                unboxing_in_progress = True

        if unboxing_in_progress:
            if find_and_click_button(open_drop_image):
                print("[ACTION] Clicked 'Open Drop'.")

                # Step 5: Try to find and click the "Confirm" button
                if find_and_click_button(confirm_button_image, timeout=3):
                    print("[ACTION] Clicked 'Confirm'.")

                    # Step 6: Wait for and click the "OK" button
                    if find_and_click_button(ok_button_image, timeout=unbox_delay):
                        print("[ACTION] Clicked 'OK'. Restarting loop to check for another drop.")
                        continue
                    else:
                        print("[WARNING] 'OK' button not found. Trying to go back.")
                        if find_and_click_button(back_button_image, timeout=3):
                            print("[ACTION] Clicked 'Back'. Returning to home screen.")
                            unboxing_in_progress = False
                            continue
                        else:
                            print("[ERROR] 'Back' button not found after OK failed. Exiting to avoid loop.")
                            break
                else:
                    print("[WARNING] 'Confirm' button did not appear — likely no drops left.")
                    if find_and_click_button(back_button_image, timeout=3):
                        print("[ACTION] Clicked 'Back'. Going to home screen to retry.")
                        unboxing_in_progress = False
                        continue
                    else:
                        print("[ERROR] 'Back' button not found after missing confirm. Exiting.")
                        break
            else:
                print("[WARNING] 'Open Drop' button not found. Possibly finished all crates.")
                unboxing_in_progress = False
                break

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n[INFO] Interrupted by user. Exiting cleanly.")

print("[END] Script finished.")
