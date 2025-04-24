import pygame


class NineSlice:
    def __init__(self, image: pygame.Surface):
        self.image = image
        size = self.image.get_size()
        self.tile_size = (size[0] // 3, size[1] // 3)
        
        self.tiles = []
        for y in range(3):
            for x in range(3):
                tile_rect = pygame.Rect(x * self.tile_size[0], y * self.tile_size[1], *self.tile_size)

                self.tiles.append(self.image.subsurface(tile_rect))

    def draw(self, surface: pygame.Surface, rect: pygame.Rect):
        # defining some short names
        tile_w, tile_h = self.tile_size[0], self.tile_size[1]
        center_w = max(rect.w - tile_w * 2, 0)
        center_h = max(rect.h - tile_h * 2, 0)

        # drawing corners
        surface.blit(self.tiles[0], rect.topleft)
        surface.blit(self.tiles[2], (rect.right - tile_w, rect.top))
        surface.blit(self.tiles[6], (rect.left, rect.bottom - tile_h))
        surface.blit(self.tiles[8], (rect.right - tile_w, rect.bottom - tile_h))

        # draw each side
        top_side = pygame.transform.scale(self.tiles[1], (center_w, tile_h))
        surface.blit(top_side, (rect.left + tile_w, rect.top))

        bottom_side = pygame.transform.scale(self.tiles[7], (center_w, tile_h))
        surface.blit(bottom_side, (rect.left + tile_w, rect.bottom - tile_h))

        left_side = pygame.transform.scale(self.tiles[3], (tile_w, center_h))
        surface.blit(left_side, (rect.left, rect.top + tile_w))

        right_side = pygame.transform.scale(self.tiles[5], (tile_w, center_h))
        surface.blit(right_side, (rect.right - tile_w, rect.top + tile_w))

        # fill in the middle
        middle = pygame.transform.scale(self.tiles[4], (center_w, center_h))
        surface.blit(middle, (rect.left + tile_w, rect.top + tile_h))

    def as_surface(self, rect: pygame.Rect) -> pygame.Surface:
        surface = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))

        rect_zero = rect.copy()
        rect_zero.topleft = (0, 0)
        self.draw(surface, rect_zero)

        return surface