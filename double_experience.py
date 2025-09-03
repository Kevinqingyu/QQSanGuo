#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re

def fix_json_syntax(content):
    """
    修复JSON文件中的语法错误（多余的逗号）
    """
    # 移除对象和数组末尾的多余逗号
    content = re.sub(r',\s*}', '}', content)
    content = re.sub(r',\s*]', ']', content)
    return content

def double_monster_experience(file_path):
    """
    将怪物数据文件中所有怪物的经验值翻倍
    """
    # 读取原始文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复JSON语法
    content = fix_json_syntax(content)
    
    # 解析JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return
    
    # 统计修改的怪物数量
    modified_count = 0
    
    # 遍历所有怪物数据
    for monster_name, monster_data in data.items():
        # 检查是否有经验字段
        if isinstance(monster_data, dict) and '经验' in monster_data:
            old_exp = monster_data['经验']
            # 将经验值翻倍
            monster_data['经验'] = old_exp * 2
            modified_count += 1
            print(f"修改 {monster_name}: 经验 {old_exp} -> {monster_data['经验']}")
    
    # 备份原文件
    backup_path = file_path + '.backup'
    if not os.path.exists(backup_path):
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')
        print(f"已创建备份文件: {backup_path}")
    
    # 写入修改后的数据
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent='\t')
        print(f"\n文件写入成功: {file_path}")
        
        # 验证写入结果
        with open(file_path, 'r', encoding='utf-8') as f:
            verify_content = f.read()
        verify_content = fix_json_syntax(verify_content)
        verify_data = json.loads(verify_content)
        
        # 检查几个怪物的经验值
        test_monsters = ['黄巾斥侯', '竹叶青', '金丝猴']
        for monster in test_monsters:
            if monster in verify_data and '经验' in verify_data[monster]:
                print(f"验证 {monster}: 经验 = {verify_data[monster]['经验']}")
        
    except Exception as e:
        print(f"文件写入失败: {e}")
        return
    
    print(f"\n总共修改了 {modified_count} 个怪物的经验值")
    print(f"文件已更新: {file_path}")

if __name__ == '__main__':
    # 怪物数据文件路径
    monster_file = '/Users/macintoshhd/QQSanGuo/json/怪物数据.json'
    
    if os.path.exists(monster_file):
        print(f"开始处理文件: {monster_file}")
        double_monster_experience(monster_file)
        print("处理完成！")
    else:
        print(f"文件不存在: {monster_file}")