from shipment import orderShipment
import unittest

class TestOrderShipment(unittest.TestCase):

    def validateOrderMatch(self, o1, o2):
        delta = [missing for missing in o1 + o2 if missing not in o1 or missing not in o2]
        return len(delta) == 0

    def test_BasicShipFromHappyLocation(self):
        apple = "apple"
        owd = "owd"
        inventory = "inventory"
        name = "name"
        order = { apple: 1 }
        warehouses = [{ name: owd, inventory: { apple: 1 } }]
        result = [{ owd: { apple: 1 } }]
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))
    
    def test_BasicShipFromMultipleLocations(self):
        apple = "apple"
        owd = "owd"
        dm = "dm"
        inventory = "inventory"
        name = "name"
        order = { apple: 10 }
        warehouses = [{ name: owd, inventory: { apple: 5 } }, { name: dm, inventory: { apple: 5 }}]
        result = [{ dm: { apple: 5 }}, { owd: { apple: 5 } }]
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))

    def test_NoInventory(self):
        apple = "apple"
        owd = "owd"
        inventory = "inventory"
        name = "name"
        order = { apple: 1 }
        warehouses = [{ name: owd, inventory: { apple: 0 } }]
        result = []
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))

    def test_IncompleteInventory(self):
        apple = "apple"
        owd = "owd"
        inventory = "inventory"
        name = "name"
        order = { apple: 2 }
        warehouses = [{ name: owd, inventory: { apple: 1 } }]
        result = []
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))
    
    def test_ShipFromMinimumLocations(self): 
        A = "A"
        B = "B"
        C = "C"
        D = "D"
        inventory = "inventory"
        name = "name"
        apple = "apple"

        order = { apple: 2 }
        warehouses = [{ name: A, inventory: { apple: 1 } }, { name: B, inventory: { apple: 2 } }] 
        result = [{ B: { apple: 2 } }]
        # choose second location instead of first and second
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))

        order = { apple: 2 }
        warehouses = [{ name: A, inventory: { apple: 1 } }, { name: B, inventory: { apple: 1 } }, { name: C, inventory: { apple: 2 } }] 
        result = [{ C: { apple: 2 } }]
        # choose third location instead of first and second
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))

        order = { apple: 4 }
        warehouses = [{ name: A, inventory: { apple: 1 } }, { name: B, inventory: { apple: 1 } }, { name: C, inventory: { apple: 2 } }, { name: D, inventory: { apple: 2 } }] 
        result = [{ C: { apple: 2 } }, { D: { apple: 2 } }]
        # choose third and fouth location instead of first and second and third
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))

    def test_ShipFromCheapestWarehousesGivenMultipleSolutions(self): 
        A = "A"
        B = "B"
        C = "C"
        inventory = "inventory"
        name = "name"
        apple = "apple"

        order = { apple: 4 }
        warehouses = [{ name: A, inventory: { apple: 1 } }, { name: B, inventory: { apple: 2 } }, { name: C, inventory: { apple: 3 } }] 
        result = [{ A: { apple: 1 } }, { C: { apple: 3 } }]
        # choose locations 1 and 3 instead of locations 2 and 3
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))
    
    def test_ShipMultipleGoodsFromMinimumLocations(self):
        A = "A"
        B = "B"
        C = "C"
        D = "D"
        inventory = "inventory"
        name = "name"
        apple = "apple"
        banana = "banana"

        order = { apple: 2, banana: 3}
        warehouses = [{ name: A, inventory: { apple: 1 , banana: 1} }, { name: B, inventory: { apple: 2 , banana: 1 } }, {name: C, inventory: { banana: 2 }}] 
        result = [{ B: {apple: 2, banana: 1} }, { C: {banana: 2} }]
        # choose second and third location instead of first, second and third
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))

    def test_ShipMultipleGoodsFromCheapestWarehousesGivenMultipleSolutions(self):
        A = "A"
        B = "B"
        C = "C"
        D = "D"
        inventory = "inventory"
        name = "name"
        apple = "apple"
        banana = "banana"

        order = { apple: 2, banana: 2}
        warehouses = [{ name: A, inventory: { apple: 1 , banana: 1} }, { name: B, inventory: { banana: 2 }}, {name: C, inventory:{ apple: 2 , banana: 1 } } ] 
        result = [{A: {apple: 1, banana: 1}}, { C: {apple: 1, banana: 1} }]
        # choose first and third location instead of second and third
        self.assertTrue(self.validateOrderMatch(result, orderShipment(warehouses, order)))

if __name__ == '__main__':
    unittest.main(verbosity=2)