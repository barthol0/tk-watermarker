import sys
import os
import random
import ntpath
import csv
import datetime
from tkinter import *
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader

root = Tk()
# root.config(height=500, width=500)
# root.geometry('500x500')
root.title("Tk-watermarker")
random_number = StringVar()


def select_directory():
    directory_selected = filedialog.askdirectory()
    e4.delete(0, END)
    e4.insert(0, directory_selected)
    return


def select_file():
    file_selected = filedialog.askopenfilename(
        filetypes=(("PDF documents", ".pdf"),))
    e3.delete(0, END)
    e3.insert(0, file_selected)
    return


def generate_watermark_text():
    name = e1.get()
    surname = e2.get()

    random_number_tmp = random.randint(100000000, 999999999)
    random_number.set(random_number_tmp)

    watermark_text = name + "_" + surname + "_" + random_number.get()

    return watermark_text


def put_watermark():

    watermark_text = generate_watermark_text()
    input_file_path = e3.get()
    output_file_name = ntpath.basename(
        e3.get())[:-4] + "_" + watermark_text + ".pdf"
    output_file_path = e4.get() + "/" + output_file_name
    output_file_path = output_file_path.replace('/', '\\')
    tmp_file_name = "temp.pdf"

    c = canvas.Canvas(tmp_file_name)
    c.setFont("Helvetica", 24)
    c.setFillGray(0.1, 0.1)
    c.saveState()
    c.translate(500, 100)
    c.rotate(45)
    c.drawCentredString(0, 300, watermark_text)
    c.restoreState()
    c.save()

    input_file = PdfFileReader(input_file_path)
    output_writer = PdfFileWriter()
    total_pages = input_file.getNumPages()

    for single_page in range(total_pages):
        page = input_file.getPage(single_page)
        if single_page in range(2, total_pages):
            page = input_file.getPage(single_page)
            watermark = PdfFileReader(tmp_file_name)
            page.mergePage(watermark.getPage(0))
        output_writer.addPage(page)

    with open(output_file_path, "wb") as outputStream:
        output_writer.write(outputStream)
    os.remove(tmp_file_name)

    save_in_csv()


def save_in_csv():

    data = [e1.get(), e2.get(), random_number.get(), datetime.datetime.now()]
    with open("db_wmk.csv", "a", newline="\n", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)


step = LabelFrame(root, text="Enter Details:")
step.grid(row=0, columnspan=7, sticky='W',
          padx=5, pady=5, ipadx=5, ipady=5)

Label(step, text="Name:", font="Arial 12").grid(
    row=0, sticky='E', padx=5, pady=2)
Label(step, text="Surname:", font="Arial 12").grid(
    row=1, sticky='E', padx=5, pady=2)
Label(step, text="File:", font="Arial 12").grid(
    row=2, sticky='E', padx=5, pady=2)
Label(step, text="Output location:", font="Arial 12").grid(
    row=3, sticky='E', padx=5, pady=2)

e1 = Entry(step, font="Arial 12")
e2 = Entry(step, font="Arial 12")
e3 = Entry(step, font="Arial 12")
e4 = Entry(step, font="Arial 12")

e1.grid(row=0, column=1, columnspan=5, sticky="WE", pady=3, padx=5)
e2.grid(row=1, column=1, columnspan=5, sticky="WE", pady=3, padx=5)
e3.grid(row=2, column=1, columnspan=5, sticky="WE", pady=3, padx=5)
e4.grid(row=3, column=1, columnspan=5, sticky="WE", pady=3, padx=5)

Button(step, text="Open file...", width=10, font="Arial 8 ",
       command=select_file).grid(row=2, column=7, sticky=E, pady=4, padx=5)
Button(step, text="Output...", width=10, font="Arial 8", command=select_directory).grid(
    row=3, column=7, sticky=W, pady=4, padx=5)
Button(step, text="Watermark!", width=15, font="Arial 12", activebackground="red", command=put_watermark).grid(
    row=5, column=4, sticky=W, pady=4, padx=5)

root.mainloop()
