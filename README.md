# Ominibuds

### Environment

#### 1. We need two different environment for `video player` and `eye tracker`

For video player
```python
python = 3.12
PyQt6
```

For eye tracker
```python
python = 3.6
numpy
beam tracker SDK
#change the path to your local SDK path
```

#### 2. Run code

+   For Video Player
make sure you create the `videos` dir under `video_player`
```
video_player
|-----videos
|-----record
|-----beep.wav
|-----videoPlayer.py
```
Run the follow command:
```
python videoPlayer.py -v <Path to your video>
```
The video will be paused in the beginning, 
1. click `enter` in command line to play or pause the video
2. The video will automatically pause every minute with a beep, (can be modified)
3. User need to tap 1-5 on the kayboard to report engagement.
4. The record will be saved under `record` dir and named with timestamp.

+   For Eye Tracker
Don't forget toggle game activation in the Beam app, otherwise the server will not get the data.
(You can also run `test_eyetracker.py` to test if you can get the data.)
Then run `eye_tracking_recorder.py` to start eye tracking.
Enter `q` in the command line can stop the eye tracking threading.
The record will be stored in the csv file, named will timestamp.

