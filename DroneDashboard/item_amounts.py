class item_amounts:
    intialValues = {
    "Bandaids": 0,
    "Gauzes": 0,
    "Alcohol Wipes": 0,
    "Ointment": 0,
    "Gloves": 0
    }
    currentItem = 'Bandaids'
    
    def __init__(self) -> None:
        pass
    
    def updateValue(self, itemName, amount):
        item_amounts.intialValues[itemName] = amount
        
    def updateCurrentItem(self, itemName):
        item_amounts.currentItem = itemName