import re
import threading
from functools import partial
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from plyer import filechooser
import numpy as np
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import mysql.connector
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window

Window.size = (300, 500)

username_helper = """
ScreenManager:
    FirstScreen:
    UserScreen:
    SignupScreen:
    LoginScreen:
    CameraScreen:


<FirstScreen>:
    name:'first'
    MDScreen:
        MDFloatLayout:
            md_bg_color: 226/255, 0, 48/255, 1
            Image:
                source: "image/logo.jpg"
                size_hint: .5, .5
                pos_hint: {'center_x':0.5, 'center_y':0.7}
                canvas.before:
                    Color:
                        rgb: 1, 1, 1, 1
                        Ellipse: 
                            size: 130, 130
                            pos: 110, 250
            MDLabel:
                text: "Augmented Learning"
                pos_hint: {'center_x':0.5, 'center_y':0.3}
                halign: "center"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                font_size: "45sp"
                font_name: "Poppins-SemiBold.ttf"


<UserScreen>:
    name: 'user'
    Image:
        source: "image/abc.png"
        pos_hint: {"y": .25}

    MDLabel:
        text: "Log In"
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        halign: "center"
        font_size: "30sp"
        font_name: "Poppins-SemiBold.ttf"
        theme_text_color: "Custom"
        text_color: 102/255, 0, 1, 1

    MDTextField:
        id:email
        hint_text: "Enter Email"
        helper_text_mode: "on_focus"

        pos_hint: {'center_x':0.5, 'center_y':0.4}
        size_hint_x:None
        width:250
    MDTextField:
        id:password
        hint_text: "Enter Password"
        helper_text_mode: "on_focus"

        pos_hint: {'center_x':0.5, 'center_y':0.3}
        size_hint_x:None
        width:250
    MDFillRoundFlatButton:
        text:'Sign in'
        md_bg_color: 0, 142/255, 250/255, 1
        pos_hint:{'center_x': 0.5, 'center_y': 0.19}
        on_release:
            app.receive_data(email,password)
            #root.manager.current = 'login'
            #root.manager.transition.direction = 'left'

    MDLabel:
        text: "Don't have an Account? "
        font_size: "15sp"
        pos_hint: {'center_x':0.62, 'center_y':0.1}
    MDTextButton:
        text: "Sign Up"
        theme_text_color: "Custom"
        text_color: 0, 1, 0, 1
        font_size: "15sp"
        pos_hint: {'center_x':0.74, 'center_y':0.1}
        on_release:
            root.manager.current = 'signup'
            root.manager.transition.direction = 'left'

<SignupScreen>:
    name: 'signup'
    MDLabel:
        text: "Register"
        pos_hint: {'center_x':0.5, 'center_y':0.8}
        halign: "center"
        font_size: "50sp"
        font_name: "Poppins-SemiBold.ttf"
        theme_text_color: "Custom"
        text_color:255/255, 102/255, 153/255, 1
    MDTextField:
        id:name
        hint_text: "Enter Name"
        helper_text_mode: "on_focus"

        pos_hint: {'center_x':0.5, 'center_y':0.6}
        size_hint_x:None
        width:250
    MDTextField:
        id:email
        hint_text: "Enter E-mail"
        helper_text_mode: "on_focus"
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        size_hint_x:None
        width:250
    MDTextField:
        id:password
        hint_text: "Enter Password"
        helper_text_mode: "on_focus"

        pos_hint: {'center_x':0.5, 'center_y':0.4}
        size_hint_x:None
        width:250
    MDFillRoundFlatIconButton:
        text:'Create'
        md_bg_color: 0, 142/255, 250/255, 1
        icon: "account-plus"
        theme_icon_color: "Custom"
        icon_color: 0, 0, 0, 1
        pos_hint:{'center_x': 0.5, 'center_y': 0.24}
        on_release:
            app.send_data(email,password,name)
    
    MDLabel:
        text: "Have an Account? "
        font_size: "15sp"
        pos_hint: {'center_x':0.7, 'center_y':0.15}
    MDTextButton:
        text: "Log In"
        theme_text_color: "Custom"
        text_color: 0, 1, 0, 1
        font_size: "15sp"
        pos_hint: {'center_x':0.71, 'center_y':0.15}
        on_release:
            root.manager.current = 'user'
            root.manager.transition.direction = 'right'

<LoginScreen>:
    name:'login'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:
                        orientation:'vertical'
                        MDToolbar:
                            title: 'Augmented Learning'
                            left_action_items: [["menu", lambda x: nav_drawer.set_state('toggle')]]
                            elevation:15

                        ScrollView:
                            size: self.size

                            GridLayout:
                                cols:2
                                padding: dp(7),dp(7)
                                spacing : dp(8)
                                size_hint_y: None
                                height: self.minimum_height
                                width: self.minimum_width
                                MyTile:
                                    source: 'image/img.png'
                                    height: '150dp'
                                    text : '[size=20]St Xavier intro[/size]'
                                    # stars: 5
                                    on_press:
                                        app.read_file()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source: 'image/img1.png'
                                    height: '150dp'
                                    text : '[size=20][color=#00FFFF]Computer_Basic[/color][/size]'
                                    # stars: 2
                                    on_press:
                                        app.read_file1()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source : 'image/img2.png'
                                    height: '150dp'
                                    text: '[size=20][color=#FF0000]Computer and its hardware[/size][/color]'
                                    # stars: 5
                                    on_press:
                                        app.read_file2()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source: 'image/img3.png'
                                    height: '150dp'
                                    text : '[size=20]Internet[/size]'
                                    # stars: 5
                                    on_press:
                                        app.read_file3()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source: 'image/img4.png'
                                    height: '150dp'
                                    text : '[size=20][color=#00FFFF]Machine_Learning[/color][/size]'
                                    # stars: 2
                                    on_press:
                                        app.read_file4()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source : 'image/img5.png'
                                    height: '150dp'
                                    text: '[size=20][color=#FF0000]India Geography[/size][/color]'
                                    # stars: 5
                                    on_press:
                                        app.read_file5()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source: 'image/img6.png'
                                    height: '150dp'
                                    text : '[size=20]india_History[/size]'
                                    # stars: 5
                                    on_press:
                                        app.read_file6()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source: 'image/img7.png'
                                    height: '150dp'
                                    text : '[size=20][color=#00FFFF]Wild_life[/color][/size]'
                                    # stars: 2
                                    on_press:
                                        app.read_file7()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source : 'image/img8.png'
                                    height: '150dp'
                                    text: '[size=20][color=#FF0000]Earth[/size][/color]'
                                    # stars: 5
                                    on_press:
                                        app.read_file8()
                                    on_release:
                                        root.manager.current = 'cam'
                                MyTile:
                                    source : 'image/img9.png'
                                    height: '150dp'
                                    text: '[size=20][color=#FF0000]Tom&jerry show[/size][/color]'
                                    # stars: 5
                                    on_press:
                                        app.read_file9()
                                    on_release:
                                        root.manager.current = 'cam'

            MDNavigationDrawer:
                id: nav_drawer

                BoxLayout:

                    orientation:'vertical'
                    spacing:'8dp'
                    padding:'12dp'
                    FitImage: 
                        id: img 
                        size_hint_x: 1
                        allow_stretch: True
                    MDFloatingActionButton:
                        icon:'image-plus'
                        on_release:
                            app.file_chooser()


                    MDLabel:
                        id:label1
                        text: ''
                        font_style: 'Subtitle1'
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDLabel:
                        id:label2
                        text: ''
                        font_style: 'Caption'
                        size_hint_y: None
                        height: self.texture_size[1]
                    ScrollView:
                        MDList: 
                            OneLineIconListItem:
                                text: 'Logout'
                                on_release:
                                    root.manager.current = 'user'
                                    root.manager.transition.direction = 'right'
                                IconLeftWidget:
                                    icon:'logout'

<CameraScreen>:
    name: "cam"
    orientation: 'vertical'

    FloatLayout:


        Image:
            # this is where the video will show
            # the id allows easy access
            id: vid
            size_hint: 2, 1
            allow_stretch: True  # allow the video image to be scaled
            keep_ratio: True  # keep the aspect ratio so people don't look squashed
            pos_hint: {'center_x':0.5, 'top':1}

        MDFloatingActionButton:
            icon:'arrow-left'
            pos_hint:{'center_x': 0.1, 'center_y': 0.9}
            on_release:
                root.manager.current = 'login'
                root.manager.transition.direction = 'right' 
        ToggleButton:
            text: 'Stop'
            on_release: app.stop_vid()
            size_hint_y: None
            height: '48dp'
        
<MyTile@SmartTileWithStar>
    size_hint_y : None
    height : '240dp'


"""


