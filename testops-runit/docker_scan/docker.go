package main

import (
	"bytes"
	"errors"
	"fmt"
	"os/exec"
)

func save() error {
	var stderr bytes.Buffer
	pull := exec.Command("docker", "pull", fmt.Sprintf("ocean-hub.bkjk-inc.com/bkjk/%s", "uus-uus:master"))
	pull.Run()

	save := exec.Command("docker", "save", fmt.Sprintf("ocean-hub.bkjk-inc.com/bkjk/%s", "uus-uus:master"))

	save.Stderr = &stderr

	extract := exec.Command("tar", "xf", "-")
	extract.Stderr = &stderr
	pipe, err := extract.StdinPipe()
	if err != nil {
		return err
	}
	save.Stdout = pipe
	err = extract.Start()
	if err != nil {
		return errors.New(stderr.String())
	}
	err = save.Run()
	if err != nil {
		return errors.New(stderr.String())
	}
	err = pipe.Close()
	if err != nil {
		return err
	}
	err = extract.Wait()
	if err != nil {
		return errors.New(stderr.String())
	}

	return nil
}
