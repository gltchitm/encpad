package me.gltchitm.encpad;

import com.googlecode.lanterna.gui2.ActionListBox;
import com.googlecode.lanterna.gui2.BasicWindow;
import com.googlecode.lanterna.gui2.Borders;
import com.googlecode.lanterna.gui2.Button;
import com.googlecode.lanterna.gui2.Panel;
import com.googlecode.lanterna.gui2.TextBox;
import com.googlecode.lanterna.gui2.WindowBasedTextGUI;

public class ViewNotepad {
    public static void displayNotepad(Notepad notepad, final BasicWindow window, final WindowBasedTextGUI textGUI) {
        Panel panel = new Panel();
        ActionListBox actionListBox = new ActionListBox();
        
        for (final Note note : notepad.notes) {
            actionListBox.addItem(note.name, new Runnable() {
                @Override
                public void run() {
                    Panel notePanel = new Panel();
                    notePanel.addComponent(new TextBox(note.content).setReadOnly(true));
                    window.setComponent(notePanel.withBorder(Borders.singleLine(note.name)));
                }
            });
        }

        panel.addComponent(actionListBox);
        panel.addComponent(new Button("Exit", new Runnable() {
            @Override
            public void run() {
                System.exit(0);
            }
        }));

        window.setComponent(panel.withBorder(Borders.singleLine("Encpad")));
    }
}
