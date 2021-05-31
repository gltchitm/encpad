from gi.repository import Gtk

from store import store
    
class CreateNewNotepad(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(10)

        notepad_name_box = Gtk.VBox()
        password_box = Gtk.VBox()
        password_copy_box = Gtk.VBox()
        
        password_label = Gtk.Label("Notepad Password")
        password_label.set_xalign(0.0)
        
        password_copy_label = Gtk.Label("Re-enter Notepad Password")
        password_copy_label.set_xalign(0.0)

        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)

        self.password_copy_entry = Gtk.Entry()
        self.password_copy_entry.set_visibility(False)

        password_character = self.password_entry.get_invisible_char()
        self.password_entry.set_placeholder_text(password_character * 8)
        self.password_copy_entry.set_placeholder_text(password_character * 8)

        password_box.add(password_label)
        password_box.add(self.password_entry)

        password_copy_box.add(password_copy_label)
        password_copy_box.add(self.password_copy_entry)

        create_notepad_btn = Gtk.Button("Create Notepad")
        create_notepad_btn.connect(
            "clicked",
            lambda btn: self.create_notepad()
        )

        back_btn = Gtk.Button("Back to Main Menu")
        back_btn.connect("clicked", lambda btn: self.back())
        
        self.pack_start(password_box, False, False, 0)
        self.pack_start(password_copy_box, False, False, 0)
        self.pack_start(create_notepad_btn, False, False, 0)
        self.pack_start(back_btn, False, False, 0)
    def create_notepad(self):
        password = self.password_entry.get_text()
        if password != self.password_copy_entry.get_text():
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Cannot Create Notepad"
            )
            dialog.format_secondary_text("Passwords do not match.")
            dialog.run()
            dialog.destroy()
        elif len(password) < 8:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Cannot Create Notepad"
            )
            dialog.format_secondary_text("Passwords must be at least 8 characters long.")
            dialog.run()
            dialog.destroy()
        else:
            store.set_value("password", password)
            store.set_value("notepad", {
                "untitled_number": 1,
                "notes": [
                    {
                        "name": "Untitled Note 1",
                        "content": "Your first note."
                    }
                ]
            })

            self.clear()

            store.get_value("notepad_editor").open_notepad()
            store.get_value("stack").set_visible_child_name("notepad_editor")
    def back(self):
        self.clear()
        store.get_value("stack").set_visible_child_name("welcome")
    def clear(self):
        self.password_entry.set_text("")
        self.password_copy_entry.set_text("")