from abc import ABC, abstractmethod

def human_size(n):
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if n < 1024 or unit == "ГБ":
            return f"{n:,.1f} {unit}" if unit != "Б" else f"{int(n)} Б"
        n /= 1024

class FileType(ABC):
    EXTENSION = ""

    def __init__(self, name):
        if not name.strip():
            raise ValueError("Имя файла не может быть пустым")
        self.name = name

    @abstractmethod
    def open_action(self) -> str:
        pass

    @abstractmethod
    def size_bytes(self) -> int:
        pass

    @abstractmethod
    def preview(self) -> str:
        pass

    def row(self):
        kind = self.__class__.__name__
        return f"{kind:<10s}| {self.name:<16s}| {human_size(self.size_bytes()):>12s}"


class TextFile(FileType):
    ENCODINGS = ("utf-8", "utf-16", "cp1251", "ascii")

    def __init__(self, name, text, encoding="utf-8"):
        super().__init__(name)
        if encoding not in self.ENCODINGS:
            raise ValueError(f"Кодировка не поддерживается: {encoding}")
        self.text = text
        self.encoding = encoding
        self.lines = text.count("\n") + 1 if text else 0
        self.chars = len(text)

    def open_action(self):
        return f"Открывается в текстовом редакторе ({self.encoding})"

    def size_bytes(self):
        return len(self.text.encode(self.encoding, errors="replace"))

    def preview(self):
        first = self.text.split("\n")[0][:30]
        return f"{self.lines} строк, {self.chars} симв. | «{first}…»"

class ImageFile(FileType):
    COMPRESSION = {"png": 0.5, "jpeg": 0.1, "bmp": 1.0, "gif": 0.3}

    def __init__(self, name, width, height, fmt, color_depth):
        super().__init__(name)
        if width <= 0 or height <= 0:
            raise ValueError("Размеры должны быть положительными")
        if fmt not in self.COMPRESSION:
            raise ValueError(f"Неизвестный формат: {fmt}")
        self.width, self.height = width, height
        self.fmt = fmt
        self.color_depth = color_depth

    def open_action(self):
        return "Открывается в просмотрщике изображений"

    def size_bytes(self):
        raw = self.width * self.height * self.color_depth / 8
        return int(raw * self.COMPRESSION[self.fmt])

    def preview(self):
        mp = self.width * self.height / 1e6
        return f"{self.width}×{self.height} ({mp:.1f} Мп), {self.fmt.upper()}, {self.color_depth} бит"


class AudioFile(FileType):
    def __init__(self, name, duration_sec, bitrate_kbps, channels):
        super().__init__(name)
        if channels not in ("моно", "стерео"):
            raise ValueError("Каналы: моно или стерео")
        if duration_sec <= 0 or bitrate_kbps <= 0:
            raise ValueError("Длительность и битрейт должны быть > 0")
        self.duration_sec = duration_sec
        self.bitrate_kbps = bitrate_kbps
        self.channels = channels

    def open_action(self):
        return "Воспроизводится в аудиоплеере"

    def size_bytes(self):
        return int(self.duration_sec * self.bitrate_kbps * 1000 / 8)

    def preview(self):
        m, s = divmod(self.duration_sec, 60)
        return f"{m}:{s:02d}, {self.bitrate_kbps} кбит/с, {self.channels}"


class VideoFile(FileType):
    BITS_PER_PIXEL = {"h264": 0.10, "h265": 0.05, "vp9": 0.06, "mpeg4": 0.15}
    RESOLUTIONS = {"480p": (854, 480), "720p": (1280, 720),
                   "1080p": (1920, 1080), "4k": (3840, 2160)}

    def __init__(self, name, duration_sec, resolution, fps, codec):
        super().__init__(name)
        if resolution not in self.RESOLUTIONS:
            raise ValueError(f"Неизвестное разрешение: {resolution}")
        if codec not in self.BITS_PER_PIXEL:
            raise ValueError(f"Неизвестный кодек: {codec}")
        self.duration_sec = duration_sec
        self.resolution = resolution
        self.fps = fps
        self.codec = codec

    def open_action(self):
        return "Воспроизводится в видеоплеере"

    def size_bytes(self):
        w, h = self.RESOLUTIONS[self.resolution]
        bitrate = w * h * self.fps * self.BITS_PER_PIXEL[self.codec]  # бит/с
        return int(bitrate * self.duration_sec / 8)

    def preview(self):
        m, s = divmod(self.duration_sec, 60)
        return f"{m}:{s:02d}, {self.resolution}, {self.fps} fps, {self.codec}"

if __name__ == "__main__":
    files = [
        TextFile("report.txt", "Лабораторная работа №4\nПолиморфизм\nВывод: всё работает", "utf-8"),
        TextFile("notes_ascii.txt", "hello world\nsecond line", "ascii"),
        ImageFile("photo.jpg", 4000, 3000, "jpeg", 24),
        ImageFile("logo.png", 512, 512, "png", 32),
        AudioFile("song.mp3", 215, 320, "стерео"),
        AudioFile("voice.mp3", 60, 64, "моно"),
        VideoFile("clip.mp4", 120, "1080p", 30, "h264"),
        VideoFile("movie.mkv", 5400, "4k", 24, "h265"),
    ]

    print("ПОЛИМОРФНЫЙ ОБХОД: открытие и предпросмотр")
    print("-" * 61)
    for f in files:
        print(f"{f.name:<16s}{f.open_action()}")
        print(f"{'':<16s}{f.preview()}")

    print("\nРАЗМЕРЫ ФАЙЛОВ")
    print("-" * 42)
    for f in files:
        print(f.row())
    print("-" * 42)

    total = sum(f.size_bytes() for f in files)
    biggest = max(files, key=lambda f: f.size_bytes())
    smallest = min(files, key=lambda f: f.size_bytes())
    print(f"Общий размер: {human_size(total)}")
    print(f"Самый большой: {biggest.name} ({human_size(biggest.size_bytes())})")
    print(f"Самый маленький: {smallest.name} ({human_size(smallest.size_bytes())})")

    print("\nПо убыванию размера:")
    for f in sorted(files, key=lambda f: f.size_bytes(), reverse=True):
        print(f"  {f.name:<16s}{human_size(f.size_bytes()):>12s}")