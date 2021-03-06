import speech_recognition as sr
r = sr.Recognizer()
m = sr.Microphone()

import roslib
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int8

# start ROS node
rospy.init_node('speech_recognition')
# configure ROS settings
pubs = rospy.Publisher('speech', String)


try:
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        while True:
            print("Say something!")
            audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)

                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes: # this version of Python uses bytes for strings (Python 2)
                    print(u"You said {}".format(value).encode("utf-8"))
                    pubs.publish(String(value))
                else: # this version of Python uses unicode for strings (Python 3+)
                    print("You said {}".format(value))
                    pubs.publish(String(value))
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError:
                print("Uh oh! Couldn't request results from Google Speech Recognition service")
except KeyboardInterrupt:
    pass

