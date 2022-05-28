from Files.video import *
from Files.audio import *
import os
from PIL import Image
from tkinter import ttk
# import imageio
from HTML import *
requests.urllib3.disable_warnings()

print("    Creating TKinter Window")
root = tk.Tk()
root.geometry("500x400")

URL = tk.StringVar()
URL.set("Startpage.html")

print("    Getting site '" + URL.get() + "'")
if ok(URL.get()):
    s=get_site(URL.get())
else:
    print("an error occured verify connexion.")
    exit()

print("    Set Window Title")
root.title(s.find('title').text)

URL_frame = tk.Frame(root)
URL_frame.pack(side=tk.TOP, fill="x", expand="no")
URL_input = tk.Entry(URL_frame, textvariable=URL)
URL_input.pack(side=tk.LEFT, fill="x", expand="yes")
send = tk.Button(URL_frame, text="Aller", command= lambda: parse(get_site(URL.get())))
send.pack(side=tk.RIGHT)

print("    Changing Icon to Site Icon")
#icon = open('TempFiles/webicon.ico', 'wb')
#icon.write(requests.get("https://google.fr/favicon.ico", allow_redirects=True).content)
#icon.close()
root.iconbitmap("lico.ico")

main_frame = tk.Frame(root)
main_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand="yes")

mainn_frame = tk.Frame(main_frame)
mainn_frame.pack(side= tk.TOP, fill=tk.BOTH, expand=1)

my_canvas = tk.Canvas(mainn_frame)
my_canvas.pack(side=tk.LEFT, fill="both", expand="yes")

my_scrollbar = ttk.Scrollbar(mainn_frame, orient="vertical", command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT, fill="y")
xscrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=my_canvas.xview)
xscrollbar.pack(side=tk.BOTTOM, fill="x")

