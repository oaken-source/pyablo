import pygame
import mpq
import av

resources = mpq.MPQFile('resources/diabdat.mpq')

def cutscene(resource, repeat=1):
    video = av.open(resources.open(resource))

    for frame in video.decode(video=0):
        image = pygame.image.frombuffer(frame.to_rgb().to_nd_array(),
            (frame.width, frame.height), 'RGB')
        for _ in range(repeat):
            yield image


def scale(frame, screen):
    scale = min(screen.get_width() / frame.get_width(),
        screen.get_height() / frame.get_height())

    return pygame.transform.smoothscale(frame,
        (round(frame.get_width() * scale), round(frame.get_height() * scale)))


def center(frame, screen):
    return ((screen.get_width() - frame.get_width()) / 2,
        (screen.get_height() - frame.get_height()) / 2)


def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    for frame in cutscene('File00002910.smk', repeat=2):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'])

        frame = scale(frame, screen)
        screen.blit(frame, center(frame, screen))

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
