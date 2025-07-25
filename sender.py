from flask import Flask, Response
import cv2
import argparse

app = Flask(__name__)
cap = cv2.VideoCapture(0)  # 0번 웹캠

def generate():
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start webcam video stream server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host IP to run the server on")
    parser.add_argument("--port", type=int, default=8000, help="Port number to run the server on")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
