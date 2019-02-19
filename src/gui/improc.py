from tkinter import Tk, Label, Button, Text, filedialog, END
import sys
sys.path.append("..")
import astroTUM as atum

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.communicator = {'input_path' : '',
                             'output_path' : '',
                             'message' : ''}

        def open_file():
            self.communicator['input_path'] = \
                filedialog.askopenfilename(initialdir = ".",
                                           title = "Select file",
                                           filetypes = (("fits files",
                                                         "*.fits"),
                                                        ("all files",
                                                         "*.*")))
            self.update()

        def choose_file():
            self.communicator['output_path'] = \
                filedialog.asksaveasfilename(initialdir = ".",
                                             title = "Select file",
                                             filetypes = (("fits files",
                                                           "*.fits"),
                                                          ("all files",
                                                           "*.*")))
            self.update()

        def calculate():
            """Cuts the image"""
            x_offset = int(self.text3.get("1.0", END))
            y_offset = int(self.text4.get("1.0", END))
            if not self.text5.get("1.0", END) == '\n':
                width = int(self.text5.get("1.0", END))
            else:
                width = None
            height = int(self.text6.get("1.0", END))


        # Open file
        self.text1 = Text(root, height=1, width=60)
        self.text1.grid(row=0, column=0)
        self.open_button = Button(master,
                                  text="Open",
                                  command=lambda: open_file())
        self.open_button.grid(row=0, column=1)

        # x offset
        self.text2 = Text(root, height=1, width=60)
        self.text2.grid(row=1, column=0)
        self.label1 = Label(root, text='x offset')
        self.label1.grid(row=2, column=3)
        # y offset
        self.text3 = Text(root, height=1, width=20)
        self.text3.grid(row=2, column=2)
        self.label2 = Label(root, text='y offset')
        self.label2.grid(row=3, column=3)
        # width
        self.text4 = Text(root, height=1, width=20)
        self.text4.grid(row=3, column=2)
        self.label3 = Label(root, text='width')
        self.label3.grid(row=4, column=3)
        # height
        self.text5 = Text(root, height=1, width=20)
        self.text5.grid(row=4, column=2)
        self.label4 = Label(root, text='height')
        self.label4.grid(row=5, column=3)
        self.text6 = Text(root, height=1, width=20)
        self.text6.grid(row=5, column=2)

        # Choose output file
        self.choose_button = Button(master,
                                    text="Output",
                                    command=lambda: choose_file())
        self.choose_button.grid(row=1, column=1)

        # Calculate button
        self.calc_button = Button(master, text="Calculate", command=lambda: calculate())
        self.calc_button.grid(row=6, column=2)

        # Close button
        self.close_button = Button(master, text="Close", command=lambda: master.destroy())
        self.close_button.grid(row=6, column=3)

        # Message window
        self.label5 = Label(root, text='Messages:')
        self.label5.grid(row=2, column=0, sticky="W")
        self.label6 = Label(root, text=self.communicator['message'])
        self.label6.grid(row=3, column=0, sticky="W")

    def update(self):
        """Update all stuff"""
        self.text1.delete(1.0, END)
        self.text1.insert(END, self.communicator['input_path'])
        self.text2.delete(1.0, END)
        self.text2.insert(END, self.communicator['output_path'])

def main():
    root = Tk()
    my_gui = GUI(root)
    root.mainloop()
