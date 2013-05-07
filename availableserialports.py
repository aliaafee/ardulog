import os

def AvailableSerialPorts():
	available = []
	if os.path.isdir("/dev/serial/by-path"):
		filelist = os.listdir("/dev/serial/by-path")
		for s in filelist:
			available.append(os.path.join(os.path.dirname("/dev/"), os.path.basename(os.readlink("/dev/serial/by-path/"+s))))
	return available


if __name__=='__main__':
    for s in AvailableSerialPorts():
        print s + "\n"
