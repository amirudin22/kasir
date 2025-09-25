from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from modules.db import init_db
from modules.auth import get_hwid, register_user, login

init_db()

KV = open('kvs/screens.kv').read()

class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass

class POSApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hwid = get_hwid()[:32]
        self.user = None

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

    def do_register(self, username, password, code):
        ok, msg = register_user(username, password, code, role='owner' if username=='owner' else 'kasir')
        from kivymd.toast import toast
        toast(msg)
        if ok:
            self.root.current = 'login'

    def do_login(self, username, password):
        ok, data = login(username, password)
        from kivymd.toast import toast
        if ok:
            self.user = data
            toast('Login sukses')
            self.root.current = 'dashboard'
        else:
            toast(data)

if __name__ == '__main__':
    POSApp().run()
