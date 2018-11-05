# Library for Map Generation Classes
import math
import random
from PIL import Image, ImageDraw


class Dist_Function:   # the distribution describes, on which coords mountain spots are placed
    def __init__(self, size, spray):
        self.size = size
        self.spray = spray
        self.dist = []

    def calcdist(self):                                 # calculate the distribution spread
        for x in range(0, self.size):
            y = self.size / 3 * math.sin(x * 12.0 / self.size) + x
            y = random.randrange(int(-self.size * self.spray), int(self.size * self.spray)) + y
            y = int(round(y, 0))
            self.dist.append(y)

    def clean(self, border, density):                   # defines the borders and the density of spreaded mountain tops
        for x in range(0, self.size):
            if random.randint(0, density + 10) < 10:
                self.dist[x] = -10
            elif self.dist[x] < border:
                self.dist[x] = -10
            elif self.dist[x] > self.size - border:
                self.dist[x] = -10
            elif x < border:
                self.dist[x] = -10
            elif x > self.size - border:
                self.dist[x] = -10


class Brush:
    def __init__(self, size, height):
        self.size = size
        self.height = height
        self.brush = []
        self.mid = int(self.size / 2)

        for y in range(0, self.size):
            row = []
            for x in range(0, self.size):
                row.append(0)
            self.brush.append(row)

        for y in range(0, self.size):
            for x in range(0, self.size):
                if y <= self.mid:
                    if (self.mid - y) <= x <= (self.mid + y):
                        self.brush[y][x] = 1
                        self.brush[self.size-y-1][x] = 1
                    if (self.mid - y+2) <= x <= (self.mid + y - 2):
                        self.brush[y][x] = 2
                        self.brush[self.size - y - 1][x] = 2
                    if (self.mid - y + 4) <= x <= (self.mid + y - 4):
                        self.brush[y][x] = 3
                        self.brush[self.size - y - 1][x] = 3
                    if (self.mid - y + 5) <= x <= (self.mid + y - 5):
                        self.brush[y][x] = 4
                        self.brush[self.size - y - 1][x] = 4


class Seedmap:
    def __init__(self, size):
        self.size = size
        self.map = []

        for y in range(0, self.size):
            row = []
            for x in range(0, self.size):
                row.append(0)
            self.map.append(row)

    def drawfromdist(self, dist):
        for x in range(0, self.size):
            y = dist.dist[x]
            if y > 0:
                self.map[x][y] = 1


