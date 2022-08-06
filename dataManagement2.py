from os import remove
import uuid
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
    f = open('data.txt', 'r', encoding='utf-8')
    data = f.read()
    data = data.split('\n')
    # print(data)
    for i in range(len(data)):
        if data[i] != '':
            if len(data[i]) < 20:
                data[i-1] += data[i]
                data[i] = ''
    # print(data)
    while '' in data:
        data.remove('')

    pro = []
    MEM_DB = []
    if len(data):
        for i in range(len(data)):
            pro = data[i].split(',')
            # print(pro)
            p = Product(pro[0],pro[1],pro[2],pro[3],int(pro[4]))
            MEM_DB.append(p)
    # print(MEM_DB[0].id)

    # function to change data.txt if MEM_DB changed
    def change_data(MEM_DB):
        f = open('data.txt','w',encoding='utf-8')
        pro = ''
        prod: Product
        for prod in MEM_DB:
            pro = pro + str(prod.id) + ',' + prod.imgPath + ','\
                + prod.name + ',' + prod.description + ',' + str(prod.stockQuantity) + '\n'
            f.write(pro)
            pro = ''
        f.close()
    
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
    
    # need update to change file data.txt
    def deleteProducts(idList):
        DataManager.MEM_DB = [
            x for x in DataManager.MEM_DB if x.id not in idList
        ]

        DataManager.change_data(DataManager.MEM_DB)


    def updateProduct(product: Product):

        prod: Product
        for pidx, prod in enumerate(DataManager.MEM_DB):
            if prod.id == product.id:
                DataManager.MEM_DB[pidx] = product
                break

        DataManager.change_data(DataManager.MEM_DB)

    def insertProduct(product: Product):
        
        product.id = str(uuid.uuid1())
        DataManager.MEM_DB.append(product)

        DataManager.change_data(DataManager.MEM_DB)


DataManager()



