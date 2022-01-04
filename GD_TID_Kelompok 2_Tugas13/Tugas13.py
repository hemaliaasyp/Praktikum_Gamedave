import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
from panda3d.core import TextNode

from direct.gui.DirectGui import DirectFrame

# Add some text
bk_text = "Kelompok 2 "
textObject = OnscreenText(text=bk_text, pos=(0.0, 0.70), scale=0.10,
                          fg=(6, 6, 6, 6), align=TextNode.ACenter,
                          mayChange=1)
# Callback function to set text
v = [0]
def setText(status=None):
    bk_text = "CurrentValue : %s"%v
    textObject.setText(bk_text)

def itemSel(arg):
    if arg == "Pilih Anggota Kelompok":
        l1 = DirectLabel(text="Kelompok 2", text_scale=0.07)
        l2 = DirectLabel(text="Kelas D", text_scale=0.08)
        l3 = DirectLabel(text="UNS", text_scale=0.08)

        numItemsVisible = 3
        itemHeight = 0.11

        myScrolledList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),

            incButton_pos=(0.35, 0, -0.02),
            incButton_text="",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),

            frameSize=(0.0, 0.7, -0.05, 0.59),
            frameColor=(255, 0, 0, 0.2),
            pos=(-1, 0, 0),
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
        )

        myScrolledList.addItem(l1)
        myScrolledList.addItem(l2)
        myScrolledList.addItem(l3)

        
        imageObject = OnscreenImage(
        image='welcome.jpg', pos=(-0.65, 0, -0.45), scale=0.35,)
        
    if arg == "Anggota 1":
        buttons = [DirectRadioButton(text='Pyhton', variable=v, value=[0],
                             scale=0.05, pos=(0.7, 0, -0.45), command=setText),
            DirectRadioButton(text='PHP', variable=v, value=[1],
                             scale=0.05, pos=(0.7, 0, -0.55), command=setText),
            DirectRadioButton(text='Java', variable=v, value=[2],
                             scale=0.05, pos=(0.7, 0, -0.65), command=setText),
            DirectRadioButton(text='Ruby', variable=v, value=[3],
                             scale=0.05, pos=(0.7, 0, -0.75), command=setText),
            DirectRadioButton(text='C++', variable=v, value=[4],
                             scale=0.05, pos=(0.7, 0, -0.85), command=setText)]
        for button in buttons:
            button.setOthers(buttons)

        l1 = DirectLabel(text="Algeori Wira Wahyu H", text_scale=0.04)
        l2 = DirectLabel(text="V3920006", text_scale=0.05)
        l3 = DirectLabel(text="Kelas D", text_scale=0.05)

        numItemsVisible = 3
        itemHeight = 0.11

        myScrolledList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="Sebelumnya",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),

            incButton_pos=(0.35, 0, -0.02),
            incButton_text="Selanjutnya",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),

            frameSize=(0.0, 0.2, -0.05, 0.59),
            frameColor=(255, 0, 0, 0.8),
            pos=(-1, 0, 0),
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
        )

        myScrolledList.addItem(l1)
        myScrolledList.addItem(l2)
        myScrolledList.addItem(l3)

        for fruit in ['','', '12 April', '2001']:
            l = DirectLabel(text=fruit, text_scale=0.05)
            myScrolledList.addItem(l)
        imageObject = OnscreenImage(
        image='ALGEORI.jpeg', pos=(-0.65, 0, -0.45), scale=0.35,)

    if arg == "Anggota 2":
        l1 = DirectLabel(text="Ardianita Fauziyah", text_scale=0.05)
        l2 = DirectLabel(text="V3920009", text_scale=0.05)
        l3 = DirectLabel(text="Kelas D", text_scale=0.05)

        numItemsVisible = 3
        itemHeight = 0.11

        myScrolledList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="Sebelumnya",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),

            incButton_pos=(0.35, 0, -0.02),
            incButton_text="Selanjutnya",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),

            frameSize=(0.0, 0.7, -0.05, 0.59),
            frameColor=(0,0,1,0.5),
            pos=(-1, 0, 0),
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
        )

        myScrolledList.addItem(l1)
        myScrolledList.addItem(l2)
        myScrolledList.addItem(l3)

        for fruit in ['','Tanggal Lahir', '11,', 'Oktober']:
            l = DirectLabel(text=fruit, text_scale=0.05)
            myScrolledList.addItem(l)
        imageObject = OnscreenImage(
        image='NITA.png', pos=(-0.65, 0, -0.45), scale=0.35,)

    if arg == "Anggota 3":
        l1 = DirectLabel(text="Elya Kumala Fauziyah", text_scale=0.04)
        l2 = DirectLabel(text="V3920020", text_scale=0.05)
        l3 = DirectLabel(text="Kelas D", text_scale=0.05)

        numItemsVisible = 3
        itemHeight = 0.11

        myScrolledList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="Sebelumnya",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),

            incButton_pos=(0.35, 0, -0.02),
            incButton_text="Setelahnya",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),

            frameSize=(0.0, 0.7, -0.05, 0.59),
            frameColor=(0,1,0,0.5),
            pos=(-1, 0, 0),
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
        )

        myScrolledList.addItem(l1)
        myScrolledList.addItem(l2)
        myScrolledList.addItem(l3)

        for fruit in ['','Tanggal Lahir', '11,', 'Oktober']:
            l = DirectLabel(text=fruit, text_scale=0.05)
            myScrolledList.addItem(l)
        imageObject = OnscreenImage(
        image='ELYA.png', pos=(-0.65, 0, -0.45), scale=0.35,)

    if arg == "Anggota 4":
        l1 = DirectLabel(text="Hemalia Aisyah Putri", text_scale=0.04)
        l2 = DirectLabel(text="V3920025", text_scale=0.05)
        l3 = DirectLabel(text="Kelas D", text_scale=0.05)

        numItemsVisible = 3
        itemHeight = 0.11

        myScrolledList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="Sebelumnya",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),

            incButton_pos=(0.35, 0, -0.02),
            incButton_text="Selanjutnya",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),

            frameSize=(0.0, 0.7, -0.05, 0.59),
            frameColor=(1,1,0,0.5),
            pos=(-1, 0, 0),
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
        )

        myScrolledList.addItem(l1)
        myScrolledList.addItem(l2)
        myScrolledList.addItem(l3)

        for fruit in ['','Tanggal Lahir', '11,', 'Oktober']:
            l = DirectLabel(text=fruit, text_scale=0.05)
            myScrolledList.addItem(l)
        imageObject = OnscreenImage(
        image='HEMA.jpg', pos=(-0.65, 0, -0.45), scale=0.35,)

    if arg == "Anggota 5":
        l1 = DirectLabel(text="Linda Rahmawati", text_scale=0.05)
        l2 = DirectLabel(text="V3920033", text_scale=0.05)
        l3 = DirectLabel(text="Kelas D", text_scale=0.05)

        numItemsVisible = 3
        itemHeight = 0.11

        myScrolledList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.53),
            decButton_text="Sebelumnya",
            decButton_text_scale=0.04,
            decButton_borderWidth=(0.005, 0.005),

            incButton_pos=(0.35, 0, -0.02),
            incButton_text="Selanjutnya",
            incButton_text_scale=0.04,
            incButton_borderWidth=(0.005, 0.005),

            frameSize=(0.0, 0.7, -0.05, 0.59),
            frameColor=(255, 0, 0, 0.8),
            pos=(-1, 0, 0),
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_frameSize=(-0.2, 0.2, -0.37, 0.11),
            itemFrame_pos=(0.35, 0, 0.4),
        )

        myScrolledList.addItem(l1)
        myScrolledList.addItem(l2)
        myScrolledList.addItem(l3)

        for fruit in ['','Tanggal Lahir', '11,', 'Oktober']:
            l = DirectLabel(text=fruit, text_scale=0.05)
            myScrolledList.addItem(l)
        imageObject = OnscreenImage(
        image='LINDA.jpeg', pos=(-0.65, 0, -0.45), scale=0.35,)

# Create a frame
menu = DirectOptionMenu(text="options", scale=0.1, initialitem=2,
                        items=["Pilih Anggota Kelompok", "Anggota 1",
                               "Anggota 2", "Anggota 3", "Anggota 4", "Anggota 5"],
                        highlightColor=(0.65, 0.1, 0.1, 1),
                        command=itemSel, textMayChange=1)


def showValue():
    return menu

# Procedurally select a item
menu.set(0)

# Run the program
base.run()
