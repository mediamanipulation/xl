import os
import fnmatch
import glob
import sys
from datetime import datetime

def should_include_file(file_path, patterns, verbose=False):
    """
    Determine if a file should be included based on gitignore patterns.
    With a deny-all approach, file needs to match at least one include pattern.
    """
    # Convert file path to use forward slashes for consistency
    file_path = file_path.replace('\\', '/')
    
    # Start with not included since the gitignore has a deny-all pattern
    included = False
    
    if verbose:
        print(f"Checking file: {file_path}")
    
    for pattern in patterns:
        # Check include patterns (starting with !)
        if pattern.startswith('!'):
            clean_pattern = pattern[1:]  # Remove the ! prefix
            if fnmatch.fnmatch(file_path, clean_pattern):
                if verbose:
                    print(f"  Included due to pattern: {pattern}")
                included = True
        # Check exclude patterns (regular patterns)
        else:
            if fnmatch.fnmatch(file_path, pattern):
                if verbose:
                    print(f"  Excluded due to pattern: {pattern}")
                included = False
    
    return included

def parse_gitignore(gitignore_path, verbose=False):
    """Parse the .gitignore file and return separate include and exclude patterns."""
    if not os.path.exists(gitignore_path):
        if verbose:
            print(f"No .gitignore found at {gitignore_path}")
        return []
    
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if verbose:
        print(f"Read {len(lines)} lines from .gitignore")
    
    patterns = []
    for line in lines:
        # Remove comments and whitespace
        line = line.split('#')[0].strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Add the pattern
        patterns.append(line)
        
        # Special handling for directory patterns
        if line.endswith('/') and not line.startswith('!'):
            # Add a pattern to match all files in that directory
            patterns.append(f"{line}**")
    
    if verbose:
        print(f"Parsed {len(patterns)} patterns from .gitignore")
        for pattern in patterns:
            print(f"  Pattern: {pattern}")
    
    return patterns

def is_binary_file(file_path):
    """Check if a file is binary by attempting to read it as text."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)  # Try to read as text
        return False
    except UnicodeDecodeError:
        return True
    except Exception as e:
        print(f"Error checking if {file_path} is binary: {str(e)}")
        return True  # Assume binary if there's an error

def find_included_files(root_dir, gitignore_patterns, verbose=False):
    """Find all files that should be included based on gitignore patterns."""
    included_files = []
    excluded_files = []
    binary_files = []
    error_files = []
    
    if verbose:
        print(f"Searching for files in {root_dir}")
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip .git directory
        if '.git' in dirpath.split(os.sep):
            continue
        
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root_dir)
            
            # Skip app.txt (our output file)
            if filename == 'app.txt':
                continue
            
            try:
                # Check if file is binary
                if is_binary_file(file_path):
                    if verbose:
                        print(f"  Skipping binary file: {rel_path}")
                    binary_files.append(rel_path)
                    continue
                
                # Check if file should be included
                rel_path_unix = rel_path.replace('\\', '/')
                if should_include_file(rel_path_unix, gitignore_patterns, verbose):
                    if verbose:
                        print(f"  File is included: {rel_path}")
                    included_files.append(file_path)
                else:
                    if verbose:
                        print(f"  File is excluded: {rel_path}")
                    excluded_files.append(rel_path)
            except Exception as e:
                if verbose:
                    print(f"  Error processing file {rel_path}: {str(e)}")
                error_files.append((rel_path, str(e)))
    
    if verbose:
        print(f"Found {len(included_files)} included files")
        print(f"Excluded {len(excluded_files)} files based on gitignore patterns")
        print(f"Skipped {len(binary_files)} binary files")
        print(f"Encountered errors with {len(error_files)} files")
    
    return included_files

def create_app_txt(files, output_path, verbose=False):
    """Create a single file with contents of all included files."""
    if not files:
        if verbose:
            print("No files to write to app.txt")
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write("No files found to include in app.txt")
        return
    
    successfully_written = 0
    failed_to_write = 0
    
    with open(output_path, 'w', encoding='utf-8') as out_file:
        out_file.write(f"App Content Summary\n")
        out_file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_file.write(f"Total Files: {len(files)}\n\n")
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as in_file:
                    rel_path = os.path.relpath(file_path)
                    out_file.write(f"\n\n{'='*80}\n")
                    out_file.write(f"FILE: {rel_path}\n")
                    out_file.write(f"{'='*80}\n\n")
                    
                    content = in_file.read()
                    out_file.write(content)
                    
                    if verbose:
                        print(f"Added {rel_path} to app.txt ({len(content)} characters)")
                    
                    successfully_written += 1
            except Exception as e:
                out_file.write(f"\n\n{'='*80}\n")
                out_file.write(f"FILE: {rel_path}\n")
                out_file.write(f"ERROR: Could not read file: {str(e)}\n")
                out_file.write(f"{'='*80}\n\n")
                
                if verbose:
                    print(f"Error writing {file_path} to app.txt: {str(e)}")
                
                failed_to_write += 1
    
    if verbose:
        print(f"Successfully wrote {successfully_written} files to app.txt")
        print(f"Failed to write {failed_to_write} files")

def main():
    # Enable verbose mode
    verbose = True
    
    # Get the project root directory (current directory)
    root_dir = os.getcwd()
    
    if verbose:
        print(f"Project root directory: {root_dir}")
        print(f"Python version: {sys.version}")
    
    # Parse .gitignore
    gitignore_path = os.path.join(root_dir, '.gitignore')
    gitignore_patterns = parse_gitignore(gitignore_path, verbose)
    
    if not gitignore_patterns:
        if verbose:
            print("No gitignore patterns found, using basic patterns")
        gitignore_patterns = ["*", "!*.py", "!*.json", "!*.md", "!*/"]
    
    # Find all files that should be included
    included_files = find_included_files(root_dir, gitignore_patterns, verbose)
    
    # Sort files for consistent output
    included_files.sort()
    
    if verbose:
        print(f"Found {len(included_files)} files to include in app.txt")
    
    # Output the list of files that will be included
    if verbose and included_files:
        print("Files to be included:")
        for file in included_files:
            rel_path = os.path.relpath(file, root_dir)
            print(f"  {rel_path}")
    
    # Create app.txt with all file contents
    output_path = os.path.join(root_dir, 'app.txt')
    create_app_txt(included_files, output_path, verbose)
    
    # Print summary
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"Created {output_path}")
        print(f"Included {len(included_files)} files")
        print(f"Total size: {file_size / 1024:.2f} KB")
    else:
        print(f"Failed to create {output_path}")

if __name__ == "__main__":
    main()