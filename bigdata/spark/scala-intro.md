# Scala Intro

Install sdk

```sh
curl -s "https://get.sdkman.io" | bash
export SDKMAN_DIR="/usr/local/sdkman" && curl -s "https://get.sdkman.io" | bash
```
Install Scala 2.11.12
```sh
sdk install scala 2.11.12
```

## JAVA Scala Mix project

For Gradle:

```
apply plugin: 'java'
apply plugin: 'scala'
sourceSets.main.scala.srcDir "src/main/java"
sourceSets.test.scala.srcDir "src/test/java"
sourceSets.main.java.srcDirs = []
sourceSets.test.java.srcDirs = []
```

For Maven: http://davidb.github.io/scala-maven-plugin/example_java.html
