import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS
from player import Player
from obstacle import Obstacle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.state = "SELECT"
        self.mode = "square"
        self.running = True
        self.player = None
        self.score = 0
        self.wall_timer = 0
        self.reset_game()

    def reset_game(self):
        """ゲームプレイ開始時の初期化ロジック"""
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self.all_sprites)
        self.score = 0
        self.wall_timer = pygame.USEREVENT + 1

        # モードに応じた生成間隔
        spawn_rate = 800 if self.mode == "spike" else 1200
        pygame.time.set_timer(self.wall_timer, spawn_rate)

    def handle_events(self):
        """イベント処理のみを抽出"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == "SELECT":
                self._handle_select_events(event)
            elif self.state == "PLAYING":
                self._handle_playing_events(event)
            elif self.state == "GAMEOVER":
                self._handle_gameover_events(event)

    def _handle_select_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.mode = "square"
                self.state = "PLAYING"
                self.reset_game()
            elif event.key == pygame.K_2:
                self.mode = "spike"
                self.state = "PLAYING"
                self.reset_game()

    def _handle_playing_events(self, event):
        """プレイ中のイベント処理"""
        if self.player is None:
            return
        if event.type == self.wall_timer:
            Obstacle(self.all_sprites, self.walls, is_top=True, mode=self.mode)
            Obstacle(self.all_sprites, self.walls, is_top=False, mode=self.mode)
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_UP]:
                self.player.jump()

    def _handle_gameover_events(self, event):
        """ゲームオーバー画面のイベント処理"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.state = "SELECT"

    def update(self):
        """状態の更新ロジック"""
        if self.state == "PLAYING":
            if self.player is None:
                return
            self.all_sprites.update()
            hit_wall = pygame.sprite.spritecollide(
                self.player, self.walls, False, pygame.sprite.collide_mask
            )
            hit_screen_edge = self.player.rect.top <= 0 or self.player.rect.bottom >= SCREEN_HEIGHT

            if hit_wall or hit_screen_edge:
                self.state = "GAMEOVER"
            self.score += 1

    def draw(self):
        """描画ロジックを統合"""
        self.screen.fill(BG_COLOR)

        if self.state == "SELECT":
            self.draw_select_screen()
        elif self.state == "PLAYING":
            self.all_sprites.draw(self.screen)
            score_surf = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 10))
        elif self.state == "GAMEOVER":
            self.draw_game_over()

        pygame.display.flip()

    def draw_select_screen(self):
        title_font = pygame.font.SysFont("arial", 40)
        t = title_font.render("Select Stage", True, (255, 255, 255))
        m1 = self.font.render("Press [1] : Square Walls", True, (0, 255, 200))
        m2 = self.font.render("Press [2] : Moving Spikes", True, (255, 100, 100))
        self.screen.blit(t, t.get_rect(center=(SCREEN_WIDTH//2, 150)))
        self.screen.blit(m1, m1.get_rect(center=(SCREEN_WIDTH//2, 250)))
        self.screen.blit(m2, m2.get_rect(center=(SCREEN_WIDTH//2, 300)))

    def draw_game_over(self):
        go_font = pygame.font.SysFont("arial", 48)
        text = go_font.render("GAME OVER", True, (255, 50, 50))
        retry = self.font.render("Press Space to Menu", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))
        self.screen.blit(retry, retry.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)))

    def run(self):
        """メインループ（実行管理のみ）"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
