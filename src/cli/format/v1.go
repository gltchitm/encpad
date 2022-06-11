package format

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/hmac"
	"crypto/sha256"
	"crypto/sha512"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"strings"

	"golang.org/x/crypto/pbkdf2"
)

const disclaimerV1 = `[DANGER]
This file is ENCRYPTED. It must be opened in Encpad (or a compatible editor/viewer)!
Do NOT edit this file in a normal text editor -- doing so may cause permanent data loss!
-=-=-=-=-=-=-=-=-=-=-=-
`
const versionV1 = "0.1.0-beta"

type notesV1 []struct {
	Name    string `json:"name"`
	Content string `json:"content"`
}

type DecodedNotepadV1 struct {
	Version        string  `json:"version"`
	UntitledNumber int     `json:"untitled_number"`
	Notes          notesV1 `json:"notes"`
}

type notepadDataV1 struct {
	Version        string `json:"version"`
	UntitledNumber int    `json:"untitled_number"`
	Notes          string `json:"notes"`
}

type notesEncryptionDataV1 struct {
	Salt       string `json:"salt"`
	Iv         string `json:"iv"`
	Ciphertext string `json:"cipher_text"`
	Hmac       string `json:"hmac"`
}

const (
	pbkdf2IterV1   = 500_000
	pbkdf2KeyLenV1 = 32
)

func decodeBase64V1(encodedData []byte) []byte {
	strippedEncodedData := []byte(strings.TrimRight(string(encodedData), "="))

	decodedData := make([]byte, base64.RawStdEncoding.DecodedLen(len(strippedEncodedData)))
	_, err := base64.RawStdEncoding.Decode(decodedData, strippedEncodedData)
	if err != nil {
		panic(err)
	}

	return decodedData
}

func DecryptNotepadV1(notepad, password []byte) DecodedNotepadV1 {
	buff := bytes.NewBuffer(notepad)

	disclaimer := make([]byte, len(disclaimerV1))
	_, err := buff.Read(disclaimer)
	if err != nil {
		panic(err)
	}

	if string(disclaimer) != disclaimerV1 {
		panic("Malformed notepad!")
	}

	encodedNotepadData := make([]byte, buff.Len())
	_, err = buff.Read(encodedNotepadData)
	if err != nil {
		panic(err)
	}

	decodedNotepadData := decodeBase64V1(encodedNotepadData)

	var notepadData notepadDataV1
	err = json.Unmarshal(decodedNotepadData, &notepadData)
	if err != nil {
		panic(err)
	}

	if notepadData.Version != versionV1 {
		panic("Unsupported version!")
	}

	decodedNotesEncryptionData := decodeBase64V1([]byte(notepadData.Notes))

	var notesEncryptionData notesEncryptionDataV1
	err = json.Unmarshal(decodedNotesEncryptionData, &notesEncryptionData)
	if err != nil {
		panic(err)
	}

	salt := []byte(notesEncryptionData.Salt)
	iv := []byte(notesEncryptionData.Iv)
	ciphertext := decodeBase64V1([]byte(notesEncryptionData.Ciphertext))

	expectedHmac, err := hex.DecodeString(notesEncryptionData.Hmac)
	if err != nil {
		panic(err)
	}

	key := pbkdf2.Key(password, salt, pbkdf2IterV1, pbkdf2KeyLenV1, sha512.New)

	blockCipher, err := aes.NewCipher(key)
	if err != nil {
		panic(err)
	}

	cbc := cipher.NewCBCDecrypter(blockCipher, iv)
	decryptedNotes := make([]byte, len(ciphertext))
	cbc.CryptBlocks(decryptedNotes, ciphertext)

	notes := []byte(strings.TrimRight(string(decryptedNotes), " "))

	hash := hmac.New(sha256.New, key)
	hash.Write(notes)

	if !hmac.Equal(hash.Sum(nil), expectedHmac) {
		panic("HMAC mismatch!")
	}

	var parsedNotes notesV1
	err = json.Unmarshal(notes, &parsedNotes)
	if err != nil {
		panic(err)
	}

	return DecodedNotepadV1{
		Version:        "1",
		UntitledNumber: notepadData.UntitledNumber,
		Notes:          parsedNotes,
	}
}