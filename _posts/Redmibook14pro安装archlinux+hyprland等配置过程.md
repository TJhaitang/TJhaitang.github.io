---
title: Redmibook14pro从零开始的archlinux安装与配置
tags:
  - '普罗米修斯'
date: 2024-12-09 14:28:43
---

## 前言

## Reference

- [archlinux简明指南](https://arch.icekylin.online/guide/rookie/basic-install.html)
- [end-4/dots-hyprland](https://end-4.github.io/dots-hyprland-wiki/zh-cn/i-i/01setup/)
- [chinese input for Electron](https://zhuanlan.zhihu.com/p/692564515)
- [sound driver](https://github.com/DarkStalkr/Xiaomi_RedmiBookPro16_Audio_Fix)
- [fxitx5皮肤](https://www.cnblogs.com/maicss/p/15056420.html)
- [配置设备休眠](https://arch.icekylin.online/guide/advanced/optional-cfg-2)
- [grub-theme](https://github.com/vinceliuice/grub2-themes)
- [Xwayland高分屏](https://zhuanlan.zhihu.com/p/661883396)
- [lazyvim](https://www.lazyvim.org/)
- [lazyvim进一步配置](https://fanlumaster.github.io/2023/11/25/Lazyvim-configure-from-scratch/)

---

## 初步安装

准备好电脑、系统U盘、有线网络环境（无线也可，有线相对方便）后，按照上述链接的步骤进行安装。本文从上述链接结束处继续记录过程。

---

## 调整pacman源

- 增加archlinuxcn源

使用vim打开`/etc/pacman.conf`文件，在文件末尾添加以下内容

```bash
[archlinuxcn]
Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch
Server = https://repo.huaweicloud.com/archlinuxcn/$arch
```

- 增加32位支持

删除`/etc/pacman.d/mirrorlist`文件中的`[multilib]`部分的注释符号`#`，使其生效

- 对keyring进行更新

```bash
pacman -Syy && pacman -S archlinux-keyring archlinuxcn-keyring
```

## 添加用户

上述链接过程结束时，电脑应仅有root用户，并处于无桌面环境的情况下，此时需要添加一个日常用户

```bash
useradd -m -G wheel -s /bin/bash haitang
passwd haitang
```

使用`vim`编辑`/etc/sudoers`文件，取消`%wheel ALL=(ALL) ALL`行的注释符号`#`

## 功耗控制

### 设置休眠行为

修改以下内容

```bash /etc/systemd/logind.conf
HandlePowerKey=hibernate
HandleLidSwitchExternalPower=ignore
```

```bash /etc/mkinitcpio.conf
HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block filesystems resume fsck)
```

```bash /etc/defalut/grub
GRUB_CMDLINE_LINUX_DEFAULT="+resume=UUID=xxx"#指在参数中加入该项
```

之后，执行以下命令：
  
```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
sudo mkinitcpio -P
```

### 未完

- 设置suspend超时则hibernate
- 进一步的功耗控制

## 安装Gnome桌面

```bash
pacman -S gnome-extra
```

一路回车即可。安装完成后，输入

```bash
systemctl enable --now gdm
```

即可启动Gdm，使用日常账户haitang登录即可。

## 安装必要软件

```bash
sudo pacman -S wqy-microhei wqy-zenhei fcitx5-im fcitx5-chinese-addons firefox gnome-browser-connector power-profiles-daemon tailscale syncthing moonlight-qt texlive texlive-langchinese obsidian zotero plymouth tmux
yay -S clash-verge-rev microsoft-edge-stable-bin ttf-ubuntu-nerd-font linuxqq wechat-bin
```

- `firefox` 用于安装gnome插件
- `power-profiles-daemon` 用于调整电源模式
- 上述可能不全

## 配置开机自启动

- systemctl部分

```bash
systemctl enable --now tailscaled
systemctl enable --now syncthing@haitang
```

- hyprland OR Gnome
  - clash-verge
  - fcitx

## 给fxitx换一个皮肤

下载该[链接](https://www.cnblogs.com/maicss/p/15056420.html)中的文件，将其解压到`~/.local/share/fcitx5/themes`目录下，然后在`fcitx5配置`中选择该主题即可。


## 安装好用的gnome插件

- [Dash to Dock](https://extensions.gnome.org/extension/307/dash-to-dock/)
- [vitals](https://extensions.gnome.org/extension/1460/vitals/)
- [kimpanel](https://extensions.gnome.org/extension/261/kimpanel/)
- [appindicator](https://extensions.gnome.org/extension/615/appindicator-support/)

## 添加声卡驱动

根据上面的[链接](https://github.com/DarkStalkr/Xiaomi_RedmiBookPro16_Audio_Fix)成功播放了声音，但麦克风仍然不工作

## 安装Hyprland + end-4主题调整

首先感叹一下，Gnome是真的好看啊。
根据前面的[链接](https://end-4.github.io/dots-hyprland-wiki/zh-cn/i-i/01setup/)即可安装好Hyprland主题，然后再安装end-4主题。

### 换壁纸

```bash ~/.config/hypr/custom/exec.conf
# exec-once = swaybg -i /home/haitang/Pictures/wallpaper/f.jpg &
sleep 1 && exec-once = swww img "/home/haitang/Pictures/wallpaper/f.jpg" & #不知道为啥不起作用
```

### Foot配置

 实际上上述安装脚本已经对foot和fish进行了大量配置，我只是修改了字体与透明度

对`foot`配置文件的下述部分进行修改

```ini ~/.config/foot/foot.ini
font=UbuntuMono Nerd Font:size=13
[colors]
alpha=0.85

[key-bindings]
clipboard-copy=Control+Shift+c
clipboard-paste=Control+Shift+v
# primary-paste=Shift+Insert
search-start=Control+Shift+f
```

end-4主题中的修改主题颜色行为将覆盖上述的透明度设置，因此我屏蔽了这一部分。修改`fish`配置文件，注释以下内容

```py ~/.config/fish/config.fish
#if test -f ~/.cache/ags/user/generated/terminal/sequences.txt
#    cat ~/.cache/ags/user/generated/terminal/sequences.txt
#end
```

### Fish配置
将默认shell换为fish

```bash
chsh -s /bin/fish
```



### darkmode

其一，虽然我更加倾向于使用该主题的暗色版本，但`>dark`命令会将系统色调也换成暗色，我不希望这样。其二，不知道为什么`>dark`与`>light`命令会出错，因此，我对下述文件进行了修改

```javascript ~/.config/ags/modules/.miscutils/system.js
darkMode.connect('changed', ({ value }) => {
    let lightdark = value ? "dark" : "light";
    execAsync([`bash`, `-c`, `mkdir -p ${GLib.get_user_state_dir()}/ags/user && sed -i "1s/.*/${lightdark}/"  ${GLib.get_user_state_dir()}/ags/user/colormode.txt`])
        .then(execAsync(['bash', '-c', `${App.configDir}/scripts/color_generation/switchcolor.sh --pick`,`&`]))
        // .then(execAsync(['bash', '-c', `command -v darkman && darkman set ${lightdark}`])) // Optional darkman integration
        .catch(print);
});
```

``` bash ~/.config/ags/scripts/color_generation/applycolor.sh
apply_ags &
apply_hyprland &
apply_hyprlock &
# apply_lightdark &
# apply_gtk &
apply_fuzzel &
# apply_term &
```

### hyprlock调整

这部分懒得写了，就是适配了一下我的屏幕尺寸然后加了个毛玻璃效果

## 配置自动登陆

编辑`/etc/gdm/custom.conf`文件，修改以下内容

```ini /etc/gdm/custom.conf
[daemon]
AutomaticLoginEnable=True
AutomaticLogin=haitang
```

## 为grub增加主题

根据上述[链接](https://github.com/vinceliuice/grub2-themes)直接操作即可

## vscode无法输入中文

- 尚未解决
- 我怎么怀疑是Gnome的问题呢？

## 不清晰：Electron应用/Xwayland

该问题设计的软件有五

- microsoft-edge-stable-bin
- google-chrome
- obsidian
- linuxqq
- qqmusic

解决方法为修改相对应的在`/usr/share/applications`目录下的`.desktop`文件，在启动参数后加`--ozone-platform-hint=auto --enable-wayland-ime`即可。

同时，一方面上述软件在更新时会覆盖`.desktop`文件，另一方面上述软件也不需要更新，因此可以对上述软件的更新进行屏蔽

```bash /etc/pacman.conf
IgnorePkg = microsoft-edge-stable-bin google-chrome obsidian linuxqq qqmusic
```

Xwayland配置见[链接](https://zhuanlan.zhihu.com/p/661883396)

## plymouth
上面的安装部分中已经安装了plymouth，下面只需要启动即可。修改下述文件
```bash /etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="+splash"
```
```bash /etc/mkinitcpio.conf
HOOKS=(+plymouth)
```
之后执行
```bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
sudo mkinitcpio -P
```
即可。默认主题就是arch-logo足够了，不再进行修改。

## SSH
系统默认不启动`sshd`服务，因此需要手动启动
```bash
sudo systemctl enable --now sshd
```

## tmux
为tmux增加鼠标支持
```bash ~/.tmux.conf
set -g mouse on
```

## lazyVim

### 安装

```bash
mkdir .config/nvim
git clone https://github.com/LazyVim/starter ~/.config/nvim
rm -rf .config/nvim/.git
nvim
```

### 插件配置

目前的绝大多数需求可以完全由`LazyVim`满足，参见[链接](https://www.lazyvim.org/)

- 背景透明
```lua ~/.config/nvim/lua/plugins/colorscheme.lua
-- 核心配置
return{
  {
    "catppuccin/nvim",
    opts = {
      transparent_background = true,
    }
  }
}
```

- latexmk使用xelatex
多番尝试都失败了，最终选择编辑如下文件
```bash ~/.latexmkrc
$pdflatex = 'xelatex %O %S'
```
  

## ToDo

- 麦克风
- vscode无法使用中文输入法
  - 暂时使用hyprland可解
- kitty
- 使用nautilus打开地址
- NPU驱动
- hyprland快捷键
  - 打开设置
  - 电源管理
    - 帧率、电源管理文件
- lazyvim
- ags小组件
- 功率控制：根据archlinux简明指南
  - 这个简明指南是真的无敌
- 指纹

## 附录

简单记录一下装windows时装的东西

- clash-verge-rev
- vscode
- obs-studio
- VC runtime
- .net
- 米哈游启动器
- obsidian
- tailscale
- winbtrfs
- WPS
- 7-zip
- zotero
