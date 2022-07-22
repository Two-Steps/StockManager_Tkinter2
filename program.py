from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter.font import Font
from tkinter import messagebox
import os.path as path
import math
from dataManagement import *
import utilities as utils

class MyStockManage:
    def __init__(self):

        # config
        w_width = 700
        w_height = 600
        frame_search_width = w_width
        frame_product_width = w_width
        frame_add_del_width = w_width
        frame_search_height = int(w_height * 0.05)
        frame_product_height = int(w_height * 0.9) 
        frame_add_del_height = int(w_height * 0.05)
        # DEFINE GLOBAL VARIABLES
        self.defineGlobalVar()

        # window
        self.window = Tk()
        root = self.window
        root.geometry(f'{w_width}x{w_height}+300+10')
        root.resizable(width=False, height=False)
        root.title('Stock manage')
        # phải đặt khởi tạo font sau khi khởi tạo window
        self.defineGlobalFont()
        # todo frame
        frameSearch = Frame(master=root,
            width=frame_search_width, height=frame_search_height,
            # bg='#1ef78e'
        )
        frameProduct = Frame(master=root,
            width=frame_product_width, height=frame_product_height,
            # bg='#faf9b4'
        )
        frameAddDel = Frame(master=root,
            width=frame_add_del_width, height=frame_add_del_height,
            # bg='#faa2c8'
        )
        frameSearch.pack()
        frameProduct.pack()
        frameAddDel.pack()
        # build frame content
        self.BuildSearchContent(frameSearch)
        self.BuildProductContent(frameProduct)
        self.BuildAddDelContent(frameAddDel)

        root.mainloop()
        # end def init
    # DEFINE GLOBAL VARIABLES
    def defineGlobalVar(self):
        self.spinboxSearchVar = 25
        self.spinboxSearchMin = 5
        self.spinboxSearchMax = 3000
        self.maxItemPerPage = 4
        self.productColFrames = []
        self.currentPage = 1
        self.totalPage = -1
        self.searchName = None
        self.searchStockBelow = None
        self.productsToDelete = []

    #  DEFINE GLOBAL FONTS
    def defineGlobalFont(self):
        self.fontTimeBold = Font(family='Times', size=12, weight='bold')
        self.fontTime = Font(family='Times', size=12)
        self.fontBookAntiq = Font(family='Book Antiqua', size=10)

    # FRAME SEARCH
    def BuildSearchContent(self, parent: Frame):
        lblName = Label(master=parent, text='Product Name:', font=self.fontTimeBold)
        txtEntryName = StringVar(value=self.searchName)
        entryName = Entry(master=parent, 
            justify='center',
            font=self.fontTime,
            textvariable= txtEntryName
        )
        lblStock = Label(master=parent, text='Stock Below:', font=self.fontTimeBold)
        var = IntVar(value=self.spinboxSearchVar)
        spinboxStock = Spinbox(master=parent,
            from_=self.spinboxSearchMin,
            to= self.spinboxSearchMax,
            justify=RIGHT,
            width=5,
            font='aria 10',
            textvariable=var,
            state='readonly',
            increment= 5
        )
        btnSearch = Button(master=parent,
            text='Search',
            font=self.fontBookAntiq,
            command=lambda x= txtEntryName, y= var : self.action_search(x, y),
        )
        btnClear = Button(master=parent,
            text='Clear',
            font=self.fontBookAntiq,
            command=lambda x= entryName, y= var : self.action_clear(x, y)
        )

        lblName.pack(side=LEFT, padx=(0, 10))
        entryName.pack(side=LEFT, padx=(0, 10))
        lblStock.pack(side=LEFT, padx=(0, 10))
        spinboxStock.pack(side=LEFT, padx=(0, 10))
        btnSearch.pack(side=LEFT, padx=(0, 10))
        btnClear.pack(side=LEFT, padx=(0, 10))

    # FRAME PRODUCT
    def BuildProductContent(self, parent: Frame):
        parentWidth = parent.winfo_reqwidth()
        parentHeight = parent.winfo_reqheight()

        frameProsListWidth = parentWidth
        framePagesNavWidth = parentWidth

        frameProsListHeight = int(parentHeight * 0.95)
        framePagesNavHeight = int(parentHeight * 0.05)

        frameProsList = Frame(master=parent,
            width=frameProsListWidth,
            height=frameProsListHeight,
            # bg='#faf9b4'
        )
        framePagesNav = Frame(master=parent, 
            width=framePagesNavWidth,
            height=framePagesNavHeight,
            # bg = '#faa2c8'
        )
        frameProsList.pack()
        framePagesNav.pack()
        self.BuildProsListContent(frameProsList)
        self.BuildPagesNavContent(framePagesNav)

        # self.loadProductsList()
        # self.loadPagesNav(loadTotalPages=True)
        self.refresh_FrameProductsContent(loadTotalPages=True)

    def refresh_FrameProductsContent(self, 
        loadTotalPages,
        setCurrentPageTo: int = None
        ):
        if setCurrentPageTo:
            self.currentPage = setCurrentPageTo
        self.loadPagesNav(loadTotalPages=loadTotalPages)
        # load lại số trang trước rồi load lại sản phẩm sau
        self.loadProductsList()

    # Product List content
    def BuildProsListContent(self, parent: Frame):
        parentWidth = parent.winfo_reqwidth()
        parentHeight = parent.winfo_reqheight()
        frameProsRowHeight = int(parentHeight / 4)
        colors = ['#1ef78e', '#faf9b4', '#faa2c8', '#1ef78e']
        # hàm vẽ 1 dòng kẻ màu xám -> easy mà
        def drawGreyLine():
            Frame(master=parent,
                width=parentWidth,
                height=1,
                bg='grey'
            ).pack()
        drawGreyLine()
        for i in range(self.maxItemPerPage):
            frameProsRow = Frame(master=parent,
                width=parentWidth,
                height=frameProsRowHeight,
                # bg=colors[i]
            )
            frameProsRow.pack()
            self.BuildProsListRowContent(frameProsRow)
            drawGreyLine()

    # Build nội dung từng row trong products list
    def BuildProsListRowContent(self, parent: Frame):
        parentWidth = parent.winfo_reqwidth()
        parentHeight = parent.winfo_reqheight()
        frameColumnsWidthList = [
            parentWidth * 0.2,
            parentWidth * 0.6,
            parentWidth * 0.1,
            parentWidth * 0.1
        ]
        self.productColFrames.append([])
        for colWidth in frameColumnsWidthList:
            frameColumn = Frame(master=parent,
                width=colWidth,
                height=parentHeight,
                highlightbackground='black',
                highlightthickness=1
            )
            frameColumn.pack(side=LEFT)
            # làm gì đó - đợi tra gg nha
            # thuộc tính "proagate" để xác định xem UI con có quyết định kích thước
            # UI cha hay không ? nếu UI con nhỏ hơn thì sẽ kéo width UI cha xuống = width UI con
            frameColumn.propagate(False)
            self.productColFrames[-1].append(frameColumn)

    # Pages Navigation content
    def BuildPagesNavContent(self, parent: Frame):
        lblCurrentPageOfN = Label(master=parent,
            text= '1 of 2',
            font=self.fontTime
        )
        btnPrevPage = Button(master=parent,
            text='<<',
            font=self.fontBookAntiq,
            command=self.action_prev_page
        )
        btnNextPage = Button(master=parent,
            text='>>',
            font=self.fontBookAntiq,
            command=self.action_next_page
        )
        btnPrevPage.pack(side=LEFT, padx=(0,10))
        lblCurrentPageOfN.pack(side=LEFT, padx=(0,10))
        btnNextPage.pack(side=LEFT, padx=(0,10))

        # Access globally - phục vụ việc refresh tab nav
        self.framePageNav_btnPrevPage = btnPrevPage
        self.framePageNav_lblCurrentPageOfN = lblCurrentPageOfN
        self.framePageNav_btnNextPage = btnNextPage

    # Refresh something
    def refresh_btnPrevPage(self):
        
        newState = ACTIVE
        if self.currentPage <= 1:
            newState = DISABLED
        self.framePageNav_btnPrevPage.configure(state=newState)

    def refresh_lblCurrentPageOfN(self):
        
        newText = f'{self.currentPage} of {self.totalPage}'
        self.framePageNav_lblCurrentPageOfN.configure(text=newText)

    def refresh_btnNextPage(self):

        newState = ACTIVE
        if self.currentPage >= self.totalPage:
            newState = DISABLED
        self.framePageNav_btnNextPage.configure(state=newState)

    # FRAME ADD DEL
    def BuildAddDelContent(self, parent: Frame):
        btnAddProduct = Button(master=parent, 
        text='Add Product',
        command=self.action_add_product
        )
        btnDelProducts = Button(master=parent, 
        text='Del Products',
        command=self.action_del_products,
        state=DISABLED
        )
        btnAddProduct.pack(side=LEFT)
        btnDelProducts.pack(side=LEFT)

        # access globally
        self.g_frameAddDelete_btnDelProducts = btnDelProducts
    
    # reset the product to delete
    def reset_productsToDelete(self):
        self.productsToDelete = []
        self.g_frameAddDelete_btnDelProducts.configure(state=DISABLED)

    # ACTION
    # - Add and Delete content
    def action_add_product(self):
        print('Add Product')

    def action_del_products(self):
        # create box message
        answer = messagebox.askyesno(
            title='Delete Product',
            message='Are you sure that you want to delete?'
        )
        if answer:
            DataManager.deleteProducts(self.productsToDelete)
            
            # xóa xong nhớ refresh
            self.refresh_FrameProductsContent(
                loadTotalPages=True
            )

    # - Product content
    # -- product list
    def action_markForDelete(self, productId, variable: BooleanVar):
        # kiểm tra xem btn xóa có click hay k
        if variable.get():
            # thêm id product vào list sẽ xóa
            self.productsToDelete.append(productId)
        else:
            self.productsToDelete.remove(productId)
        # list id product xóa có ít nhất 1 phần tử => active nút xóa
        if len(self.productsToDelete) > 0:
            self.g_frameAddDelete_btnDelProducts.configure(state=ACTIVE)
        else:
            self.g_frameAddDelete_btnDelProducts.configure(state=DISABLED)

        print(self.productsToDelete)

    def action_prev_page(self):
        
        self.currentPage -= 1
        self.refresh_FrameProductsContent(loadTotalPages=False)

    def action_next_page(self):
        self.currentPage += 1
        self.refresh_FrameProductsContent(loadTotalPages=False)
        
    # - Search content
    def action_search(self, name: Entry, stock: IntVar):
        
        self.searchName = name.get()
        self.searchStockBelow = stock.get()

        self.refresh_FrameProductsContent(loadTotalPages=True,
            setCurrentPageTo = 1
        )


    def action_clear(self, name: Entry, stock: IntVar):
        self.searchName = None
        self.searchStockBelow = None

        name.delete(0, END)
        stock.set(self.spinboxSearchVar)

        self.refresh_FrameProductsContent(
            loadTotalPages=True,
            setCurrentPageTo=1
        )
    # LOADERS
    # hàm lấy danh sách phần tử theo trang hiện tại
    # nói rõ hơn thì lấy từng row - ứng với 1 phtu trong productColFrames
    def loadProductsList(self):

        # reset product to delete
        # khi biến g_frameAddDelete_btnDelProducts được khởi tạo rồi
        # hay khi ProductAddDelContent đã được khởi tạo thì mới reset
        # productsToDelete
        if hasattr(self,'g_frameAddDelete_btnDelProducts'):
            self.reset_productsToDelete()

        # clear products in GUI
        # xóa dữ liệu cũ đi đã rồi mới tải cái mới
        for row in self.productColFrames:
            # print('row',row)
            column: Frame
            for column in row:
                # print('column',column)
                children = column.children
                # print('child',children.items())
                value : Widget
                for key, value in children.items():
                    value.pack_forget()
        # Get products and draw in GUI
        # tải dữ liệu
        products = DataManager.get(
            self.maxItemPerPage,
            self.currentPage,
            self.searchName,
            self.searchStockBelow
            # todo something - khi search
        )
        for ind, product in enumerate(products):
            # enumerate là 1 buid-in funtion giúp duyệt qua list như với 
            # collection dưới dạng cặp index-value
            # viết kiểu này giúp nhanh chóng lấy được index kèm với từng giá
            # trị trong list 1 cách nhanh chóng -- Okay, 1 thứ hay ho
            # dòng dưới: đưa từng dòng sản phẩm vào frame rowColsFrames
            # ứng với 1 sản phẩm - product (xem lại def BuildProsListRowContent)
            # để tải dữ liệu theo thứ tự ảnh, tên - mô tả, số lượng, del button
            rowColsFrames = self.productColFrames[ind]

            self.loadProductRow(rowColsFrames, product)
            

    # lấy dữ liệu của từng cột trong 1 dòng - load dữ liệu cả 1 dòng
    def loadProductRow(self, rowColsFrames, product: Product):
        # tải dữ liệu ảnh - chia nhỏ quá @@
        self.loadImage(rowColsFrames[0], product)
        # tải dữ liệu tên mô tả
        self.loadNameDesc(rowColsFrames[1], product)
        # tải dữ liệu số lượng
        self.loadStockQuantity(rowColsFrames[2], product)
        # tải check button delete
        self.loadDeleteCheckButton(rowColsFrames[3], product)

    # def load image
    def loadImage(self, parent: Frame, product: Product):
        
        lblImage = Label(master=parent)
        lblImage.pack(expand=True)
        if path.exists(product.imgPath):
            imgWidth = parent.winfo_reqwidth()
            imgHeight = parent.winfo_reqheight()

            imgPath = product.imgPath
            utils.loadImageToLabel(lblImage, imgPath, imgWidth, imgHeight)
        else:
            lblImage.configure(text='No Image')
        

    # def load name description
    def loadNameDesc(self, parent: Frame, product: Product):
        parentWidth = parent.winfo_reqwidth()
        parentHeight = parent.winfo_reqheight()

        frameNameHeight = int(parentHeight * 0.1)
        frameDescHeight = int(parentHeight * 0.9)

        frameName = Frame(master=parent,
            width=parentWidth,
            height=frameNameHeight,
            # bg = 'red'
        )
        frameDesc = Frame(master=parent,
            width=parentWidth,
            height=frameDescHeight,
            # bg = 'green'
        )
        frameName.pack()
        frameDesc.pack()
        lblName = Label(master=frameName,
            text=product.name,
            font=self.fontTime
        )
        lblDesc = Label(master=frameDesc,
            text=product.description,
            font=self.fontTime
        )
        lblName.pack()
        lblDesc.pack()


    # def load stock quantity
    def loadStockQuantity(self, parent: Frame, product: Product):
        lblStockQuantity = Label(master=parent, text=product.stockQuantity, font=self.fontTime)
        lblStockQuantity.pack(expand=True) 
        # tham số expand có vè đặt nó chính giữa UI cha, maybe là thế

    # def load delete checkbutton
    def loadDeleteCheckButton(self, parent: Frame, product: Product):
        var = BooleanVar(value=False)
        pid = product.id
        checkBtnDel = Checkbutton(master=parent,
            variable=var,
            command= lambda x = pid, y = var: self.action_markForDelete(x,y)
        )
        checkBtnDel.pack(expand=True)

    def loadPagesNav(self, loadTotalPages = False):
        
        if loadTotalPages:
            totalItems = DataManager.total(
                self.searchName,
                self.searchStockBelow
            )
            self.totalPage = math.ceil(totalItems/self.maxItemPerPage)
        # fix bug sau khi xóa product số trang bị lớn hơn tổng
        if self.currentPage > self.totalPage:
            self.currentPage = self.totalPage

        self.refresh_btnPrevPage()
        self.refresh_btnNextPage()
        self.refresh_lblCurrentPageOfN()
MyStockManage()