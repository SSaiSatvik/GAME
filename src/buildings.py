import numpy as np
import points as pt
import time
from characters import barbarians, dragons, balloons, archers, superarchers, healers
import king


class Building:
    def destroy(self):
        self.destroyed = True
        if self.type == 'wall':
            if(pt.level_of_building >= 3):
                vmap=self.V.map
                for i in range(len(vmap)):
                    for j in range(len(vmap[i])):
                        item = vmap[i][j].split(':')[0]
                        if(item == pt.SPAWN):
                            King = king.getHero(pt.hero)
                            if(abs(King.position[0] - self.position[0]) + abs(King.position[1] - self.position[1]) < 2):
                                King.deal_damage(self.self_damage)
                            troops = archers + superarchers + barbarians
                            for troop in troops:    
                                dist = abs(troop.position[0] - self.position[0]) + abs(troop.position[1] - self.position[1])
                                if(dist < 2):
                                    troop.deal_damage(self.self_damage)
                                
            self.V.remove_wall(self)
        elif self.type == 'hut':
            self.V.remove_hut(self)
        elif self.type == 'cannon':
            self.V.remove_cannon(self)
        elif self.type == 'wizardtower':
            self.V.remove_wizard_tower(self)
        elif self.type == 'townhall':
            self.V.remove_town_hall(self)


class Hut(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (2, 2)
        self.V = V
        self.destroyed = False
        self.health = 40
        self.max_health = 40
        self.type = 'hut'


class Cannon(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (2, 2)
        self.V = V
        self.destroyed = False
        self.health = 60 + 30*(pt.level_of_building)
        self.max_health = 60 + 30*(pt.level_of_building)
        self.type = 'cannon'
        self.attack = 4 + pt.level_of_building
        self.attack_radius = 5 + (int((pt.level_of_building)//2))
        self.isShooting = False

    def scan_for_targets(self, King):
        self.isShooting = False

        troops = barbarians + archers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop)
                return
            
        troops = superarchers
        for troop in troops:
            if((time.time()-troop.timestart)>=10):
                if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                    self.isShooting = True
                    self.attack_target(troop)
                    return


        # for barb in barbarians:
        #     if (barb.position[0] - self.position[0])**2 + (barb.position[1] - self.position[1])**2 <= self.attack_radius**2:
        #         self.isShooting = True
        #         self.attack_target(barb)
        #         return
        # for dragon in dragons:
        #     if (dragon.position[0] - self.position[0])**2 + (dragon.position[1] - self.position[1])**2 <= self.attack_radius**2:
        #         self.isShooting = True
        #         self.attack_target(dragon)
        #         return

        if King.alive == False:
            return

        if(King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.attack_radius**2:
            self.isShooting = True
            self.attack_target(King)

    def attack_target(self, target):
        if(self.destroyed == True):
            return
        target.deal_damage(self.attack)


class Wall(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (1, 1)
        self.V = V
        self.destroyed = False
        self.health = 100 + 40*(pt.level_of_building)
        self.max_health = 100 + 40*(pt.level_of_building)
        self.type = 'wall'
        self.self_damage=200


class TownHall(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (4, 3)
        self.V = V
        self.destroyed = False
        self.health = 100
        self.max_health = 100
        self.type = 'townhall'


class WizardTower(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (1, 1)
        self.V = V
        self.destroyed = False
        self.health = 60 + 30*(pt.level_of_building)
        self.max_health = 60 + 30*(pt.level_of_building)
        self.type = 'wizardtower'
        self.attack = 4 + pt.level_of_building
        self.attack_radius = 5 + int((pt.level_of_building)/2)
        self.isShooting = False

    def scan_for_targets(self, King):
        print("wizard",self.health)
        self.isShooting = False
        troops = barbarians+ archers + dragons + balloons
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop,0)
                return
            
        troops = superarchers
        for troop in troops:
            if((time.time()-troop.timestart)>=10):
                if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                    self.isShooting = True
                    self.attack_target(troop,0)
                    return

        troops = healers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop,0)
                return

        if King.alive == False:
            return

        if(King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.attack_radius**2:
            self.isShooting = True
            self.attack_target(King,1)

    def attack_target(self, target, isKing):
        if(self.destroyed == True):
            return

        if isKing == 1:
            target.deal_damage(self.attack)
        i = target.position[0] - 1
        j = target.position[1] - 1
        troops = barbarians+ archers + dragons + balloons + healers
        for row in range(i, i+3):
            for col in range(j, j+3):
                if(row < 0 or col < 0):
                    continue
                for troop in troops:
                    if(troop.position[0] == row and troop.position[1] == col):
                        troop.deal_damage(self.attack)


def shoot_cannons(King, V):
    for cannon in V.cannon_objs:
        V.cannon_objs[cannon].scan_for_targets(King)


def shoot_wizard_towers(King, V):
    for tower in V.wizard_tower_objs:
        V.wizard_tower_objs[tower].scan_for_targets(King)
