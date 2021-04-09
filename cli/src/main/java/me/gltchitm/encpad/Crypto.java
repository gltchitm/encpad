package me.gltchitm.encpad;

import java.security.GeneralSecurityException;
import java.security.spec.KeySpec;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

import org.json.JSONObject;

public class Crypto {
    private static SecretKey pbkdf2Hmac(String password, byte[] salt) throws GeneralSecurityException {
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA512");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 500_000, 256);
        return new SecretKeySpec(factory.generateSecret(spec).getEncoded(), "AES");
    }
    public static String decrypt(String encryptedString, String password) {
        try {
            JSONObject encrypted = new JSONObject(new String(Base64Util.decode(encryptedString)));
            byte[] cipherText = Base64Util.decode(encrypted.getString("cipher_text"));
            byte[] salt = encrypted.getString("salt").getBytes();
            byte[] iv = encrypted.getString("iv").getBytes();

            SecretKey key = Crypto.pbkdf2Hmac(password, salt);
            Cipher cipher = Cipher.getInstance("AES/CBC/NoPadding");
            cipher.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv));

            return new String(cipher.doFinal(cipherText));
        } catch (GeneralSecurityException exception) {
            return null;
        }
    }
}
