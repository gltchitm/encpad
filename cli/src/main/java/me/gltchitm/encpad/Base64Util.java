package me.gltchitm.encpad;

import java.util.Base64;

public class Base64Util {
    public static byte[] decode(String encodedText) {
        return Base64.getDecoder().decode(encodedText.getBytes());
    }
}
