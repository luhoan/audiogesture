**Motivations**
I was inspired and curious as to how computer vision can work within machine learning contexts. 
With that being said, this is a freshmen project that I sought to put myself towards, having a
little bit of ML background around due to my Sin Karkinos project.


This project is an upgrade from my original established SVM project. 

Here, we utilize a different model (google's mediapipe hand landmarker) that allows us to track
21 plotted points on a hand using opencv. From this, we use those models to recognize and train
off of hand signals that allows you to control your own system's audio. 

I wanted to add a dynamic listening audio system that can tell when your system is already playing
music, however, we just have a fixed boolean for that. It thinks that you arent' playing any music. 

Open palm = play/stop music
Fist = play/stop music
point left = previous song/beginning of current song
point right = next song
thumbs up = increase volume
thumbs down = decrease volume
pinch = mute

Right now, as of August 2026, the current model is being fine tuned on a few hundred photos of my own hands
so that they're able to recognize the last 3 gestures much better.

**INSTRUCTIONS to run:**
Run main.py within HandDJ, not in the root. It should open up a camera and track your hand and gestures 
immediately. 
