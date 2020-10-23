import xml.etree.ElementTree as ET
import mysite.settings as settings

def parseXMLwithET():
    bounding_boxes = dict()
    posture_points = dict()
    poly_gons = dict()
    poly_lines = dict()
    labels_info = dict()

    tree = ET.parse( settings.INPUT_DATA_DIRECTORY+'/annotations.xml' )
    root = tree.getroot()
    meta = root.find('meta')
    task = meta[0]
    labels = task.find('labels')
    segments = task.find('segments')
    segment = segments.find('segment')
    seg_start_frame = segment.find('start')
    seg_stop_frame = segment.find('stop')

    #color mapping stored in labels_info{}
    for label in labels:
        label_name = label.find('name')
        label_color = label.find('color')
        labels_info[label_name.text] = label_color.text

    #track information divided into the objects according to their shapes.
    tracks = root.findall('track')
    for track in tracks:
        track_id = int(track.attrib['id'])
        boundingboxes = track.findall("box")
        polygons = track.findall("polygon")
        polylines = track.findall("polyline")
        posturepoints = track.findall("points")

        if(len(boundingboxes) != 0):
            bounding_boxes[track_id] = boundingboxes
            bounding_boxes[track_id].append(track.attrib['label'])
        elif (len(posturepoints) != 0):
            posture_points[track_id]= posturepoints
            posture_points[track_id].append(track.attrib['label'])
        elif (len(polygons) != 0):
            poly_gons[track_id] = polygons
            poly_gons[track_id].append(track.attrib['label'])
        elif (len(polylines) != 0):
            poly_lines[track_id] = polylines
            poly_lines[track_id].append(track.attrib['label'])

    #all the accumulated info into one dictionary
    parsedInfo = {
                  "boundingboxes": bounding_boxes,
                  "polygons":poly_gons,
                  "polylines":poly_lines,
                  "posture_points":posture_points,
                  "labels_info": labels_info,
                  "segment_start":seg_start_frame.text,
                  "segment_stop": seg_stop_frame.text
                 }
    return parsedInfo

def getVideoName():
    tree = ET.parse(settings.INPUT_DATA_DIRECTORY+'/annotations.xml')
    root = tree.getroot()
    meta = root.find('meta')
    source = meta.find('source')
    return source.text
