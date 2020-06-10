# Voice recognition project
# This is the voice assistant Grimmels
# Extremely powerfull

import os, time, random, wavio
import sounddevice as sd
import speech_recognition as sr
# from win10toast import ToastNotifier

class UI(object):
    """docstring for UI."""

    def wrapMessage(self, message):
        """returns string with a width of 30 chars, wrapped in ascii"""
        res = '-'*30
        c = 0
        for i in range(-1, len(message)):
            if(c % 30 == 0):
                if(c == 0):
                    res += '\n'
                else:
                    # find previous space and new line
                    res += message[i]
                    notSpace = True
                    end = len(res)-1
                    while(notSpace and end > 30):
                        notSpace = (res[end] != ' ')
                        end -= 1
                        i -= 1
                    i -= 1
                    res = res[:end+1] + '\n' + res[end+2:]
            else:
                res += message[i]
            c += 1

        res += '\n'
        res += '-'*30

        return res




class Bot():
    """docstring for Bot."""

    def __init__(self):
        pass


class Audio():
    """docstring for Audio."""
    #
    # def __init__(self):
    #     pass


    def setValidRecording(self):
        """get valid samplerates and channels, return true if found, false otherwise"""
        # from most probable to least, testing better rates first
        self.channels = 0
        self.fs = 0
        sampleRates = [44100, 50000, 48000, 44056, 32000, 22050, 16000, 11025, 8000]

        noValid = True
        c = 0
        while(noValid and c < len(sampleRates)):
            for i in range(1, 3):
                # check channels (1, 2)
                try:
                    sd.check_input_settings(channels=i, samplerate=sampleRates[c])
                    noValid = False
                    self.channels = i
                    self.fs = sampleRates[c]
                except:
                    pass

        if(noValid):
            res = False
        else:
            res = True

        return res


    def getWavFile(self, arg):
        pass




def timer(hour, min, sec):
    # toaster = ToastNotifier()
    cHour = 0
    while(cHour < hour):
        t.sleep(3600)  # Wait an hour
        cHour += 1
    cMin = 0
    while(cMin < min):
        t.sleep(60)  # Wait a minute
        cMin += 1
    cSec = 0
    while(cSec < sec):
        t.sleep(1)  # Wait a second
        cSec += 1
    # Once all the tjmers run down, display the message
    # toaster.show_toast("Timer", f"Your {hour} hour, {min} minute {sec} second timer is up")


def respond(usrInput):
    usrL = usrInput.lower()
    unknown = ["My creator doesn't know what he's doing. That's probably you isn't it?",
               "My name is GRIMMELS (I don't understand)",
               "I'm a computer program. I don't know how to respond and I have no fear."]
    greeting = ['hi', 'hey', 'hello', 'how\'s it going', 'hey grimmels', 'how\'s life', 'how are things',
                'what\'s cracking', 'what\'s good', 'how are you', 'what\'s up',
                'what is up', 'how are ya']
    greetingRes = ["Hello. They call me Grimmels.", "Oh hello!", "Oh Hi!"
                   "Hello, my name is Grimmels but you can call me \"The Grim Reaper\"",
                   "Hello! I love meeting new people! I don't remember any of them..."]

    res = ''
    for i in range(len(greeting)):
        if(greeting[i] in usrL):
            res = random.choice(greetingRes)
            break

    if('minute' in usrL or 'second' in usrL or 'hour' in usrL):
        # Prepare the timer
        usrLst = []
        hour = 0
        min = 0
        sec = 0
        if('-' in usrL):
            # Sometimes it will be in the format of "22-minutes" ect...
            usrL = usrL.replace('-', ' ')
        usrLst = usrL.split()

        if('hour' in usrL):
            numIndex = usrLst.index('hour') - 1  # Get number before "hour"
            if(usrLst[numIndex] == 'one'):  # 'one' is the only case like this
                # All other numbers show numerical form eg) 22
                hour = 1
            else:
                hour = int(usrLst[numIndex])
        if('minute' in usrL):
            numIndex = usrLst.index('minute') - 1
            if(usrLst[numIndex] == 'one'):
                min = 1
            else:
                min = int(usrLst[numIndex])
        if('second' in usrL):
            numIndex = usrLst.index('second') - 1
            if(usrLst[numIndex] == 'one'):
                sec = 1
            else:
                sec = int(usrLst[numIndex])

        hText = ''
        mText = ''
        sText = ''
        if(hour > 0):
            hText = str(hour) + ' hour'
        if(min > 0):
            mText = str(min) + ' minute'
        if(sec > 0):
            sText = str(sec) + ' second'
        print(f"Ok, setting a {hText} {mText} {sText} timer")

        timer(hour, min, sec)
    elif('grimmels' in usrL):
        res += " I Can't believe you know my name! I must be famous!"
    else:
        res = random.choice(unknown)

    return res


def test():
        sd.check_input_settings(channels=2, samplerate=44010)

    # sd.check_input_settings(sd.default.device, 2, sd.default.dtype, sd.default.extra_settings, 44010)


def main():

    audio = Audio()
    valid = audio.setValidRecording()

    if(not valid):
        print("No valid recording devices were detected. Make sure your microphone is working.")
    else:
        r = sr.Recognizer()

        # Don't accept recording longer than 15 seconds
        initialTime = time.time()
        myrecording = sd.rec(int(15 * audio.fs), samplerate=audio.fs, channels=audio.channels)
        res = ""
        for i in range(3, 0, -1):
            # Countdown (total time: 1.5 secs)
            res += f"{i} "
            print(f"Press Enter to start recording in {res}", end='\r')
            time.sleep(0.5)
        print()

        input("Press Enter to stop recording: ")
        finalTime = time.time() - initialTime

        if(finalTime > 15):
            print("That was way too long and I don't understand much. Even if",
                  "it's short. But jeez that was actually like", finalTime//1,
                  "seconds. JEEZ!")
        else:
            # Save a file of what the mic captured
            wavio.write('input.wav', myrecording, audio.fs, sampwidth=2)

            micInput = sr.AudioFile('input.wav')

            with micInput as source:
                r.adjust_for_ambient_noise(source)
                # Uses first second in the offset time, subtract 1 because it is used for ambient
                # noise adjustment. Note this 1 second will always exist because the countdown
                audio = r.record(source, duration=finalTime)
            words = r.recognize_google(audio)
            ui = UI()
            print(' '*14 + "Me:")
            print(ui.wrapMessage(words))
            # print("\n\t\t", words)
            response = respond(words)

            print(' '*13 + "Bot:")
            print(ui.wrapMessage(response), '\n')

    if(os.path.exists("input.wav")):
        os.remove("input.wav")


if __name__ == '__main__':
    main()
