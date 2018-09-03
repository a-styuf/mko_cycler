from tkinter import *

root = Tk()

topButton = Button(root, text = 'Кнопка сверху')
topButton.grid(row = 0, column = 0)
lowFrame = Frame(root)
lowFrame.grid(row = 1, column = 0)

canvas = Canvas(lowFrame)
canvas.pack(side = 'left')
frame = Frame(canvas)
myscrollbar = Scrollbar(lowFrame, orient = 'vertical', command = canvas.yview)
canvas.configure(yscrollcommand = myscrollbar.set)
myscrollbar.pack(side = 'right', fill = Y)

canvas.create_window((0, 0), window = frame, anchor = 'nw')
def conf(event):
    canvas.configure(scrollregion = canvas.bbox('all'))
frame.bind('<Configure>', conf)

for i in range(50):
    b = Button(frame, text = str(i))
    b.grid(row = i, column = 0)

root.mainloop()