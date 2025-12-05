"""
F1 Auto-Press using Interception Driver for MSI App Player
REQUIRES: 
- Interception driver installed (install-interception.exe /install)
- System reboot after driver installation
- Run as Administrator
- pip install interception
"""

import time
import threading
from interception import ffi, lib

# Configuration
IDLE_THRESHOLD = 0.8
last_activity_time = time.time()
lock = threading.Lock()
running = True

# Interception constants
def INTERCEPTION_KEYBOARD(device):
    return device > 0 and device < 11

def INTERCEPTION_MOUSE(device):
    return device > 10 and device < 21

# Create callback for filter
@ffi.callback("int(int)")
def keyboard_filter(device):
    return INTERCEPTION_KEYBOARD(device)

# Key states
KEY_DOWN = 0x00
KEY_UP = 0x01

# F1 scan code
SCANCODE_F1 = 0x3B

def send_f1_double(context):
    """Send F1 key press twice"""
    try:
        # Create keyboard stroke structure
        stroke = ffi.new("InterceptionKeyStroke *")
        
        # First F1 press - DOWN
        stroke.code = SCANCODE_F1
        stroke.state = KEY_DOWN
        lib.interception_send(context, 1, ffi.cast("InterceptionStroke *", stroke), 1)
        time.sleep(0.05)
        
        # First F1 press - UP
        stroke.state = KEY_UP
        lib.interception_send(context, 1, ffi.cast("InterceptionStroke *", stroke), 1)
        time.sleep(0.1)
        
        # Second F1 press - DOWN
        stroke.state = KEY_DOWN
        lib.interception_send(context, 1, ffi.cast("InterceptionStroke *", stroke), 1)
        time.sleep(0.05)
        
        # Second F1 press - UP
        stroke.state = KEY_UP
        lib.interception_send(context, 1, ffi.cast("InterceptionStroke *", stroke), 1)
        
        return True
    except Exception as e:
        print(f"❌ Error sending F1: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_idle_and_press(context):
    """Check if idle and send F1 if needed"""
    global last_activity_time
    
    with lock:
        now = time.time()
        elapsed = now - last_activity_time
        
        if elapsed >= IDLE_THRESHOLD:
            print(f"⏱️  Idle {IDLE_THRESHOLD:.1f}s → F1 x2")
            send_f1_double(context)
            last_activity_time = time.time()

def monitor_idle(context):
    """Monitor for idle time"""
    while running:
        time.sleep(0.1)
        check_idle_and_press(context)

def monitor_keyboard(context):
    """Monitor keyboard activity to reset idle timer"""
    global last_activity_time
    
    try:
        stroke = ffi.new("InterceptionKeyStroke *")
        
        while running:
            # Wait for device with timeout
            device = lib.interception_wait_with_timeout(context, 100)
            
            if device > 0:
                # Check if it's a keyboard
                if INTERCEPTION_KEYBOARD(device):
                    # Receive the stroke
                    received = lib.interception_receive(context, device, ffi.cast("InterceptionStroke *", stroke), 1)
                    
                    if received > 0:
                        # Reset idle timer on any key press
                        with lock:
                            last_activity_time = time.time()
                        
                        # Pass through the keystroke
                        lib.interception_send(context, device, ffi.cast("InterceptionStroke *", stroke), 1)
    except Exception as e:
        print(f"⚠️  Keyboard monitor error: {e}")
        import traceback
        traceback.print_exc()

def main():
    global running
    
    try:
        print("🔧 Initializing Interception driver...")
        
        # Create interception context
        context = lib.interception_create_context()
        
        if not context:
            print("❌ Failed to create Interception context!")
            print("\n⚠️  Troubleshooting:")
            print("1. Did you REBOOT after installing the driver?")
            print("2. Are you running as Administrator?")
            print("3. Is Interception driver installed? Run: install-interception.exe /install")
            return
        
        print("✅ Interception driver loaded!")
        print(f"⏱️  Idle threshold: {IDLE_THRESHOLD}s")
        print("🎮 Script active - will auto-press F1 x2 after idle period")
        print("⌨️  Type 't' + ENTER to manually test F1 x2")
        print("🛑 Press Ctrl+C to stop")
        print("=" * 60)
        
        # Set keyboard filter to intercept all keyboard events
        lib.interception_set_filter(context, keyboard_filter, 0xFFFF)
        
        # Start idle monitor thread
        monitor_thread = threading.Thread(target=monitor_idle, args=(context,), daemon=True)
        monitor_thread.start()
        
        # Start keyboard monitor thread
        keyboard_thread = threading.Thread(target=monitor_keyboard, args=(context,), daemon=True)
        keyboard_thread.start()
        
        # Main loop for manual testing
        print("\n✅ Ready! Testing manual trigger first...")
        print("Type 't' and press ENTER to test F1 double-press")
        
        while True:
            try:
                user_input = input()
                if user_input.lower() == 't':
                    print("🧪 Manual test - Sending F1 x2...")
                    if send_f1_double(context):
                        print("✅ F1 x2 sent successfully!")
                        print("   → Check if your mouse cursor flashed in MSI App Player")
                    else:
                        print("❌ Failed to send F1")
                elif user_input.lower() == 'q':
                    print("🛑 Quitting...")
                    break
            except KeyboardInterrupt:
                print("\n🛑 Interrupted by Ctrl+C")
                break
            except EOFError:
                time.sleep(0.1)
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n⚠️  Most common issues:")
        print("1. Not running as Administrator")
        print("2. Didn't reboot after driver installation")
        print("3. Driver installation failed")
    finally:
        running = False
        if 'context' in locals() and context:
            lib.interception_destroy_context(context)
        print("\n✅ Stopped")

if __name__ == "__main__":
    main()