#!/usr/bin/env python3
"""
Raindrops CSV to Obsidian Web Clipper Markdown Converter

This script converts CSV backup files from Raindrops.io to markdown files
compatible with the Obsidian Web Clipper format.

Usage:
    python raindrops-to-obsidian-clipper.py input.csv [output_directory]

Version: 1.0
"""

import csv
import os
import re
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
import argparse
import sys


def sanitize_filename(title):
    """
    Sanitize a string to be used as a filename.
    
    Args:
        title (str): The original title
        
    Returns:
        str: Sanitized filename
    """
    if not title or title.strip() == '':
        return "Untitled"
    
    # Remove or replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    filename = re.sub(r'[^\w\s\-_.,()[\]{}#@&+=!~]', '', filename)
    filename = re.sub(r'\s+', ' ', filename).strip()
    
    # Limit length (Windows has 255 char limit, leave room for .md extension)
    if len(filename) > 250:
        filename = filename[:250].rstrip()
    
    return filename if filename else "Untitled"


def extract_domain(url):
    """
    Extract domain from URL for author field.
    
    Args:
        url (str): The URL
        
    Returns:
        str: Domain name or empty string if invalid URL
    """
    try:
        if not url or url.strip() == '':
            return ''
        domain = urlparse(url).netloc
        return domain.replace('www.', '') if domain else ''
    except:
        return ''


def format_tags(tags_str, folder):
    """
    Format tags for the YAML front matter.
    
    Args:
        tags_str (str): Comma-separated tags string
        folder (str): Folder name to be used as additional tag
        
    Returns:
        list: List of formatted tags
    """
    tags = ['clippings']  # Always include 'clippings' tag
    
    # Add folder as tag if it's not 'Unsorted'
    if folder and folder.lower() != 'unsorted':
        # Convert folder name to lowercase and replace spaces with hyphens
        folder_tag = folder.lower().replace(' ', '-')
        tags.append(folder_tag)
    
    # Process existing tags
    if tags_str and tags_str.strip():
        existing_tags = [tag.strip().lower().replace(' ', '-') 
                        for tag in tags_str.split(',') 
                        if tag.strip()]
        tags.extend(existing_tags)
    
    # Remove duplicates while preserving order
    unique_tags = []
    for tag in tags:
        if tag not in unique_tags:
            unique_tags.append(tag)
    
    return unique_tags


def format_date(date_str):
    """
    Format date string for YAML front matter.
    
    Args:
        date_str (str): ISO date string
        
    Returns:
        str: Formatted date (YYYY-MM-DD) or empty string
    """
    try:
        if not date_str or date_str.strip() == '':
            return ''
        # Parse ISO format and return just the date part
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except:
        return ''


def create_markdown_content(row):
    """
    Create markdown content from a CSV row.
    
    Args:
        row (dict): Dictionary containing the CSV row data
        
    Returns:
        str: Formatted markdown content
    """
    title = row.get('title', '').strip()
    url = row.get('url', '').strip()
    excerpt = row.get('excerpt', '').strip()
    note = row.get('note', '').strip()
    tags_str = row.get('tags', '').strip()
    folder = row.get('folder', '').strip()
    created = row.get('created', '').strip()
    cover = row.get('cover', '').strip()
    highlights = row.get('highlights', '').strip()
    
    # Format components
    domain = extract_domain(url)
    author = f"[[{domain}]]" if domain else ""
    formatted_date = format_date(created)
    formatted_tags = format_tags(tags_str, folder)
    
    # Build YAML front matter
    yaml_lines = ['---']
    
    if author:
        yaml_lines.append('author:')
        yaml_lines.append(f"- '{author}'")
    
    if formatted_date:
        yaml_lines.append(f"created: '{formatted_date}'")
    
    if excerpt:
        # Escape quotes and handle multiline descriptions
        escaped_excerpt = excerpt.replace('"', '\\"').replace('\n', ' ')
        yaml_lines.append(f'description: {escaped_excerpt}')
    
    yaml_lines.append("published: ''")
    
    if url:
        yaml_lines.append(f'source: {url}')
    
    yaml_lines.append('tags:')
    for tag in formatted_tags:
        yaml_lines.append(f'- {tag}')
    
    yaml_lines.append(f'title: {title}')
    yaml_lines.append('---')
    
    # Build content
    content_lines = yaml_lines[:]
    
    # Add summary section if we have excerpt or note
    if excerpt or note:
        content_lines.append('')
        content_lines.append('## Summary')
        content_lines.append('')
        if excerpt:
            content_lines.append(excerpt)
        if note:
            if excerpt:
                content_lines.append('')
            content_lines.append(note)
    
    # Add highlights if available
    if highlights and highlights.strip():
        content_lines.append('')
        content_lines.append('## Highlights')
        content_lines.append('')
        content_lines.append(highlights)
    
    # Add source link
    if url:
        content_lines.append('')
        content_lines.append('## Source')
        content_lines.append('')
        content_lines.append(f'[View Original]({url})')
    
    return '\n'.join(content_lines)


