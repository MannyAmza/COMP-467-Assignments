import csv

def extract_info(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    info = {}
    for line in lines:
        if line.startswith("Producer:"):
            info["Producer"] = line.split(":")[1].strip()
        elif line.startswith("Operator:"):
            info["Operator"] = line.split(":")[1].strip()
        elif line.startswith("Job:"):
            info["Job"] = line.split(":")[1].strip()
        elif line.startswith("Notes:"):
            info["Notes"] = lines[lines.index(line) + 1].strip()
        elif line.strip().startswith("/"):  # Check if line starts with "/"
            if "Locations" not in info:
                info["Locations"] = []
            info["Locations"].append(line.strip())

    return info

def filter_errors(data):
    cleaned_data = {}
    for path, frames in data.items():
        cleaned_frames = [frame for frame in frames if frame != "<err>" and frame != "<null>"]
        cleaned_data[path] = cleaned_frames
    return cleaned_data

def consolidate_frames(data):
    consolidated_data = {}
    for path, frames in data.items():
        if path not in consolidated_data:
            consolidated_data[path] = frames
        else:
            consolidated_data[path].extend(frames)
    return consolidated_data

def create_frame_ranges(frames):
    ranges = []
    frames = sorted(frames, key=int)  # Sort frames numerically
    start = frames[0]
    end = frames[0]
    for frame in frames[1:]:
        if int(frame) == int(end) + 1:
            end = frame
        else:
            if start == end:
                ranges.append(start)
            else:
                ranges.append(f"{start}-{end}")
            start = frame
            end = frame
    if start == end:
        ranges.append(start)
    else:
        ranges.append(f"{start}-{end}")
    return ranges

def process_baselight_file(filename):
    data = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                parts = line.split()
                path = parts[0]
                frames = [frame for frame in parts[1:] if frame.isdigit()]
                if path in data:
                    data[path].extend(frames)
                else:
                    data[path] = frames
    return data

def write_to_csv(xytech_info, consolidated_data, output_filename):
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header row for Xytech info
        writer.writerow(["Producer", "Operator", "Job", "Notes"])
        writer.writerow([xytech_info.get("Producer", ""), xytech_info.get("Operator", ""), xytech_info.get("Job", ""), xytech_info.get("Notes", "")])

        # Add empty row
        writer.writerow([])

        # Write header row for Baselight info
        writer.writerow(["Location", "Frames to Fix"])
        
        # Write file paths/locations and frames to the CSV file
        for path, frames in consolidated_data.items():
            for frame_range in frames:
                writer.writerow([path, frame_range])

    print("CSV file generated successfully.")

# Process Baselight_export.txt file
filename_baselight = "Project 1/Baselight_export.txt"
baselight_data = process_baselight_file(filename_baselight)
cleaned_data = filter_errors(baselight_data)
consolidated_data = consolidate_frames(cleaned_data)

# Create frame ranges for Baselight_export.txt
for path, frames in consolidated_data.items():
    consolidated_data[path] = create_frame_ranges(frames)

# Process Xytech.txt file
filename_xytech = "Project 1/Xytech.txt"
xytech_info = extract_info(filename_xytech)

# Write the extracted information to a CSV file
output_filename = "Project 1/output.csv"
write_to_csv(xytech_info, consolidated_data, output_filename)
