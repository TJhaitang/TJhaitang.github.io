#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在 _drafts 目录下创建新草稿文件
用法：python create_draft.py <文件名>
示例：python create_draft.py "我的新文章"
      将创建：2026-03-24-我的新文章.md
"""

import sys
from pathlib import Path
from datetime import datetime


def create_draft(draft_name):
    """
    在 _drafts 目录下创建新草稿
    
    Args:
        draft_name: 草稿名称（不包含扩展名）
        
    Returns:
        True 如果创建成功，否则 False
    """
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    
    # _drafts 目录路径 (相对于脚本目录的父目录)
    drafts_dir = script_dir.parent / '_drafts'
    
    # 检查 _drafts 目录是否存在
    if not drafts_dir.exists():
        print(f"错误：_drafts 目录不存在 - {drafts_dir}")
        return False
    
    # 生成当前日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 创建文件名
    filename = f"{today}-{draft_name}.md"
    file_path = drafts_dir / filename
    
    # 检查文件是否已存在
    if file_path.exists():
        print(f"警告：文件已存在 - {filename}")
        response = input("是否覆盖？(y/n): ").strip().lower()
        if response not in ['y', 'yes']:
            print("已取消操作")
            return False
    
    # 创建默认的 front matter 模板
    frontmatter = f"""---
title: {draft_name}
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags: []
categories: []
---

# {draft_name}

在这里开始写作...

<!--more-->

"""
    
    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
        
        print(f"✓ 草稿创建成功！")
        print(f"  文件名：{filename}")
        print(f"  路径：{file_path}")
        return True
        
    except Exception as e:
        print(f"✗ 创建失败：{e}")
        return False


def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("=" * 60)
        print("草稿创建工具")
        print("=" * 60)
        print(f"用法：python {sys.argv[0]} <草稿名称>")
        print()
        print("示例:")
        print(f"  python {sys.argv[0]} \"我的第一篇草稿\"")
        print(f"  python {sys.argv[0]} \"组会记录\"")
        print()
        print("=" * 60)
        sys.exit(1)
    
    # 获取草稿名称 (支持带引号的多词名称)
    draft_name = sys.argv[1]
    
    print("=" * 60)
    print("创建新草稿")
    print("=" * 60)
    print(f"草稿名称：{draft_name}")
    print()
    
    # 创建草稿
    success = create_draft(draft_name)
    
    print()
    print("=" * 60)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