class Heightmap:
    def __init__(self, size, border):
        self.size = size
        self.border = border
        self.map = []
        self.forest = []
        self.rivers = []

        for y in range(0, size):
            row = []
            forestrow = []
            riverrow = []
            for x in range(0, size):
                row.append(-2)
                forestrow.append(0)
                riverrow.append(0)
            self.map.append(row)
            self.forest.append(forestrow)
            self.rivers.append(riverrow)

    def generate(self, seedmap, brush):
        for y in range(0, self.size):
            for x in range(0, self.size):
                if seedmap.map[x][y] == 1:
                    for j in range(-brush.mid, brush.mid):
                        for i in range(-brush.mid, brush.mid):
                            self.map[x + i][y + j] += brush.brush[brush.mid + i][brush.mid + j]

    def gen2_prep(self, seedmap):
        print("start generating mountaintops")
        for y in range(0, self.size):
            for x in range(0, self.size):
                if seedmap.map[x][y] == 1:
                    self.map[x][y] = random.randrange(1, 8, 1)

    def slopedown(self):
        print("starting slopedown")
        for y in range(1, self.size-1):                                       # row loop
            for x in range(1, self.size-1):                                   # line loop
                activecell = self.map[x][y]                                   # define the active cell
                for n in range(-1, 2):                                         # search area in row
                    for m in range(-1, 2):                                    # search area in line
                        if m != 0 or n != 0:                                  # ignore active cell for comparison
                            compcell = self.map[x + m][y + n]                 # define to be compared cell
                            if compcell > activecell:                         # comparison only for lower cells
                                if compcell > 4:                             # mountains need steeper slope (higher 40)
                                    if m == 0 and random.randint(0, 1) == 0:   # mountains are extended n / s
                                        activecell = compcell                 # sometime they extend
                                    else:                                     # else
                                        activecell = compcell - 1             # sometimes they don't
                                elif random.randint(0, 10) < 3:                # for areas underneath 40
                                    activecell = compcell                     # there is a higher prob for extension
                                else:
                                    activecell = compcell - 1                 # else normal slope down
                self.map[x][y] = activecell

        # now do it backwarts
        print("reversing slope down route")
        for y in range(self.size-2, 1, -1):                                          # row loop
            for x in range(self.size-2, 1, -1):                                      # line loop
                activecell = self.map[x][y]                                          # define active Cell
                for n in range(-1, 2):                                                # search area row
                    for m in range(-1, 2):                                           # search area line
                        if m != 0 or n != 0:                                         # ignore active cell for comparison
                            compcell = self.map[x + m][y + n]                        # define to be compared cell
                            if compcell > activecell:                                # only lower cells are compared
                                if compcell > 4:                                     # Mountains: higher than 40
                                    if m == 0 and random.randint(0, 1) == 0:          # for north-south mountains have
                                        activecell = compcell                        # a chance to be extended
                                    else:                                            # and sometimes
                                        activecell = compcell - 1                    # they don't extend
                                elif random.randint(0, 10) < 3:                      # areas that are lower
                                    activecell = compcell                            # extend with higher chance
                                else:
                                    activecell = compcell - 1                        # else normal slopedown
                self.map[x][y] = activecell

    def cleanup(self):
        print("Starting Cleanup")
        for y in range(1, self.size - 1):                                               # row loop
            for x in range(1, self.size - 1):                                           # line loop
                activecell = self.map[x][y]                                             # define active cell
                for n in range(-1, 2):                                                  # search area row
                    for m in range(-1, 2):                                              # search area line
                        if m != 0 or n != 0 :
                            compcell = self.map[x+m][y+n]
                            if activecell < compcell + 1:
                                compcell -= 1
                self.map[x][y] = compcell
        print("reversed cleanup")
        for y in range(self.size - 2, 1, -1):                                            # row loop
            for x in range(self.size - 2, 1, - 1):                                       # line loop
                activecell = self.map[x][y]                                             # define active cell
                for n in range(-1, 2):                                                  # search area row
                    for m in range(-1, 2):                                              # search area line
                        if m != 0 or n != 0:
                            compcell = self.map[x+m][y+n]
                            if compcell > activecell + 1:
                                self.map[x][y] = compcell - 1

    def genforest(self, debug=False):
        if debug:
            print("Generating Forestmap")
        scan_area = int(self.size/50)
        min_area = int(self.size/50 - self.size/300)
        max_area = int(self.size / 50 + self.size / 300)
        count = 0
        if debug:
            print(scan_area, min_area, max_area)
        for y in range(self.border, self.size - self.border):         # row loop
            for x in range(self.border, self.size - self.border):     # line loop
                if random.randint(0, 10000) < 2:
                    count += 1
                    for n in range(-scan_area, scan_area):              # search area row
                        for m in range(-scan_area, scan_area):          # search area line
                            activecell = self.map[x+m][y+n]           # define active Cell
                            distance = math.sqrt(m * m + n * n)
                            if distance < random.randrange(min_area, max_area) and 5 < activecell < 40:
                                self.forest[x+m][y+n] = 1
        print("Forests generated:", count)

    def seedrivers(self, debug=False):
        if debug:
            print("Generating River map")
        count = 0
        for y in range(self.border, self.size - self.border):         # row loop
            for x in range(self.border, self.size - self.border):     # line loop
                activecell = self.map[x][y]
                if 40 < activecell < 70 and random.randint(0, 10000) < 100:
                    count += 1
                    self.rivers[x][y] = 1
        if debug:
            print("Rivers seeded:", count)

    def genrivers(self, debug=False):
        if debug:
            print("Generating River map")
        for y in range(self.border, self.size - self.border):               # row loop
            for x in range(self.border, self.size - self.border):           # line loop
                if self.rivers[x][y] == 1 and not isnext(self.rivers, x, y):
                    print("new seed found")                                 # seed found , flow down
                    done = False
                    found = False
                    wd = 0
                    while self.map[x][y] > 0 and not done and wd < 1000:
                        done = True
                        if random.randint(0, 0) == 0:
                            start = -1
                            stop = 2
                            step = 1
                        else:
                            start = 1
                            stop = -2
                            step = -1
                        for n in range(start, stop, step):              # suchbereich spalte
                            for m in range(start, stop, step):                            # suchbereich Zeile
                                found = False
                                if abs(m) != abs(n):
                                    activecell = self.map[x][y]
                                    compcell = self.map[x+m][y+n]
                                    print(x, y, m, n, activecell, compcell)
                                    if self.rivers[x+m][y+n] == 0:
                                        if compcell <= activecell:
                                            print("field is lower or same height")
                                            if activecell % 10 == 0:
                                                x = x + m
                                                y = y + n
                                                self.rivers[x][y] = 1
                                                done = False
                                                print(x, y, compcell, "added after plateau")
                                                found = True
                                                break
                                            elif activecell % 10 == 5:
                                                x = x + m
                                                y = y + n
                                                self.rivers[x][y] = 1
                                                done = False
                                                print(x, y, compcell, "added after slope")
                                                found = True
                                                break
                            if found:
                                found = False
                                break

                        wd += 1
                        if wd > 500:
                            print("Watchdog high")
        if debug:
            print("River map generated completed")

    def to_list(self):
        return_list = []

        for y in range(0, self.size - 1):
            for x in range(0, self.size - 1):
                return_list.append(self.map[x][y])
        return return_list

    def newgrayscale(self, filename):
        image = Image.new("RGB", (self.size, self.size), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        oldprogress = 0
        for y in range(0, self.size):
            for x in range(0, self.size):
                level = self.map[x][y]
                level = level + 20
                draw.point((x, y), (level * 3, level * 3, level * 3))
            progress = int(y / self.size * 10)
            if progress != oldprogress:
                print(progress * 10, " ", end="")
            oldprogress = progress
        print("")
        del draw

        image.save(filename)

    def newtreemap(self, filename):
        image = Image.new("RGB", (self.size, self.size), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        oldprogress = 0

        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.forest[x][y] == 1:
                    draw.point((x, y), (255, 255, 255))

            progress = int(y / self.size * 10)
            if progress != oldprogress:
                print(progress * 10, " ", end="")
                oldprogress = progress
        print("")
        del draw

        image.save(filename)

    def newrivermap(self, filename):
        image = Image.new("RGB", (self.size, self.size), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        old_progress = 0
        print("Rivermap", end=" ")
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.rivers[x][y] == 1:
                    draw.point((x, y), (255, 255, 255))

            progress = int(y / self.size * 10)
            if progress != old_progress:
                print(progress * 10, " ", end="")
                old_progress = progress
        print("")
        del draw

        image.save(filename)

    def newimage(self, filename):
        image = Image.new("RGB", (self.size, self.size), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        old_progress = 0
        for y in range(0, self.size):
            for x in range(0, self.size):
                level = self.map[x][y]

                if level == - 2:
                    draw.point((x, y), (0, 16,  80))
                elif level == -1:
                    draw.point((x, y), (0, 16, 128))
                elif level == 0:
                    draw.point((x, y), (0, 16, 255))
                elif level == 1:
                    draw.point((x, y), (255, 200, 132))
                elif level == 2:
                    draw.point((x, y), (0, 120, 0))
                elif level == 3:
                    draw.point((x, y), (0, 130, 0))
                elif level == 4:
                    draw.point((x, y), (0, 140, 0))
                elif level == 5:
                    draw.point((x, y), (0, 150, 0))
                elif level == 6:
                    draw.point((x, y), (0, 160, 0))
                elif level == 7:
                    draw.point((x, y), (0, 170, 0))
                elif level >= 8:
                    draw.point((x, y), (0, 180, 0))

                if self.forest[x][y] == 1:
                    draw.point((x, y), (0, 80, 0))
                if self.rivers[x][y] == 1:
                    draw.point((x, y), (0, 50, 128))
            progress = int(y / self.size * 10)
            if progress != old_progress:
                print(progress * 10, " ", end="")
            old_progress = progress
        print("")
        del draw

        image.save(filename)

    def print(self):

        for row in range(0, self.size):
            print(self.map[row])


def isnext(tocheck, x, y, fourway=True):
    if tocheck[x-1][y] == 1 or tocheck[x+1][y] == 1 or tocheck[x][y-1] == 1 or tocheck[x][y+1] == 1 or not fourway and\
                (tocheck[x-1][y-1] == 1 or tocheck[x+1][y+1] == 1 or tocheck[x-1][y+1] == 1 or tocheck[x+1][y-1]) == 1:
        return True
    else:
        return False

# End of File
