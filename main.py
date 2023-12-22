
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import MDTabsBase
from kivymd.toast import toast


from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest

from plyer import notification
from plyer import vibrator

from Module1 import Solution, pairs
from nltk.chat.util import Chat, reflections

from pytube import YouTube
from moviepy.editor import *

from random import choice
import webbrowser

import cv2
import threading
import numpy as np
from PIL import Image as kk
from functools import partial

from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineIconListItem


Window.size = (300, 500)


class ContentNavigationDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

    def on_start(self):
        self.set_list_md_icons()

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''
        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                }
            )
        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)


class Tab2(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    screen_manager = ObjectProperty()


class Example(MDApp):
    def build(self):
        self.title = "AI DRAGO"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("GUI.kv")
    turn = "X"
    winner = False
    X_win = 0
    O_win = 0

    def doit(self):

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(
            '//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//Trainer//trainer.yml')
        cascadePath = "//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

        font = cv2.FONT_HERSHEY_SIMPLEX

        # iniciate id counter
        id = 0
        self.do_vid = True
        cv2.namedWindow('Hidden', cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

        # resize the window to (0,0) to make it invisible
        cv2.resizeWindow('Hidden', 0, 0)

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)

        cam.set(3, 640)  # set video widht
        cam.set(4, 480)  # set video height

        # Define min window size to be recognized as a face
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)

        while (self.do_vid):

            ret, img = cam.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for(x, y, w, h) in faces:

                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                # Check if confidence is less them 100 ==> "0" is perfect match
                if (confidence < 100):
                    with open("//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//Assets.txt") as xpp:
                        a = xpp.read().split()
                        for i in range(len(a)):
                            b = a[i].split("=")

                            if id == int(b[0]):
                                id = b[1]

                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))

                cv2.putText(img, str(id), (x+5, y-5),
                            font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x+5, y+h-5),
                            font, 1, (255, 255, 0), 1)

            cv2.imshow('Hidden', img)

            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break

            Clock.schedule_once(partial(self.display_frame, img))
        # Do a bit of cleanup
        print("\n [INFO] Exiting Program and cleanup stuff")
        cam.release()
        cv2.destroyAllWindows()

    def stop_vid(self):
        # stop the video capture loop
        self.do_vid = False

    def display_frame(self, img, dt):
        # display the current video img in the kivy Image widget

        # create a Texture the correct size and format for the img
        texture = Texture.create(
            size=(img.shape[1], img.shape[0]), colorfmt='bgr')

        # copy the img data into the texture
        texture.blit_buffer(img.tobytes(order=None),
                            colorfmt='bgr', bufferfmt='ubyte')

        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()

        # actually put the texture in the kivy Image widget
        self.root.ids.vid.source = texture

    def A(self):
        return threading.Thread(target=self.doit, daemon=True).start()

    def setimg(self):

        def setpic(face_id, face_name):
            cam = cv2.VideoCapture(0)
            cam.set(3, 640)  # set video width
            cam.set(4, 480)  # set video height

            face_detector = cv2.CascadeClassifier(
                '//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//haarcascade_frontalface_default.xml')

            with open("//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//Assets.txt", "a") as f:
                f.write("\n"+face_id+"="+face_name+"\n")

            print(
                "\n [INFO] Initializing face capture. Look the camera and wait ...")
            # Initialize individual sampling face count
            count = 0

            while(True):

                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:

                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    count += 1

                    # Save the captured image into the datasets folder
                    cv2.imwrite("//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//DATA//" +
                                str(face_name)+"." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])

                    cv2.imshow('image', img)

                k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
                if k == 27:
                    break
                elif count >= 30:  # Take 30 face sample and stop video
                    break

            # Do a bit of cleanup
            print("\n [INFO] Exiting Program and cleanup stuff")
            cam.release()
            cv2.destroyAllWindows()

            path = '//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//DATA'

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            detector = cv2.CascadeClassifier(
                "//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//haarcascade_frontalface_default.xml")

            # function to get the images and label data

            def getImagesAndLabels(path):

                imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
                faceSamples = []
                ids = []

                for imagePath in imagePaths:

                    PIL_img = kk.open(imagePath).convert(
                        'L')  # convert it to grayscale
                    img_numpy = np.array(PIL_img, 'uint8')

                    id = int(os.path.split(imagePath)[-1].split(".")[1])
                    faces = detector.detectMultiScale(img_numpy)

                    for (x, y, w, h) in faces:
                        faceSamples.append(img_numpy[y:y+h, x:x+w])
                        ids.append(id)

                return faceSamples, ids

            print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
            faces, ids = getImagesAndLabels(path)
            recognizer.train(faces, np.array(ids))

            # Save the model into trainer/trainer.yml
            # recognizer.save() worked on Mac, but not on Pi
            recognizer.write(
                '//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//Trainer//trainer.yml')

            # Print the numer of faces trained and end program
            print("\n [INFO] {0} faces trained. Exiting Program".format(
                len(np.unique(ids))))
        face_id = self.root.ids.imgid.text
        face_name = self.root.ids.imgname.text
        with open("//home//ai//Documents//Python//opencv//OpenCV-Face-Recognition-master//FacialRecognition//Assets.txt") as xpp:
            a = xpp.read().split()
            for i in range(len(a)):
                b = a[i].split("=")

                if face_id != b[0]:
                    setpic(face_id, face_name)
                    break

    def short_it(self):
        url = self.root.ids.URL.text.strip()
        if url == "":
            try:
                vibrator.vibrate(0.1)
            except:
                pass
            kwargs = {
                "title": "Error",
                "message": "No URL detected!",
                "ticker": "New message",
                "toast": True,
                "app_icon": "message-alert",
            }
            notification.notify(**kwargs)
            return
        kwargs = {
            "title": "Wait",
            "message": "Please wait...",
            "ticker": "New message",
            "toast": True,
            "app_icon": "message-alert",
        }
        notification.notify(**kwargs)

        try:
            # Sends request and waits to finish
            Clock.start_clock()
            req1 = UrlRequest(
                f"https://short-link-api.vercel.app/?query={url}", timeout=10
            )
            while not req1.is_finished:
                Clock.tick()
            Clock.stop_clock()

            result = req1.result
            try:
                link1 = result["click.ru"]
            except:
                link1 = "No data"

            try:
                link2 = result["da.gd"]
            except:
                link2 = "No data"

            try:
                link3 = result["is.gd"]
            except:
                link3 = "No data"

            try:
                link4 = result["osdb.link"]
            except:
                link4 = "No data"

            self.ids.Link1.text = f"[ref={link1}]{link1}[/ref]"
            self.ids.Link2.text = f"[ref={link2}]{link2}[/ref]"
            self.ids.Link3.text = f"[ref={link3}]{link3}[/ref]"
            self.ids.Link4.text = f"[ref={link4}]{link4}[/ref]"

            # Saves URLs to database
            with open("//home//ai//Documents//Python//MyApp_KMD//url.txt", "w") as data:
                data.write(f"{link1}\n{link2}\n{link3}\n{link4}\n")

            kwargs = {
                "title": "Done",
                "message": "Urls Copied!",
                "ticker": "New message",
                "toast": True,
                "app_icon": "message-alert",
            }
            notification.notify(**kwargs)

        except:
            kwargs = {
                "title": "Error",
                "message": "unexpected error occurred",
                "ticker": "New message",
                "toast": True,
                "app_icon": "message-alert",
            }
            notification.notify(**kwargs)

    # Function to open Shorted URLs
    # You can open them by clicking on URLs
    def open_url(self, mode):
        with open("//home//ai//Documents//Python//MyApp_KMD//url.txt", "r") as data:
            lines = data.readlines()
            link1 = lines[0].split("\n")[0]
            link2 = lines[1].split("\n")[0]
            link3 = lines[2].split("\n")[0]
            link4 = lines[3].split("\n")[0]

        if mode == 1:
            webbrowser.open(link1) if link1 != "No data" else None
        elif mode == 2:
            webbrowser.open(link2) if link2 != "No data" else None
        elif mode == 3:
            webbrowser.open(link3) if link2 != "No data" else None
        elif mode == 4:
            webbrowser.open(link4) if link2 != "No data" else None

    def nowi(self):
        if self.winner == False and \
                self.root.ids.btn1.disabled == True and \
                self.root.ids.btn2.disabled == True and \
                self.root.ids.btn3.disabled == True and \
                self.root.ids.btn4.disabled == True and \
                self.root.ids.btn5.disabled == True and \
                self.root.ids.btn6.disabled == True and \
                self.root.ids.btn7.disabled == True and \
                self.root.ids.btn8.disabled == True and \
                self.root.ids.btn9.disabled == True:
            self.root.ids.score.text = "It's a tie!!"
            self.restart2()

    def disable_all_buttons(self):
        self.root.ids.btn1.disabled = True
        self.root.ids.btn2.disabled = True
        self.root.ids.btn3.disabled = True
        self.root.ids.btn4.disabled = True
        self.root.ids.btn5.disabled = True
        self.root.ids.btn6.disabled = True
        self.root.ids.btn7.disabled = True
        self.root.ids.btn8.disabled = True
        self.root.ids.btn9.disabled = True

    def End_game(self, a, b, c):
        self.winner = True
        self.disable_all_buttons()
        self.root.ids.score.text = f""
        toast(f"{a.text} Wins!")
        if a.text == "X":
            self.X_win += 1
        if a.text == "O":
            self.O_win += 1
        self.root.ids.game1.text = f"X - {self.X_win} | O - {self.O_win}"

        self.restart2()

    def win(self):
        if self.root.ids.btn1.text != "" and self.root.ids.btn1.text == self.root.ids.btn2.text and self.root.ids.btn2.text == self.root.ids.btn3.text:
            self.End_game(self.root.ids.btn1,
                          self.root.ids.btn2, self.root.ids.btn3)
        if self.root.ids.btn4.text != "" and self.root.ids.btn4.text == self.root.ids.btn5.text and self.root.ids.btn5.text == self.root.ids.btn6.text:
            self.End_game(self.root.ids.btn4,
                          self.root.ids.btn5, self.root.ids.btn6)
        if self.root.ids.btn7.text != "" and self.root.ids.btn7.text == self.root.ids.btn8.text and self.root.ids.btn8.text == self.root.ids.btn9.text:
            self.End_game(self.root.ids.btn7,
                          self.root.ids.btn8, self.root.ids.btn9)
        if self.root.ids.btn1.text != "" and self.root.ids.btn1.text == self.root.ids.btn4.text and self.root.ids.btn4.text == self.root.ids.btn7.text:
            self.End_game(self.root.ids.btn1,
                          self.root.ids.btn4, self.root.ids.btn7)
        if self.root.ids.btn2.text != "" and self.root.ids.btn2.text == self.root.ids.btn5.text and self.root.ids.btn5.text == self.root.ids.btn8.text:
            self.End_game(self.root.ids.btn2,
                          self.root.ids.btn5, self.root.ids.btn8)
        if self.root.ids.btn3.text != "" and self.root.ids.btn3.text == self.root.ids.btn6.text and self.root.ids.btn6.text == self.root.ids.btn9.text:
            self.End_game(self.root.ids.btn3,
                          self.root.ids.btn6, self.root.ids.btn9)
        if self.root.ids.btn1.text != "" and self.root.ids.btn1.text == self.root.ids.btn5.text and self.root.ids.btn5.text == self.root.ids.btn9.text:
            self.End_game(self.root.ids.btn1,
                          self.root.ids.btn5, self.root.ids.btn9)
        if self.root.ids.btn3.text != "" and self.root.ids.btn3.text == self.root.ids.btn5.text and self.root.ids.btn5.text == self.root.ids.btn7.text:
            self.End_game(self.root.ids.btn3,
                          self.root.ids.btn5, self.root.ids.btn7)
        self.nowi()

    def presser(self, btn):
        if self.turn == "X":
            btn.text = "X"
            btn.disabled = True
            self.root.ids.score.text = "O's Turn!"
            self.turn = "O"
        else:
            btn.text = "O"
            btn.disabled = True
            self.root.ids.score.text = "X's Turn!"
            self.turn = "X"
        self.win()

    def restart2(self):
        a = choice("XO")
        self.turn = a
        self.root.ids.btn1.disabled = False
        self.root.ids.btn2.disabled = False
        self.root.ids.btn3.disabled = False
        self.root.ids.btn4.disabled = False
        self.root.ids.btn5.disabled = False
        self.root.ids.btn6.disabled = False
        self.root.ids.btn7.disabled = False
        self.root.ids.btn8.disabled = False
        self.root.ids.btn9.disabled = False

        self.root.ids.btn1.text = ""
        self.root.ids.btn2.text = ""
        self.root.ids.btn3.text = ""
        self.root.ids.btn4.text = ""
        self.root.ids.btn5.text = ""
        self.root.ids.btn6.text = ""
        self.root.ids.btn7.text = ""
        self.root.ids.btn8.text = ""
        self.root.ids.btn9.text = ""

        self.root.ids.btn1.color = "green"
        self.root.ids.btn2.color = "green"
        self.root.ids.btn3.color = "green"
        self.root.ids.btn4.color = "green"
        self.root.ids.btn5.color = "green"
        self.root.ids.btn6.color = "green"
        self.root.ids.btn7.color = "green"
        self.root.ids.btn8.color = "green"
        self.root.ids.btn9.color = "green"
        self.winner = False
        self.root.ids.score.text = f"{a}'s Turn!"

    def restart1(self):
        a = choice("XO")
        self.turn = a
        self.root.ids.btn1.disabled = False
        self.root.ids.btn2.disabled = False
        self.root.ids.btn3.disabled = False
        self.root.ids.btn4.disabled = False
        self.root.ids.btn5.disabled = False
        self.root.ids.btn6.disabled = False
        self.root.ids.btn7.disabled = False
        self.root.ids.btn8.disabled = False
        self.root.ids.btn9.disabled = False

        self.root.ids.btn1.text = ""
        self.root.ids.btn2.text = ""
        self.root.ids.btn3.text = ""
        self.root.ids.btn4.text = ""
        self.root.ids.btn5.text = ""
        self.root.ids.btn6.text = ""
        self.root.ids.btn7.text = ""
        self.root.ids.btn8.text = ""
        self.root.ids.btn9.text = ""

        self.root.ids.btn1.color = "green"
        self.root.ids.btn2.color = "green"
        self.root.ids.btn3.color = "green"
        self.root.ids.btn4.color = "green"
        self.root.ids.btn5.color = "green"
        self.root.ids.btn6.color = "green"
        self.root.ids.btn7.color = "green"
        self.root.ids.btn8.color = "green"
        self.root.ids.btn9.color = "green"
        self.winner = False
        self.X_win = 0
        self.O_win = 0
        self.root.ids.game1.text = f"X - {self.X_win} | O - {self.O_win}"
        self.root.ids.score.text = f"{a}'s Turn!"

    def send_message(self):
        self.chat = Chat(pairs, reflections)
        user_message = self.root.ids.user_input.text
        if user_message:
            response = self.chat.respond(user_message)
            self.root.ids.chat_layout.add_widget(
                MDLabel(text='You: ' + user_message, size_hint_y=None, height=(50)))
            self.root.ids.chat_layout.add_widget(
                MDLabel(text='Bot: ' + response, size_hint_y=None, height=(50)))
            self.root.ids.chat_scroll.scroll_to(
                self.root.ids.chat_layout.children[0])

            self.root.ids.user_input.text = ''

    def download_mp3(self):
        try:
            if self.root.ids.url_input.text == "":
                toast('Plz Enter URL')
            else:
                yt = YouTube(self.root.ids.url_input.text)
                video = yt.streams.filter(only_audio=True).first()
                file_name = video.download()
                base, ext = os.path.splitext(file_name)
                new_file_name = base + '.mp3'
                os.rename(file_name, new_file_name)
                toast('MP3 downloaded successfully!')
        except Exception as e:
            toast('Error: ' + str(e))

    def download_mp4(self):
        try:
            if self.root.ids.url_input.text == "":
                toast('Plz Enter URL')
            else:
                yt = YouTube(self.root.ids.url_input.text)
                video = yt.streams.filter(res='1080p').first()
                file_name = video.download()
                base, ext = os.path.splitext(file_name)
                new_file_name = base + '.mp4'
                video_clip = VideoFileClip(file_name)
                audio_clip = video_clip.audio
                audio_clip.write_audiofile(new_file_name)
                audio_clip.close()
                video_clip.close()
                os.remove(file_name)
                toast('MP4 downloaded successfully!')
        except Exception as e:
            toast('Error: ' + str(e))

    def show_data(self):
        pwd = Solution()
        if self.root.ids.user_input1.text == "":
            self.check_ID = 'Plz Enter Password'
        else:
            ou = str(pwd.strongPasswordChecker(self.root.ids.user_input1.text))
            if ou == "0":
                self.check_ID = "Strongest Password !"
            elif ou == "1":
                self.check_ID = "Strong Password !"
            elif ou == "2":
                self.check_ID = "Normal Password !"
            elif ou == "3":
                self.check_ID = "Weak Password !"
            else:
                self.check_ID = "Weakest Password !"
        self.close_b = MDFlatButton(
            text="Close",
            on_press=self.close_dialog
        )
        self.dialog = MDDialog(
            title='User ID Check',
            text=self.check_ID,
            size_hint=(0.8, 1),
            buttons=[self.close_b]
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def on_start(self):
        self.root.ids.tabs.add_widget(Tab(tab_label_text="t1", icon="magnify"))
        self.root.ids.tabs.add_widget(
            Tab2(tab_label_text="t2", icon="face-recognition", screen_manager=self.root.ids.screen_manager))

    def switch_tab_by_object(self):
        try:
            x = next(self.iter_list_objects)
            print(f"Switch slide by object, next element to show: [{x}]")
            self.root.ids.tabs.switch_tab(x)
        except StopIteration:
            # reset the iterator an begin again.
            self.iter_list_objects = iter(
                list(self.root.ids.tabs.get_tab_list()))
            self.switch_tab_by_object()

    def switch_tab_by_name(self):
        '''Switching the tab by name.'''
        try:
            x = next(self.iter_list_names)
            print(f"Switch slide by name, next element to show: [{x}]")
            self.root.ids.tabs.switch_tab(x)
        except StopIteration:
            # Reset the iterator an begin again.
            self.iter_list_names = iter(list(self.icons))
            self.switch_tab_by_name()


if __name__ == "__main__":
    app = Example()
    app.run()
