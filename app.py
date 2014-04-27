from Tkinter import *
import ImageTk
import Image
import tkSimpleDialog
import tkMessageBox

from finder import Finder

class RouteDialog(tkSimpleDialog.Dialog):
    def body(self,master):
        self.sourceTxt = Entry(master)
        Label(master,text = "Enter Source").grid(row = 0, column = 0)
        self.sourceTxt.grid(row = 0, column = 1)
        Label(master,text = "Enter Destination").grid(row = 1, column = 0)
        self.destTxt = Entry(master)
        self.destTxt.grid(row= 1, column = 1)

    def apply(self):
        self.source = self.sourceTxt.get()
        self.dest = self.destTxt.get()

class NeighbourDialog(tkSimpleDialog.Dialog):
    def body(self,master):
        self.sourceTxt = Entry(master)
        Label(master, text = "Enter source").grid(row = 0, column = 0)
        self.sourceTxt.grid(row = 0, column =1)
        #Label(master, text = "Enter Radius").grid(row = 1, column = 0)
        #self.radiusTxt = Entry(master)
        #self.radiusTxt.grid(row = 1, column = 1)
        Label(master, text = "Enter Type of destinations").grid(
            row = 1,
            column = 0
            )
        #self.typeTxt = Entry(master)
        self.typeTxt = StringVar(master)
        self.typeTxt.set("Dept")
        w = OptionMenu(master, self.typeTxt, "Hall","Dept","Centre","Facility","Service","Landmark","Restaurant","Hospital","Market","School")
        w.grid(row = 1, column = 1)

    def apply(self):
        self.source = self.sourceTxt.get()
        self.type = self.typeTxt.get()

class Application(Frame):
    def __init__(self,master=None,map=None):
        if map is None:
            self.map = {'w' : 2382, 'h' : 1075, 'path' : 'map.jpg'}
        else:
            self.map = map
        self.master = master
        Frame.__init__(self,master)
        self.grid()
        self.createWidgets()
        self.renderMap()
        #self.renderRoute([[0,0],[10,10],[1000,390],[500,300],[100,100]])
        # d = Dialog(self)
        # #source,dest = d.apply()
        # #print source,dest
        # r = Finder.find(d.source,d.dest)
        # print "GOT ROUTE"
        # print r
        # self.renderRoute(r)

    def renderMap(self):
        self.map_img = Image.open(self.map['path'])
        self.tkpi = ImageTk.PhotoImage(self.map_img)
        #img = PhotoImage(file=self.map['path'])

        self.map["id"] = self.canvas.create_image(0,0, anchor=NW,
                                                  image= self.tkpi,
                                                  state= NORMAL)
        print self.map["id"]


    def findNeighbour(self):
        self.renderMap()
        d = NeighbourDialog(self)
        type_name = d.typeTxt.get()
        src = d.source
        r = Finder.findNeighbours(src, type_name)
        print "type = "+type_name
        if len(r) > 0:
            print "GOT ROUTES"
            dlist = ""
            for i in r:
                print i
                dlist = dlist + str(i[-1][2])+","
                self.renderRoute(i)
                
            
            tkMessageBox.showinfo(str(len(r))+" Results Found", dlist)
        else :
            tkMessageBox.showinfo("No results","No destinations match your query")
                

    def findRoute(self):
        self.renderMap()
        d = RouteDialog(self)
        r = Finder.findRoute(d.source,d.dest)
        if len(r) > 0:
            print "GOT ROUTE"
            print r
            self.renderRoute(r)
        else :
            tkMessageBox.showinfo("No results","No destinations match your query")

    def createWidgets(self):
        self.quitButton = Button(self,text="Quit",command=self.quit)
        self.findNeighbourBtn = Button(self,text="Find Neighbours",
                                    command = self.findNeighbour)
        self.findRouteBtn = Button(self,text="Find Route",
                                   command = self.findRoute)
        self.findNeighbourBtn.grid(row = 2, column = 0)
        self.findRouteBtn.grid(row = 2, column = 1)
        self.quitButton.grid(row = 2, column = 2, columnspan = 1)
        self.canvas = Canvas(self,width=1300,
                             height=650,
                             scrollregion=(0,0,self.map['w'], self.map['h']))
        self.canvas.grid(row=0, column = 0, columnspan = 2)

        scr1 = Scrollbar(self,orient=VERTICAL,command = self.canvas.yview)
        scr2 = Scrollbar(self,orient=HORIZONTAL, command = self.canvas.xview)
        scr1.grid(row = 0, column = 2, sticky=N+S)
        scr2.grid(row = 1, column = 0, sticky=E+W, columnspan = 2)
        self.canvas["xscrollcommand"] = scr2.set
        self.canvas["yscrollcommand"] = scr1.set
        scr1.config(command = self.canvas.yview)

    # route is list of lists
    def renderRoute(self,route):
        num_points = len(route)
        print "Length of route ="+str(num_points)
        for i in range(num_points-1):
            pt = route[i]
            pt_next = route[i+1]
            #self.canvas.create_line(pt[0])
            x1 = 2382*(pt[0])/(84.02)
            y1 = 1075*(pt[1])/(37.91)
            x2 = 2382*(pt_next[0])/(84.02)
            y2 = 1075*(pt_next[1])/(37.91)
            print "("+str(x1) + ","+str(y1)+")-->("+str(x2)+","+str(y2)+")"
            self.canvas.create_line(x1,y1, x2, y2, width = 5, fill="#FF0000")
            #self.canvas.create_line(24.32*pt[0]/(84.02),10.67*pt[1]/(37.91),24.32*pt_next[0]/84.02, 10.67*pt_next[1]/37.91,
            #fill="#FF0000", width=2)

    def createDialog(self):
        self.dialog = Dialog()

if __name__ == "__main__":
    root = Tk()
    root.resizable(0,0)
    app = Application(master = root)
    app.master.title("Sample Application")
    app.mainloop()
    
# 2.65 - 100m 
