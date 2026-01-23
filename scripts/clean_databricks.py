#!/usr/bin/env python3
"""
清理 Databricks 文章中的导航栏和页脚垃圾内容
只修改格式，不改动正文翻译
"""

import re
from pathlib import Path

class DatabricksArticleCleaner:
    def __init__(self):
        self.content_dir = Path("content/posts")
        self.cleaned = 0
        self.skipped = 0
        
        # 要删除的导航菜单模式
        self.nav_patterns = [
            r'\*\*探索\*\*.*?(?=\n#|\n##|\nFOX|\n巴斯夫|\n本文|\nAI已|\n基于)',
            r'\*\*面向高管\*\*',
            r'\*\*面向初创企业\*\*',
            r'\*\*湖仓一体架构\*\*',
            r'\*\*Mosaic 研究\*\*',
            r'\*\*客户\*\*\n\*\*客户案例\*\*',
            r'\*\*合作伙伴\*\*\n\*\*云服务提供商\*\*.*?(?=\n\*\*产品\*\*)',
            r'\*\*产品\*\*\n\*\*Databricks 平台\*\*.*?(?=\n\*\*解决方案\*\*|\n#)',
            r'\*\*解决方案\*\*\n\*\*Databricks 行业解决方案\*\*.*?(?=\n\*\*资源\*\*|\n#)',
            r'\*\*资源\*\*\n\*\*学习\*\*.*?(?=\n#|\n准备好开始)',
            r'\*\*公司\*\*\n\*\*我们是谁\*\*.*?(?=\n#|\n准备好)',
            r'\*\*深入探索\*\*',
            r'\*\*架构中心\*\*',
            r'\*\*演示中心\*\*',
            r'\*\*资源中心\*\*',
        ]
        
        # 页脚内容模式
        self.footer_patterns = [
            r'databricks logo\n.*?databricks logo',
            r'Databricks Inc\.\n\n160 Spear Street.*?保留所有权利。',
            r'隐私声明\n\|使用条款.*?您的隐私选择',
            r'查看 Databricks 的招聘职位',
            r'© Databricks \d{4}。保留所有权利。.*?Apache Software Foundation 的商标。',
        ]
        
        # 重复内容模式（同一行出现多次）
        self.duplicate_patterns = [
            r'(面向行业的Databricks.*?更快实现重要成果)\n\1',
            r'(通信\n媒体与娱乐.*?查看所有行业)\n\1',
            r'(学习培训.*?架构中心)\n\1',
            r'(公司关于我们.*?安全与信任)\n\1',
        ]
    
    def clean_article(self, filepath: Path) -> bool:
        """清理单篇文章，返回是否有修改"""
        content = filepath.read_text(encoding='utf-8')
        original = content
        
        # 分离 frontmatter 和正文
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
            else:
                return False
        else:
            return False
        
        # 清理正文
        cleaned_body = self._clean_body(body)
        
        # 如果有变化，保存
        if cleaned_body != body:
            new_content = f"---{frontmatter}---{cleaned_body}"
            filepath.write_text(new_content, encoding='utf-8')
            return True
        return False
    
    def _clean_body(self, body: str) -> str:
        """清理正文内容"""
        
        # 1. 删除连续的空列表项
        body = re.sub(r'(\n\s*-\s*\n){2,}', '\n\n', body)
        body = re.sub(r'^\s*-\s*$', '', body, flags=re.MULTILINE)
        
        # 2. 删除导航菜单块（大块匹配）
        # 匹配从 **探索** 或类似开始到正文开始的整块
        body = re.sub(
            r'\*\*探索\*\*\n\*\*面向高管\*\*.*?(?=\n# [^#]|\n## [^#]|\n\n[A-Z一-龥])',
            '',
            body,
            flags=re.DOTALL
        )
        
        # 3. 删除重复的菜单文本块
        body = re.sub(
            r'面向行业的Databricks通信媒体.*?更快实现重要成果\n',
            '',
            body,
            flags=re.DOTALL
        )
        
        # 4. 删除学习/活动/博客等菜单
        body = re.sub(
            r'学习培训发现.*?架构中心\n',
            '',
            body
        )
        
        # 5. 删除公司信息菜单
        body = re.sub(
            r'公司关于我们.*?安全与信任\n',
            '',
            body
        )
        
        # 6. 删除独立的菜单项列表
        menu_items = [
            '通信', '媒体与娱乐', '金融服务', '公共部门', '医疗与生命科学',
            '零售', '制造业', '查看所有行业', 'AI Agents（智能体）',
            '网络安全', '营销', '数据迁移', '专业服务',
            '关于我们', '我们的团队', 'Databricks Ventures', '联系我们',
            '在Databricks工作', '开放职位', '奖项与认可', '新闻中心',
            '安全与信任', '客户支持', '文档', '社区', '资源中心',
            '演示中心', '架构中心', 'Data \+ AI 峰会', 'Data \+ AI 全球巡演',
            'AI 日', '活动日历', 'databricks logo',
        ]
        for item in menu_items:
            body = re.sub(rf'^{re.escape(item)}\n', '', body, flags=re.MULTILINE)
        
        # 7. 删除页脚
        body = re.sub(
            r'Databricks Inc\.\n\n160 Spear Street.*?1-866-330-0121',
            '',
            body,
            flags=re.DOTALL
        )
        body = re.sub(
            r'© Databricks \d{4}。.*?Apache Software Foundation 的商标。',
            '',
            body,
            flags=re.DOTALL
        )
        body = re.sub(r'隐私声明\n\|使用条款.*?您的隐私选择', '', body)
        
        # 8. 删除重复的标题
        lines = body.split('\n')
        seen_titles = set()
        cleaned_lines = []
        for line in lines:
            if line.startswith('# ') or line.startswith('## '):
                if line in seen_titles:
                    continue
                seen_titles.add(line)
            # 跳过连续重复行
            if cleaned_lines and line == cleaned_lines[-1] and line.strip():
                continue
            cleaned_lines.append(line)
        body = '\n'.join(cleaned_lines)
        
        # 9. 清理多余空行
        body = re.sub(r'\n{4,}', '\n\n\n', body)
        
        # 10. 删除 "不错过任何Databricks的帖子" 及后面的推荐文章
        body = re.sub(
            r'不错过任何Databricks的帖子.*?(?=\n---\n|\Z)',
            '',
            body,
            flags=re.DOTALL
        )
        
        return body
    
    def clean_all_databricks(self):
        """清理所有 Databricks 文章"""
        print("=" * 60)
        print("清理 Databricks 文章")
        print("=" * 60)
        
        # 找到所有 Databricks 文章
        databricks_files = list(self.content_dir.glob("*databricks*.md"))
        print(f"\n找到 {len(databricks_files)} 篇 Databricks 文章\n")
        
        for filepath in databricks_files:
            print(f"处理: {filepath.name}...", end=" ")
            if self.clean_article(filepath):
                print("✓ 已清理")
                self.cleaned += 1
            else:
                print("- 无需修改")
                self.skipped += 1
        
        print("\n" + "=" * 60)
        print(f"完成！清理了 {self.cleaned} 篇，跳过 {self.skipped} 篇")
        print("=" * 60)


if __name__ == "__main__":
    cleaner = DatabricksArticleCleaner()
    cleaner.clean_all_databricks()
