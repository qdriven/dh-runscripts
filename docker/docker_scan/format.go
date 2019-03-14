package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
)

type Feature struct {
	Name            string          `json:"Name,omitempty"`
	NamespaceName   string          `json:"NamespaceName,omitempty"`
	VersionFormat   string          `json:"VersionFormat,omitempty"`
	Version         string          `json:"Version,omitempty"`
	Vulnerabilities []Vulnerability `json:"Vulnerabilities,omitempty"`
	AddedBy         string          `json:"AddedBy,omitempty"`
}

type Vulnerability struct {
	Name          string                 `json:"Name,omitempty"`
	NamespaceName string                 `json:"NamespaceName,omitempty"`
	Description   string                 `json:"Description,omitempty"`
	Link          string                 `json:"Link,omitempty"`
	Severity      string                 `json:"Severity,omitempty"`
	Metadata      map[string]interface{} `json:"Metadata,omitempty"`
	FixedBy       string                 `json:"FixedBy,omitempty"`
	FixedIn       []Feature              `json:"FixedIn,omitempty"`
}

type Ray struct {
	LayerName string    `json:"LayerName"`
	Features  []Feature `json:"Features"`
}

func dumpUsefulInfo(fileName string) {
	content, err := ioutil.ReadFile(fileName)
	if err != nil {
		panic(err)
	}

	var r Ray
	if err := json.Unmarshal(content, &r); err != nil {
		panic(err)
	}

	fmt.Println(r.LayerName)
	var data string

	for _, feature := range r.Features {
		ver := strings.Split(feature.Version, ":")
		Fver := strings.Split(feature.Vulnerabilities[0].FixedBy, ":")

		data += "FeatureName: " + feature.Name + "\n"
		data += "Severity: " + feature.Vulnerabilities[0].Severity + "\n"
		data += "CurrentVersion: " + ver[len(ver)-1] + "\n"
		data += "FixedBy: " + Fver[len(Fver)-1] + "\n"
		data += "Link: " + feature.Vulnerabilities[0].Link + "\n\n"
	}

	b := []byte(data)
	err = ioutil.WriteFile(fileName, b, 0644)
}

func main() {
	//dumpUsefulInfo("/tmp/result/bkjk/addr-svc.bak")
	fp, err := os.Open("/tmp/result/bkjk")
	if err != nil {
		panic(err)
	}

	files, err := fp.Readdir(0)
	if err != nil {
		panic(err)
	}

	for _, file := range files {
		fmt.Println("dumping...", file.Name())
		dumpUsefulInfo(filepath.Join("/tmp/result/docerkscan", file.Name()))
	}

}
