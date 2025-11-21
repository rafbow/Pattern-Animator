import time
import sys
import math
import random
import threading
from datetime import datetime

# Untuk mendeteksi keyboard input tanpa blocking
try:
    import msvcrt  # Windows
    def get_key():
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8', errors='ignore')
        return None
except ImportError:
    import termios
    import tty
    import select
    def get_key():  # Unix/Linux/Mac
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None

class PatternGenerator:
    """Generate berbagai pattern secara otomatis"""
    
    @staticmethod
    def simple_pattern(width=8):
        """Pattern sederhana"""
        return '*' * width
    
    @staticmethod
    def wave_pattern(frame, width=20):
        """Pattern gelombang sinusoidal"""
        pattern = []
        for i in range(width):
            height = int(3 * math.sin(i * 0.5 + frame * 0.2) + 3)
            pattern.append('#' if height > 2 else '.')
        return ''.join(pattern)
    
    @staticmethod
    def pulse_pattern(frame, min_width=3, max_width=15):
        """Pattern yang membesar-mengecil"""
        width = int((max_width - min_width) / 2 * math.sin(frame * 0.1) + (max_width + min_width) / 2)
        return '█' * width
    
    @staticmethod
    def random_chars(width=10):
        """Random characters"""
        chars = ['@', '#', '$', '%', '&', '*', '+', '=', '~']
        return ''.join(random.choice(chars) for _ in range(width))
    
    @staticmethod
    def alternating_pattern(frame, width=12):
        """Pattern yang berganti-ganti"""
        char1, char2 = '▓', '░'
        return ''.join(char1 if (i + frame // 2) % 2 == 0 else char2 for i in range(width))
    
    @staticmethod
    def arrow_pattern(direction='right'):
        """Pattern panah"""
        if direction == 'right':
            return '====>'
        else:
            return '<===='
    
    @staticmethod
    def box_pattern(frame, size=5):
        """Pattern kotak yang berputar"""
        patterns = ['▖', '▘', '▝', '▗']
        return patterns[frame % 4] * size
    
    @staticmethod
    def fibonacci_pattern(length=10):
        """Pattern berdasarkan fibonacci"""
        fib = [0, 1]
        while len(fib) < length:
            fib.append(fib[-1] + fib[-2])
        return ''.join('█' if x % 2 == 0 else '▒' for x in fib[:length])
    
    @staticmethod
    def fractal_pattern(iteration, length=15):
        """Simple fractal pattern"""
        pattern = '█'
        for _ in range(iteration % 4):
            pattern = pattern + '▒' + pattern
        return pattern[:length]

class AnimationController:
    """Controller utama untuk animasi"""
    
    def __init__(self):
        self.indent = 0
        self.indentIncreasing = True
        self.speed = 0.1  # Delay dalam detik
        self.max_indent = 40
        self.running = True
        self.paused = False
        self.frame = 0
        
        # Pattern settings
        self.pattern_mode = 0
        self.pattern_modes = [
            ('Simple', lambda f: PatternGenerator.simple_pattern()),
            ('Wave', lambda f: PatternGenerator.wave_pattern(f)),
            ('Pulse', lambda f: PatternGenerator.pulse_pattern(f)),
            ('Random', lambda f: PatternGenerator.random_chars()),
            ('Alternate', lambda f: PatternGenerator.alternating_pattern(f)),
            ('Arrow Right', lambda f: PatternGenerator.arrow_pattern('right')),
            ('Arrow Left', lambda f: PatternGenerator.arrow_pattern('left')),
            ('Box Rotate', lambda f: PatternGenerator.box_pattern(f)),
            ('Fibonacci', lambda f: PatternGenerator.fibonacci_pattern()),
            ('Fractal', lambda f: PatternGenerator.fractal_pattern(f))
        ]
        
        # Statistics
        self.bounce_count = 0
        self.start_time = datetime.now()
        self.show_stats = False
        
    def get_current_pattern(self):
        """Dapatkan pattern berdasarkan mode saat ini"""
        name, generator = self.pattern_modes[self.pattern_mode]
        return generator(self.frame)
    
    def change_pattern(self, direction=1):
        """Ganti pattern mode"""
        self.pattern_mode = (self.pattern_mode + direction) % len(self.pattern_modes)
        print(f"\n[Pattern Changed: {self.pattern_modes[self.pattern_mode][0]}]")
    
    def adjust_speed(self, factor):
        """Adjust kecepatan animasi"""
        self.speed = max(0.01, min(1.0, self.speed * factor))
        print(f"\n[Speed: {self.speed:.2f}s]")
    
    def adjust_range(self, delta):
        """Adjust jarak gerakan"""
        self.max_indent = max(10, min(80, self.max_indent + delta))
        print(f"\n[Range: {self.max_indent}]")
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
        state = "PAUSED" if self.paused else "RESUMED"
        print(f"\n[{state}]")
    
    def toggle_stats(self):
        """Toggle tampilan statistik"""
        self.show_stats = not self.show_stats
    
    def get_stats(self):
        """Dapatkan statistik running"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        return (f"Time: {int(elapsed)}s | Bounces: {self.bounce_count} | "
                f"Speed: {self.speed:.2f}s | Range: {self.max_indent} | "
                f"Pattern: {self.pattern_modes[self.pattern_mode][0]}")
    
    def update_position(self):
        """Update posisi pattern"""
        if self.paused:
            return
        
        if self.indentIncreasing:
            self.indent += 1
            if self.indent >= self.max_indent:
                self.indentIncreasing = False
                self.bounce_count += 1
        else:
            self.indent -= 1
            if self.indent <= 0:
                self.indentIncreasing = True
                self.bounce_count += 1
        
        self.frame += 1
    
    def render(self):
        """Render frame saat ini"""
        pattern = self.get_current_pattern()
        output = ' ' * self.indent + pattern
        
        if self.show_stats:
            output += f"  [{self.get_stats()}]"
        
        print(output)
    
    def show_help(self):
        """Tampilkan bantuan kontrol"""
        help_text = """
╔══════════════════════════════════════════════════════════╗
║           KEYBOARD CONTROLS - HELP MENU                  ║
╠══════════════════════════════════════════════════════════╣
║  SPEED CONTROL:                                          ║
║    ↑ or W  : Increase speed (faster animation)           ║
║    ↓ or S  : Decrease speed (slower animation)           ║
║                                                           ║
║  PATTERN CONTROL:                                        ║
║    → or D  : Next pattern                                ║
║    ← or A  : Previous pattern                            ║
║    R       : Random pattern mode                         ║
║                                                           ║
║  RANGE CONTROL:                                          ║
║    + or =  : Increase movement range                     ║
║    - or _  : Decrease movement range                     ║
║                                                           ║
║  GENERAL:                                                ║
║    SPACE   : Pause/Resume animation                      ║
║    I       : Toggle statistics display                   ║
║    H or ?  : Show this help                              ║
║    Q       : Quit program                                ║
║                                                           ║
║  Available Patterns: Simple, Wave, Pulse, Random,        ║
║                     Alternate, Arrow, Box, Fibonacci     ║
╚══════════════════════════════════════════════════════════╝
"""
        print(help_text)

def input_thread(controller):
    """Thread untuk menangani input keyboard"""
    # Setup terminal untuk non-blocking input di Unix
    if sys.platform != 'win32':
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while controller.running:
                key = get_key()
                if key:
                    handle_key(key, controller)
                time.sleep(0.01)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    else:
        while controller.running:
            key = get_key()
            if key:
                handle_key(key, controller)
            time.sleep(0.01)

def handle_key(key, controller):
    """Handle keyboard input"""
    key = key.lower()
    
    # Speed control
    if key in ['w', 'W'] or ord(key) == 72:  # Up arrow
        controller.adjust_speed(0.8)  # Lebih cepat
    elif key in ['s', 'S'] or ord(key) == 80:  # Down arrow
        controller.adjust_speed(1.25)  # Lebih lambat
    
    # Pattern control
    elif key in ['d', 'D'] or ord(key) == 77:  # Right arrow
        controller.change_pattern(1)
    elif key in ['a', 'A'] or ord(key) == 75:  # Left arrow
        controller.change_pattern(-1)
    elif key in ['r', 'R']:
        controller.pattern_mode = random.randint(0, len(controller.pattern_modes) - 1)
        print(f"\n[Random Pattern: {controller.pattern_modes[controller.pattern_mode][0]}]")
    
    # Range control
    elif key in ['+', '=']:
        controller.adjust_range(5)
    elif key in ['-', '_']:
        controller.adjust_range(-5)
    
    # General controls
    elif key == ' ':
        controller.toggle_pause()
    elif key in ['i', 'I']:
        controller.toggle_stats()
    elif key in ['h', 'H', '?']:
        controller.show_help()
    elif key in ['q', 'Q']:
        controller.running = False

def show_welcome_screen():
    """Tampilkan welcome screen dan petunjuk"""
    welcome = """
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║            🎨 ADVANCED PATTERN ANIMATOR WITH AUTO-GENERATOR 🎨       ║
║                                                                      ║
║              Dibuat dengan Python - Interactive Animation            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════════╗
║                          📖 PETUNJUK PENGGUNAAN                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Program ini akan menampilkan animasi pattern yang bergerak          ║
║  horizontal bolak-balik dengan berbagai variasi pattern otomatis.    ║
║                                                                      ║
║  ⚙️  KONTROL KECEPATAN:                                               ║
║     ↑ / W    → Percepat animasi                                      ║
║     ↓ / S    → Perlambat animasi                                     ║
║                                                                      ║
║  🎨 KONTROL PATTERN:                                                 ║
║     → / D    → Pattern berikutnya                                    ║
║     ← / A    → Pattern sebelumnya                                    ║
║     R        → Random pattern                                        ║
║                                                                      ║
║  📏 KONTROL JARAK GERAKAN:                                           ║
║     + / =    → Perlebar jarak gerakan                                ║
║     - / _    → Persempit jarak gerakan                               ║
║                                                                      ║
║  🎮 KONTROL UMUM:                                                    ║
║     SPACE    → Pause / Resume animasi                                ║
║     I        → Tampilkan/Sembunyikan statistik                       ║
║     H / ?    → Tampilkan bantuan (kapan saja)                        ║
║     Q        → Keluar dari program                                   ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                      🎨 10 PATTERN TERSEDIA:                         ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  1. Simple      → Pattern bintang klasik (********)                  ║
║  2. Wave        → Gelombang sinusoidal bergerak                      ║
║  3. Pulse       → Pattern membesar dan mengecil                      ║
║  4. Random      → Karakter acak berubah-ubah                         ║
║  5. Alternate   → Pattern bergantian (▓░▓░)                          ║
║  6. Arrow Right → Panah ke kanan (====>)                             ║
║  7. Arrow Left  → Panah ke kiri (<====)                              ║
║  8. Box Rotate  → Kotak berputar (▖▘▝▗)                              ║
║  9. Fibonacci   → Berdasarkan deret Fibonacci                        ║
║  10. Fractal    → Pattern fractal sederhana                          ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                        💡 TIPS & TRIK:                               ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  • Tekan SPACE untuk pause dan lihat detail pattern                  ║
║  • Tekan I untuk melihat statistik real-time                         ║
║  • Kombinasikan speed tinggi dengan pattern kompleks!                ║
║  • Tekan R berulang untuk eksplorasi pattern random                  ║
║  • Gunakan + dan - untuk menyesuaikan dengan ukuran layar            ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

"""
    print(welcome)

def show_pattern_preview():
    """Tampilkan preview dari setiap pattern"""
    print("\n╔══════════════════════════════════════════════════════════════════════╗")
    print("║                       🎨 PREVIEW PATTERN                             ║")
    print("╠══════════════════════════════════════════════════════════════════════╣")
    
    patterns = [
        ("Simple", PatternGenerator.simple_pattern()),
        ("Wave", PatternGenerator.wave_pattern(0)),
        ("Pulse", PatternGenerator.pulse_pattern(0)),
        ("Random", PatternGenerator.random_chars()),
        ("Alternate", PatternGenerator.alternating_pattern(0)),
        ("Arrow Right", PatternGenerator.arrow_pattern('right')),
        ("Arrow Left", PatternGenerator.arrow_pattern('left')),
        ("Box Rotate", PatternGenerator.box_pattern(0)),
        ("Fibonacci", PatternGenerator.fibonacci_pattern()),
        ("Fractal", PatternGenerator.fractal_pattern(0))
    ]
    
    for i, (name, pattern) in enumerate(patterns, 1):
        print(f"║  {i:2d}. {name:15s} → {pattern:30s}                ║")
    
    print("╚══════════════════════════════════════════════════════════════════════╝\n")

def get_user_confirmation():
    """Minta konfirmasi user untuk memulai"""
    while True:
        print("\n╔══════════════════════════════════════════════════════════════════════╗")
        print("║                       PILIHAN MENU:                                  ║")
        print("╠══════════════════════════════════════════════════════════════════════╣")
        print("║  1. Mulai Animasi                                                    ║")
        print("║  2. Lihat Preview Pattern                                            ║")
        print("║  3. Lihat Petunjuk Lengkap                                           ║")
        print("║  Q. Keluar                                                           ║")
        print("╚══════════════════════════════════════════════════════════════════════╝")
        
        choice = input("\n👉 Pilih menu [1/2/3/Q]: ").strip().lower()
        
        if choice == '1':
            return True
        elif choice == '2':
            show_pattern_preview()
        elif choice == '3':
            show_welcome_screen()
        elif choice == 'q':
            print("\n👋 Terima kasih! Sampai jumpa lagi.\n")
            return False
        else:
            print("\n❌ Pilihan tidak valid! Silakan pilih 1, 2, 3, atau Q.")

def show_countdown():
    """Tampilkan countdown sebelum mulai"""
    print("\n🚀 Animasi akan dimulai dalam:")
    for i in range(3, 0, -1):
        print(f"   {i}...", end='', flush=True)
        time.sleep(1)
    print(" GO! 🎉\n")
    time.sleep(0.5)

def main():
    """Main program loop"""
    # Tampilkan welcome screen
    show_welcome_screen()
    
    # Minta konfirmasi user
    if not get_user_confirmation():
        sys.exit(0)
    
    # Countdown sebelum mulai
    show_countdown()
    
    # Bersihkan layar untuk animasi (opsional)
    print("\n" * 2)
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     🎬 ANIMASI DIMULAI - Tekan H untuk bantuan          ║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    controller = AnimationController()
    
    # Start input thread
    input_handler = threading.Thread(target=input_thread, args=(controller,), daemon=True)
    input_handler.start()
    
    try:
        while controller.running:
            controller.render()
            time.sleep(controller.speed)
            controller.update_position()
            
    except KeyboardInterrupt:
        controller.running = False
    
    # Tampilkan final statistics
    print("\n\n╔════════════════════════════════════════════════════════════════════════════════════════╗")
    print(f"║  Final Statistics: {controller.get_stats()}  ║")
    print("╚════════════════════════════════════════════════════════════════════════════════════════╝")
    print("Thank you for using Pattern Animator!")
    sys.exit()

if __name__ == "__main__":
    main()