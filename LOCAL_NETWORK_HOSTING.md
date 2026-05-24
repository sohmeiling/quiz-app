# Local Network Hosting for the Quiz App

Use these steps when you want classmates or family members on the same Wi-Fi network to open your quiz from their own device.

This is only for a local network. It is not the same as publishing a real website on the internet.

## 1. Prepare the project

Open the `quiz-app` folder in VS Code or in your terminal.

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
python -m pip install -r requirements.txt
```

```bash
python db_scripts.py
```

### macOS

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
```

```bash
python db_scripts.py
```

The `db_scripts.py` command creates the quiz database. You only need to run it again if you want to reset the sample quiz data.

If you use the VS Code Run button, select the virtual environment interpreter first:

1. Press `Ctrl + Shift + P` on Windows or `Cmd + Shift + P` on macOS.
2. Search for `Python: Select Interpreter`.
3. Choose the interpreter inside the `.venv` folder.

On Windows, it should look similar to:

```text
.venv\Scripts\python.exe
```

On macOS, it should look similar to:

```text
.venv/bin/python
```

## 2. Allow other devices to connect

Open `quiz.py`.

At the bottom of the file, change:

```python
app.run()
```

to:

```python
app.run(host='0.0.0.0')
```

The address `0.0.0.0` tells Flask to listen for requests from other devices on the same local network.

## 3. Start the quiz server

In the `quiz-app` folder, run:

### Windows

If you opened a new terminal, turn on the virtual environment first:

```bash
.venv\Scripts\activate
```

```bash
python quiz.py
```

### macOS

If you opened a new terminal, turn on the virtual environment first:

```bash
source .venv/bin/activate
```

```bash
python quiz.py
```

Keep this terminal window open while people are using the quiz. To stop the server, press `Ctrl + C`.

If you see `ModuleNotFoundError: No module named 'flask'`, check that the virtual environment is turned on and that Flask has been installed.

## 4. Find your computer's IP address

Your IP address is the address other devices will type into their browser.

### Windows

Open Command Prompt and run:

```bash
ipconfig
```

Look for `IPv4 Address`.

### macOS

Open Terminal and run:

```bash
ipconfig getifaddr en0
```

If nothing appears, try:

```bash
ipconfig getifaddr en1
```

### Linux

Open Terminal and run:

```bash
hostname -I
```

Use the first IP address shown.

## 5. Open the quiz from another device

Make sure the other device is connected to the same Wi-Fi network.

In the browser on that device, type:

```text
http://YOUR-IP-ADDRESS:5000/
```

Example:

```text
http://192.168.1.55:5000/
```

The number `5000` is Flask's default port.

## Troubleshooting

- Check that both devices are on the same Wi-Fi network.
- Check that the Flask server is still running.
- If a firewall message appears, allow Python or Flask to accept incoming network connections.
- Make sure you typed `http://`, not `https://`.
- Make sure the URL includes `:5000` at the end of the IP address.

## After the activity

For normal solo testing, you can change the bottom of `quiz.py` back to:

```python
app.run()
```
