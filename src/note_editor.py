from gi.repository import Gtk

from store import store

class NoteEditor(Gtk.VBox):
    def __init__(self, note, on_name_updated):
        Gtk.VBox.__init__(self)
        self.set_border_width(8)
        self.set_spacing(10)

        self.note = note
        self.on_name_updated = on_name_updated

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_shadow_type(type=Gtk.ShadowType.IN)
        scrolled_window.show()

        self.name_entry = Gtk.Entry()
        self.name_entry.set_text(self.note['name'])
        self.name_entry.set_placeholder_text('Note Name')
        self.name_entry.set_max_length(30)
        self.name_entry.connect('changed', self.name_changed)
        self.name_entry.show()

        text_view = Gtk.TextView()
        text_view.set_margin_top(5)
        text_view.set_margin_bottom(5)
        text_view.set_margin_left(5)
        text_view.set_margin_right(5)
        text_view.set_wrap_mode(Gtk.WrapMode.CHAR)
        text_view.show()

        self.buffer = text_view.get_buffer()
        self.buffer.set_text(self.note['content'])
        self.buffer.connect('changed', self.text_changed)

        scrolled_window.add(text_view)

        self.pack_start(self.name_entry, False, False, 0)
        self.pack_start(scrolled_window, True, True, 0)

        self.show()
    def name_changed(self, _entry):
        self.note['name'] = self.name_entry.get_text()
        self.on_name_updated(self.note['name'])
        store['confirm_close'] = True
    def text_changed(self, _text_view):
        self.note['content'] = self.buffer.get_text(
            self.buffer.get_start_iter(),
            self.buffer.get_end_iter(),
            True
        )
        store['confirm_close'] = True
