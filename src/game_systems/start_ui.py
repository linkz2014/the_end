import pygame
from game_systems.data import *
from misc_widgets import false_glitch
from misc_widgets.setting import *
from misc_widgets.txtview import *

def draw_start_screen(screen,font_name,clock,game_settings:dict):
    game_mode_index = 0
    game_modes = ["新游戏","继续","选项","退出"]
    glitch_power = 0
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and game_mode_index < len(game_modes)-1:
                    game_mode_index += 1
                elif event.key == pygame.K_w and game_mode_index > 0:
                    game_mode_index -= 1
                elif event.key == pygame.K_RETURN:
                    if game_modes[game_mode_index] == "退出":
                        pygame.quit()
                        return True
                    elif game_modes[game_mode_index] == "新游戏":
                        glitch_power = 0.19
                    elif game_modes[game_mode_index] == "选项":
                        setting_page = SettingScreen(
                            screen,
                            clock,
                            load_font(font_name,28),
                            load_font(font_name, 22),
                            font_name,
                            game_settings
                        )
                        game_settings = setting_page.run()
                        #手写保留2位小数
                        game_settings["volume"] = int(game_settings["volume"]*100)/100
                    else:
                        waiting = False
                        return False

        clock.tick(FPS)
        glitch_power = max(glitch_power - 0.15 * 0.03, 0)

        # 离屏缓冲区绘制
        buffer = pygame.Surface((WIDTH, HEIGHT),pygame.SRCALPHA)
        # 调用外部模块的故障特效
        buffer = false_glitch.add_horizontal_glitch(buffer, WIDTH, HEIGHT, glitch_power)
        false_glitch.draw_crt_lines(buffer, WIDTH, HEIGHT)

        screen.blit(buffer, (0, 0))
        pygame.display.flip()
        screen.fill((125,125,125))

        draw_text(screen,"结局",WIDTH/2-25,50,(255,255,255),35,font_name,True)
        #间隔30
        s = 0
        for game_mode in game_modes:
            is_bold = game_mode == game_modes[game_mode_index]
            if game_mode != "新游戏":
                darkness = 255
            else:
                darkness = 100
            draw_text(screen,game_mode,WIDTH/2-25,150+s,(darkness,darkness,darkness),25,font_name,is_bold)
            s+=30

def draw_loading_screen(screen,clock,font_name):
    last_time = 0
    sleep_time = 1000

    all_cmd_message = [
        ['正在加载游戏数据.','info'],
        ['正在加载游戏数据..','info'],
        ['正在加载游戏数据...','info'],
        ['正在加载游戏数据:10%','info'],
        ['正在加载游戏数据:15%','info'],
        ['正在加载游戏数据:30%','info'],
        ['正在加载游戏数据:45%','info'],
        ['正在加载游戏数据:75%','info'],
        ['正在加载游戏数据:90%','info'],
        ['正在加载游戏数据:99%','info'],
        ['游戏数据加载成功:林华唐公司.结局','info'],
        ['正在加载角色数据.','info'],
        ['正在加载角色数据..','info'],
        ['正在加载角色数据...','info'],
        ['正在加载角色数据:5%','info'],
        ['正在加载角色数据:10%','info'],
        ['正在加载角色数据:13%','info'],
        ['正在加载角色数据:15%','info'],
        ['正在加载角色数据:20%','info'],
        ['正在加载角色数据:28%','info'],
        ['正在加载角色数据:40%','info'],
        ['正在加载角色数据:50%','info'],
        ['出现意外数据!','error'],
        ['正在抹除意外数据0/85','info'],
        ['正在抹除意外数据1/85','info'],
        ['正在抹除意外数据2/85','info'],
        ['正在抹除意外数据5/85','info'],
        ['正在抹除意外数据8/85','info'],
        ['正在抹除意外数据15/85','info'],
        ['正在抹除意外数据60/85','info'],
        ['正在抹除意外数据75/85','info'],
        ['正在抹除意外数据84/85','info'],
        ['意外数据抹除成功','info'],
        ['正在加载场景数据...','info'],
        ['正在加载场景数据:10%','info'],
        ['正在加载场景数据:25%','info'],
        ['正在加载场景数据:75%','info'],
        ['正在加载场景数据:80%','info'],
        ['正在加载场景数据:85%','info'],
        ['正在加载场景数据:90%','info'],
        ['正在加载场景数据:99%','info'],
        ['场景数据加载成功','info'],
        ['正在加载主角选择ui..','info'],
        ['正在加载主角选择ui:5%','info'],
        ['正在加载主角选择ui:75%','info'],
        ['正在加载主角选择ui:90%','info'],
        ['正在加载主角选择ui:99%','info'],
        ['主角选择ui加载成功','info'],
        ['正在进入.','info'],
        ['正在进入..','info'],
        ['正在进入...','info'],
        ['``','info']
    ]
    now_cmd_message = [[400-i*36,30,["",""]] for i in range(13)]

    clock.tick(FPS)
    pygame.display.flip()
    screen.fill((0,0,0))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        
        now_time = pygame.time.get_ticks()


        if now_time-last_time > max(sleep_time,70):
            last_time = now_time
            for i in range(12,0,-1):
                now_cmd_message[i][2] = now_cmd_message[i-1][2]
            now_cmd_message[0][2] = all_cmd_message.pop(0)

            for now_cmd in now_cmd_message:
                if now_cmd[2][0] != "":
                    if now_cmd[2][1] == "info":
                        draw_cmd_text(screen,now_cmd[2][0],now_cmd[1],now_cmd[0],(255,255,255),30,font_name)
                    else:
                        draw_cmd_text(screen,now_cmd[2][0],now_cmd[1],now_cmd[0],(255,0,0),30,font_name)

            if len(all_cmd_message) == 0:
                waiting = False
                return False

            sleep_time -= 100
            clock.tick(FPS)
            pygame.display.flip()
            screen.fill((0,0,0))

