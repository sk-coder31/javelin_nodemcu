from flask import Flask, render_template, request
import socket
import json

app = Flask(__name__)

def receive_data_from_nodemcu(server_ip, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    server_address = (server_ip, port)
    print(f"Connecting to {server_address[0]}:{server_address[1]}")

    try:

        sock.connect(server_address)
        print("Connected to server")

        data = sock.recv(1024)
        data_dict = json.loads(data.decode('utf-8'))
        incoming_data = data_dict['jav_data']
        time_of_flight = incoming_data['tof']
        angle = incoming_data['angle']
        velocity = incoming_data['velocity']
        distance = incoming_data['distance']
        pressure = incoming_data['pressure']
        ans = [time_of_flight, angle, velocity, distance, pressure]

        print(f"Time of Flight={time_of_flight}")
        print(f"Angle Thrown={angle}")
        print(f"Velocity Thrown={velocity}")
        print(f"Distance Covered={distance}")
        print(f"Pressure={pressure}")
        return ans

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:

        print("Closing connection")
        sock.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        server_ip = request.form['server_ip']
        port = int(request.form['port'])
        data = receive_data_from_nodemcu(server_ip, port)
        return render_template('index.html', data=data)
    return render_template('index.html', data=None)

if __name__ == '__main__':
    app.run(debug=True)
