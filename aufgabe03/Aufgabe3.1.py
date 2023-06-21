class Set:
    def __init__(self, list_: list):
        self.list_ = list_

    def __str__(self):
        """represent str of object as {elem1, elem2, ...}"""
        if len(self.list_) == 0:
            return "∅"
        return '{' + ', '.join(f'{elem}' for elem in self.list_) + "}"

    def __repr__(self):
        """Zur schönen Ausgabe in tuplen und listen"""
        if len(self.list_) == 0:
            return "∅"
        return '{' + ', '.join(f'{elem}' for elem in self.list_) + "}"

    def union(self, other):
        return Set([x for x in self.list_ if x not in other.list_] + other.list_)

    def __add__(self, other):
        """overload add operator as union-Operator"""
        return Set([x for x in self.list_ if x not in other.list_] + other.list_)

    def intersect(self, other):
        return Set([x for x in self.list_ if x in other.list_])

    def __and__(self, other):
        """overload and as intersect-operator"""
        return Set([x for x in self.list_ if x in other.list_])

    def __sub__(self, other):
        """Overload sub as complement-operator"""
        return Set([elem for elem in self.list_ if elem not in other.list_])

    def __iter__(self):
        yield from self.list_

    def __contains__(self, e):
        return e in self.list_

    def __len__(self):
        return len(self.list_)

    def __getitem__(self, i):
        return self.list_[i]

    def subset(self, selection):
        try:
            return Set([elem for elem in self.list_ if selection(elem)])
        except:
            # für lambdas mit a, b = elem in übergabe, sehr hässlich gelöst...
            return Set([(a, b) for a, b in self.list_ if selection(a, b)])

    def powerset(self):
        """use binary representation of (length of list-1) to get powerset"""
        powerSet = []
        for i in range(1 << len(self.list_)):  # 1<<len(list_) = 2^len(list)
            sub = []
            for j in range(len(self.list_)):
                if (i & (1 << j) > 0):
                    # (1<<j means 1*(2^j))) check which bit is 1
                    # append according bit(element) to partial subset
                    sub.append(self.list_[j])
            powerSet.append(Set(sub))
        return Set(powerSet)

    def __mul__(self, other):
        c = [[(x, y) for x in self.list_] for y in other.list_]
        return CartesianProduct([x for sublist in c for x in sublist])


def strangeN(n):
    """Von Neumannsche-Mengendefinition : Definition der natürlichen Zahlen allein aus Mengen"""
    if n == 0:
        return Set("")
    return strangeN(n - 1) + Set([strangeN(n - 1)])


def binomialCoefficients(num):
    n = Set([x for x in range(0, num)])
    npow = n.powerset()
    print(npow)
    biko = [0 for x in range(0, num + 1)]
    for t in npow:
        biko[len(t)] += 1
    return biko


class CartesianProduct(Set):
    def __init__(self, list_: list):
        super().__init__(list_)


class Relation(CartesianProduct):
    def __init__(self, s: Set, r=None):
        super().__init__(s.list_)
        car = self * self
        self.r = r
        if r is not None:
            self.rel = car.subset(r)
        else:
            self.rel = car

    def __str__(self):
        str1 = super().__str__()
        str2 = self.rel.__str__()
        return "A: " + str1 + "\n mit Relation: " + str2

    def reflexivitaet(self):
        for a in self.list_:
            if (a, a) not in self.rel:
                return False
        return True

    def symmetrie(self):
        for (a, b) in self.rel:
            if (b, a) not in self.rel:
                return False
        return True

    def transitivitaet(self):
        for (a, b) in self.rel:
            for c in self.list_:
                if (b, c) not in self.rel:
                    return False
        return True

    def aquivalent(self):
        return self.symmetrie() and self.transitivitaet() and self.reflexivitaet()


