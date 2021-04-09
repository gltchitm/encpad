from gi.repository import Gtk

from crypto import encrypt, decrypt
from base64 import b64encode
from store import store
from json import dumps

from note_editor import NoteEditor

import sys

class NotepadEditor(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(10)

        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)

        buttons_box = Gtk.Box()
        buttons_box.set_spacing(10)

        new_note_button = Gtk.Button("New Note")
        delete_note_button = Gtk.Button("Delete Note")
        save_and_exit_button = Gtk.Button("Save & Exit")

        new_note_button.connect("clicked", lambda btn: self.new_note())
        delete_note_button.connect("clicked", lambda btn: self.delete_note())
        save_and_exit_button.connect("clicked", lambda btn: self.save())

        buttons_box.pack_start(new_note_button, True, True, 0)
        buttons_box.pack_start(delete_note_button, True, True, 0)
        buttons_box.pack_start(save_and_exit_button, True, True, 0)

        self.pack_start(self.notebook, True, True, 0)
        self.pack_start(buttons_box, False, False, 0)
    def init_editor(self, note):
        label = Gtk.Label(note["name"])
        editor = NoteEditor(note, lambda name: label.set_label(name))
        return self.notebook.append_page(editor, label)
    def open_notepad(self):
        for note in store.get_value("notepad")["notes"]:
            index = self.init_editor(note)
    def new_note(self):
        untitled_number = store.get_value("notepad")["untitled_number"] + 1
        store.get_value("notepad")["untitled_number"] += 1

        note = {
            "name": "Untitled Note %d" % untitled_number,
            "content": "A new note"
        }

        index = self.init_editor(note)

        store.get_value("notepad")["notes"].append(note)
        store.set_value("confirm_close", True)

        self.notebook.set_current_page(index)
    def save(self):
        unencrypted_notepad = store.get_value("notepad")
        encrypted_notepad = b64encode(
            bytes(
                dumps({
                    "version": store.get_value("VERSION"),
                    "untitled_number": unencrypted_notepad["untitled_number"],
                    "notes": encrypt(
                        dumps(unencrypted_notepad["notes"]),
                        store.get_value("password")
                    )
                }),
                "utf-8"
            )
        ).decode("utf-8")
        file_chooser = Gtk.FileChooserDialog(
            title="Encpad",
            parent=self.get_toplevel(),
            action=Gtk.FileChooserAction.SAVE,
            buttons=("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)
        )
        file_chooser.set_current_name("Untitled.encpad")

        response = file_chooser.run()
        filename = file_chooser.get_filename()
        
        file_chooser.destroy()

        if response == Gtk.ResponseType.OK:
            with open(filename, "w") as file:
                file.write(
                    store.get_value("ENCRYPTED_DISCLAIMER") +
                    encrypted_notepad
                )
            sys.exit(0)
    def delete_note(self):
        if len(store.get_value("notepad")["notes"]) > 1:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text="Delete Note"
            )
            dialog.format_secondary_text("Are you sure you want to delete this note?")
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.YES:
                notepad = store.get_value("notepad")
                del notepad["notes"][self.notebook.get_current_page()]
                self.notebook.remove_page(self.notebook.get_current_page())
                store.set_value("notepad", notepad)
        else:
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Cannot Delete Note"
            )
            dialog.format_secondary_text("You cannot delete the final note.")
            dialog.run()
            dialog.destroy()