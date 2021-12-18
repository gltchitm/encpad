from gi.repository import Gtk

from crypto import encrypt
from store import store
from json import dumps

from note_editor import NoteEditor

class NotepadEditor(Gtk.VBox):
    def __init__(self):
        Gtk.VBox.__init__(self)
        self.set_spacing(10)

        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)

        buttons_box = Gtk.Box()
        buttons_box.set_spacing(10)

        new_note_button = Gtk.Button('New Note')
        save_and_exit_button = Gtk.Button('Save & Exit')
        self.delete_note_button = Gtk.Button('Delete Note')

        new_note_button.connect('clicked', lambda _btn: self.new_note())
        save_and_exit_button.connect('clicked', lambda _btn: self.save())
        self.delete_note_button.connect('clicked', lambda _btn: self.delete_note())

        buttons_box.pack_start(new_note_button, True, True, 0)
        buttons_box.pack_start(self.delete_note_button, True, True, 0)
        buttons_box.pack_start(save_and_exit_button, True, True, 0)

        self.pack_start(self.notebook, True, True, 0)
        self.pack_start(buttons_box, False, False, 0)

        self.connect('map', self.map)
    def init_editor(self, note):
        label = Gtk.Label(note['name'])
        editor = NoteEditor(note, lambda name: label.set_label(name))
        return self.notebook.append_page(editor, label)
    def map(self, _data):
        for note in store['notepad']['notes']:
            self.init_editor(note)
        self.delete_note_button.set_sensitive(len(store['notepad']['notes']) > 1)
    def new_note(self):
        store['notepad']['untitled_number'] += 1
        untitled_number = store['notepad']['untitled_number']

        note = {
            'name': 'Untitled Note %d' % untitled_number,
            'content': ''
        }

        index = self.init_editor(note)

        store['notepad']['notes'].append(note)
        store['confirm_close'] = True

        self.delete_note_button.set_sensitive(True)

        self.notebook.set_current_page(index)
    def save(self):
        encrypted_notepad = encrypt(
            bytes(dumps(store['notepad']), 'utf-8'),
            bytes(store['password'], 'utf-8')
        )

        file_chooser = Gtk.FileChooserDialog(
            title='Encpad',
            parent=self.get_toplevel(),
            action=Gtk.FileChooserAction.SAVE,
            buttons=('Cancel', Gtk.ResponseType.CANCEL, 'Save', Gtk.ResponseType.OK)
        )
        file_chooser.set_current_name('Untitled.encpad')

        response = file_chooser.run()
        filename = file_chooser.get_filename()

        file_chooser.destroy()

        if response == Gtk.ResponseType.OK:
            with open(filename, 'wb') as file:
                file_header = bytes(
                    'encpad[{format_version}]\0[encpadpy-{application_version}]\0'.format(
                        format_version=store['FORMAT_VERSION'],
                        application_version=store['APPLICATION_VERSION']
                    ),
                    'utf-8'
                )

                file.write(file_header + encrypted_notepad)
            exit(0)
    def delete_note(self):
        if len(store['notepad']['notes']) > 1:
            dialog = Gtk.MessageDialog(
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text='Delete Note'
            )
            dialog.format_secondary_text('Are you sure you want to delete this note?')
            response = dialog.run()
            dialog.destroy()
            if response == Gtk.ResponseType.YES:
                notepad = store['notepad']
                del notepad['notes'][self.notebook.get_current_page()]
                self.notebook.remove_page(self.notebook.get_current_page())
                store['notepad'] = notepad
        if len(store['notepad']['notes']) <= 1:
            self.delete_note_button.set_sensitive(False)
