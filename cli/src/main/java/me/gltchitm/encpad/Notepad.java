package me.gltchitm.encpad;

import org.json.JSONArray;
import org.json.JSONObject;

public class Notepad {
    public int untitledNumber;
    public Note[] notes;

    public Notepad(int untitledNumber, JSONArray notes) {
        this.untitledNumber = untitledNumber;

        this.notes = new Note[notes.length()];
        for (int i = 0; i < notes.length(); i++) {
            JSONObject unparsedNote = notes.getJSONObject(i);
            this.notes[i] = new Note(unparsedNote.getString("name"), unparsedNote.getString("content"));
        }
    }
}
