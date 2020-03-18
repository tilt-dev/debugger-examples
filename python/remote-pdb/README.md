# Run with Tilt, Debug wtih [`remote-pdb`](https://pypi.org/project/remote-pdb/)

To see `remote-pdb` in action:

1. Clone this repo and call `tilt up` to run the app
2. Hit `localhost:8000` to see the current behavior
3. To enable the debugger, uncomment the appropriate line in [app.py](https://github.com/windmilleng/debugger-examples/blob/master/python/remote-pdb/app.py)
4. Hit `localhost:8000` again; the request will hang because the app hit a breakpoint
5. In a separate terminal window, open a TCP connection to `localhost:5555`, e.g. via Netcat: `nc 127.0.0.1 5555`
6. Congrats, you've accessed the debugger! Poke around and inspect the system state. Type `c(ontinue)` to resume execution.
