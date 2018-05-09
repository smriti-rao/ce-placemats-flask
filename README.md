## Using the image
### Building and running
Add the following aliases to your current shell (or add it to your .bashrc/.bash_profile to include in every shell):

`alias buildCePlacemats='docker build -t ce-placemats .'`

`alias runCePlacemats='docker run --rm -d -p 8080:80 ce-placemats'`

`alias buildAndRunCePlacemats='buildCePlacemats && runCePlacemats'`

To build and run the image, simply run `buildAndRunCePlacemats`.

### Terminate it
Find it using `docker ps | grep ce-placemats` and then `docker kill 
<ce-placemats container-id>`