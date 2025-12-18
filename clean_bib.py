import re
import os

# From main.aux, find all 
# \bibcite{yu2025can}{69}

# From ref.bib, split all text with @. 
# For something like:
'''
@InProceedings{hamann2024low,
  author = {Hamann, Friedhelm and Ghosh, Suman and Martínez, Ignacio Juárez and Hart, Tom and Kacelnik, Alex and Gallego, Guillermo},
  title = {Low-power, Continuous Remote Behavioral Localization with Event Cameras},
  booktitle = CVPR,
  year = {2024},
}
'''
# If "hamann2024low" is not in the main.aux file, remove it from ref.bib. Output to filtered.bib.
# Note: There are things like "@STRING{WACV = {Proc. of Winter Conference on Applications of Computer Vision}}" that need to be kept.

def extract_citations_from_aux(aux_file_path):
	"""
	Extract citation keys from the aux file.
	"""
	citation_keys = set()
	
	try:
		with open(aux_file_path, 'r', encoding='utf-8') as f:
			content = f.read()
			
		# Find all \bibcite{key}{number} patterns
		citations = re.findall(r'\\bibcite{([^}]+)}{[^}]+}', content)
		citation_keys = set(citations)
	except Exception as e:
		print(f"Error reading AUX file: {e}")
	
	return citation_keys

def filter_bib_entries(bib_file_path, citation_keys, output_file_path):
	"""
	Filter the bib file to keep only cited entries and special entries like @STRING.
	"""
	try:
		with open(bib_file_path, 'r', encoding='utf-8') as f:
			content = f.read()
		
		# Split the content at @ characters to separate entries
		parts = content.split('@')
		
		# The first part (before any @ sign) can be kept as is
		filtered_parts = [parts[0]]
		
		kept_count = 0
		removed_count = 0
		
		# Process each BibTeX entry
		for part in parts[1:]:
			if not part.strip():
				continue
			
			# Check if it's a special entry like @STRING
			if part.lower().startswith(('string', 'comment', 'preamble')):
				filtered_parts.append('@' + part)
				kept_count += 1
				continue
			
			# For regular entries, extract the citation key
			match = re.match(r'([a-zA-Z]+)\s*{\s*([^,\s]+)', part)
			if match:
				entry_type, key = match.groups()
				if key in citation_keys:
					filtered_parts.append('@' + part)
					kept_count += 1
				else:
					removed_count += 1
			else:
				# If we can't parse it properly, keep it to be safe
				filtered_parts.append('@' + part)
				kept_count += 1
		
		# Write filtered entries to output
		with open(output_file_path, 'w', encoding='utf-8') as f:
			f.write(''.join(filtered_parts))
			
		print(f"Kept {kept_count} entries, removed {removed_count} entries.")
		print(f"Filtered bib file saved to {output_file_path}")
		
	except Exception as e:
		print(f"Error processing BIB file: {e}")

def main():
	# Get the file paths
	current_dir = os.path.dirname(os.path.abspath(__file__))
	aux_file = os.path.join(current_dir, "main.aux")
	bib_file = os.path.join(current_dir, "ref.bib")
	output_file = os.path.join(current_dir, "filtered.bib")
	
	# Extract citations from aux file
	citation_keys = extract_citations_from_aux(aux_file)
	print(f"Found {len(citation_keys)} citations in the AUX file.")
	
	# Filter bib file
	filter_bib_entries(bib_file, citation_keys, output_file)

if __name__ == "__main__":
	main()
