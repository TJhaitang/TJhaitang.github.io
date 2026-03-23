#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_posts 文件夹文件名重命名脚本
功能：遍历 _posts 文件夹，将文件名开头不为日期的文件，
     根据其 front matter 中的 date 字段更新文件名，将日期放在原文件名前
"""

import os
import re
from pathlib import Path
from datetime import datetime


def extract_date_from_frontmatter(file_path):
    """
    从 Markdown 文件的 front matter 中提取 date 字段
    
    Args:
        file_path: 文件路径
        
    Returns:
        提取的日期字符串 (YYYY-MM-DD 格式)，如果未找到则返回 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有 front matter (以 --- 开头)
        if not content.startswith('---'):
            return None
        
        # 查找第二个 --- 的位置
        end_match = re.search(r'\n---\n', content[3:])
        if not end_match:
            return None
        
        frontmatter = content[3:end_match.start() + 3]
        
        # 提取 date 字段
        date_match = re.search(r'^date:\s*(.+)$', frontmatter, re.MULTILINE)
        if not date_match:
            return None
        
        date_str = date_match.group(1).strip()
        
        # 尝试解析多种日期格式
        date_formats = [
            '%Y-%m-%d %H:%M:%S',  # 2021-10-27 00:50:23
            '%Y-%m-%d',           # 2018-06-01
            '%Y/%m/%d %H:%M:%S',  # 2021/10/27 00:50:23
            '%Y/%m/%d',           # 2021/10/27
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # 如果所有格式都失败，尝试直接提取 YYYY-MM-DD 部分
        simple_date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_str)
        if simple_date_match:
            return simple_date_match.group(1)
            
        return None
        
    except Exception as e:
        print(f"读取文件 {file_path} 时出错：{e}")
        return None


def is_filename_with_date(filename):
    """
    检查文件名是否已经以日期开头 (YYYY-MM-DD-)
    
    Args:
        filename: 文件名
        
    Returns:
        True 如果文件名以日期开头，否则 False
    """
    # 匹配 YYYY-MM-DD- 或 YYYY_MM_DD_ 格式
    pattern = r'^\d{4}[-_]\d{2}[-_]\d{2}[-_]'
    return bool(re.match(pattern, filename))


def rename_file(file_path, date_str):
    """
    重命名文件，在文件名前添加日期
    
    Args:
        file_path: 原文件路径
        date_str: 日期字符串 (YYYY-MM-DD)
        
    Returns:
        新文件路径
    """
    directory = file_path.parent
    original_name = file_path.name
    
    # 创建新文件名
    new_name = f"{date_str}-{original_name}"
    new_path = directory / new_name
    
    # 检查新文件名是否已存在
    if new_path.exists():
        print(f"  ⚠️  跳过：新文件名已存在 - {new_name}")
        return None
    
    # 重命名文件
    try:
        file_path.rename(new_path)
        print(f"  ✓ 重命名：{original_name} → {new_name}")
        return new_path
    except Exception as e:
        print(f"  ✗ 重命名失败：{e}")
        return None


def process_posts_folder(posts_dir):
    """
    处理 _posts 文件夹中的所有文件
    
    Args:
        posts_dir: _posts 文件夹路径
    """
    posts_path = Path(posts_dir)
    
    if not posts_path.exists():
        print(f"错误：目录不存在 - {posts_dir}")
        return
    
    # 获取所有 markdown 文件
    md_files = list(posts_path.glob('*.md'))
    
    if not md_files:
        print("未找到任何 .md 文件")
        return
    
    print(f"找到 {len(md_files)} 个 markdown 文件")
    print("-" * 60)
    
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in md_files:
        filename = file_path.name
        
        # 检查文件名是否已经包含日期
        if is_filename_with_date(filename):
            print(f"⊘ 跳过 (已有日期): {filename}")
            skipped_count += 1
            continue
        
        # 从 front matter 提取日期
        date_str = extract_date_from_frontmatter(file_path)
        
        if not date_str:
            print(f"✗ 跳过 (无日期字段): {filename}")
            error_count += 1
            continue
        
        # 重命名文件
        new_path = rename_file(file_path, date_str)
        if new_path:
            renamed_count += 1
    
    print("-" * 60)
    print(f"处理完成:")
    print(f"  ✓ 重命名：{renamed_count} 个文件")
    print(f"  ⊘ 已跳过：{skipped_count} 个文件 (已有日期)")
    print(f"  ✗ 出错误：{error_count} 个文件 (无日期字段)")


def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    
    # _posts 目录路径 (相对于脚本目录的父目录)
    posts_dir = script_dir.parent / '_posts'
    
    print("=" * 60)
    print("_posts 文件重命名工具")
    print("=" * 60)
    print(f"目标目录：{posts_dir}")
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
