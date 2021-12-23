#Pada bagian ini mengimport library
from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import filedialog
import os

#membuat class ImageViewer
class ImageView:
    #konstruktor untuk kelas yang dibuat
	def __init__(self,root):
		self.root = root
        #membuat judul di atas
		self.root.title("Image Viewer")
        #membuat bentuk kotak di atas
		self.root.geometry('850x530')
        #membuat bentuk ukuran kotak yang diatas 
		self.root.resizable(0,0)
		self.i = 0
		# Pada bagian ini menampilkan list gambar
		self.Image_list = []
		# Pada bagian ini path default yang digunakan
		self.path =""
		# Pada bagian ini ekstensi pada gambar
		self.extension = ['JPG','BMP','PNG']
 
		# Pada bagian ini membuat kanvas
		self.canvas = Canvas(self.root,bd=5,relief=RIDGE)
		self.canvas.place(x=0,y=0,height=500,width=850)
 
		# Pada bagian ini membuat tombol dengan ukuran dan koordinat
		self.previous_button = Button(self.root,text="<",width=3,font=('arial',10,'bold'),command=self.previous_image)
		self.previous_button.place(x=360,y=500)
        
		self.next_button = Button(self.root,text=">",width=3,font=('arial',10,'bold'),command=self.next_image)
		self.next_button.place(x=455,y=500)
 
		self.open_button = Button(self.root,text="Open",width=5,font=('arial',10,'bold'),command=self.open_file)
		self.open_button.place(x=400,y=500)
 
	#Pada bagian ini membuka fungsi
	def open_file(self):
		self.path = filedialog.askdirectory()
		if self.path:
			self.Image_list = []
			self.add_image()
 
    #Pada bagian ini menambahkan file gambar
	def add_image(self):
		for image in os.listdir(self.path):
			ext = image.split('.')[::-1][0].upper()
			if ext in self.extension:
				self.Image_list.append(image)
 
		self.resize(self.Image_list[0])
 
	#Pada bagian ini funsinya mengubah ukuran gambar
	def resize(self,image):
		if self.path :
			os.chdir(self.path)
			image_p = self.path + '\\' + str(image)
			img = PIL.Image.open(image)
			# Pada bagian menampilakan gambar
			width, height = img.size
			if (int(width) > 850 and int(height) < 500):
				img = img.resize((850, height))
			elif (int(height) > 500 and int(width) < 850):
				img = img.resize((width, 500))
			elif (int(width) > 850 and int(height) > 500):
				img = img.resize((840, 480))
 
			storeobj = ImageTk.PhotoImage(img)
			self.canvas.delete(self.canvas.find_withtag("bacl"))
			w = self.canvas.winfo_width()
			h = self.canvas.winfo_height()
            #Pada bagian ini menyimpan referensi gambar 
			self.canvas.image = storeobj 
			self.canvas.create_image(w / 2, h / 2, image=storeobj, anchor=CENTER)
			self.root.title("Image Viewer ({})".format(image_p))
    #Pada bagian ini melanjutkan gambar yang dipilih  
	def next_image(self):
		self.i+=1
		try:
			self.image = self.Image_list[self.i]
			self.resize(self.image)
		except:
			pass
    #Pada bagian ini sebelum gambar yang dipilih 
	def previous_image(self):
		self.i -=1
		try:
			self.image = self.Image_list[self.i]
			self.resize(self.image)
		except:
			self.i = 1

if __name__ == '__main__':
	root = Tk()
	img = ImageView(root)
	root.mainloop()