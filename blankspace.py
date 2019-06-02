# Read lines as a list
fh = open("D:\\FRESH_IBM\\hierarchy.txt", "r")
lines = fh.readlines()
fh.close()
# Weed out blank lines with filter
lines = filter(lambda x: not x.isspace(), lines)
# Write
fh = open("D:\\FRESH_IBM\\hierarchy_removed_blank_space.txt", "w")
fh.write("".join(lines))
# should also work instead of joining the list:
# fh.writelines(lines)
fh.close()