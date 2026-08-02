

import webview, uvicorn, threading, time, socket




def start_api():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="warning")

# start fastapi in the background
threading.Thread(target=start_api, daemon=True).start()


# انتظار حتى يصبح الخادم جاهزًا
while True:
    try:
        with socket.create_connection(("127.0.0.1", 8000), timeout=1):
            break
    except OSError:
        time.sleep(0.1)


webview.create_window(
    title="مواعيد الحجامة",
    url="http://127.0.0.1:8000",
    width=1200,
    height=800,
)

gui = "cef"
webview.start(gui=gui)