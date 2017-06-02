import pygame
from pygame.locals import QUIT, VIDEORESIZE
import mpq
import av

pygame.mixer.pre_init(channels=1)
pygame.init()

RESOURCES = mpq.MPQFile('resources/diabdat.mpq')

def cutscene(resource):
    def video():
        data = av.open(RESOURCES.open(resource))
        for frame in data.decode(video=0):
            image = pygame.image.frombuffer(
                frame.to_nd_array(format='rgb24'),
                (frame.width, frame.height), 'RGB')
            yield image

    fifo = av.AudioFifo()
    data = av.open(RESOURCES.open(resource))
    for frame in data.decode(audio=0):
        fifo.write(frame)

    resampler = av.AudioResampler(format='s16p', layout='mono')
    audio = pygame.mixer.Sound(array=resampler.resample(fifo.read()).to_nd_array()[0])

    return video(), audio


def scale(frame, screen):
    factor = min(
        screen.get_width() / frame.get_width(),
        screen.get_height() / frame.get_height())

    return pygame.transform.smoothscale(
        frame,
        (round(frame.get_width() * factor), round(frame.get_height() * factor)))


def center(frame, screen):
    return (
        (screen.get_width() - frame.get_width()) / 2,
        (screen.get_height() - frame.get_height()) / 2)


def main():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    frames, audio = cutscene('File00002910.smk')
    audio.play()
    for frame in frames:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'])

        frame = scale(frame, screen)
        screen.blit(frame, center(frame, screen))

        pygame.display.flip()
        clock.tick(15)

    frames, audio = cutscene('File00001475.smk')
    audio.play()
    for frame in frames:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.dict['size'])

        frame = scale(frame, screen)
        screen.blit(frame, center(frame, screen))

        pygame.display.flip()
        clock.tick(15)


if __name__ == '__main__':
    main()
