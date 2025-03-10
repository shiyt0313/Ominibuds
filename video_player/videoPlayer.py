import sys
import argparse
import threading
import time
from PyQt6.QtCore import QMetaObject
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGroupBox, QFormLayout, QRadioButton, QButtonGroup, QPushButton, QSlider
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt, QTimer


class VideoPlayer(QWidget):
    def __init__(self, video_file=None):
        super().__init__()

        self.ispause = True
        self.videofile = video_file

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.record_path = f"./record/{timestamp}.txt"

        # Layouts
        main_layout = QHBoxLayout()
        video_layout = QVBoxLayout()
        questionnaire_layout = QVBoxLayout()

        # Video Player
        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)

        # Progress Bar (Slider)
        # self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        # self.progress_slider.setRange(0, 100)
        # self.progress_slider.sliderMoved.connect(self.set_position)
        # self.media_player.positionChanged.connect(self.update_progress)
        # self.media_player.durationChanged.connect(self.update_duration)

        # Current Time & Remaining Time labels
        self.current_time_label = QLabel("00:00")
        self.current_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_time_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.current_time_label.setFixedHeight(20)

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.current_time_label)
        # time_layout.addWidget(self.progress_slider)
        # self.remaining_time_label = QLabel("00:00")

        self.questionnaire_group = QGroupBox()
        # questionnaire_layout.addWidget(questionnaire_group)
        form_layout = QFormLayout()

        questions = [
            "I paid attention to this video.",
            "I pretended to watch the video but actually not",
            "I enjoyed learning new things from this video.",
            "I asked myself questions to make sure I understood the video content."
        ]

        likert_options = ["1", "2", "3", "4", "5"]

        self.radio_groups = []  # Store radio buttons for later retrieval
        self.survey_label = QLabel("Please rate your engagement \n1 for strongly disagree and 5 for strongly agree")
        self.survey_label.setStyleSheet("font-size: 16px; font-weight: bold; color: red;")
        form_layout.addWidget(self.survey_label)

        for question in questions:
            question_layout = QVBoxLayout()
            label = QLabel(question)
            label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
            question_layout.addWidget(label)

            button_group = QButtonGroup(self)  # Create a separate button group for each question
            button_group.setExclusive(True)
            likert_layout = QHBoxLayout()
            for option in likert_options:
                radio_button = QRadioButton(option)
                radio_button.setStyleSheet("""
                    font-size: 18px;
                    padding: 10px;
                    QRadioButton::indicator {
                        width: 25px;
                        height: 25px;
                    }
                """)
                likert_layout.addWidget(radio_button)
                button_group.addButton(radio_button)
            question_layout.addLayout(likert_layout)
            self.radio_groups.append(button_group)  # Save buttons
            form_layout.addRow(question_layout)
        self.questionnaire_group.setLayout(form_layout)
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #4CAF50; color: white;")
        self.submit_button.clicked.connect(self.record_responses)


        horizontal_layout = QVBoxLayout()
        horizontal_layout.addWidget(self.questionnaire_group)
        horizontal_layout.addWidget(self.submit_button)
        horizontal_layout.setAlignment(self.submit_button, Qt.AlignmentFlag.AlignTop)  # Align button to the top of the form
        
        questionnaire_layout.addLayout(horizontal_layout)

        self.overlay = QWidget(self.questionnaire_group)
        self.overlay.setStyleSheet("background-color: rgba(128, 128, 128, 0.7);")
        self.overlay.setGeometry(self.questionnaire_group.rect())  # Set the same geometry as the questionnaire group

        
        # print(horizontal_layout.geometry())
        # self.overlay.hide()  # Start hidden


        # Video Layout
        video_layout.addLayout(time_layout)
        video_layout.addWidget(self.video_widget)
        # video_layout.addWidget(self.progress_slider)

        # video_layout.addLayout(time_layout)

        # Combine layouts
        main_layout.addLayout(video_layout, 3)
        # main_layout.addLayout(questionnaire_layout, 1)

        self.setLayout(main_layout)
        # self.setWindowTitle("Video Player with Real-Time Command Input")
     

        # Timer for updating the current time and remaining time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

        # self.media_player.mediaStatusChanged.connect(self.media_status_changed)

        # Open the video file if provided
        if video_file:
            self.media_player.setSource(QUrl.fromLocalFile(video_file))
            self.ispause = True
            self.media_player.pause()
            self.lock_questionnaire()
    
    
            
    def lock_questionnaire(self):
    # Disable all widgets in the questionnaire group
        for group in self.radio_groups:
            group.setExclusive(False)  # Disable exclusive selection
            for button in group.buttons():
                button.setChecked(False)
                button.setEnabled(False) 

        # for widget in self.questionnaire_group.findChildren(QWidget):
        #     widget.setEnabled(False)
        self.submit_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #ccc; color: white;")
        self.submit_button.setEnabled(False)

        self.overlay.setVisible(True)  # Show the overlay
        # self.questionnaire_layout.setVisible(False)  # Hide the questionnaire layout
    def unlock_questionnaire(self):
    # Enable all widgets in the questionnaire group
        for group in self.radio_groups:

            for button in group.buttons():
                 # Ensure button is enabled before unchecking
                button.setEnabled(True) 
            group.setExclusive(True)  # Enable exclusive selection
                


        self.submit_button.setStyleSheet("font-size: 18px; padding: 10px; background-color: #4CAF50; color: white;")
        self.submit_button.setEnabled(True)
        self.overlay.setVisible(False)  # Hide the overlay

    def open_file(self, filename):
        """Open a video file."""
        self.media_player.setSource(QUrl.fromLocalFile(filename))
        self.media_player.play()

    def update_progress(self, position):
        """Update progress bar as video plays."""
        if self.media_player.duration() > 0:
            self.progress_slider.setValue(int((position / self.media_player.duration()) * 100))

    def update_duration(self, duration):
        """Update slider range based on video duration."""
        self.progress_slider.setRange(0, 100)

    def set_position(self, value):
        """Seek video when slider is moved."""
        if self.media_player.duration() > 0:
            self.media_player.setPosition(int((value / 100) * self.media_player.duration()))

    def update_time(self):
        """Update current time and remaining time."""
        current_time = self.media_player.position() / 1000  # Convert milliseconds to seconds
        duration = self.media_player.duration() / 1000  # Convert milliseconds to seconds

        current_time_formatted = self.format_time(current_time)
        self.current_time_label.setText(f"{current_time_formatted}")
        # remaining_time_formatted = self.format_time(duration - current_time)
        # self.remaining_time_label.setText(f"Remaining Time: {remaining_time_formatted}")

    def format_time(self, seconds):
        """Convert seconds into MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"
    def record_responses(self):
        """Record and print user responses when submit is clicked."""
        responses = []
        for i, group in enumerate(self.radio_groups):
            selected_button = group.checkedButton()
            if selected_button:
                responses.append(f"Q{i+1}: {selected_button.text()}")
            else:
                return
                # responses.append(f"Q{i+1}: No response")


        print("\nUser Responses:")

        record_file = open(self.record_path, "a")
        record_file.write(self.current_time_label.text() + ' '+ self.videofile + "\n")

        for response in responses:
            print(response)
            record_file.write(response + "\n")
        record_file.write("\n")
        record_file.close()
        self.lock_questionnaire()

        if self.ispause:
            self.ispause = False
        self.media_player.play()    
        
  

    def control_video(self):
        """Real-time control via command line input."""
        while True:
            command = input().lower()

            if command == '':
                if self.ispause:
                    QMetaObject.invokeMethod(self.media_player, "play", Qt.ConnectionType.QueuedConnection)
                    self.ispause = False
                else:
                    QMetaObject.invokeMethod(self.media_player, "pause", Qt.ConnectionType.QueuedConnection)
                    self.ispause = True
            elif command == 'q':
                if not self.ispause:
                    QMetaObject.invokeMethod(self.media_player, "pause", Qt.ConnectionType.QueuedConnection)
                    self.ispause = True
                self.unlock_questionnaire()
                
            # elif command.startswith('v'):
            #     new_video_file = command[1:].strip()
            #     if new_video_file:
                    
            #         self.media_player.setSource(QUrl.fromLocalFile(new_video_file))
                
            #     else:
            #         print("Please provide a valid video file path.")
            elif command == 't':
                current_time = self.media_player.position() / 1000
                duration = self.media_player.duration() / 1000
                current_time_formatted = self.format_time(current_time)
                remaining_time_formatted = self.format_time(duration - current_time)
                print(f"Current Time: {current_time_formatted}")
                print(f"Remaining Time: {remaining_time_formatted}")
            else:
                print("Unknown command. Please try again.")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Video Player Control")
    parser.add_argument('-v','--video_file', type=str, help="Path to the video file")
    return parser.parse_args()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    args = parse_args()

    # Initialize the player and load the video file
    player = VideoPlayer(video_file=args.video_file)

    # Start the control thread to listen for real-time commands
    control_thread = threading.Thread(target=player.control_video, daemon=True)
    control_thread.start()

    player.show()
    sys.exit(app.exec())