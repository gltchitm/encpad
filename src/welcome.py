from gi.repository import Gtk

from migrate import can_migrate_notepad
from store import store

class Welcome(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(10)

        new_notepad_button = Gtk.Button('New Notepad')
        load_notepad_button = Gtk.Button('Load Notepad')

        new_notepad_button.connect(
            'clicked',
            lambda _btn: store['stack'].set_visible_child_name('create_new_notepad')
        )
        load_notepad_button.connect(
            'clicked',
            lambda _btn: self.load_notepad()
        )

        self.pack_start(new_notepad_button, True, True, 0)
        self.pack_start(load_notepad_button, True, True, 0)
    def load_notepad(self):
        file_chooser = Gtk.FileChooserDialog(
            title='Encpad',
            parent=self.get_toplevel(),
            action=Gtk.FileChooserAction.OPEN,
            buttons=('Cancel', Gtk.ResponseType.CANCEL, 'Open', Gtk.ResponseType.OK)
        )

        response = file_chooser.run()
        filename = file_chooser.get_filename()

        file_chooser.destroy()

        if response != Gtk.ResponseType.OK:
            return

        with open(filename, 'rb') as file:
            def read_until_null():
                result = b''
                byte = file.read(1)

                while byte != b'\0':
                    result += byte
                    byte = file.read(1)

                    if byte == b'':
                        break

                return result

            encpad_version = read_until_null()

            read_until_null()

            encrypted_notepad = file.read()

            if encpad_version != bytes('encpad[' + store['FORMAT_VERSION'] + ']', 'utf-8'):
                file.seek(0)
                file_data = file.read()

                if can_migrate_notepad(file_data):
                    dialog = Gtk.MessageDialog(
                        message_type=Gtk.MessageType.QUESTION,
                        buttons=Gtk.ButtonsType.YES_NO,
                        text='Migrate Notepad'
                    )
                    dialog.format_secondary_text(
                        'This notepad appears to have been encrypted with an old version '
                        'of Encpad. You must migrate it if you want to use it with this '
                        'program. Migrate notepad?'
                    )

                    response = dialog.run()
                    dialog.destroy()

                    if response != Gtk.ResponseType.YES:
                        return

                    encrypted_notepad = file_data

                    store['migrate_notepad'] = True
                else:
                    dialog = Gtk.MessageDialog(
                        message_type=Gtk.MessageType.ERROR,
                        buttons=Gtk.ButtonsType.OK,
                        text='Unsupported Notepad'
                    )
                    dialog.format_secondary_text(
                        'This notepad may have been encrypted with a verison of Encpad that '
                        'this program does not support or it may be corrupt. Try decrypting '
                        'it with the version of Encpad that was used to encrypt it.'
                    )

                    dialog.run()
                    dialog.destroy()

                    return
            else:
                store['migrate_notepad'] = False

            store['encrypted_notepad'] = encrypted_notepad
            store['stack'].set_visible_child_name('unlock_notepad')
