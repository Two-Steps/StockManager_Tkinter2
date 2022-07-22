class Product:

    def __init__(self,
        id = None,
        imgPath = '',
        name = '',
        description = '',
        stockQuantity = 0
    ):
        self.id = id
        self.imgPath = imgPath
        self.name = name
        self.description = description
        self.stockQuantity = stockQuantity

class DataManager:
    MEM_DB = [
        Product(1, 'image\\apple.png', 'Apple', 'This is an apple', 12),
        Product(2, 'image\kiwi.png', 'Kiwi', 'Nice fruit!', 120),
        Product(3, 'image\luu.png', 'Luu', 'I love this', 400),
        Product(4, 'image\mango.png', 'Mango', 'Eat eat eat', 5),
        Product(5, 'image\_apple.png', 'Apple', 'This is an apple2', 635),
        Product(6, 'image\kiwi.png', 'Kiwi', 'This is an kiwi', 54),
        Product(7, 'image\luu.png', 'Luu', 'This is an luu', 9),
        Product(8, 'image\mango.png', 'Mango', 'This is an mango', 120),
        Product(9, 'image\kiwi.png', 'Kiwi', 'This is an kiwi2', 95),
        Product(10, 'image\mango.png', 'Mango', 'This is an mango2', 248)
    ]

    def get(maxItemsPerPage, pageNumber, name: str, stockBelow: int):

        startInd = maxItemsPerPage * (pageNumber - 1)
        endInd = startInd + maxItemsPerPage
        data = DataManager.MEM_DB
        data = DataManager.filterData(data, name, stockBelow)
        return data[startInd:endInd]
    
    def total(name: str, stockBelow: int):
        # todo something for search
        data = DataManager.MEM_DB
        data = DataManager.filterData(data, name, stockBelow)
        return len(data)

    def filterData(data, name: str, stockBelow: int):

        if name:
            data = [x for x in data if name.lower() in x.name.lower()]

        if stockBelow:
            data = [x for x in data if x.stockQuantity <= stockBelow]

        return data
    
    def deleteProducts(idList):
        DataManager.MEM_DB = [
            x for x in DataManager.MEM_DB if x.id not in idList
        ]


