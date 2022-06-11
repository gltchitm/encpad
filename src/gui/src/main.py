import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from store import store

from create_new_notepad import CreateNewNotepad
from notepad_editor import NotepadEditor
from unlock_notepad import UnlockNotepad
from welcome import Welcome

store['FORMAT_VERSION'] = '2'
store['BRAND'] = 'encpadpy'
store['APPLICATION_VERSION'] = '1.0.0'

class Encpad(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Encpad')

        store['password'] = None
        store['notepad'] = None

        self.set_border_width(20)

        self.set_default_size(360, 560)
        self.set_resizable(False)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(200)

        store['stack'] = stack

        stack.add_named(Welcome(), 'welcome')
        stack.add_named(UnlockNotepad(), 'unlock_notepad')
        stack.add_named(CreateNewNotepad(), 'create_new_notepad')
        stack.add_named(NotepadEditor(), 'notepad_editor')

        stack.set_visible_child_name('welcome')

        self.connect('delete-event', self.window_delete)
        self.add(stack)
    def window_delete(self, _widget, _event):
        if store['confirm_close']:
            dialog = Gtk.MessageDialog(
                message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                text='You have unsaved changes.'
            )
            dialog.format_secondary_text('Are you sure you want to exit without saving them?')
            response = dialog.run()
            dialog.destroy()
            if response != Gtk.ResponseType.YES:
                return True
        return False

if __name__ == '__main__':
    window = Encpad()
    window.connect('destroy', Gtk.main_quit)
    window.show_all()

    Gtk.main()
