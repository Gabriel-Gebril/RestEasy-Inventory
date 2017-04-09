#File: Gebril_Project.py
#Date: April 9th, 2017
#Description: An inventory management system.

import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk

from tkinter import messagebox
from tkinter import filedialog

header = ['Item Number', 'Quantity','Item Name','Item Location','Item Description']
#This acts as the container for all my items. Each item is a tuple and this is a list of tuples.
Item_list = []

#The app class that contains the bulk of the functionality
class app(object):
    """using a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        container = ttk.Frame()
        container.pack(fill='both', expand=True)

        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=1, sticky='nsew', in_=container)
        vsb.grid(column=1, row=1, sticky='ns', in_=container)
        hsb.grid(column=0, row=2, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        # create item entry labels
        ItemNumber_Label= tk.Label(text="Item Number: ")
        ItemNumber_Label.grid(column=0,row=3,stick="W",in_=container)

        Quantity_Label= tk.Label(text="Quantity: ")
        Quantity_Label.grid(column=0, row=4, sticky="W",in_=container)

        ItemName_Label= tk.Label( text="Item Name: ")
        ItemName_Label.grid(column=0, row=5, sticky="W",in_=container)

        ItemLocation_Label= tk.Label(text="Item Location: ")
        ItemLocation_Label.grid(column=0, row=6, sticky="W",in_=container)

        ItemDes_Label= tk.Label(text="Item Description: ")
        ItemDes_Label.grid(column=0, row=7, sticky="W",in_=container)
        
        # create item entry boxes
        ItemNumber_txt= tk.StringVar()
        ItemNumber_Entry= tk.Entry(textvariable=ItemNumber_txt)
        ItemNumber_Entry.grid(column = 0, row = 3, sticky = 'W', padx = 110,in_=container)

        Quantity_txt= tk.StringVar()
        Quantity_Entry= tk.Entry(textvariable=Quantity_txt)
        Quantity_Entry.grid(column = 0, row = 4, sticky = 'W', padx = 110,in_=container)

        ItemName_txt= tk.StringVar()
        ItemName_Entry= tk.Entry(textvariable=ItemName_txt)
        ItemName_Entry.grid(column = 0, row = 5, sticky = 'W', padx = 110,in_=container)

        ItemLocation_txt= tk.StringVar()
        ItemLocation_Entry= tk.Entry(textvariable=ItemLocation_txt)
        ItemLocation_Entry.grid(column = 0, row = 6, sticky = 'W', padx = 110,in_=container)

        ItemDes_txt= tk.StringVar()
        ItemDes_Entry= tk.Entry(textvariable=ItemDes_txt)
        ItemDes_Entry.grid(column = 0, row = 7, sticky = "W", padx = 110,in_=container)

        Search_txt= tk.StringVar()
        Search_Entry= tk.Entry(textvariable=Search_txt)
        Search_Entry.grid(column = 0, row = 0, sticky= "E",padx=5,in_=container)

        # button commands
        def add(): 
            try:
                assert (ItemNumber_txt.get() != '' or Quantity_txt.get() != '' or ItemName_txt.get() != '' or ItemLocation_txt.get() != '' or ItemDes_txt.get() !=''), "Not all categories are filled!"
                if not ItemNumber_txt.get().isdigit() or not Quantity_txt.get().isdigit():
                    raise ValueError
                if search(Item_list,ItemNumber_txt.get()):
                    raise Exception
                Item_list.append((ItemNumber_txt.get(),Quantity_txt.get(),ItemName_txt.get(),ItemLocation_txt.get(),ItemDes_txt.get()))
                self.tree.insert('', 'end', values=(ItemNumber_txt.get(),Quantity_txt.get(),ItemName_txt.get(),ItemLocation_txt.get(),ItemDes_txt.get()))
                ItemNumber_txt.set("")
                Quantity_txt.set("")
                ItemName_txt.set("")
                ItemLocation_txt.set("")
                ItemDes_txt.set("")
                msort(Item_list)
                sortby(self.tree,0,0)
            except ValueError:
                messagebox.showwarning("Warning",("Make sure the all item categories are filled correctly and try again!"))
            except AssertionError:
                messagebox.showwarning("Warning",("Make sure the all item categories are filled in and try again!"))
            except Exception:
                messagebox.showwarning("Warning",("That item already exists! Try the update button!"))

        def delete():
            try:
                ItemListIndex = search(Item_list,ItemNumber_txt.get())
                IIDn = self.tree.get_children()
                
                curItem = self.tree.focus()
                if curItem != '':                
                    dictRow = self.tree.item(curItem)
                    values = dictRow['values']
                    values[0] = str(values[0])
                    values[1] = str(values[1])
                    values=tuple(values)
                    
                if ItemNumber_txt.get() == '' and curItem != '':
                    if messagebox.askyesno("Confirm",("Are you sure you want to delete item"+" " + values[0]+"?")):
                        self.tree.delete(curItem)
                        Item_list.pop(search(Item_list,values[0]))
                elif ItemNumber_txt.get() != '' and curItem == '' and ItemListIndex != None:
                    if messagebox.askyesno("Confirm","Are you sure you want to delete item"+" "+ItemNumber_txt.get()+"?"):
                        Item_list.pop(ItemListIndex)
                        self.tree.delete(IIDn[ItemListIndex])
                elif ItemNumber_txt.get() != '' and curItem != '' and ItemNumber_txt.get() != values[0] and ItemListIndex != None:
                    if messagebox.askyesno("Confirm","Are you sure you want to delete item"+" "+ItemNumber_txt.get()+"?"):
                        Item_list.pop(ItemListIndex)
                        self.tree.delete(IIDn[ItemListIndex])
                elif ItemNumber_txt.get() == values[0] and curItem != '':
                    if messagebox.askyesno("Confirm","Are you sure you want to delete item"+" "+ItemNumber_txt.get()+"?"):
                        self.tree.delete(curItem)
                        Item_list.pop(search(Item_list,values[0]))
                else:
                    raise Exception("You haven't selected anything to delete!")
            except Exception:
                pass
                ItemNumber_txt.set("")
                Quantity_txt.set("")
                ItemName_txt.set("")
                ItemLocation_txt.set("")
                ItemDes_txt.set("")
        #Uses previously defined binary search to display the searched item  
        def searchfun():
            try:
                ItemListIndex = search(Item_list,Search_txt.get())
                assert (Search_txt.get().isdigit()),"That is not a proper item number!"
                if ItemListIndex == None:
                    raise Exception
                IIDn = self.tree.get_children()

                self.tree.selection_set(IIDn[ItemListIndex])
                
                ItemNumber_txt.set(Item_list[ItemListIndex][0])
                Quantity_txt.set(Item_list[ItemListIndex][1])
                ItemName_txt.set(Item_list[ItemListIndex][2])
                ItemLocation_txt.set(Item_list[ItemListIndex][3])
                ItemDes_txt.set(Item_list[ItemListIndex][4])
            except AssertionError:
                messagebox.showwarning("Warning","Please enter a properly formatted item number!")
            except Exception:
                messagebox.showwarning("Warning","That item is not in the database! YET!")
        def update():
            try:
                if ItemNumber_txt.get() == '' or (Quantity_txt.get()== '' and ItemName_txt.get()== '' and ItemLocation_txt.get()=='' and ItemDex_txt.get() ==''):
                    raise Exception ("Nothing to update")
                if not ItemNumber_txt.get().isdigit() or not Quantity_txt.get().isdigit():
                    raise ValueError
                ItemListIndex = search(Item_list,ItemNumber_txt.get())
                assert (ItemListIndex != None),"The item you are trying to update does not exist, maybe try the add fuction!"
                IIDn = self.tree.get_children()

                Item_list[ItemListIndex] = (ItemNumber_txt.get(),Quantity_txt.get(),ItemName_txt.get(),ItemLocation_txt.get(),ItemDes_txt.get())
                self.tree.item(IIDn[ItemListIndex],option=None, values=(ItemNumber_txt.get(),Quantity_txt.get(),ItemName_txt.get(),ItemLocation_txt.get(),ItemDes_txt.get()))

                ItemNumber_txt.set("")
                Quantity_txt.set("")
                ItemName_txt.set("")
                ItemLocation_txt.set("")
                ItemDes_txt.set("")
            except AssertionError:
                messagebox.showwarning("Warning","The item you are trying to update does not exist! Try the add button!")
            except Exception:
                messagebox.showwarning("Warning","You haven't put enough information to update anything!")
            except ValueError:
                messagebox.showwarning("Warning","You have entered something incorrectly! Please review the information you are trying to update and try again!")
        def load():    
            try:
                tlist=[]
                    
                f = filedialog.askopenfile(mode='r',defaultextension=".txt")
                if f is None:
                    return
                
                for line in f:
                    for word in line.split(','):
                        tlist.append(word)
                for item in tlist:
                    tlist = list(map(str.rstrip, tlist))
                for i in range(len(tlist)):
                    tlist[i] = str(tlist[i])
                        
                if (len(tlist)%5==0):
                    tlist= [tuple(tlist[i:i+5]) for i in range(0,len(tlist),5)]
                else:
                    raise Exception("File Not Formatted Properly")
                f.close
                
                IIDn = self.tree.get_children()
                
                for i in range(len(IIDn)):
                    self.tree.delete(IIDn[i])
                msort(tlist)
                for i in range(len(tlist)):
                    self.tree.insert('', 'end', values=(tlist[i][0],tlist[i][1],tlist[i][2],tlist[i][3],tlist[i][4]))

                Item_list.clear()
                Item_list.extend(tlist)
            except Exception:
                messagebox.showwarning("Warning",("The file you tried to open was not formatted properly!"))
        # create buttons
        New_Button = ttk.Button(text = "New", command= add)
        New_Button.grid(column=0, row = 8, sticky = "W",in_=container,padx=20,pady=5)

        Update_Button = ttk.Button(text = "Update", command= update)
        Update_Button.grid(column=0, row = 8, sticky = "W",in_=container,pady=5,padx=115)

        Load_Button = ttk.Button(text = "Load (By filename.txt)", command= load)
        Load_Button.grid(column=0, row = 0, sticky = "W",pady=5,in_=container)

        Search_Button = ttk.Button(text = "Search (By Item Number)", command= searchfun)
        Search_Button.grid(column=0, row = 0, sticky = "E",padx=140,pady=5,in_=container)

        Save_Button = ttk.Button(text = "Save", command=save)
        Save_Button.grid(column=0, row = 8, sticky = "E",in_=container,pady=5)

        Delete_Button = ttk.Button(text = "Delete", command= delete)
        Delete_Button.grid(column=0, row = 8, sticky = "E",in_=container,pady=5,padx=95)

    def _build_tree(self):
        for col in header:
            self.tree.heading(col, text=col.title())
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in Item_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width dynamically
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(header[ix],width=None)<col_w:
                    self.tree.column(header[ix], width=col_w)

# generic methods that don't need to be in the app class as they don't contribute to formatting.   
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    for i in range(len(data)):
        data[i] = list(data[i])
    for i in range(len(data)):
        data[i][0] = int(data[i][0])
    for i in range(len(data)):
        data[i] = tuple(data[i])
    #sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    for i in range(len(data)):
        data[i] = list(data[i])
    for i in range(len(data)):
        data[i][0] = str(data[i][0])
    for i in range(len(data)):
        data[i] = tuple(data[i])

#Mergesort
def msort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        msort(lefthalf)
        msort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if int(lefthalf[i][0]) < int(righthalf[j][0]):
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
    return alist

#Binary search but for indexes
def search(alist,itemnum):
            if len(alist) == 0:
                pass
            else:
                midpoint = len(alist)//2
                if alist[midpoint][0]==itemnum:
                    return Item_list.index(alist[midpoint])
                else:
                    if itemnum<alist[midpoint][0]:
                        return search(alist[:midpoint],itemnum)
                    else:
                        return search(alist[midpoint+1:],itemnum)

def save():
        f = filedialog.asksaveasfile(mode='w',defaultextension=".txt")
        if f is None:
            return
        
        for i in range(len(Item_list)):
            for n in range(len(Item_list[i])):
                if n < len(Item_list[i])-1:
                    f.write(Item_list[i][n] + ",")
                else:
                    f.write(Item_list[i][n])
            f.write("\n")
        f.close()

# main method        
if __name__ == '__main__':
    Item_list = msort(Item_list)
    root = tk.Tk()
    root.title("RestEasy Inventory")
    listbox = app()
    root.mainloop()
