package format

import (
	"bytes"
	"encoding/json"

	"golang.org/x/crypto/argon2"
	"golang.org/x/crypto/chacha20poly1305"
)

const formatTagV2 = "encpad[2]"

type NotepadDataV2 struct {
	UntitledNumber int `json:"untitled_number"`
	Notes          []struct {
		Name    string `json:"name"`
		Content string `json:"content"`
	} `json:"notes"`
}

type DecodedNotepadV2 struct {
	Version string        `json:"version"`
	Brand   string        `json:"brand"`
	Data    NotepadDataV2 `json:"data"`
}

func readHeaderV2(buff *bytes.Buffer) string {
	header, err := buff.ReadBytes('\x00')
	if err != nil {
		panic(err)
	}

	return string(header[:len(header)-1])
}

const (
	argon2TimeV2    = 4
	argon2MemeoryV2 = 88064
	argon2ThreadsV2 = 3
	argon2KeyLenV2  = 32
)

func DecryptNotepadV2(notepad, password []byte) DecodedNotepadV2 {
	buff := bytes.NewBuffer(notepad)

	formatTag := readHeaderV2(buff)
	if string(formatTag) != formatTagV2 {
		panic("Format not supported!")
	}

	brand := readHeaderV2(buff)
	if len(brand) <= 2 || brand[0] != '[' || brand[len(brand)-1] != ']' {
		panic("Invalid brand!")
	}

	salt := make([]byte, 32)
	nonce := make([]byte, 24)
	ciphertextAndTag := make([]byte, buff.Len()-(32+24))

	_, err := buff.Read(salt)
	if err != nil {
		panic(err)
	}

	_, err = buff.Read(nonce)
	if err != nil {
		panic(err)
	}

	_, err = buff.Read(ciphertextAndTag)
	if err != nil {
		panic(err)
	}

	key := argon2.IDKey(password, salt, argon2TimeV2, argon2MemeoryV2, argon2ThreadsV2, argon2KeyLenV2)

	aead, err := chacha20poly1305.NewX(key)
	if err != nil {
		panic(err)
	}

	decryptedData, err := aead.Open(nil, nonce, ciphertextAndTag, nil)
	if err != nil {
		panic(err)
	}

	var notepadData NotepadDataV2
	err = json.Unmarshal(decryptedData, &notepadData)
	if err != nil {
		panic(err)
	}

	return DecodedNotepadV2{
		Version: "2",
		Brand:   string(brand[1 : len(brand)-1]),
		Data:    notepadData,
	}
}
