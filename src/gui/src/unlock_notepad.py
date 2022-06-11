from gi.repository import Gtk

from migrate import migrate_notepad
from crypto import decrypt
from store import store
from json import loads

class UnlockNotepad(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(10)

        password_box = Gtk.VBox()

        password_label = Gtk.Label('Enter Password')
        password_label.set_xalign(0.0)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)

        password_character = self.password_entry.get_invisible_char()
        self.password_entry.set_placeholder_text(password_character * 8)

        password_box.add(password_label)
        password_box.add(self.password_entry)

        self.unlock_btn = Gtk.Button('Unlock Notepad')
        back_btn = Gtk.Button('Back to Main Menu')

        self.unlock_btn.connect('clicked', lambda _btn: self.unlock())
        back_btn.connect('clicked', lambda _btn: self.back())

        self.pack_start(password_box, False, False, 0)
        self.pack_start(self.unlock_btn, False, False, 0)
        self.pack_start(back_btn, False, False, 0)

        self.connect('map', self.map)
    def map(self, _data):
        self.unlock_btn.set_label(('Migrate' if store['migrate_notepad'] else 'Unlock') + ' Notepad')
    def unlock(self):
        try:
            encrypted_notepad = store['encrypted_notepad']
            password = self.password_entry.get_text()

            if store['migrate_notepad']:
                notepad = migrate_notepad(encrypted_notepad, bytes(password, 'utf-8'))
            else:
                notepad = loads(decrypt(encrypted_notepad, bytes(password, 'utf-8')))

            store['password'] = password
            store['notepad'] = notepad

            store['stack'].set_visible_child_name('notepad_editor')
        except Exception:
            dialog = Gtk.MessageDialog(
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text=('Migration' if store['migrate_notepad'] else 'Decrypt') + ' Failed'
            )
            dialog.format_secondary_text('You may have entered an incorrect password.')
            dialog.run()
            dialog.destroy()

            self.password_entry.set_text('')
    def back(self):
        self.password_entry.set_text('')
        store['stack'].set_visible_child_name('welcome')
