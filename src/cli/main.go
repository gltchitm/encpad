package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"github.com/gltchitm/encpad/cli/format"
	"golang.org/x/term"
)

func main() {
	path := flag.String("path", "", "the path to the .encpad file")
	indent := flag.Bool("indent", true, "whether or not to indent the output")
	formatVersion := flag.String("format", "v2", "the format version to use (v1 or v2)")

	flag.Parse()

	notepad, err := os.ReadFile(*path)
	if err != nil {
		panic(err)
	}

	print("Password: ")
	password, err := term.ReadPassword(int(os.Stdin.Fd()))
	if err != nil {
		panic(err)
	}

	println()

	var decrypted any

	switch *formatVersion {
	case "v1":
		decrypted = format.DecryptNotepadV1(notepad, password)
	case "v2":
		decrypted = format.DecryptNotepadV2(notepad, password)
	default:
		panic("Unknown format version!")
	}

	var output []byte

	if *indent {
		output, err = json.MarshalIndent(decrypted, "", "    ")
		if err != nil {
			panic(err)
		}
	} else {
		output, err = json.Marshal(decrypted)
		if err != nil {
			panic(err)
		}
	}

	fmt.Println(string(output))
}
