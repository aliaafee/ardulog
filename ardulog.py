import serial, time, threading, sqlite3




class Ardulog(threading.Thread):
	def __init__(self, port='', speed=9600, dbfile="log.db", dbtable='log', savetodb = False):
		self._port = port
		self._speed = speed
		self._timeout = 5
		
		self._savetodb = savetodb
		self._dbfile = dbfile
		self._dbtable = dbtable
		
		self._connected = False
		
		self._current_time = 0
		threading.Thread.__init__(self)
		
		self.log_list = []
		self.log_list_max = 1000


	def settings(self,port, speed, dbfile, dbtable='log'):
		self._port = port
		self._speed = speed
		self._dbfile = dbfile
		self._dbtable = dbtable
		
	'''
	def get_log(self, duration=0):
		if not self._connected:
			return ""
			
		if duration > 0:
			start = self._current_time - duration
			end = self._current_time
			
			result = self.dbread.execute(
				"SELECT * FROM "+self._dbtable+" WHERE time >= ?",
				(start,) )
		else:
			result = self.dbread.execute(
				"SELECT * FROM "+self._dbtable)

		return result
	'''	
	
	def get_log_list(self):
		return self.log_list
		
	def run_witout_logging(self):
		try:
			ser = serial.Serial(
				self._port,
				self._speed,
				timeout = self._timeout)
			ser.open()
			print "Serial Connected"
		except serial.SerialException, e:
			print "Serial Connection Error"
			return False
			
		self._connected = True
		
		try:
			while self._connected:
				line = ser.readline(1024)
				if line != "":
					line = line.split(",")
					if len(line) == 3:
						if line[0] == 'LOG' and line[1] != '' and line[2] != '':
							try:
								time = int(line[1])
								value = float(line[2])
								self._current_time = time
								#save to list
								self.log_list.append((time, value))
								if len(self.log_list) > 1000:
									del(self.log_list[0])
							except ValueError, e:
								print e
								print (line[1], line[2])
		except serial.SerialException, e:
			self._connected = False
			ser.close()
			print "Serial error, conn closed"
			return False
			
		self._connected = False
		ser.close()
		print "Closed"
		
		
	def run_with_logging(self):
		try:
			ser = serial.Serial(
				self._port,
				self._speed,
				timeout = self._timeout)
			ser.open()
			print "Serial Connected"
		except serial.SerialException, e:
			print "Serial Connection Error"
			return False
			
		try:
			dbconn = sqlite3.connect(self._dbfile)
			dbconn.execute(
				"CREATE TABLE IF NOT EXISTS "+self._dbtable+" (time INTEGER, value REAL)")
			dbconn.commit()
			print "DB Connected"
		except sqlite3.DatabaseError, e:
			print "Db Connection Error"
			return False
			
		self._connected = True
			
		try:
			while self._connected:
				line = ser.readline(1024)
				if line != "":
					line = line.split(",")
					if len(line) == 3:
						if line[0] == 'LOG' and line[1] != '' and line[2] != '':
							try:
								time = int(line[1])
								value = float(line[2])
								self._current_time = time
								#save to db
								if self._savetodb:
									dbconn.execute(
										"INSERT INTO "+self._dbtable+" VALUES (?,?)",
										(time, value) )
									dbconn.commit()
								#save to list
								self.log_list.append((time, value))
								if len(self.log_list) > 1000:
									del(self.log_list[0])
							except ValueError, e:
								print e
								print (line[1], line[2])
		except sqlite3.DatabaseError, e:
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
		ser.close()
		dbconn.close()
		print "Closed"
		
		
	def run(self):
		if self._savetodb:
			self.run_with_logging()
		else:
			self.run_witout_logging()
	
	
	def start(self):
		#self.dbread = sqlite3.connect(self._dbfile)
		threading.Thread.start(self)
		
		
	def stop(self):
		self._connected = False
		#self.dbread.close()
		
		
		
		
def main():
	logger = Ardulog('/dev/ttyUSB0', 9600)
	logger.start()
	print "logger started"
	
	while True:
		rows = logger.get_log(500)
		#time.sleep(1)
		print "reading"
		for row in rows:
			print row
		time.sleep(5)
		
		
if __name__ == '__main__' :
	main()
		
