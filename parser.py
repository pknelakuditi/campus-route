import MySQLdb
import math

def main():
	count = 0
	db = MySQLdb.connect(host = "localhost", user = "root", passwd = "pavan", db = "project")
	db.autocommit(True)
	f = open('iitkgp.gml','r')
	cursor=db.cursor()
	cursor2=db.cursor()
	for line in f:
		count = count + 1
		if line.find("gml:pos")!=-1:
			p = line.split(">")
			p1 = p[1].split("<")
			x,y = p1[0].split()
		if line.find("name")!=-1:
			p = line.split(">")
			p1 = p[1].split("<")
			name = p1[0].split()
			if name:
				st=" "
				name1 =  st.join(name)
		if line.find("type")!=-1:
			p = line.split(">")
			p1 = p[1].split("<")
			types = p1[0].split()
			if types:
				st=" "
				type1 = st.join(types)
		if line.find("loc_id")!=-1:
			p = line.split(">")
			p1 = p[1].split("<")
			loc_id = p1[0].split()
		if line.find("</location>")!=-1:
			p = cursor.execute("SELECT * FROM nodes where x='"+ str(x) + "' and y = '"+ str(y) + "'")
			if p ==0:
				cursor.execute("INSERT IGNORE INTO `gis_dummy`.`nodes` (x,y) VALUES ('"+str(x)+"','"+str(y)+"');")
			if name and types and loc_id:
				cursor2.execute("SELECT node_id FROM `nodes` WHERE x="+str(x)+" and y="+str(y))
				node_id = cursor2.fetchone()
				cursor.execute("INSERT IGNORE into gis_dummy.locations (loc_id,node_id,name,type) VALUES ( '"+str(loc_id[0])+"' , '"+str(node_id[0])+"' , '"+name1+"' , '"+type1+ "' ); ")
		if line.find("coordinates")!=-1:
			p = line.split(">")
			p1 = p[1].split("<")
			p2 = p1[0].split(' ')
			if (len(p2) == 2):
				x1 = p2[0].split(",")
				x2 = p2[1].split(",")
				if len(x1)==2 and len(x2)==2:
					cursor2.execute("SELECT node_id FROM nodes WHERE x="+str(x1[0])+" and y="+str(x1[1]))
					start = cursor2.fetchone()
					cursor2.execute("SELECT node_id FROM nodes WHERE x="+str(x2[0])+" and y="+str(x2[1]))
					end = cursor2.fetchone()
					dist = math.sqrt((float(x1[0])-float(x2[0]))**2 + (float(x1[1])-float(x2[1]))**2)
					cursor.execute("INSERT IGNORE into gis_dummy.lanes (start,end,length) VALUES ( '"+str(start[0])+"' , '"+str(end[0])+"' , '"+str(dist)+"' ); ")
					
if __name__ == '__main__':
	main()
