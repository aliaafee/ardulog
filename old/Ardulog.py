import serial, time, threading, sqlite3




class Arduolog(threading.Thread):
	def __init__(self, port='', speed=9600, dbfile="log.db"):
		self._port = port
		self._speed = speed
		self._timeout = 5
		
		self._dbfile = dbfile
		
		self._connected = False
		
		self._current_time = 0
		threading.Thread.__init__(self)
		
		self.dbread = sqlite3.connect(self._dbfile)

		
	def get_log(self, duration=0):
		if not self._connected:
			return ""
	
		if duration > 0:
			print self._current_time
			start = self._current_time - duration
			end = self._current_time
			
			result = self.dbread.execute(
				"SELECT * FROM log WHERE time >= ?",
				(start,) )
		else:
			result = self.dbread.execute(
				"SELECT * FROM log")

		return result
		
		
	def run(self):
		try:
			ser = serial.Serial(
				self._port,
				self._speed,
				timeout = self._timeout)
			ser.open()
			self._connected = True
			print "Serial Connected"
		except serial.SerialException, e:
			return False
			
		try:
			dbconn = sqlite3.connect(self._dbfile)
			dbconn.execute(
				"CREATE TABLE log (time INTEGER, value REAL)")
			dbconn.commit()
			print "DB Connected"
		except serial.DatabaseError, e:
			return False
			
		try:
			while self._connected:
				line = ser.readline(1024)
				line = line.split(",")
				if len(line) > 1:
					if line[0] == 'LOG':
						time = int(line[1])
						value = float(line[2])
						self._current_time = time
						dbconn.execute(
							"INSERT INTO log VALUES (?,?)",
							(time, value) )
						dbconn.commit()
		except serial.DatabaseError, e:
			self._connected = False
			dbconn.close()
			ser.close()
			print "Db error, conn closed"
			return False
		except serial.SerialException, e:
			self._connected = False
			dbconn.close()
			ser.close()
			print "Serial error, conn closed"
			return False
			
		self._connected = False
		self.close_serial()
		dbconn.close()
		print "Closed"
	
	
	def stop(self):
		self._connected = False
		
		
		
		
def main():
	logger = Arduolog('/dev/ttyUSB0', 9600)
	logger.start()
	print "logger started"
	
	while True:
		rows = logger.get_log(100)
		#time.sleep(1)
		print "reading"
		for row in rows:
			print row
		time.sleep(5)
		
		
if __name__ == '__main__' :
	main()
		
