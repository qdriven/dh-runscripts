//TODO Dir exist
//Spider
//

package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"net"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

//https://github.com/arminc/clair-scanner
//https://github.com/coreos/clair
const (
	clairServer  = "http://127.0.0.1:8090"
	dockerServer = "http://127.0.0.1:800"
)

type Repository struct {
	ID           int    `json:"id"`
	Name         string `json:"name"`
	ProjectID    int    `json:"project_id"`
	Description  string `json:"description"`
	UpdateTime   string `json:"update_time"`
	CreationTime string `json:"creation_time"`
	PullCount    int    `json:"pull_count"`
}

type LayerResult struct {
	LayerName string    `json:"LayerName"`
	Features  []Feature `json:"Features"`
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

type Feature struct {
	Name            string          `json:"Name,omitempty"`
	NamespaceName   string          `json:"NamespaceName,omitempty"`
	VersionFormat   string          `json:"VersionFormat,omitempty"`
	Version         string          `json:"Version,omitempty"`
	Vulnerabilities []Vulnerability `json:"Vulnerabilities,omitempty"`
	AddedBy         string          `json:"AddedBy,omitempty"`
}

type Error struct {
	Message string `json:"Message,omitempty"`
}

type Layer struct {
	Name             string            `json:"Name"`
	Path             string            `json:"Path,omitempty"`
	ParentName       string            `json:"ParentName,omitempty"`
	Format           string            `json:"Format"`
	IndexedByBersion string            `json:"IndexedByBersion, omitempty"`
	Headers          map[string]string `json:"Headers, omitempty"`
	Features         []Feature         `json:"Features,omitempty"`
}

type LayerEnvelope struct {
	Layer *Layer `json:"Layer,omitempty"`
	Error *Error `json:"Error,omitempty"`
}

func loadManifestLayers(curDir, repoName string) ([]string, error) {
	fp, err := os.Open(fmt.Sprintf("%s/%s/manifest.json", curDir, repoName))
	if err != nil {
		panic(err)
	}
	defer fp.Close()

	type manifestItem struct {
		Config   string
		RepoTags []string
		Layers   []string
	}

	var manifest []manifestItem
	if err := json.NewDecoder(fp).Decode(&manifest); err != nil {
		panic(err)
	} else if len(manifest) != 1 {
		panic(err)
	}
	var layers []string
	for _, layer := range manifest[0].Layers {
		layers = append(layers, strings.TrimSuffix(layer, "/layer.tar"))
	}
	return layers, nil
}

func postLayer(repoName, layerName, parentLayerName string) error {
	data := LayerEnvelope{Layer: &Layer{
		Name:       layerName,
		Path:       fmt.Sprintf("%s/%s/%s/layer.tar", dockerServer, repoName, layerName),
		ParentName: parentLayerName,
		Format:     "docker"}}

	reqData, err := json.Marshal(data)
	if err != nil {
		return err
	}

	request, err := http.NewRequest("POST", fmt.Sprintf("%s/v1/layers", clairServer), bytes.NewBuffer(reqData))
	if err != nil {
		return err
	}

	request.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	response, err := client.Do(request)
	if err != nil {
		return err
	}
	defer response.Body.Close()

	if response.StatusCode != 201 {
	}

	return nil
 getLayer(layerName string) (LayerResult, error) {
	severityHigh := 0
	severityMidLow := 0
	var LR LayerResult

	response, err := http.Get(clairServer + fmt.Sprintf("/v1/layers/%s?vulnerabilities", layerName))
	if err != nil {
		return LayerResult{}, err
	}

	if response.StatusCode != 200 {
	}
	defer response.Body.Close()

	var apiResponse LayerEnvelope
	if err := json.NewDecoder(response.Body).Decode(&apiResponse); err != nil {
		return LayerResult{}, err
	} else if apiResponse.Error != nil {
		return LayerResult{}, errors.New(apiResponse.Error.Message)
	}

	for _, feature := range (*apiResponse.Layer).Features {
		if len(feature.Vulnerabilities) > 0 {
			LR.LayerName = layerName
			for _, vulnerability := range feature.Vulnerabilities {
				if severity := vulnerability.Severity; severity == "High" {
					severityHigh += 1
				} else {
					severityMidLow += 1
				}
				LR.Features = append(LR.Features, feature)
			}
		}
	}

	return LR, nil
}

func main() {
	repos, err := listAppRepos()
	if err != nil {
		panic(err)
	}

	for _, repo := range repos {
		if repo.PullCount > 0 {
			projName := strings.Split(repo.Name, "/")[0]
			repoName := strings.Split(repo.Name, "/")[1]
			tag := "master"
			if err := analyseRepo(projName, repoName, tag); err != nil {
				fmt.Println(fmt.Sprintf("Encountered %s when %s", err.Error(), repo.Name))
			}
		}
	}
}

func listAppRepos() ([]Repository, error) {
	var repos []Repository
	response, err := http.Get(DOCKER_BASE)
	if err != nil {
		return repos, err
	}

	if response.StatusCode != 200 {
	}

	if err := json.NewDecoder(response.Body).Decode(&repos); err != nil {
		return repos, err
	}
	defer response.Body.Close()

	return repos, nil
}

func listenHTTP(path, allowedHost string, ch chan error) {
	restrictedFileServer := func(path, allowedHost string) http.Handler {
		fc := func(w http.ResponseWriter, r *http.Request) {
			host, _, err := net.SplitHostPort(r.RemoteAddr)
			if err == nil && strings.EqualFold(host, allowedHost) {
				http.FileServer(http.Dir(path)).ServeHTTP(w, r)
				return
			}
			w.WriteHeader(403)
		}
		return http.HandlerFunc(fc)
	}
	ch <- http.ListenAndServe(":8080", restrictedFileServer(path, allowedHost))
}

func save(projName, repoName, tag string) error {
	err := os.Mkdir(repoName, os.ModeDir)
	if err != nil {
		return err
	}

	var stderr bytes.Buffer
	pull := exec.Command("docker", "pull", fmt.Sprintf("domain.com/%s/%s:%s", projName, repoName, tag))
	pull.Run()

	save := exec.Command("docker", "save", fmt.Sprintf("domain.com/%s/%s:%s", projName, repoName, tag))

	save.Stderr = &stderr

	extract := exec.Command("tar", "xf", "-", "-C"+repoName)
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

func analyseRepo(projName, repoName, tag string) error {
	if err := save(projName, repoName, tag); err != nil {
		return err
	}

	curDir, err := filepath.Abs(filepath.Dir(os.Args[0]))
	if err != nil {
		return err
	}
	/*
		ch := make(chan error)
		go listenHTTP(curDir, "127.0.0.1", ch)
		select {
		case <-ch:
		case <-time.After(10 * time.Second):
			break
		}
	*/

	layerNames, _ := loadManifestLayers(curDir, repoName)
	for index, _ := range layerNames {
		if index == 0 {
			postLayer(repoName, layerNames[index], "")
		} else {
			postLayer(repoName, layerNames[index], layerNames[index-1])
		}
	}
	layerResult, err := getLayer(layerNames[len(layerNames)-1])
	if err != nil {
		return err
	}

	if layerResult.LayerName != "" {
		layerResult.LayerName = filepath.Join(projName, repoName)
		data, err := json.Marshal(layerResult)
		if err != nil {
			return err
		}

		if err := ioutil.WriteFile(filepath.Join(curDir, "result", filepath.Join(projName, repoName)), data, 0644); err != nil {
			return err
		}

	}

	defer os.RemoveAll(filepath.Join(curDir, repoName))

	return nil
}
