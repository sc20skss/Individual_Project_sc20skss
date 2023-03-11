
class MCState():
    def __init__(self):
        self.chidren = []
        self.parent = self
        self.simulations = 0
        self.wins = 0
        self.visitCount = 0
    def Addchild(self, childstate):
        self.chidren.append(childstate)
    def GetChildren(self, parent):
        return parent.chidren
    def SetParent(self, parent):
        self.parent = parent
    def GetParent(slef, state):
        return state.parent
    def AddSimulations(self, num):
        self.simulations += num
    def GetSimulations(self, state):
        return self.simulations
    def AddWins(self, num):
        self.wins += num
    def GetWins(self, state):
        return state.wins
    def AddVisitCounts(self):
        self.visitCount += 1
    def GetVisitCounts(self):
        return self.visitCount