class FirstScreen(Screen):
    pass


class UserScreen(Screen):
    pass


class SignupScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class CameraScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(FirstScreen(name='first'))
sm.add_widget(UserScreen(name='user'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(CameraScreen(name='cam'))
sm.add_widget(SignupScreen(name='signup'))


class ALApp(MDApp):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Z|a-z]{2,}\b'
    database = mysql.connector.Connect(host="localhost", user="root", password="aman", database="login",
                                       port="3306",
                                       auth_plugin="mysql_native_password")
    cursor = database.cursor(buffered=True)
    cursor.execute("select * from logindata")
    for i in cursor.fetchall():
        print(i[0], i[1])

    def build(self):
        self.theme_cls.primary_palette = 'Orange'
        self.theme_cls.theme_style = 'Dark'
        screen = Screen()
        self.username = Builder.load_string(username_helper)
        screen.add_widget(self.username)
        return screen

    def send_data(self, email, password, name):
        if re.fullmatch(self.regex, email.text):
            self.cursor.execute(f"insert into logindata values('{email.text}','{password.text}','{name.text}')")
            self.database.commit()
            self.username.get_screen('login').ids.label1.text = str(name.text)
            email.text = ""
            password.text = ""
            name.text = ""
            self.username.get_screen('user').manager.current = 'user'

    def receive_data(self, email, password):
        self.cursor.execute("select * from logindata")
        email_list = []
        for i in self.cursor.fetchall():
            email_list.append(i[0])
        if email.text in email_list and email.text != "":
            self.cursor.execute(f"select password from logindata where email='{email.text}'")

            for j in self.cursor:
                if password.text == j[0]:
                    self.username.get_screen('login').manager.current = 'login'
                    self.username.get_screen('login').ids.label2.text = str(email.text)

                else:
                    cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
                    self.dialog = MDDialog(title='Invalid Username or Password',
                                           text="Please input a valid username or password", size_hint=(0.7, 0.2),
                                           buttons=[cancel_btn_username_dialogue])
                    self.dialog.open()

        else:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(title='Invalid Username or Password',
                                   text="Please input a valid username or password", size_hint=(0.4, 0.1),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        name = self.cursor.execute(f"select password from logindata where email='{email.text}'")
        print(name)

    def close_username_dialogue(self, obj):
        self.dialog.dismiss()

    def read_file(self):
        threading.Thread(target=self.doit, daemon=True).start()

    def doit(self):

        self.do_vid = True
        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img.png')
        myVid = cv2.VideoCapture('video/vid.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)

            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file1(self):
        threading.Thread(target=self.doit1, daemon=True).start()

    def doit1(self):

        self.do_vid = True

        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img1.png')
        myVid = cv2.VideoCapture('video/vid1.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file2(self):
        threading.Thread(target=self.doit2, daemon=True).start()

    def doit2(self):

        self.do_vid = True

        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img2.png')
        myVid = cv2.VideoCapture('video/vid2.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file3(self):
        threading.Thread(target=self.doit3, daemon=True).start()

    def doit3(self):

        self.do_vid = True
        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img3.png')
        myVid = cv2.VideoCapture('video/vid3.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file4(self):
        threading.Thread(target=self.doit4, daemon=True).start()

    def doit4(self):

        self.do_vid = True
        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img4.png')
        myVid = cv2.VideoCapture('video/vid4.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file5(self):
        threading.Thread(target=self.doit5, daemon=True).start()

    def doit5(self):

        self.do_vid = True
        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img5.png')
        myVid = cv2.VideoCapture('video/vid5.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file6(self):
        threading.Thread(target=self.doit6, daemon=True).start()

    def doit6(self):

        self.do_vid = True
        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img6.png')
        myVid = cv2.VideoCapture('video/vid6.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file7(self):
        threading.Thread(target=self.doit7, daemon=True).start()

    def doit7(self):

        self.do_vid = True
        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img7.png')
        myVid = cv2.VideoCapture('video/vid7.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file8(self):
        threading.Thread(target=self.doit8, daemon=True).start()

    def doit8(self):

        self.do_vid = True
        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img8.png')
        myVid = cv2.VideoCapture('video/Vid8.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()

    def read_file9(self):
        threading.Thread(target=self.doit9, daemon=True).start()

    def doit9(self):
        self.do_vid = True
        cam = cv2.VideoCapture(0)
        imgTarget = cv2.imread('image/img9.png')
        myVid = cv2.VideoCapture('video/Vid9.mp4')
        success, imgVideo = myVid.read()
        hT, wT, cT = imgTarget.shape
        imgVideo = cv2.resize(imgVideo, (wT, hT))
        orb = cv2.ORB_create(nfeatures=1000)
        kp1, des1 = orb.detectAndCompute(imgTarget, None)
        # start processing loop
        while (self.do_vid):
            ret, imgWebcam = cam.read()
            imgAug = imgWebcam.copy()
            detection = False
            frameCounter = 0
            kp2, des2 = orb.detectAndCompute(imgWebcam, None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append(m)
            imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
            if len(good) > 20:
                detection = True
                srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
                matrix, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC, 5)
                pts = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(-1, 1, 2)
                dst = cv2.perspectiveTransform(pts, matrix)
                img2 = cv2.polylines(imgWebcam, [np.int32(dst)], True, (255, 0, 255), 3)
                imgWarp = cv2.warpPerspective(imgVideo, matrix, (imgWebcam.shape[1], imgWebcam.shape[0]))
                maskNew = np.zeros((imgWebcam.shape[0], imgWebcam.shape[1]), np.uint8)
                cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
                maskTnv = cv2.bitwise_not(maskNew)
                imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskTnv)
                imgAug = cv2.bitwise_or(imgWarp, imgAug)
            if detection == False:
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frameCounter = 0
            else:
                if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                    myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    frameCounter = 0
            success, imgVideo = myVid.read()
            imgVideo = cv2.resize(imgVideo, (wT, hT))
            Clock.schedule_once(partial(self.display_frame, imgAug))
            cv2.waitKey(1)
        cam.release()
        cv2.destroyAllWindows()


    def display_frame(self, frame, dt):
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        self.username.get_screen('cam').ids.vid.texture = texture

    def file_chooser(self):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            self.username.get_screen('login').ids.img.source = selection[0]

    def on_start(self):
        Clock.schedule_once(self.first, 15)

    def first(self, *args):
        self.username.get_screen('user').manager.current = 'user'

    def stop_vid(self):
        # stop the video capture loop
        self.do_vid = False

ALApp().run()