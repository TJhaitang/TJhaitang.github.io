#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片路径校验调整脚本
功能：遍历 _posts 文件夹中的所有 markdown 文件，
     将相对路径的图片地址转换为 GitHub 绝对地址
     相对路径前添加：https://raw.githubusercontent.com/TJhaitang/TJhaitang.github.io/refs/heads/master/_posts/
"""

import os
import re
from pathlib import Path


# GitHub 原始内容 URL 前缀
GITHUB_RAW_PREFIX = "https://raw.githubusercontent.com/TJhaitang/TJhaitang.github.io/refs/heads/master/_posts/"


def is_relative_path(image_url):
    """
    检查图片 URL 是否为相对路径
    
    Args:
        image_url: 图片 URL 字符串
        
    Returns:
        True 如果是相对路径，否则 False
    """
    # 不以 http://, https://, // 开头的视为相对路径
    return not re.match(r'^(https?:)?//', image_url)


def convert_to_absolute_path(image_url, current_file_dir):
    """
    将相对路径转换为绝对路径
    
    Args:
        image_url: 原图片 URL
        current_file_dir: 当前 markdown 文件所在目录
        
    Returns:
        转换后的绝对路径 URL
    """
    if not is_relative_path(image_url):
        return image_url
    
    # 去除可能的前导 ./ 
    if image_url.startswith('./'):
        image_url = image_url[2:]
    
    # 对于相对路径，直接添加 GitHub RAW 前缀
    # 因为原路径是相对于 _posts 目录的（如 images/xxx.png）
    absolute_url = GITHUB_RAW_PREFIX + image_url
    
    return absolute_url


def process_markdown_images(file_path):
    """
    处理单个 markdown 文件中的图片链接
    
    Args:
        file_path: markdown 文件路径
        
    Returns:
        修改后的内容，以及是否发生了更改
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 获取文件所在目录
        file_dir = file_path.parent
        
        # Markdown 图片语法：![alt](url)
        # 匹配所有图片链接
        image_pattern = r'(!\[.*?\])\((.*?)\)'
        
        def replace_image_url(match):
            """替换图片 URL 的回调函数"""
            alt_text = match.group(1)
            image_url = match.group(2).strip()
            
            # 转换相对路径为绝对路径
            new_url = convert_to_absolute_path(image_url, file_dir)
            
            # 如果 URL 没有变化，保持原样
            if new_url == image_url:
                return match.group(0)
            
            return f'{alt_text}({new_url})'
        
        # 替换所有图片链接
        new_content = re.sub(image_pattern, replace_image_url, content)
        
        # 检查是否有改动
        modified = new_content != original_content
        
        return new_content, modified
        
    except Exception as e:
        print(f"  ✗ 处理文件 {file_path.name} 时出错：{e}")
        return None, False


def process_posts_folder(posts_dir):
    """
    处理 _posts 文件夹中的所有 markdown 文件
    
    Args:
        posts_dir: _posts 文件夹路径
    """
    posts_path = Path(posts_dir)
    
    if not posts_path.exists():
        print(f"错误：目录不存在 - {posts_dir}")
        return
    
    # 获取所有 markdown 文件（不包括子目录）
    md_files = list(posts_path.glob('*.md'))
    
    if not md_files:
        print("未找到任何 .md文件")
        return
    
    print(f"找到 {len(md_files)} 个 markdown 文件")
    print("-" * 60)
    
    modified_count = 0
    unchanged_count = 0
    error_count = 0
    
    for file_path in md_files:
        filename = file_path.name
        
        # 处理文件
        new_content, modified = process_markdown_images(file_path)
        
        if new_content is None:
            error_count += 1
            continue
        
        if modified:
            # 写回文件
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ 已更新：{filename}")
                modified_count += 1
            except Exception as e:
                print(f"✗ 写入失败 {filename}: {e}")
                error_count += 1
        else:
            print(f"⊘ 无改动：{filename}")
            unchanged_count += 1
    
    print("-" * 60)
    print(f"处理完成:")
    print(f"  ✓ 已修改：{modified_count} 个文件")
    print(f"  ⊘ 未改动：{unchanged_count} 个文件")
    print(f"  ✗ 出错误：{error_count} 个文件")


def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    
    # _posts 目录路径 (相对于脚本目录的父目录)
    posts_dir = script_dir.parent / '_posts'
    
    print("=" * 60)
    print("图片路径校验调整工具")
    print("=" * 60)
    print(f"目标目录：{posts_dir}")
    print(f"相对路径将转换为：{GITHUB_RAW_PREFIX}")
    print()
    
    # 询问用户确认
    response = input("是否继续？(y/n): ").strip().lower()
    if response not in ['y', 'yes']:
        print("已取消操作")
        return
    
    print()
    process_posts_folder(posts_dir)
    
    print()
    print("=" * 60)


if __name__ == '__main__':
    main()
