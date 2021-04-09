from gi.repository import Gtk

from crypto import decrypt
from base64 import b64decode
from store import store
from json import loads

class UnlockNotepad(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(10)

        password_box = Gtk.VBox()

        password_label = Gtk.Label("Enter Password")
        password_label.set_xalign(0.0)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)

        password_character = self.password_entry.get_invisible_char()
        self.password_entry.set_placeholder_text(password_character * 8)

        password_box.add(password_label)
        password_box.add(self.password_entry)

        unlock_btn = Gtk.Button("Unlock Notepad")
        back_btn = Gtk.Button("Back to Main Menu")

        unlock_btn.connect("clicked", lambda btn: self.unlock())
        back_btn.connect("clicked", lambda btn: self.back())

        self.pack_start(password_box, False, False, 0)
        self.pack_start(unlock_btn, False, False, 0)
        self.pack_start(back_btn, False, False, 0)
    def unlock(self):
        notepad = store.get_value("notepad")

        decrypted_notes = decrypt(
            notepad["notes"],
            self.password_entry.get_text()
        )

        if decrypted_notes == None:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Bad Decrypt"
            )
            dialog.format_secondary_text("You may have entered an incorrect password.")
            dialog.run()
            dialog.destroy()

            self.password_entry.set_text("")
        else:
            notepad["notes"] = loads(decrypted_notes)

            store.set_value("password", self.password_entry.get_text())
            store.set_value("notepad", notepad)
            
            store.get_value("notepad_editor").open_notepad()

            store.get_value("stack").set_visible_child_name("notepad_editor")
    def back(self):
        self.password_entry.set_text("")
        store.get_value("stack").set_visible_child_name("welcome")