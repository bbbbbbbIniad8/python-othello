import pygame


# 左上に座標を表示
def debug_mouse_coord(screen, font):
    mouseX,mouseY = pygame.mouse.get_pos()
    text = font.render(f'{mouseX},{mouseY}', True, (255, 255, 255))
    screen.blit(text, (0, 0))


# マウスのｘｙ座標を分割座標に変換
def where_mouse_mass(Mass_size, shift):
    mouseX, mouseY = pygame.mouse.get_pos()
    N_MassX, N_MassY = ((mouseX-shift[0])//Mass_size[0], (mouseY-shift[1])//Mass_size[1])
    return N_MassX, N_MassY


# 指定したｘｙ座標を分割座標に変換
def exchange_mass(mass_size, X, Y):
    N_MassX, N_MassY = (X//mass_size[0], Y//mass_size[1])
    return N_MassX, N_MassY


# 分割座標を通常座標に変換
def exchange_coord(mass_size, shift, X, Y):
    N_MassX, N_MassY = (X * mass_size[0] + shift[0], Y * mass_size[1] + shift[1])
    return N_MassX, N_MassY


# 分割座標をもとにマウスカーソルを追いかける形で図形を表示
def tracking_mass(screen, mass_size, shift):
    N_MassX, N_MassY = where_mouse_mass(mass_size, shift)
    pygame.draw.rect(screen, (0, 255, 255), (N_MassX*mass_size[0]+shift[0], N_MassY*mass_size[1]+shift[1],
                                           mass_size[0], mass_size[1]),3)



# 指定した分割座標上に図形を表示
def put_on_mass(screen, Mass_size, shift, X, Y, color, KATATI):
    X = Mass_size[0] * X + shift[0]
    Y = Mass_size[1] * Y + shift[1]
    if KATATI == "丸":
        pygame.draw.circle(screen, color, (X+Mass_size[0]//2, Y+Mass_size[0]//2), Mass_size[0]//2-0.5)

    elif KATATI =="四角":
        pygame.draw.rect(screen, color, (X, Y, Mass_size[0], Mass_size[1]), 1)

    elif KATATI == "小四角":
        MASSX = Mass_size[0] // 4
        MASSY = Mass_size[1] // 4
        pygame.draw.rect(screen, color, (X+Mass_size[0]//2-MASSX/2,Y+Mass_size[1]//2-MASSY/2, MASSX, MASSY))
