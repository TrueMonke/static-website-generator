# static-website-generator
 
## Description

Allows you to create static sites by writing them in markdown rather than HTML.

Creates a public directory and copies over the content directory files over. 
Converts any markdown files `.md` into HTML files `.html` when copying.

Project idea is from the boot.dev guided project lesson `static site generator` which can be found at:

https://www.boot.dev/learn/build-static-site-generator

## How to use

1. place required static site files into the content directory, including markdown files to be converted
2. run main.sh to generate the public directory based on the content directory
3. run start_server.sh to launch a simple http server and see the results
