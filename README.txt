Programs:
	CMPT310-ASN1part1.py - Part 1, finding the shortest path
	CMPT310-ASN1part2.py - Part 2, finding a path using landmarks

Prerequisites:
	These programs require Python version 2.7 in order to run.

Running:
	Program/Part 1:
		for running on the default 18x18 grid with start point (0,0) and end point (17,17) use:
			python CMPT310-ASN1part1.py
		for running with different start points and end points on the default 18x18 grid use:
			python CMPT310-ASN1part1.py <startX> <startY> <goalX> <goalY>
		for running with custom start and end points on a custom map (file, note: 0's are normal tiles and 1's are walls) use:
			python CMPT310-ASN1part1.py <startX> <startY> <goalX> <goalY> <mapFile>

	Program/Part 2:
		for running on the default 18x18 grid with start point (0,0) and end point (17,17) use:
			python CMPT310-ASN1part2.py
		for running with different start points and end points on the default 18x18 grid use:
			python CMPT310-ASN1part2.py <startX> <startY> <goalX> <goalY>
		
Examples:
	Part 1:
		python CMPT310-ASN1part1.py
		python CMPT310-ASN1part1.py 0 0 13 14
		python CMPT310-ASN1part1.py 14 12 13 14
		python CMPT310-ASN1part1.py 3 15 0 0 map1.txt
		python CMPT310-ASN1part1.py 3 15 19 19 map1.txt
		python CMPT310-ASN1part1.py 0 0 3 15 map2.txt (Note: This should produce no path found)

	Part 2:
		python CMPT310-ASN1part2.py
		python CMPT310-ASN1part2.py 0 0 13 14
		python CMPT310-ASN1part2.py 14 12 13 14
		python CMPT310-ASN1part2.py 3 13 16 3