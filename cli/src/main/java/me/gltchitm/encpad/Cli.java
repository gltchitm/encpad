package me.gltchitm.encpad;

import com.googlecode.lanterna.gui2.*;
import com.googlecode.lanterna.screen.Screen;
import com.googlecode.lanterna.screen.TerminalScreen;
import com.googlecode.lanterna.terminal.DefaultTerminalFactory;
import com.googlecode.lanterna.terminal.Terminal;

import java.io.IOException;
import java.util.Arrays;

public class Cli {
    public static void main(String[] args) throws IOException {
        Terminal terminal = new DefaultTerminalFactory().createTerminal();
        
        Screen screen = new TerminalScreen(terminal);
        screen.startScreen();

        Panel panel = new Panel();
        panel.setLayoutManager(new LinearLayout(Direction.VERTICAL));
        panel.setLayoutData(BorderLayout.Location.CENTER);

        BasicWindow window = new BasicWindow();
        window.setHints(Arrays.asList(Window.Hint.CENTERED));
        window.setComponent(panel.withBorder(Borders.singleLine("Encpad")));

        final WindowBasedTextGUI textGUI = new MultiWindowTextGUI(screen);

        ViewNotepad.displayNotepad(LoadNotepad.loadNotepad(textGUI), window, textGUI);

        textGUI.addWindowAndWait(window);
    }
}