def getAquivalenzklassen(relation, classes = [], first_iter = True):
    if not relation.aquivalent():
        raise ValueError("Relation is not Äquivalenzrelation")

    print(Set([relation.list_[0]]))

    if first_iter:
        classes.append(Set([relation.list_[0]]))
        new_test = Relation(Set(relation.list_[1:]), relation.r)
        print(new_test)
        return getAquivalenzklassen(new_test, classes, False)

        #classes.append(Set(relation[0]))
        #new_test = Set(relation[1:])
        #return getAquivalenzklassen(new_test, classes, False)

    if len(relation.list_) == 0:
        return classes

    for i in classes:

        print(classes)
        if Relation(i+Set([relation.list_[0]]), relation.r).aquivalent:
            i += Set([relation.list_[0]])
            return getAquivalenzklassen(Relation(Set(relation.list_[1:]), relation.r), classes, False)

    classes.append(Set([relation.list_[0]]))
    return getAquivalenzklassen(Relation(Set(relation.list_[1:]), relation.r),classes, False)


def moegen(s):
    """Relation für Beziehungen"""
    return ("Alice" or "Bob") in s


def r1(s):
    a, b = s
    return a <= b


def r2(s):
    a, b = s
    return a < b


def r3(s):
    a, b = s
    return a == b


def restklasse(s, m=5):
    a, b = s
    return not ((a - b) % m) and ((a - b != 0) or (a == b == 0))


def mitA(s):
    return "a" in s


# Aufgabe 3.1.1
print("Aufgabe 3.1.1")
A = Set(["hund", "katze", "maus"])
B = Set("")
C = Set(["tiger", "schlange"])
D = Set(["hund", "maus"])
E = A + C


print(B)
print(E)
print(A and D)
print(A - D)

print()
if "hund" in A:
    print("woof woof")

print()
for i in E:
    print(i)

print(A.subset(lambda x: len(x) == 4))
print(A.subset(mitA))

# Aufgabe 3.1.2
print("\n Aufgabe 3.1.2")
print(A)
print("Potenzmenge", A.powerset())
print("Neumansche Mengendefinition für 15: ", strangeN(15))
print("Binomialkoeffizienten für n = 3: ", binomialCoefficients(3))

# Aufgabe 3.1.5
# Bsp beziehungen
print("\n Bsp. Beziehungen")
Personen = Set(["Alice", "Bob", "Charles", "Denise", "Eric"])
Rpersonen1 = Relation(Personen, moegen)
Rpersonen2 = Relation(Personen)
print(Rpersonen1)
print("Äquivalent:", Rpersonen1.aquivalent())
print("Reflexivität:", Rpersonen1.reflexivitaet(), "Symmetrisch:", Rpersonen1.symmetrie(), "Transitiv:",
      Rpersonen1.transitivitaet())
print(Rpersonen2)
print("Äquivalent:", Rpersonen2.aquivalent())
print("Reflexivität:", Rpersonen2.reflexivitaet(), "Symmetrisch:", Rpersonen2.symmetrie(), "Transitiv:",
      Rpersonen2.transitivitaet())

# Bsp Ordnungen
print("\n Bsp. Ordnungen")
N = Set([x for x in range(0, 4)])
R1 = Relation(N, r1)
R2 = Relation(N, r2)
R3 = Relation(N, r3)
print(R1)
print("Äquivalent:", R1.aquivalent())
print("Reflexivität:", R1.reflexivitaet(), "Symmetrisch:", R1.symmetrie(), "Transitiv:", R1.transitivitaet())
print(R2)
print("Äquivalent:", R2.aquivalent())
print("Reflexivität:", R2.reflexivitaet(), "Symmetrisch:", R2.symmetrie(), "Transitiv:", R2.transitivitaet())
print(R3)
print("Äquivalent:", R3.aquivalent())
print("Reflexivität:", R3.reflexivitaet(), "Symmetrisch:", R3.symmetrie(), "Transitiv:", R3.transitivitaet())

# Bsp Restklassen
print("\n Restklassen")
N = Set([x for x in range(0, 7)])
Restklasse5 = Relation(N, restklasse)
func = lambda a, b: not ((a - b) % 5)  # ??? aus aufgabenstellung nicht ersichtlich ob tuple der Form (a, a) entspricht (0,0) dabei sein sollen...
R= Relation(N, func)
print(R)
print(Restklasse5)
print("Äquivalent:", Restklasse5.aquivalent())
print("Reflexivität:", Restklasse5.reflexivitaet(), "Symmetrisch:", Restklasse5.symmetrie(), "Transitiv:",
      Restklasse5.transitivitaet())

print(Rpersonen2.r)
getAquivalenzklassen(Rpersonen2)