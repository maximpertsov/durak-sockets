class DrawPile:
    def __init__(self, *, draw_pile):
        self._draw_pile = draw_pile

    def serialize(self):
        return self._draw_pile

    def size(self):
        return len(self._draw_pile)

    def draw(self, count):
        result = self._draw_pile[:count]
        self._draw_pile = self._draw_pile[count:]
        return result
