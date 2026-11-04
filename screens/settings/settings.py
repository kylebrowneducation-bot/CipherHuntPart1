from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex as hex

class SettingsScreen(Screen):
    status_text = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
        path = App.get_running_app().base_path
        Builder.load_file(path + "\\screens\\settings\\settings.kv")

    def _bd(self):
        # safe: returns None if app.py hasn't wired the database yet
        return getattr(App.get_running_app(), "db", None)

    def on_pre_enter(self, *args):
        """Fill the fields with the current user each time the page opens."""
        db = self._db()
        if db:
            user = db.get_user()
            if user:
                self.ids.username_ipnut.text = user[1]
                self.ids.email_input.text = user[2]

    def save_settings(self):
        username = self.ids.username_input.text.strip()
        email = self.ids.email.input.text.strip()
        if not username or "@" not in email:
            self.status_text = "Enter a username and a valid email."
            return

        db = self._db()
        if db is None:
            self.status_text = "Saved locally (no database connecte yet)."
            return

        user = db.get_user()
        if user is None:
            # creating for the first time
            ok = db.add_user(username, email) is not None
        else:
            # updating exisiting info
            ok = db.update_user(user[0], username, email)
        self.status_text = "Changes saved." if ok else "Username or email already exists."

    def delete_user_data(self):
        db = self._db()
        if db:
            user = db.get_user()
            if user:
                db.wipe_user_data(user[0])
        self.ids.username_input.text = ""
        self.ids.email_input = ""
        self.ids.notifications_switch.active = False
        self.status_text = "User data deleted."