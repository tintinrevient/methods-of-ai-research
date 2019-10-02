import csv

class LookUp:

    def __init__(self):
        self.list = []

    def load(self, filename):

        file = open(filename, "r")
        reader = csv.reader(file)

        for restaurantname, pricerange, area, food, phone, addr, postcode in reader:

            item = {"restaurantname": restaurantname, "pricerange": pricerange, "area": area, "food": food,
                    "phone": phone, "addr": addr, "postcode": postcode}
            self.list.append(item)

        file.close()



if __name__ == "__main__":

    lookup = LookUp()

    filename = "/Users/zhaoshu/Documents/workspace/methods-of-ai-research/part-1c/restaurantinfo.csv"
    lookup.load(filename)

    print(lookup.list)
