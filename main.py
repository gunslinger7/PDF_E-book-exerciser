import random
import fitz # pymupdf library that worok with pdf
from PIL import Image # for displaying images
import customtkinter as custk # GUI

sequnce_counter = 0 # Counter for
current_page = list # 2 element list containing the current page number and the coordinates of the image displayed
doc = fitz.open('files/sinetra.pdf') # open the original file (and copy it later on so it stays untouched)
custk.set_appearance_mode("dark")
custk.set_default_color_theme('blue')
root = custk.CTk()
root.geometry("900x300")
pages_with_it = {} # stores the page numbers that contain the desired information, and coordinates of text
ordered_keys = [] # stores sorted dictionary keys.

def finder(query,start=0,stop=doc.page_count): # appends page numbers containing the query
    pages = fitz.open() #create a document
    pages.insert_pdf(doc, from_page=start, to_page=stop) # copy all the pages and insert into document
    for page in pages:  #for each page
        rects = page.search_for(query)
        if  len(rects) == 1:
            print(rects)
            print(page.number)
            for rect in rects:
                pages_with_it[str(page.number)] =  rect
        i =0
        if len(rects)> 1:
            print(rects)
            print(page.number)
            for rect in rects:
                pages_with_it[str(page.number) +"h" +str(i)] = rect
                i+=1
def png_loader(num, current_up=False, current_down = False,current_skip=False,previous_current=False): # displays and crops the image of desired query, num tells which one to show from pages_with_it list
          global current_page #access to data about current displayed page
          page_num = num # copy for later use
          if "h" in num: #check if page uses that word more than once
              num = num[:num.find("h")+1]
              num = num.replace("h","")
          temp_doc = fitz.open()
          temp_doc.insert_pdf(doc, from_page=int(num), to_page=int(num))
          page = temp_doc[0]
          page.set_mediabox(fitz.Rect(0, 0, page.mediabox_size[0], page.mediabox_size[1]))
          if current_skip == True: #skips to next page when button pressed
              current_page[0] = str(int(num)+1)
              tempo_doc = fitz.open()
              tempo_doc.insert_pdf(doc, from_page=int(current_page[0]), to_page=int(current_page[0]))
              page = tempo_doc[0]
              page.set_mediabox(fitz.Rect(0, 0, page.mediabox_size[0], page.mediabox_size[1]))
              page.set_cropbox(fitz.Rect(0, current_page[1][1], page.mediabox_size[0], current_page[1][3] + 35))
              matrix = fitz.Matrix(8, 8)
              pix = page.get_pixmap(matrix=matrix)
              pix.save("temp.png")
          elif previous_current == True: #skips to previous page when button is pressed
              current_page[0] = str(int(num)-1)
              tempo_doc = fitz.open()
              tempo_doc.insert_pdf(doc, from_page=int(current_page[0]), to_page=int(current_page[0]))
              page = tempo_doc[0]
              page.set_mediabox(fitz.Rect(0, 0, page.mediabox_size[0], page.mediabox_size[1]))
              page.set_cropbox(fitz.Rect(0, current_page[1][1], page.mediabox_size[0], current_page[1][3] + 35))
              matrix = fitz.Matrix(8, 8)
              pix = page.get_pixmap(matrix=matrix)
              pix.save("temp.png")
          elif current_down == True: # moves cropbox downwards when button is pressed
            x = 20
            current_page[1] = (0,current_page[1][1]+x,page.mediabox_size[0],current_page[1][3]+x)
            page.set_cropbox(fitz.Rect(0, current_page[1][1], page.mediabox_size[0], current_page[1][3] + 35 ))
          elif current_up == True: # moves cropbox upwards when button is pressed
            x = -20
            current_page[1] = (0,current_page[1][1]+x,page.mediabox_size[0],current_page[1][3]+x)
            page.set_cropbox(fitz.Rect(0, current_page[1][1], page.mediabox_size[0], current_page[1][3] + 35 ))

          else: #places cropbox where the query was found
            coord = pages_with_it[page_num]
            current_page = [page_num, coord]
            page.set_cropbox(fitz.Rect(0, coord[1], page.mediabox_size[0], coord[3]+35))
          matrix = fitz.Matrix(8, 8)
          pix = page.get_pixmap(matrix = matrix)
          pix.save("temp.png") #saves the current image as png

def label_renewer(): #updates the current image
    img = Image.open("temp.png")
    img1 = img.copy()
    img.close()
    image = custk.CTkImage(light_image=img1, size=(800, 70))
    image_label = custk.CTkLabel(root, image=image)
    image_label.place(x=50, y=60)
def randomizer(): #chooses one element randomly
    i = random.choice(list(pages_with_it.keys()))
    png_loader(str(i))
    label_renewer()
    print(pages_with_it)

def next_forward(): #goes to previous found page
    global sequnce_counter
    if sequnce_counter < len(pages_with_it.keys()) - 1:
        sequnce_counter += 1
        ordered_keys = sorted(list(pages_with_it.keys()))
        page_number = ordered_keys[sequnce_counter]
        png_loader(str(page_number))
        label_renewer()
def backward(): #goes to previous found page
    global sequnce_counter
    if sequnce_counter > 0:
        sequnce_counter -= 1
        ordered_keys = sorted(list(pages_with_it.keys()))
        page_number = ordered_keys[sequnce_counter]
        png_loader(str(page_number))
        label_renewer()
def submit(): #clears up cache, gets the entry from entry box and searches for the query
    sequnce_counter = 0
    pages_with_it.clear()
    ordered_keys.clear()
    serch = search_input.get()
    finder(serch)
    print("Search is done")
    print(len(pages_with_it.keys()))

def upwards(): # moves cropbox upwards when the button is pressed
    global current_page
    page_num = current_page[0]
    coord = current_page[1]
    png_loader(page_num , current_up=True)
    label_renewer()
def downwards(): # moves cropbox downwards when the button is pressed
    global current_page
    page_num = current_page[0]
    coord = current_page[1]
    png_loader(page_num,current_down=True)
    label_renewer()
def next_page_skip(): #skips to next page when the button is pressed
    global current_page
    num = current_page[0]
    png_loader(num,current_skip=True)
    label_renewer()
def previoius_page_skip(): #skips to previous page when the button is pressed
    global current_page
    num = current_page[0]
    png_loader(num,previous_current=True)
    label_renewer()


# Different Buttons for Different purposes
search_input = custk.CTkEntry(root)
search_input.place(x=60, y=150)

submit_button = custk.CTkButton(master=root, fg_color=("black", "darkred"), text="submit",command=submit)
submit_button.place(x=60, y=190)

random_found = custk.CTkButton(master=root, fg_color=("black", "black"), text="random", command=randomizer)
random_found.place(x=220, y=150)

next_forward = custk.CTkButton(master=root, fg_color=("black", "black"), text="next", command=next_forward)
next_forward.place(x=380, y=150)

next_backward = custk.CTkButton(master=root, fg_color=("black", "black"), text="back", command=backward)
next_backward.place(x=380, y=190)

up_button = custk.CTkButton(master=root, fg_color=("black", "black"), text="up",command=upwards)
up_button.place(x=540, y=150)

down_button = custk.CTkButton(master=root, fg_color=("black", "black"), text="down",command=downwards)
down_button.place(x=540, y=190)

next_page = custk.CTkButton(master=root, fg_color=("black", "black"), text="next page",command=next_page_skip)
next_page.place(x=700, y=150)

previous_page = custk.CTkButton(master=root, fg_color=("black", "black"), text="previous page",command=previoius_page_skip)
previous_page.place(x=700, y=190)

root.mainloop()
