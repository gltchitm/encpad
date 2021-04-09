from gi.repository import Gtk

from base64 import b64decode
from store import store
from json import loads

class Welcome(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(10)
        
        new_notepad_button = Gtk.Button("New Notepad")
        load_notepad_button = Gtk.Button("Load Notepad")

        new_notepad_button.connect(
            "clicked",
            lambda btn: store.get_value("stack").set_visible_child_name("create_new_notepad")
        )
        load_notepad_button.connect(
            "clicked",
            lambda btn: self.load_notepad()
        )

        self.pack_start(new_notepad_button, True, True, 0)
        self.pack_start(load_notepad_button, True, True, 0)
    def load_notepad(self):
        file_chooser = Gtk.FileChooserDialog(
            title="Encpad",
            parent=self.get_toplevel(),
            action=Gtk.FileChooserAction.OPEN,
            buttons=("Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        )

        response = file_chooser.run()
        filename = file_chooser.get_filename()

        file_chooser.destroy()

        if response == Gtk.ResponseType.OK:
            try:
                with open(filename, "r") as file:
                    parsed_notepad = loads(
                        b64decode(
                            bytes(
                                file.read().replace(
                                    store.get_value("ENCRYPTED_DISCLAIMER"),
                                    "",
                                    1
                                ),
                                "utf-8"
                            )
                        ).decode("utf-8")
                    )
                    if parsed_notepad["version"] != store.get_value("VERSION"):
                        dialog = Gtk.MessageDialog(
                            transient_for=self.get_toplevel(),
                            message_type=Gtk.MessageType.WARNING,
                            buttons=Gtk.ButtonsType.YES_NO,
                            text="Version Mismatch"
                        )
                        dialog.format_secondary_text(
                            (
                                "This notepad was saved in version %s, " +
                                "but you are using %s.\n" +
                                "Are you sure you want to proceed? " +
                                "Doing so may cause notepad corruption."
                            ) % (parsed_notepad["version"], store.get_value("VERSION"))
                        )

                        response = dialog.run()
                        
                        dialog.destroy()

                        if response == Gtk.ResponseType.NO:
                            return
                        
                    store.set_value("notepad", parsed_notepad)
                    store.get_value("stack").set_visible_child_name("unlock_notepad")
            except Exception:
                dialog = Gtk.MessageDialog(
                    transient_for=self.get_toplevel(),
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.OK,
                    text="Loading Failed"
                )
                dialog.format_secondary_text(
                    "Could not load notepad!"
                )

                response = dialog.run()
                
                dialog.destroy()