def draw_choice_screen(screen,clock,font_name,player_save_name):
    player_name = ""
    genders = ["男/他","女/她","奇美拉/祂","其他/祂"]
    gender_index = 0

    clock.tick(FPS)
    pygame.display.flip()
    screen.fill((0,0,0))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and gender_index < len(genders)-1:
                    gender_index += 1
                elif event.key == pygame.K_w and gender_index > 0:
                    gender_index -= 1
                elif event.key == pygame.K_RETURN:
                    write_data(f"性别:{genders[gender_index]}\n")
                    waiting = False
        
        clock.tick(FPS)
        pygame.display.flip()
        screen.fill((0,0,0))
        draw_text(screen,"请问你的性别是？",WIDTH/2-25,50,(255,255,255),35,font_name,True)
        #间隔3
        s = 0
        for gender in genders:
            is_bold = gender == genders[gender_index]
            darkness = 225
            draw_text(screen,gender,WIDTH/2-25,150+s,(darkness,darkness,darkness),25,font_name,is_bold)
            s+=30

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if player_name != "":
                        write_data(f"名字:{player_name}\n")
                        if player_name == "teto" and gender_index == 2:
                            waiting = False
                            return "teto_end"
                        waiting = False
                        return False
                elif event.unicode:
                    player_name += event.unicode
        
        clock.tick(FPS)
        pygame.display.flip()
        screen.fill((0,0,0))
        draw_text(screen,"请问你的姓名？",WIDTH/2-25,50,(255,255,255),35,font_name,True)
        draw_text(screen,player_name,WIDTH/2-25,150,(255,255,255),25,font_name,False)

def draw_start_plot_screen(screen,clock,font_name):
    
    start_plot_display = DialogBox(
        screen,
        load_font(font_name,25),
        [
            "我的父母把我送到了这个学校",
            "我的父母都不想见到我",
            "没办法的我只能认命....",
            "因为有保安的看守，我根本逃不出去"
        ],
        box_rect=(0,300,WIDTH,160),
        box_color=(50,50,50),
        text_color=(90,240,255),
        text_offset_x=60,
        text_offset_y=350
    )

    start_plot_display2 = DialogBox(
        screen,
        load_font(font_name,25),
        [
            "你手上多出来一张纸",
            "上面写着：三楼 6(5)"
        ],
        box_rect=(0,300,WIDTH,160),
        box_color=(50,50,50),
        text_color=(255,255,255),
        text_offset_x=60,
        text_offset_y=350
    )

    clock.tick(FPS)
    pygame.display.flip()
    screen.fill((0,0,0))
    
    start_plot_display.reset()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if start_plot_display.handle_event(event):
                waiting = False
        
        s = clock.tick(FPS)
        tp = s/1000
        
        start_plot_display.update(tp)
        screen.fill((0,0,0))
        screen.blit(people_img,(250,25))
        start_plot_display.draw()
        pygame.display.flip()

    start_plot_display2.reset()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if start_plot_display2.handle_event(event):
                waiting = False
                return False
        
        s = clock.tick(FPS)
        tp = s/1000
        
        start_plot_display2.update(tp)
        screen.fill((0,0,0))
        screen.blit(class_paper_img,(250,25))
        start_plot_display2.draw()
        pygame.display.flip()