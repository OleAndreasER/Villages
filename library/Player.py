class Player:
    resources = {
        "wood": 0,
        "stone": 0
    }

    def hasResources(self, cost):
        return all(self.resources[resource] >= amount
                   for resource, amount in cost.items())

    def spend(self, cost): #assuming hasResources
        for resource, amount in cost.items():
            self.resources[resource] -= amount
            
currentPlayer = Player()
