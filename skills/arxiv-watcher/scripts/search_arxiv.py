#!/usr/bin/env python3
"""ArXiv 论文搜索脚本（Windows 兼容版）"""
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def search_arxiv(query, count=5):
    """搜索 ArXiv 论文"""
    encoded_query = urllib.parse.quote(query)
    url = f"https://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={count}&sortBy=submittedDate&sortOrder=descending"
    
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'ArXiv-Watcher/1.0')
    
    with urllib.request.urlopen(req, timeout=30) as response:
        xml_data = response.read().decode('utf-8')
    
    # 解析 XML
    root = ET.fromstring(xml_data)
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip()
        summary = entry.find('atom:summary', ns).text.strip()
        id_elem = entry.find('atom:id', ns)
        paper_id = id_elem.text.split('/abs/')[-1] if id_elem is not None else 'N/A'
        link = f"https://arxiv.org/abs/{paper_id}"
        pdf_link = f"https://arxiv.org/pdf/{paper_id}"
        
        # 提取作者
        authors = []
        for author in entry.findall('atom:author', ns):
            name = author.find('atom:name', ns)
            if name is not None:
                authors.append(name.text)
        
        # 提取日期
        published = entry.find('atom:published', ns)
        date = published.text.split('T')[0] if published is not None else 'N/A'
        
        papers.append({
            'title': title,
            'summary': summary[:300] + '...' if len(summary) > 300 else summary,
            'paper_id': paper_id,
            'link': link,
            'pdf_link': pdf_link,
            'authors': ', '.join(authors[:3]) + (' et al.' if len(authors) > 3 else ''),
            'date': date
        })
    
    return papers

if __name__ == '__main__':
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'artificial intelligence'
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    papers = search_arxiv(query, count)
    
    print(f"\n{'='*80}")
    print(f"ArXiv 搜索结果: {query} (共找到 {len(papers)} 篇论文)")
    print(f"{'='*80}\n")
    
    for i, paper in enumerate(papers, 1):
        print(f"【{i}】{paper['title']}")
        print(f"    作者: {paper['authors']}")
        print(f"    日期: {paper['date']}")
        print(f"    链接: {paper['link']}")
        print(f"    摘要: {paper['summary']}")
        print(f"{'-'*80}\n")
