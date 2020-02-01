# Parse a CSV file into a list of rows
def parseCSVtoList(f):
  result = []
  for r in open(f):
    r = r.strip()
    if not r: continue
    r = r.split(',')
    result.append(r)
  return result[1:] # Remove header row

stops = {}
for r in parseCSVtoList(basePath + "/gtfs/stops.txt"): 
    print("INSERT INTO Stop (StopID, lat, lon) VALUES(%d,%f,%f);" % (int(r[0]),r[4],r[5]))

