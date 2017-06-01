import pygame

def main():
    screen = pygame.display.set_mode((1024, 768))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
