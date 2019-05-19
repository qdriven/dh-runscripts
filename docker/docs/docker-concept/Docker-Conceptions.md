# Docker Conceptions

Here are Docker's Basic Conceptions:

1. Image
2. Contaniner
3. Repository

How to explain these three conceptions,take a look at follow picture:

![docker-conception.jpg]

## Image

Docker image is like a `root` file system, which support
running application. It is small,only neccessary components
in it.

And Docker store these files in different layers. It makes
easier to composite and change.

## Container

`image` and `container` is like the relationship between 
`class` and `instance`, image is a template, and container is an running template with states like running,stop,delted,pause, and also some variables for given instance.

## Repositories or Registry

Normally different docker containers running in different
machines, but in different machines, how to get the docker images to run the container? Obviously a maven repository like is needed, to store different categories of docker image with different versions. Yes, Docker repository is just like a MAVEN repository.


## Docker Image Command Cheatsheet

we already know the what docker images is. So some commands is easy to understand.

Docker Image Command:

- docker pull <image_name>
- docker image rm <image_name>
- docker image list
- docker image build
- docker image commit
- 