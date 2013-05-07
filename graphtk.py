from Tkinter import *

class GraphTk(Canvas):
	def __init__(self, master=None, width=320, height=240, bg="#FFFFFF"):
		Canvas.__init__(self, master, width=width, height=height, bg=bg)
		
		self._xstart = 0.0
		self._xend = 1000.0
		self._xstep = 100.0
		self._xrng = self._xend - self._xstart
		
		self._ystart = 0.0
		self._yend = 1024.0
		self._ystep = 100
		self._yrng = self._yend - self._ystart
		
		self._graph_width = width - 80
		self._graph_height = height - 80
		self._graph_pos_x = 40
		self._graph_pos_y = 40
		
		self.set_x_axis(0.0, 1000.0)
		self.set_y_axis(0.0, 1024.0, 100)
		
		
		self._points = []
		
		
	def add_point(self, x, y):
		self._points.append((x, y))
		
		
	def clear_points(self):
		self._points = []
		
		
	def set_x_axis(self, xstart, xend, xstep=0):
		self._xstart = float(xstart)
		self._xend = float(xend)
		self._xrng = self._xend - self._xstart
		if xstep == 0:
			self._xstep = self._xrng/10.0
		else:
			self._xstep = float(xstep)
		
		
	def set_y_axis(self, ystart, yend, ystep=0):
		self._ystart = float(ystart)
		self._yend = float(yend)
		self._yrng = self._yend - self._ystart
		if ystep == 0:
			self._ystep = self._yrng/10.0
		else:
			self._ystep = float(ystep)
	
	
	def convertx(self, x):
		return ((float(x)-self._xstart)/self._xrng * self._graph_width) + self._graph_pos_x
		
		
	def converty(self, y):
		return (self._graph_height - ((float(y)-self._ystart)/self._yrng * self._graph_height)) + self._graph_pos_y
		
		
	def draw_x_axis(self):
		self.delete("x-axis")
		
		self.create_line(
			self._graph_pos_x, self._graph_pos_y + self._graph_height,
			self._graph_pos_x + self._graph_width , self._graph_pos_y + self._graph_height,
			tag="x-axis",
			fill="#000000")
			
		y = self._ystart
		yt = self.converty(y)
		for x in xrange(int(self._xstart),int(self._xend)+1,int(self._xstep)):
			xt = self.convertx(x)
			self.create_line(
				xt, yt,
				xt, yt+5,
				tag="x-axis")
			self.create_text(
				xt, yt+5, 
				#text=str(round(float(x)/1000.0,1)),
				text=x,  
				anchor=N,  
				font='Helvetica 8',
				tag="x-axis")
				
				
	def draw_y_axis(self):
		self.delete("y-axis")
		
		self.create_line(
			self._graph_pos_x, self._graph_pos_y + self._graph_height,
			self._graph_pos_x, self._graph_pos_y,
			tag="y-axis",
			fill="#000000")
			
		x = self._xstart
		xt = self.convertx(x)
		for y in xrange(int(self._ystart),int(self._yend)+1,int(self._ystep)):
			yt = self.converty(y)
			self.create_line(
				xt, yt,
				xt-4, yt,
				tag="y-axis")
			self.create_text(
				xt-4, yt, 
				text=str(y), 
				anchor=E,  
				font='Helvetica 8',
				tag="y-axis")
				
				
	def draw_graph(self):
		if len(self._points) == 1:
			self.delete("line")
			x, y = self._points[0]
			xt = self.convertx(x)
			yt = self.converty(y)
			
			self.create_line(
				xt, yt,
				xt, yt+1,
				tag="line" )
				
		elif len(self._points) > 1:
			self.delete("line")
			first = True
			
			for point in self._points:
				x, y = point
				xt = self.convertx(x)
				yt = self.converty(y)
				if first:
					first = False
					prev_xt = xt
					prev_yt = yt
				else:
					self.create_line(
						xt, yt,
						prev_xt, prev_yt,
						tag="line" )
					prev_xt = xt
					prev_yt = yt
						
						
	def draw(self):
		self.draw_x_axis()
		self.draw_y_axis()
		self.draw_graph()
	
	
	
	
def main():
	app = GraphTk()
	app.grid(column=0, row=0)
	
	app.set_x_axis(-300, 300,100)
	app.set_y_axis(-600, 600,300)
	
	app.add_point(-300, 600)
	app.add_point(-200, 130)
	app.add_point(-100, 50)
	app.add_point(0, -100)
	app.add_point(100, -50)
	app.add_point(200, -130)
	app.add_point(300, -600)
	app.draw()
	
	app.master.title("graphtk")
	app.mainloop()


if __name__ == '__main__' :
	main()
		
		
		
		
		
		
