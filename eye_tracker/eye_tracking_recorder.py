import sys
sys.path.append("D:\BeamSDK-Windows64-1.1.0\API\python")
import time

from eyeware.client import TrackerClient
import time
import numpy as np
import threading


gaze_data = []
tracking = True
        
def record_gaze(x, y, lost = False):
    current_time = time.time()
    gaze_data.append({
                'timestamp': current_time,
                'x': x,
                'y': y,
                'lost': lost
            })
            
def tracking_client():
    global tracking
    gaze_tracker = TrackerClient()
    sample_interval = 1.0 / 30  # 
    
    while tracking:
        if gaze_tracker.connected:
            # print("  * Gaze on Screen:")
            screen_gaze = gaze_tracker.get_screen_gaze_info()
            screen_gaze_is_lost = screen_gaze.is_lost
            # print("      - Lost track:       ", screen_gaze_is_lost)
            if not screen_gaze_is_lost:
                x = screen_gaze.x
                y = screen_gaze.y
                record_gaze(x, y, lost = screen_gaze_is_lost)
            else:
                record_gaze(0, 0, lost = screen_gaze_is_lost)   
            time.sleep(sample_interval)  # 30 Hz采样频率
        else:
            MESSAGE_PERIOD_IN_SECONDS = 2
            time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
            print("No connection with tracker server")

def keyboard_input():
    global tracking
    while True:
        key = input()
        if key == 'q':
            tracking = False
            break

# 使用示例
if __name__ == "__main__":
    try:
        thread_tracking = threading.Thread(target=tracking_client)
        thread_keyboard = threading.Thread(target=keyboard_input)
        thread_tracking.start()
        thread_keyboard.start()
        thread_tracking.join()
        thread_keyboard.join()
        
        # 保存数据
        print(f"Save {len(gaze_data)} samples...")
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        with open(f'eye_tracking_data_{timestamp}.csv', 'w') as f:
            f.write("timestamp,x,y,lost\n")  # 添加列标题
            for data in gaze_data:
                f.write(f"{data['timestamp']},{data['x']},{data['y']},{data['lost']}\n")
        print("Data saved!")
        
    except KeyboardInterrupt:
        tracking = False
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tracking = False
    