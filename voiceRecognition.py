# Voice recognition project
# This is the voice assistant Gilbert
# Extremely powerfull

import os, time, random, wavio
import sounddevice as sd
import speech_recognition as sr

class UI():
    """To help with the terminal UI"""

    def wrapMessage(self, message):
        """returns string with a width of 30 chars, wrapped in hyphens"""
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
    """For all the bots features: responses, actions, ect..."""

    def __init__(self):
        self.isWindows = False


    def respond(self, message):
        usrL = message.lower()
        unknown = ["My creator doesn't know what he's doing. That's probably you isn't it?",
                   "My name is Gilbert (I don't understand)",
                   "I'm a computer program. I don't know how to respond and I have no fear."]
        greeting = ['hi', 'hey', 'hello', 'how\'s it going', 'hey Gilbert', 'how\'s life', 'how are things',
                    'what\'s cracking', 'what\'s good', 'how are you', 'what\'s up',
                    'what is up', 'how are ya']
        greetingRes = ["Hello. They call me Gilbert.", "Oh hello!", "Oh Hi!"
                       "Hello, my name is Gilbert but you can call me \"The Grim Reaper\"",
                       "Hello! I love meeting new people! I don't remember any of them..."]

        res = ""
        for i in range(len(greeting)):
            if(f" {greeting[i]} " in usrL):
                res = random.choice(greetingRes)
                break

        if('gilbert' in usrL):
            res += " I Can't believe you know my name! I must be famous!"

        if('minute' in usrL or 'second' in usrL or 'hour' in usrL):
            # remove hyphens, and "hours minutes seconds"
            timeWords = ["hour", "minute", "second"]
            usrL = usrL.replace('-', ' ')
            for i in range(len(timeWords)):
                usrL = usrL.replace(timeWords[i]+'s', timeWords[i])

            messageIn = usrL.split()

            hours = mins = secs = 0

            for i in range(len(messageIn)):
                for j in range(len(timeWords)):
                    if(messageIn[i] == timeWords[j]):
                        numBefore = messageIn[i-1]
                        if(numBefore.isdigit()):
                            if(j == 0):
                                hours = int(numBefore)
                            if(j == 1):
                                mins = int(numBefore)
                            if(j == 2):
                                secs = int(numBefore)
                        elif(numBefore == "one"):
                            if(j == 0):
                                hours = 1
                            if(j == 1):
                                mins = 1
                            if(j == 2):
                                secs = 1


            hText = mText = sText= ""
            if(hours > 0):
                hText = f" {hours} hour"
            if(mins > 0):
                mText = f" {mins} minute"
            if(secs > 0):
                sText = f" {secs} second"

            ui = UI()
            print(ui.wrapMessage(f"Ok, setting a{hText}{mText}{sText} timer"))
            print(' '*13 + "...")
            self.timer(hours, mins, secs)
            res += f"Your{hText}{mText}{sText} timer is up!"

        if(len(res) == 0):
            res = random.choice(unknown)

        return res


    def timer(self, hour, min, sec):
        cHour = 0
        while(cHour < hour):
            time.sleep(3600)  # Wait an hour
            cHour += 1
        cMin = 0
        while(cMin < min):
            time.sleep(60)  # Wait a minute
            cMin += 1
        cSec = 0
        while(cSec < sec):
            time.sleep(1)  # Wait a second
            cSec += 1



class Audio():
    """
    for everything related to audio, recording, saving files,
    reading files, getting speach to text, ect...
    """

    def setValidRecording(self):
        """get valid samplerates and channels, return true if found, false otherwise"""
        # from most probable to least, testing better rates first
        self.channels = 0
        self.fs = 0
        sampleRates = [16000, 44100, 48000, 44056, 32000, 22050, 16000, 11025, 8000]

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

        return (not noValid)


    def record(self):
        """starts recording"""
        self.r = sr.Recognizer()
        self.recording = sd.rec(int(15 * self.fs), samplerate=self.fs, channels=self.channels)


    def speachToText(self, elapsed):
        """returns the text of what was said"""

        # Save a file of what the mic captured
        wavio.write('input.wav', self.recording, self.fs, sampwidth=3)

        micInput = sr.AudioFile('input.wav')

        with micInput as source:
            self.r.adjust_for_ambient_noise(source)
            # Uses first second in the offset time, subtract 1 because it is used for ambient
            # noise adjustment. Note this 1 second will always exist because the countdown
            audio = self.r.record(source, duration=elapsed)

        try:
            words = self.r.recognize_google(audio)  # let's make Google do the hard work
        except:
            ui = UI()
            print()
            print(ui.wrapMessage(("Your audio could not be understood. This is an issue with the microphone. "
                                 "Make sure your microphone is not muted and is working properly. An audio "
                                 "file \"input.wav\" has been generated so you can hear what your voice "
                                 "recording sounds like.")))
            print()

        return words



def main():
    audio = Audio()
    bot = Bot()
    valid = audio.setValidRecording()

    if(not valid):
        print("No valid recording devices were detected. Make sure your microphone is working.")
    else:
        ui = UI()
        audio.record()

        # Don't accept recording longer than 15 seconds
        initialTime = time.time()

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
                  "it's short. But jeez that was actually like", int(finalTime),
                  "seconds. JEEZ!")
        else:
            words = audio.speachToText(finalTime)

            print('\n' + ' '*14 + "Me:")
            print(ui.wrapMessage(words))

            print(' '*13 + "Bot:")
            response = bot.respond(words)
            print(ui.wrapMessage(response), '\n')

    if(os.path.exists("input.wav")):
        os.remove("input.wav")



if __name__ == '__main__':
    main()
