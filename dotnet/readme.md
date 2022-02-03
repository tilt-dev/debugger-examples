# Debugging C# in VS Code with Tilt

## Prerequisites
- Docker Desktop with Kubernetes enabled
- Tilt
- kubectl 
- VS Code

## To Run this example
1. Run `tilt up` - this should build the sample project docker image and launch it in tilt
1. In VS Code, go to 'Run and Debug', and select 'K8s Attach'
1. Press F5 or the green arrow.
1. Set a breakpoint in the WeatherForecastController's `Get` method.
1. Go to `localhost:5555/weatherforecast`. your breakpoint should get hit

## Project Setup
There's a few steps to set your project up for debugging. Essentially you are "remote" debugging into the container inside a Kubernetes pod.
### Docker file
You'll need to have your project built with the debug symbols included as well as having the dotnet debugger installed in your container. One option would be to create a second docker file (e.g. `Docker-dev`) so that you can reserve the regular `Dockerfile` for CI/CD builds, etc.

This assumes that you are using the 'standard' multi-stage Dockerfile provided by microsoft. (See the Dockerfile in this repo for an example)

1. Set the build commands to use the `Debug` configuration in your Dockerfile.
   - ```
     # Example:
     RUN dotnet build "dotnet-api.csproj" -c Debug -o /app/build

     RUN dotnet publish "dotnet-api.csproj" -c Debug -o /app/publish
     ```
1. Install the dotnet debugger in your container
    - ```
      RUN apt update
      RUN apt install -y curl unzip procps
      RUN curl -sSL https://aka.ms/getvsdbgsh | bash /dev/stdin -v latest -l /vsdbg
      ```

### launch.json
The launch.json file in the .vscode folder uses `kubectl` to connect VS Code to the debugger running in your container.

1. copy the following in to the launch.json file
    - ```
      {
            "name": "K8s Attach",
            "type": "coreclr",
            "request": "attach",
            "processId": 1,
            "justMyCode": true,
            "pipeTransport": {
                "pipeProgram": "kubectl",
                "pipeArgs": [
                    "exec",
                    "-i",
                    "deploy/dotnet-api",
                    "--"
                ],
                "pipeCwd": "${workspaceFolder}",
                "debuggerPath": "/vsdbg/vsdbg",
                "quoteArgs": false
            },
            "sourceFileMap": {
                // update these directories to match your code base
                "/src": "${workspaceFolder}/src",
                "/app": "${workspaceFolder}/src/dotnet-api"
            }
        }
        ```
1. You may need to update the `sourceFileMap` field to match the folder stucture of your project. `/src` is the overall folder of your source code, and `/app` points to the program you are debugging

### Tiltfile
Make sure the docker builds defined in your tilt file point to the dev version of your dockerfile so that they will be built with the debug symbols included.