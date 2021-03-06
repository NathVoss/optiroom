from flask import Flask
from flask import abort
from flask import jsonify
from flask_mysqldb import MySQL
from flask_restplus import Resource, Api
import socket

app = Flask(__name__)
api = Api(app)

mysql = MySQL()
app.config['MYSQL_HOST'] = 'dev.optiroom.net'
app.config['MYSQL_USER'] = 'opti_api'
app.config['MYSQL_PASSWORD'] = 'YFdcxYJS:ng3PcvndfGeIeRxhuOYiP'
app.config['MYSQL_DB'] = 'optiroom'
mysql.init_app(app)

@api.route('/system')
class System(Resource):
    def get(self):
        return {'state': 'up','version': '0.1.7', 'motd': 'N/A'}

@api.route('/test')
class System(Resource):
    def get(self):

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM opti_building")
        row = cur.fetchone()
        if row:
            return {'state': row[1]}
        else:
            return {'state': 'Username and/or password incorrect.'}


@api.route('/motd')
class System(Resource):
    def get(self):
        return {'motd': 'N/A'}

@api.route('/rooms')
class Rooms(Resource):
    def get(self):
        rooms = []
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM get_rooms")
        for row in cur:
            room = {
            'building_id': row[0],
            'building_name': row[1],
            'room_id': row[2],
            'floorNum': row[3],
            'roomType': row[4],
            'roomDescription': row[5]}
            rooms.append(room)
        return jsonify(rooms)

@api.route('/rooms/full')
class Rooms(Resource):
    def get(self):
        rooms = []
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM get_roomsFull")
        for row in cur:
            room = {
            'building_id': row[0],
            'building_name': row[1],
            'room_id': row[2],
            'floorNum': row[3],
            'roomType': row[4],
            'roomDescription': row[5],
            'nbPlace': row[6],
            'hasSpeaker': row[7],
            'hasProjector': row[8]}
            rooms.append(room)
        return jsonify(rooms)

@api.route('/room/<string:room_id>')
class Room(Resource):
    def get(self, room_id):
        if room_id == 'A10':
            return {'A10': {'numFloor': '0','idBuilding': '1','typeRoom': '1', 'opti_light': 'avaliable', 'opti_heat': 'avaliable', 'nbSeats': '250', 'projector' : 'true', 'soundSystem': 'true'}}
        elif room_id == 'L04':
            return {'L04': {'numFloor': '0','idBuilding': '1', 'typeRoom': '2', 'opti_light': 'false', 'opti_heat': 'avaliable', 'nbSeats': '70', 'projector' : 'true', 'soundSystem': 'false'}}
        else:
        	return {'error':'Invalid room number'}, 404

@api.route('/state/<string:room_id>')
class Room(Resource):
    def get(self, room_id):
        if room_id == 'A10':
            return {'A10': {'state': 'busy'}}
        elif room_id == 'L04':
            return {'L04': {'state': 'available'}}
        else:
        	return {'error':'Invalid room number'}, 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