def convert_csv_to_markdown(csv_file, output_dir='output'):
    """
    Convert Raindrops CSV to Obsidian Web Clipper markdown files.
    
    Args:
        csv_file (str): Path to the input CSV file
        output_dir (str): Output directory for markdown files
        
    Returns:
        tuple: (successful_conversions, failed_conversions)
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    successful_conversions = 0
    failed_conversions = 0
    created_files = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            # Use csv.Sniffer to detect delimiter
            sample = file.read(1024)
            file.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(file, delimiter=delimiter)
            
            # Count total rows for progress
            total_rows = sum(1 for _ in reader)
            file.seek(0)
            reader = csv.DictReader(file, delimiter=delimiter)
            
            print(f"Processing {total_rows} entries from CSV...")
            print()
            
            for row in reader:
                try:
                    title = row.get('title', '').strip()
                    if not title:
                        title = "Untitled"
                    
                    # Create filename
                    filename = sanitize_filename(title) + '.md'
                    filepath = os.path.join(output_dir, filename)
                    
                    # Create markdown content
                    markdown_content = create_markdown_content(row)
                    
                    # Write file
                    with open(filepath, 'w', encoding='utf-8') as md_file:
                        md_file.write(markdown_content)
                    
                    successful_conversions += 1
                    created_files.append(filename)
                    
                except Exception as e:
                    print(f"Error processing row with title '{row.get('title', 'Unknown')}': {e}")
                    failed_conversions += 1
                    continue
    
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return 0, 1
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return 0, 1
    
    # Print summary
    print()
    print("Conversion complete!")
    print(f"Successfully converted: {successful_conversions} files")
    print(f"Failed conversions: {failed_conversions}")
    
    if created_files:
        print("Files created or modified:")
        # Show first 10 files as examples
        for filename in created_files[:10]:
            print(f"- {output_dir}/{filename}")
        if len(created_files) > 10:
            print(f"... and {len(created_files) - 10} more files")
    
    return successful_conversions, failed_conversions


def main():
    """Main function to handle command line arguments and run the conversion."""
    parser = argparse.ArgumentParser(
        description='Convert Raindrops CSV backup to Obsidian Web Clipper markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python raindrops-to-obsidian-clipper.py bookmarks.csv
  python raindrops-to-obsidian-clipper.py bookmarks.csv my_notes
  python raindrops-to-obsidian-clipper.py bookmarks.csv /path/to/obsidian/vault
        """
    )
    
    parser.add_argument('csv_file', help='Path to the Raindrops CSV backup file')
    parser.add_argument('output_dir', nargs='?', default='output',
                       help='Output directory for markdown files (default: output)')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.csv_file):
        print(f"Error: Input file '{args.csv_file}' does not exist.")
        sys.exit(1)
    
    # Run conversion
    successful, failed = convert_csv_to_markdown(args.csv_file, args.output_dir)
    
    # Exit with appropriate code
    if failed > 0 and successful == 0:
        sys.exit(1)  # All conversions failed
    elif failed > 0:
        sys.exit(2)  # Some conversions failed
    else:
        sys.exit(0)  # All conversions successful


if __name__ == '__main__':
    main()