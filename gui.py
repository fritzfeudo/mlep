# from tkinter import Tk, Label, Button
from tkinter import *
from tkinter import filedialog
from encoder import encode
from decoder import decode
import os

class MLepGUI:
    def __init__(self, master):
        self.master = master
        master.title("MLEP")
        master.geometry("500x500")
        master.configure(bg="#472d30", highlightthickness=0, highlightbackground="white", highlightcolor="white")
        # master.resizable(False, False)

        positionRight = int(master.winfo_screenwidth()/2 - 250)
        positionDown = int(master.winfo_screenheight()/2 - 250)
        master.geometry("+{}+{}".format(positionRight, positionDown))

        self.notif_area = Text(master, height="10", padx=5, pady=5, bg="#723d46", fg="white", font=("ubuntu", 10), highlightthickness=0, relief=FLAT)
        self.notif_area.insert(INSERT, "Welcome!")
        self.notif_area.config(state=DISABLED)
        self.notif_area.place(relx=0, rely=0, relheight=0.4, relwidth=1)

        self.compress_button = Button(master, text="Compress", command=self.compress, bg="#c9cba3", activebackground="#8e8f74", fg="black", font=('ubuntu', 12), highlightthickness=0, relief=FLAT)
        self.compress_button.place(relx=0.5, rely=0.50, anchor=CENTER, relheight=0.1, relwidth=0.5)

        self.decompress_button = Button(master, text="Decompress", command=self.decompress, bg="#ffe1a8", activebackground="#8e8f74",fg="black", font=('ubuntu', 12), highlightthickness=0, relief=FLAT)
        self.decompress_button.place(relx=0.5, rely=0.65, anchor=CENTER, relheight=0.1, relwidth=0.5)

        self.close_button = Button(master, text="Close", command=master.quit, bg="#e26d5c", activebackground="#8e8f74",fg="black", font=('ubuntu', 12), highlightthickness=0, relief=FLAT)
        self.close_button.place(relx=0.5, rely=0.92, anchor=CENTER, relheight=0.1, relwidth=0.5)

    def compress(self):
        input_file = filedialog.askopenfilename(initialdir="~/Desktop", parent=self.master)
        # fn, fext = os.path.splitext(input_file)
        # output_file = filedialog.asksaveasfilename(initialfile="{}.mlep".format(fn), defaultextension=".mlep")
        output_file = filedialog.asksaveasfilename(initialfile="compressed.mlep", defaultextension=".mlep")

        self.notif_area.config(state=NORMAL)
        self.notif_area.delete('1.0', END)
        self.notif_area.insert(INSERT, "Compressing...\n\nThis may take a while.")
        self.notif_area.config(state=DISABLED)
        self.notif_area.update_idletasks()

        if(input_file != '' and input_file != () and output_file != '' and output_file != ()):
            elapsed_time, frame_rate, frame_count = encode(input_file, output_file)
            filename = output_file
            original_size = os.path.getsize(input_file)
            compressed_size = os.path.getsize(output_file)
            compression_ratio = compressed_size / original_size * 100
            space_savings = 100 - compression_ratio

            print("\n\nOutput: {}\n\nOriginal Size: {} bytes\nCompressed Size: {} bytes\nCompression Ratio: {}%\nSpace Savings: {}%\n\nFrame Count: {}\nFrame Rate: {}\nElapsed time: {} seconds".format(filename, original_size, compressed_size, compression_ratio, space_savings, frame_count, frame_rate, elapsed_time))

            self.notif_area.config(state=NORMAL)
            self.notif_area.delete('1.0', END)
            self.notif_area.insert(INSERT, "Done!\n\nOutput: {}\n\nOriginal Size: {} bytes\nCompressed Size: {} bytes\nCompression Ratio: {}%\nSpace Savings: {}%\n\nFrame Count: {}\nFrame Rate: {}\nElapsed time: {} seconds".format(filename, original_size, compressed_size, compression_ratio, space_savings, frame_count, frame_rate, elapsed_time))
            self.notif_area.config(state=DISABLED)
            self.notif_area.update_idletasks()
        else:
            self.notif_area.config(state=NORMAL)
            self.notif_area.delete('1.0', END)
            self.notif_area.insert(INSERT, "No file chosen.")
            self.notif_area.config(state=DISABLED)
            self.notif_area.update_idletasks()             

    def decompress(self):
        input_file = filedialog.askopenfilename(initialdir="~/Desktop", parent=self.master)
        # fn, fext = os.path.splitext(input_file)
        # output_file = filedialog.asksaveasfilename(initialfile="{}.avi".format(fn), defaultextension=".avi")
        output_file = filedialog.asksaveasfilename(initialfile="decompressed.avi", defaultextension=".avi")

        self.notif_area.config(state=NORMAL)
        self.notif_area.delete('1.0', END)
        self.notif_area.insert(INSERT, "Decompressing...\n\nThis may take a while.")
        self.notif_area.config(state=DISABLED)
        self.notif_area.update_idletasks()

        if(input_file != '' and input_file != () and output_file != '' and output_file != ()):
            elapsed_time, frame_rate, frame_count = decode(input_file, output_file)
            filename = output_file
            filesize = os.path.getsize(output_file)

            print("\n\nOutput: {}\nSize: {} bytes\n\nFrame Count {}\nFrame Rate: {}\nElapsed time: {} seconds".format(filename, filesize, frame_count, frame_rate, elapsed_time))

            self.notif_area.config(state=NORMAL)
            self.notif_area.delete('1.0', END)
            self.notif_area.insert(INSERT, "Done!\n\nOutput: {}\nSize: {} bytes\n\nFrame Count {}\nFrame Rate: {}\nElapsed time: {} seconds".format(filename, filesize, frame_count, frame_rate, elapsed_time))
            self.notif_area.config(state=DISABLED)
            self.notif_area.update_idletasks()
        else:
            self.notif_area.config(state=NORMAL)
            self.notif_area.delete('1.0', END)
            self.notif_area.insert(INSERT, "No file chosen.")
            self.notif_area.config(state=DISABLED)
            self.notif_area.update_idletasks()            


if __name__ == "__main__":
    root = Tk()
    my_gui = MLepGUI(root)
    root.mainloop()