from collections import defaultdict
class WarehousesManager:
    def __init__(self, warehouses):
        self.warehouses = warehouses
        self.absolute_inventory = defaultdict(int)
        self.loadWarehouses()

    def loadWarehouses(self):
        for warehouse in self.warehouses:
            inventory = warehouse["inventory"]
            for item, quantity in inventory.items():
                self.absolute_inventory[item] += quantity

    def isOrderPossible(self, order): 
        for item, quantity in order.items():
            if item not in self.absolute_inventory:
                return False
            if not quantity <= self.absolute_inventory[item]:
                return False
        return True
    
    def isOrderFulfilled(self, order, filled):
        if len(order) != len(filled):
            return False
        for order_item, order_quantity in order.items():
            if order_item not in filled:
                return False
            if filled[order_item] != order_quantity:
                return False
        return True

    def dfs(self, solution, solution_warehouses_used, order, currently_fulfilled, ls, capacity):
        # Using capacity to optimize solution, the idea being that once we have the first solution, 
        # we only want to look at other solutions of the same length or shorter than the first solution.
        # capacity will continue to update as we find smaller solutions, thus allowing us to ignore solutions
        # that have more warehouses and speed up the search
        if capacity is not None and len(solution) > capacity:
            return
        if self.isOrderFulfilled(order, currently_fulfilled):
            if capacity is None or capacity > len(solution):
                capacity = len(solution)
            ls.append(solution)
            return
        
        for i, warehouse in enumerate(self.warehouses):
            if i in solution_warehouses_used:
                continue

            name = warehouse["name"]
            inventory = warehouse["inventory"]

            filled = currently_fulfilled.copy()
            sol = solution.copy()
            sol_used = solution_warehouses_used.copy()

            shipment = {}
            for item, quantity in order.items():
                if item in inventory:
                    val = min(quantity - filled[item], inventory[item])
                    filled[item] += val
                    shipment[item] = val
            if len(shipment):
                sol.append({name: shipment})
                sol_used.add(i)

            self.dfs(sol, sol_used, order, filled, ls, capacity)

    def fulfillOrder(self, order):
        solutions = []
        capacity = None
        self.dfs([], set(), order, defaultdict(int), solutions, capacity)
        return sorted(solutions, key=lambda x : len(x))[0]
        #because of the way we are iterating over warehouses in dfs, when we sort by length,
        #it will also already be sorted by "priority" of cheapest warehouses

def orderShipment(warehouses, req):
    #checking feasibility of the order
    if not req or len(req) == 0 or not warehouses or len(warehouses) == 0:
        return []
    manager = WarehousesManager(warehouses)
    #checking if we can deliverr (pun intended) on the order
    if not manager.isOrderPossible(req):
        return []
    #now we know that we have a possible solution
    return manager.fulfillOrder(req)