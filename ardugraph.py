from Tkinter import *
import tkMessageBox
from availableserialports import *
from ardulog import *
from graphtk import *
import serial

class Ardugraph(Frame):
	def __init__(self, master=None):
		self._refresh_interval = 1
		
		Frame.__init__(self, master)
		
		self.create_widgets()

		self._logger_started = False
		
		self._graph = []
		self._graph_time_range = 1000
		
		
	def create_widgets(self):
		self.bt_toggle = Button(self, text='Start', command=self.toggle_logger)
		
		avialable_ports = AvailableSerialPorts()
		if len(avialable_ports) == 0:
			tkMessageBox.showerror(
				"Arduino Logger",
				"No Serial Ports were found, Cannot continue")
			exit()
		self.var_serialport = StringVar()
		self.var_serialport.set(avialable_ports[0])
		self.om_serialport = OptionMenu(self,self.var_serialport,*avialable_ports)
		
		available_speeds = serial.Serial.BAUDRATES
		self.var_serialspeed = StringVar()
		self.var_serialspeed.set(9600)
		self.om_serialspeed = OptionMenu(self,self.var_serialspeed,*available_speeds)
		
		self.bt_quit = Button(self, text='Quit', command=self.quit)
		
		self.var_save_log = IntVar()
		self.var_save_log.set(0)
		self.ck_save_log = Checkbutton(self, text='Log to', variable=self.var_save_log)
		
		self.var_dbfile = StringVar()
		self.var_dbfile.set('log.db')
		self.en_db = Entry(self, textvariable=self.var_dbfile)
		
		self.graph = GraphTk(self, width=320, height=240, bg="#FFFFFF")
		
		self.status_bar = Label(self, text="")
		
		top=self.winfo_toplevel()
		top.columnconfigure(0, weight=1)
		top.rowconfigure(0, weight=1)
		self.rowconfigure(2, weight=1)
		self.columnconfigure(1, weight=1)
		
		self.bt_toggle.grid(row=0, column=0, sticky=N+S+E+W)
		self.om_serialport.grid(row=0,column=1,sticky=N+S+E+W)
		self.om_serialspeed.grid(row=0,column=2,sticky=N+S+E+W)
		self.bt_quit.grid(row=0,column=3,sticky=N+S+E+W)
		self.ck_save_log.grid(row=1,column=0,sticky=N+S+E+W)
		self.en_db.grid(row=1,column=1,columnspan=3,sticky=N+S+E+W)
		self.graph.grid(row=2,column=0,columnspan=4)
		self.status_bar.grid(row=3,column=0,columnspan=4,sticky=N+S+E+W)
		
		
	def toggle_logger(self):
		if self._logger_started:
			self.stop()
			self.bt_toggle['text'] = "Start"
		else:
			self.start()
			self.bt_toggle['text'] = "Stop"
		
		
	def start(self):
		if self.var_save_log.get() == 0:
			print "run without logging"
			self._logger = Ardulog(
				port=self.var_serialport.get(),
				speed=self.var_serialspeed.get() )
		else:
			print "run with logging"
			self._logger = Ardulog(
				port=self.var_serialport.get(),
				speed=self.var_serialspeed.get(),
				savetodb=True,
				dbfile=self.var_dbfile.get(),
				dbtable=time.strftime("log_%Y%m%d%H%M%S") )
		self._logger.start()
		self._logger_started = True
		
		self.om_serialport['state'] = DISABLED
		self.om_serialspeed['state'] = DISABLED
		self.ck_save_log['state'] = DISABLED
		self.en_db['state'] = DISABLED
		
		self.refresh()
		
		
	def stop(self):
		self._logger.stop()
		self._logger_started = False
		
		self.om_serialport['state'] = NORMAL
		self.om_serialspeed['state'] = NORMAL
		self.ck_save_log['state'] = NORMAL
		self.en_db['state'] = NORMAL
		
		
	def refresh(self):
		if self._logger_started:
			rows = self._logger.get_log_list()
			
			if len(rows) > 1:
				self.graph.clear_points()
				
				xend, yend = rows[len(rows)-1]
				xstart = xend - self._graph_time_range
				
				self.graph.set_x_axis(xstart, xend)
				self.graph.set_y_axis(0, 1024.0, 200.0)
				
				for row in rows:
					time, value = row
					if time >= xstart:
						self.graph.add_point(time, value)
						
				self.graph.draw_y_axis()
				self.graph.draw_graph()

			self.after(self._refresh_interval,self.refresh)

	
	def quit(self):
		if self._logger_started:
			self.stop()
			
		Frame.quit(self)
		
		
		
		
def main():
	app = Ardugraph()
	app.grid(sticky=N+S+E+W)
	
	app.master.title("Ardugraph")
	app.mainloop()


if __name__ == '__main__' :
	main()
			
