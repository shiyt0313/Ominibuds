import sys
import argparse
import threading
import time
from PyQt6.QtCore import QMetaObject, Q_ARG, pyqtSlot
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt, QTimer
from PyQt6.QtGui import QKeyEvent



class VideoPlayer(QWidget):
    """
    Video Player Class
    Features:
    1. Play video
    2. Record engagement data and video control events
    3. Log timestamps for all events
    """
    def __init__(self, video_file=None):
        """
        Initialize video player
        Args:
            video_file: Path to the video file
        """
        super().__init__()

        # Basic state variables
        self.ispause = True  # Whether video is paused
        self.videofile = video_file  # Video file path
        self.last_beep_time = 0  # Last prompt sound time
        self.waiting_for_input = False  # Whether waiting for user input
        self.start_time = time.time()  # Record session start time

        # Initialize sound effect for prompts
        self.beep_sound = QSoundEffect()
        self.beep_sound.setSource(QUrl.fromLocalFile("beep.wav"))  # Set sound file
        self.beep_sound.setVolume(0.5)  # Set volume to 50%

        # Create record file with timestamp
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.record_path = f"./record/{timestamp}.txt"
        # Record session start
        with open(self.record_path, "w") as record_file:
            record_file.write(f"Session started at {timestamp}\n")
            record_file.write(f"Video file: {video_file}\n")
            record_file.write(f"Start timestamp (epoch): {self.start_time}\n\n")

        # Create UI layouts
        main_layout = QVBoxLayout()  # Main layout (vertical)
        video_layout = QVBoxLayout()  # Video area layout (vertical)

        # Initialize video components
        self.video_widget = QVideoWidget()  # Video display widget
        self.media_player = QMediaPlayer()  # Media player
        self.audio_output = QAudioOutput()  # Audio output
        self.media_player.setAudioOutput(self.audio_output)  # Set audio output
        self.media_player.setVideoOutput(self.video_widget)  # Set video output

        # Create time display label
        self.current_time_label = QLabel("00:00")
        self.current_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center alignment
        self.current_time_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.current_time_label.setFixedHeight(20)

        # Organize layouts
        time_layout = QHBoxLayout()  # Time display area layout (horizontal)
        time_layout.addWidget(self.current_time_label)

        # Add components to video layout
        video_layout.addLayout(time_layout)  # Add time display
        video_layout.addWidget(self.video_widget)  # Add video display

        # Set main layout
        main_layout.addLayout(video_layout)
        self.setLayout(main_layout)

        # Create timer for updating time display
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)  # Update every second
        self.timer.start(1000)

        # If video file provided, load and pause at start
        if video_file:
            self.media_player.setSource(QUrl.fromLocalFile(video_file))
            self.ispause = True
            self.media_player.pause()

    @pyqtSlot(str, str)
    def record_event(self, event_type, additional_info=""):
        """
        Record any event with timestamp
        Args:
            event_type: Type of event (play/pause/engagement)
            additional_info: Any additional information about the event
        """
        current_time = self.current_time_label.text()
        timestamp = time.time()
        elapsed = timestamp - self.start_time
        
        with open(self.record_path, "a") as record_file:
            record_file.write(f"Timestamp: {timestamp:.3f}\n")
            record_file.write(f"Elapsed time: {elapsed:.3f}s\n")
            record_file.write(f"Video time: {current_time}\n")
            record_file.write(f"Event: {event_type}\n")
            if additional_info:
                record_file.write(f"Details: {additional_info}\n")
            record_file.write("\n")

    def keyPressEvent(self, event: QKeyEvent):
        """
        Handle keyboard press events
        Args:
            event: Keyboard event object
        """
        # Only process keys when waiting for input
        if not self.waiting_for_input:
            return

        key = event.key()
        # Check if pressed key is 1-5
        if Qt.Key.Key_1.value <= key <= Qt.Key.Key_5.value:
            engagement_level = key - Qt.Key.Key_0.value  # Convert key value to 1-5
            self.record_engagement(engagement_level)  # Record engagement
            self.waiting_for_input = False  # End waiting state
            if self.ispause:
                self.ispause = False
                self.media_player.play()  # Resume video playback
                self.record_event("play", "After engagement input")

    def record_engagement(self, level):
        """
        Record user engagement to file
        Args:
            level: Engagement level (1-5)
        """
        print(f"\nEngagement level: {level}")  # Display in console
        self.record_event("engagement", f"Level: {level}")

    def update_time(self):
        """
        Update time display
        Triggered every second
        """
        current_time = self.media_player.position() / 1000  # Get current time (ms to s)
        duration = self.media_player.duration() / 1000  # Get video duration

        # Check every minute if prompt needed
        if int(current_time) > 0 and int(current_time) % 4 == 0 and int(current_time) != self.last_beep_time:
            self.beep_sound.play()  # Play prompt sound
            self.last_beep_time = int(current_time)  # Update last prompt time
            if not self.ispause:
                self.media_player.pause()  # Pause video
                self.ispause = True
                self.waiting_for_input = True  # Start waiting for user input
                self.record_event("pause", "Automatic pause for engagement input")

        # Update time display
        current_time_formatted = self.format_time(current_time)
        self.current_time_label.setText(f"{current_time_formatted}")

    def format_time(self, seconds):
        """
        Convert seconds to MM:SS format
        Args:
            seconds: Time in seconds
        Returns:
            str: Formatted time string
        """
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    def control_video(self):
        """
        Handle command line control
        Supported commands:
        - Enter: Toggle play/pause
        - t: Display current time and remaining time
        """
        while True:
            command = input().lower()
            if command == '':  # Enter key
                if self.ispause:
                    QMetaObject.invokeMethod(self.media_player, "play", Qt.ConnectionType.QueuedConnection)
                    self.ispause = False
                    # Record the play event directly
                    self.record_event("play", "Manual play")
                else:
                    QMetaObject.invokeMethod(self.media_player, "pause", Qt.ConnectionType.QueuedConnection)
                    self.ispause = True
                    # Record the pause event directly
                    self.record_event("pause", "Manual pause")
            elif command == 't':  # Show time info
                current_time = self.media_player.position() / 1000
                duration = self.media_player.duration() / 1000
                current_time_formatted = self.format_time(current_time)
                remaining_time_formatted = self.format_time(duration - current_time)
                print(f"Current Time: {current_time_formatted}")
                print(f"Remaining Time: {remaining_time_formatted}")


def parse_args():
    """
    Parse command line arguments
    Returns:
        argparse.Namespace: Parsed arguments object
    """
    parser = argparse.ArgumentParser(description="Video Player Control")
    parser.add_argument('-v','--video_file', type=str, help="Path to the video file")
    return parser.parse_args()


if __name__ == "__main__":
    # Program entry point
    app = QApplication(sys.argv)
    args = parse_args()
    player = VideoPlayer(video_file=args.video_file)  # Create player instance
    control_thread = threading.Thread(target=player.control_video, daemon=True)  # Create control thread
    control_thread.start()  # Start control thread
    player.show()  # Show player window
    sys.exit(app.exec())  # Run application