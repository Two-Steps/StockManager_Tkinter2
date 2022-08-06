from doctest import master
from tkinter import *
from tkinter import ttk
import os.path as path
import tkinter.filedialog as filedialog

from dataManagement2 import*
import utilities as utils

class ProductEditor(Toplevel):
    
    def __init__(self, master: Tk, product: Product, callback_onAddEdit):

        self.product = product
        self.callback_onAddEdit = callback_onAddEdit
        # sử dụng lại hàm khởi tạo của lớp cha - Toplevel 
        # để sử dụng toàn bộ hàm, thuộc tính của nó vì ta đã viết lại hàm khởi
        # tạo của riêng class con ProductEditor
        # nhớ xem lại OOP Python
        super().__init__(master=master)

        titleText = 'Add new product'
        if self.product.id:
            titleText = f'Edit product: {product.name}'
        self.title(titleText)

        width = 800
        height = 300
        self.geometry(f'{width}x{height}')
        self.resizable(False, False)

        frameImageWidth = width*0.3
        frameNameDescWidth = width*0.5
        frameStockAddUpdateWidth = width*0.2

        frameImage = Frame(master=self,
            width=frameImageWidth,
            height=height,
            # bg='red'
        )

        frameNameDesc = Frame(master=self,
            width=frameNameDescWidth,
            height=height,
            # bg='green'
        )

        frameStockAddUpdate = Frame(master=self,
            width=frameStockAddUpdateWidth,
            height=height,
            # bg='blue'
        )

        frameImage.pack(side=LEFT)
        frameNameDesc.pack(side=LEFT)
        frameStockAddUpdate.pack(side=LEFT)

        self._BuildFrameImageContent(frameImage)
        self._BuildFrameNameDescContent(frameNameDesc)
        self._BuildFrameStockAddUpdateContent(frameStockAddUpdate)

        # END def __init__

    def _BuildFrameImageContent(self, parent: Frame):
        
        parentWidth = parent.winfo_reqwidth()
        parentHeight = parent.winfo_reqheight()

        frameImageHeight = int(parentHeight*0.9)
        frameBtnHeight = int(parentHeight*0.1)

        frameImage = Frame(master=parent,
            width=parentWidth, height=frameImageHeight,
            # bg='orange'
        )
        frameBtn = Frame(master=parent,
            width=parentWidth, height=frameBtnHeight,
            # bg='purple'
        )
        frameImage.pack()
        frameBtn.pack()
        frameImage.propagate(False)
        frameBtn.propagate(False)

        imgText = self.product.name if self.product.id else 'Choose an image'
        lblImage = Label(master= frameImage, text= imgText)

        if path.exists(self.product.imgPath):
            utils.loadImageToLabel(lblImage,
                self.product.imgPath,
                parentWidth,
                frameImageHeight
            )
        lblImage.pack(expand=True)

        btnBrowseImage = Button(master=frameBtn,
            text= 'Open Image',
            command= self._action_browseImageFiles
        )
        btnBrowseImage.pack(expand=True)

        # Access globally
        self.frameImage_lblImage = lblImage
        self.frameImage_lblImage_imgPath = self.product.imgPath
        self.frameImage_width = parentWidth
        self.frameImage_height = frameImageHeight

    # END _BuildFrameImageContent

    def _BuildFrameNameDescContent(self, parent: Frame):
        
        parentWidth = parent.winfo_reqwidth()
        parentHeight = parent.winfo_reqheight()

        frameNameHeight = parentHeight*0.2
        frameDescHeight = parentHeight*0.8

        labelFrameName = LabelFrame(master=parent,
            width=parentWidth, height=frameNameHeight,
            text='Name'
        )
        labelFrameDesc = LabelFrame(master=parent,
            width=parentWidth, height=frameDescHeight,
            text='Description'
        )
        labelFrameName.pack()
        labelFrameDesc.pack()
        labelFrameName.propagate(False)
        labelFrameDesc.propagate(False)
        # singer line
        entryName = Entry(master=labelFrameName)
        entryName.insert(0, self.product.name)
        # multi line
        textDesc = Text(master=labelFrameDesc)
        textDesc.insert(1.0, self.product.description)

        entryName.pack(fill='x', ipady=5, padx=10)
        textDesc.pack(padx=10, pady=10)

        # Access globally
        self.frameNameDesc_entryName = entryName
        self.frameNameDesc_textDesc = textDesc

    # END _BuildFrameNameDescContent

    def _BuildFrameStockAddUpdateContent(self, parent: Frame):
        
        parentWidth = parent.winfo_reqwidth()
        parentHeight = parent.winfo_reqheight()

        frameStockHeight = parentHeight*0.8
        frameAddEditHeight = parentHeight*0.2

        frameStock = Frame(master=parent,
            width=parentWidth, height=frameStockHeight,
            # bg='blue'
        )
        frameAddEdit = Frame(master=parent,
            width=parentWidth, height=frameAddEditHeight,
            # bg='orange'
        )

        frameStock.pack()
        frameAddEdit.pack()
        # ngăn wiget con thay đổi size wiget cha
        frameStock.propagate(False)
        frameAddEdit.propagate(False)

        lblStock = Label(master=frameStock, text='Stock Quantity:')
        spinValue = self.product.stockQuantity if self.product.id else 0
        spinboxVar = IntVar(value= spinValue)
        spinboxStock = Spinbox(master=frameStock,
            from_ = 0,
            to= 5000,
            width=5,
            justify='right',
            textvariable= spinboxVar
        )

        lblStock.pack(side=LEFT, padx=10)
        spinboxStock.pack(side=LEFT)

        btnAddEdit = Button(master=frameAddEdit,
            text='Update' if self.product.id else 'Add',
            command=self._action_addUpdateProduct
        )
        btnAddEdit.pack(expand=True)

        # Access globally
        self.frameStock_spinboxVar = spinboxVar

    # END _BuildFrameStockAddUpdateContent

    #-------------------------------
    # ACTION
    # FRAME IMAGE
    def _action_browseImageFiles(self):
        # vì filedialog.askopenfilename trả về tên path file 
        # nên đặt nó là 1 biến để xài luôn
        filename = filedialog.askopenfilename(
            # nếu viết thế này: khi đóng sẽ hiện màn hình chính (main program)
            # master = self,
            # nếu viết thế này: khi đóng quay về screen add/edit
            parent=self,
            title='Select a File',
            filetypes= [
                ('image files', '.png'),
                ('image files', '.jpg'),
                ('image files', '.jpeg')
            ]
        )

        # update frameImage_lblImage_imgPath
        self.frameImage_lblImage_imgPath = filename
        if filename:
            utils.loadImageToLabel(
                self.frameImage_lblImage,
                filename,
                self.frameImage_width,
                self.frameImage_height
            )

    # FRAME NAME AND DESCRIPTION


    # FRAME STOCK AND ADD/UPDATE
    def _action_addUpdateProduct(self):
        # step1: lấy mọi biến ta cần và ném nó vào self (Access globally đó)
        # step2:
        # self.product.name = self.frameNameDesc_entryName.get()
        product = Product()
        product.id = self.product.id
        product.name = self.frameNameDesc_entryName.get()
        product.description = self.frameNameDesc_textDesc.get(1.0, END)
        product.stockQuantity = self.frameStock_spinboxVar.get()
        product.imgPath = self.frameImage_lblImage_imgPath

        # to do save this and reload list of products
        self.callback_onAddEdit(product)

        self.destroy()