my_canvas.configure(yscrollcommand=my_scrollbar.set, xscrollcommand=xscrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

vid = Video()
vidb = 0

second_frame = tk.Frame(my_canvas)

my_canvas.create_window((0,0), window = second_frame, anchor="nw")

print("    Parsing HTML")

def pause():
    vid.pause()
    if vidb['text'] == '| |':
        vidb['text'] = '►'
    else:
        vidb['text'] = '| |'
    
def show_object(object):
    print(object.type)
    if object.type == "Button":
       tk.Button(second_frame, text = object.text, fg = object.fg, font=(object.font_type, object.font_size), borderwidth = object.borderwidth).pack()
    if object.type == "Label":
       tk.Label(second_frame, text=object.text, fg = object.fg, font=(object.font_type, object.font_size)).pack()
    if object.type == "Entry":
       tk.Entry(second_frame, textvariable=object.textvariable, fg = object.fg, font=(object.font_type, object.font_size)).pack()
    if object.type == "Image":
       photo = tk.PhotoImage(file = object.image)
       imgb = tk.Button(second_frame, text = ' ', image = photo, borderwidth = 0)
       imgb.image = photo
       imgb.pack()
    if object.type == "Video":
        global vid
        global vidb
        print(imageio.get_reader(object.image).get_meta_data()["duration"])
        vidframespace = tk.Frame(second_frame)
        vidbframespace = tk.Frame(vidframespace)
        vid = Video()
        vidframe = tk.Label(vidframespace)
        vid.openfile(object.image, vidframe, vidframespace)
        vidb = tk.Button(vidbframespace, text = "►", command = pause)
        vidb.pack(side = 'left')
        vidframespace.pack()
        vidframe.pack(side="top")
        vidbframespace.pack(side = "bottom")
        vid.play()
    if object.type == "aButton":
        if object.image != '':
            photo = tk.PhotoImage(file = object.image)
            ab = tk.Button(second_frame, text=object.text, image = photo, borderwidth = object.borderwidth, fg = object.fg, font=(object.font_type, object.font_size))
            ab.image = photo
            ab.pack()
        else:
            tk.Button(second_frame, text=object.text, borderwidth = object.borderwidth, fg = object.fg, font=(object.font_type, object.font_size)).pack()
    return 0

def unrange(i):
    r = []
    while i!=0:
        i = i - 1
        r.append(i)
    return r

def parse(s):
    for widget in second_frame.winfo_children():
        widget.destroy()
    root.iconbitmap("lico.ico")
    c = list(s.html.body.children)
    c = list(filter(('\n').__ne__, c)) # remove all \n from list
    print(c)
    default_object = GraphicalObject()
    current_object = GraphicalObject()

    for x in range(len(c)-1):
        f = None 
        y = 0
        d = []
        if str(c[x])[0] == "<":
            while f != c[x]:
                f=s.findAll(c[x].name)[y]
                y= y + 1
            d = list(f.descendants)
            print("        f = ", f)
            print("        d = ", d)
        elif str(c[x]).find('\n') != -1:
            f=c[x]

        current_object = GraphicalObject()
        d.insert(0, f)
        print("      final d = ", d)
        for i in range(len(d)):
        
            print("making ", len(d), "iterations, actually are the", i)
            print(str(d[i])[0:6])
            if str(d[i])[0:4] == "<img":
                print("New image: " + str(get_src(d[i])))
                URL = str(get_src(d[i]))
                for j in unrange(len(URL)):
                    if URL[j] == '.':
                        break
                ext = URL[j:]
                with open('TempFiles/'+str(i)+ext, 'wb') as f:
                    f.write(requests.get(str(get_src(d[i]))).content)
                im = Image.open(r'TempFiles/'+str(i)+ext)
                im.thumbnail((get_width(d[i]), get_height(d[i])), Image.Resampling.LANCZOS)
                im.save(r'TempFiles/'+str(i)+'.png', 'png')
                current_object = GraphicalObject("Image", image = str('TempFiles/'+ str(i) + '.png'), text = "image")
            elif str(d[i])[0:6] == "<video":
                print("New video: " + str(get_src(d[i])))
                URL = str(get_src(d[i]))
                for j in unrange(len(URL)):
                    if URL[j] == '.':
                        break
                ext = URL[j:]
                with open('TempFiles/'+str(i)+ext, 'wb') as f:
                    f.write(requests.get(str(get_src(d[i]))).content)
                current_object = GraphicalObject("Video", image = str('TempFiles/'+ str(i) + ext), text = "video")
            elif str(d[i])[0:2] == "<a":
                print("New Href data: " + str(d[i]))
                current_object = GraphicalObject("aButton", text=current_object.text, fg="blue", borderwidth = 0, font_size=current_object.font_size)

            elif str(d[i])[0:3] == "<H1" or str(d[i])[0:3] == "<h1":
                print("New Head data 1: " + str(d[i]))
                current_object = GraphicalObject(current_object.type, text=current_object.text, font_size=25, fg=current_object.fg, borderwidth = current_object.borderwidth)

            elif str(d[i])[0:3] == "<H2" or str(d[i])[0:3] == "<h2":
                print("New Head data 2: " + str(d[i]))
                current_object = GraphicalObject(current_object.type, text=current_object.text, font_size=18, fg=current_object.fg, borderwidth = current_object.borderwidth)

            elif str(d[i])[0:3] == "<H3" or str(d[i])[0:3] == "<h3":
                print("New Head data 3: " + str(d[i]))
                current_object = GraphicalObject(current_object.type, text=current_object.text, font_size=14, fg=current_object.fg, borderwidth = current_object.borderwidth)

            elif str(d[i])[0:3] == "<H4" or str(d[i])[0:3] == "<h4":
                print("New Head data 4: " + str(d[i]))
                current_object = GraphicalObject(current_object.type, text=current_object.text, font_size=12, fg=current_object.fg, borderwidth = current_object.borderwidth)

            elif str(d[i])[0:3] == "<H5" or str(d[i])[0:3] == "<h5":
                print("New Head data 5: " + str(d[i]))
                current_object = GraphicalObject(current_object.type, text=current_object.text, font_size=10, fg=current_object.fg, borderwidth = current_object.borderwidth)

            elif str(d[i])[0:3] == "<H6" or str(d[i])[0:3] == "<h6":
                print("New Head data 6: " + str(d[i]))
                current_object = GraphicalObject(current_object.type, text=current_object.text, font_size=7, fg=current_object.fg, borderwidth = current_object.borderwidth)

            elif str(d[i])[0:6] == "<input":
                if get_type(d[i]) == "hidden":
                    print("New Hidden input: " + str(d[i]))

                elif get_type(d[i]) == "submit":
                    print("New input: " + str(d[i]))
                    current_object = GraphicalObject("Button", text = get_value(d[i]))

                else:
                    print("New input: " + str(d[i]))
                    v = tk.StringVar()
                    v.set(get_value(d[i]))
                    current_object = GraphicalObject("Entry", text="entry", textvariable = v)

            elif d[i] != "":
                print("New Simple data: " + str(d[i]))
                current_object = GraphicalObject(current_object.type, image=current_object.image, text=d[i].string, font_size=current_object.font_size, fg=current_object.fg, borderwidth = current_object.borderwidth)
            if current_object.text == '':
                continue
            else:
                print("showing object:", current_object)
                show_object(current_object)
            
         
         
            
parse(s)
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
root.mainloop()
print("closing...")
print("deleting files...")
folder = 'TempFiles/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
        
print("files deleted")
print("close")