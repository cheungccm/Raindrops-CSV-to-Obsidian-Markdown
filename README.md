# Raindrops to Obsidian Web Clipper Converter

A Python script that converts CSV backup files from Raindrops.io to markdown files compatible with the Obsidian Web Clipper format.

## Features

- **Batch Conversion**: Convert entire Raindrops.io CSV backups to Obsidian-compatible markdown files
- **YAML Front Matter**: Generates proper metadata including author, creation date, tags, and source URL
- **Smart Tag Management**: Automatically includes 'clippings' tag and converts folder names to tags
- **Content Organization**: Structures content with Summary, Highlights, and Source sections
- **Safe File Naming**: Sanitizes titles to create valid filenames across different operating systems
- **Progress Tracking**: Shows conversion progress and summary statistics
- **Error Handling**: Graceful handling of malformed data with detailed error reporting

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone this repository or download the script:
```bash
git clone https://github.com/yourusername/raindrops-to-obsidian-clipper.git
cd raindrops-to-obsidian-clipper
```

2. Make the script executable (optional):
```bash
chmod +x raindrops-to-obsidian-clipper.py
```

## Usage

### Basic Usage

```bash
python raindrops-to-obsidian-clipper.py input.csv
```

This will create markdown files in an `output/` directory.

### Specify Output Directory

```bash
python raindrops-to-obsidian-clipper.py bookmarks.csv my_notes
```

### Export Directly to Obsidian Vault

```bash
python raindrops-to-obsidian-clipper.py bookmarks.csv /path/to/obsidian/vault
```

### Command Line Options

- `csv_file`: Path to the Raindrops CSV backup file (required)
- `output_dir`: Output directory for markdown files (optional, default: 'output')
- `--version`: Show version information
- `--help`: Show help message

## Input Format

The script expects a CSV file exported from Raindrops.io with the following columns:
- `id`: Unique identifier
- `title`: Article/bookmark title
- `note`: Personal notes
- `excerpt`: Article excerpt/description
- `url`: Source URL
- `folder`: Raindrops folder name
- `tags`: Comma-separated tags
- `created`: Creation date (ISO format)
- `cover`: Cover image URL
- `highlights`: Article highlights
- `favorite`: Favorite status

## Output Format

Each bookmark is converted to a markdown file with:

### YAML Front Matter
```yaml
---
author:
- '[[domain.com]]'
created: '2025-01-15'
description: Article description or excerpt
published: ''
source: https://example.com/article
tags:
- clippings
- folder-name
- custom-tag
title: Article Title
---
```

### Content Structure
- **Summary**: Contains excerpt and personal notes
- **Highlights**: Article highlights (if available)
- **Source**: Link back to original article

## Examples

### Converting a Raindrops Export
```bash
# Export your bookmarks from Raindrops.io as CSV
python raindrops-to-obsidian-clipper.py raindrops-export.csv

# Output will be in ./output/ directory
ls output/
```

### Integration with Obsidian
```bash
# Convert directly to your Obsidian vault
python raindrops-to-obsidian-clipper.py raindrops-export.csv "/Users/username/Documents/MyVault/Web Clips"
```

## File Naming

The script automatically sanitizes filenames by:
- Removing invalid characters (`<>:"/\|?*`)
- Replacing multiple spaces with single spaces
- Limiting filename length to 250 characters
- Fallback to "Untitled" for empty titles

## Error Handling

The script provides detailed error reporting:
- **File not found**: Clear error message for missing input files
- **Malformed data**: Continues processing other entries if one fails
- **Encoding issues**: Handles UTF-8 encoding properly
- **Exit codes**: 0 (success), 1 (all failed), 2 (some failed)

## Output Example

```
Processing 1250 entries from CSV...

Conversion complete!
Successfully converted: 1247 files
Failed conversions: 3
Files created or modified:
- output/How to Build Better Habits.md
- output/The Science of Learning.md
- output/Productivity Tips for Remote Work.md
... and 1244 more files
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0
- Initial release
- Basic CSV to markdown conversion
- YAML front matter generation
- Tag and folder processing
- File sanitization
- Error handling and progress reporting

## Troubleshooting

### Common Issues

**"CSV file not found"**
- Ensure the CSV file path is correct
- Check file permissions

**"Some conversions failed"**
- Check the error messages for specific issues
- Verify CSV format matches Raindrops.io export format

**"Files not appearing in Obsidian"**
- Ensure output directory is within your Obsidian vault
- Try refreshing Obsidian's file explorer

### Support

If you encounter issues or have suggestions, please [open an issue](https://github.com/yourusername/raindrops-to-obsidian-clipper/issues) on GitHub.

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7970958/aa987efd-989e-4d9a-9136-91c6ccb928e2/raindrops-to-obsidian-clipper.py
